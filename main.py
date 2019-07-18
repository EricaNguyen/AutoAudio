#main.py
import sys
import pyaudio
import aubio
import math
import time
import numpy as np 
import warnings
warnings.simplefilter("ignore", DeprecationWarning)

#linking together
from noteClass import Note
from freqAnalyzer import getFreq
from validateMeasures import noteD, whichStaff, getNoteLength
import KeyChart
import filterList

#Setting up Stream
FRAME_SIZE = 1024 * 2
FRAMES_PER_FFT = 16 # FFT = Fast Fourier Transform
#FORMAT = pyaudio.paInt16
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100 # Samples per second
CHUNK = 1024 # Number of data samples (Bytes)
#CHUNK = 2048
RECORD_SECONDS = 5
TOLERANCE = 0.8
WAVE_OUTPUT_NAME = "def_output.wav"

# Open the stream
p = pyaudio.PyAudio()
stream = p.open(
    format = FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input = True,
    frames_per_buffer = CHUNK
)

if len(sys.argv) > 1: # If file-name specified on cmdline
    WAVE_OUTPUT_NAME = sys.argv[1] # output file with this name
    outputsink = aubio.sink(WAVE_OUTPUT_NAME, RATE)
else:
    outputsink = aubio.sink(WAVE_OUTPUT_NAME, RATE)

# Aubio's Pitch Recognition
fDetection = aubio.pitch("default", 2048, 1024, RATE)
fDetection.set_unit("Hz")
fDetection.set_silence(-40)
fDetection.set_tolerance(TOLERANCE)


print("* RECORDING")
(staff, my_notes) = getFreq(stream, CHUNK, fDetection, outputsink)

# Closing stream
stream.stop_stream()
stream.close()
p.terminate()
print("* RECORDING STOPPED")

#CODE TO REMOVE OUTLIER FREQUENCIES

newStaffu = ""
newStaffl = ""

#print all recorded notes (shortened)
print("before joining")
# for noteObj in my_notes:
#    noteObj.printNote()

#New algorithm:
#first loop through and join split up notes
fixed_my_notes = filterList.fixDuration(my_notes)

#prints correctly
print("after joining ||| before outlier removal")
# for noteObj in fixed_my_notes:
#    noteObj.printNote()

#NOW remove all recorded notes with duration of 1
#insert all with duration > 1 into new_my_notes
#the total duration is also calculated
tempDuration = 0
for noteObj in fixed_my_notes:
    tempDuration += noteObj.duration

(tempq, tempw, temphf, tempe, temps) = noteD(tempDuration, fixed_my_notes)
(new_my_notes, sumOfDuration) = filterList.outlierRemoval(fixed_my_notes, tempe)

#Determining Note Type using holistic perspective

#LilyPond durations
#---------------------------------------------
#sumOfDuration = 0
lengthCounter = 0
#Assuming measures are 4/4
measureLength = 4

wholeNote = '1'
halfNote = '2'
quarterNote = '4'
eighthNote = '8'
sixteenthNote = '16'

rest = 'r'
bar = '| '
tie = '~ '
space = ' '

#Quarter Note
(q, w, hf, e, s) = noteD(sumOfDuration, new_my_notes)

sixteenthNoteLength = .25
eighthNoteLength = .5
quarterNoteLength = 1
halfNoteLength = 2
wholeNoteLength = 4

#Note Duration List
noteDurKeys = (s, e, q, hf, w)
#---------------------------------------------

def getNoteType(myInt):
    typeN = ''
    
    if myInt == s:
        typeN += sixteenthNote
    elif myInt == e:
        typeN += eighthNote
    elif myInt == hf:
        typeN += halfNote
    elif myInt == w:
        typeN += wholeNote
    else:
        typeN += quarterNote
    return typeN


for noteObj in new_my_notes: 
    # Classifying Note Durations
    classified = KeyChart.findNoteDuration(noteObj.duration, noteDurKeys)
    pitch = noteObj.pitch
    # Current notes length
    getType = int(getNoteType(classified))

    # Measure Validity Check
    # setting the duration length of the note
    noteObj.durationLength = getNoteLength(getType)
    dLength = noteObj.durationLength
    lengthCounter += dLength
    
    fullMeasure = lengthCounter == measureLength
    exceedingMeasure = lengthCounter > measureLength
    #insufficientMeasure = lengthCounter < measureLength
        
    #Spliting into upper and lower staff
    numOfApos = whichStaff(pitch)[1]
    numOfComm = whichStaff(pitch)[0]

    #If note is Octave 3 or lower
    if numOfComm == 1 or numOfApos + numOfComm == 0:
        # If valid measure
        if fullMeasure:
            pitch = pitch + getNoteType(classified) + space
            #Append note to lower staff
            newStaffl += pitch
            #Otherwise append a rest to upper staff with corresponding duration
            newStaffu += rest + getNoteType(classified) + space
            #Append the bar to both staffs to cut valid measure
            newStaffl += bar
            newStaffu += bar
            #Reset counter
            lengthCounter = 0
        # If invalid measure and overflow
        elif exceedingMeasure:
            # Delete the current notes length from the counter
            # Find suitabe split so that the measure is valid
            notesToFillMeasure = 0
            notesToAppendAfterMeasure = 0

            validLengthCounter = lengthCounter - dLength
            # OVerflow amount
            overflow = lengthCounter - measureLength
            lengthCounter = overflow
            # Finding the suitable length to validate the measure  
            while True:
                done = False
                for i in range(16):
                    # Debugging: print('overflow',overflow, 'Original NL', dLength, 'ValidLC',validLengthCounter,'| noteType', getNoteType(classified), '| noteLength', ((i+1) * getNoteLength(int(getNoteType(classified)))), '| Total Length', validLengthCounter + ((i+1) * getNoteLength(int(getNoteType(classified)))))
                    if validLengthCounter + ((i+1) * getNoteLength(int(getNoteType(classified)))) == measureLength:
                        notesToFillMeasure = i+1
                        done = True
                        break
                if done:
                    break
                classified = classified / 2
            
            suitableNoteLength = getNoteLength(int(getNoteType(classified)))
            print(suitableNoteLength, validLengthCounter)

            while overflow != 0:
                overflow = overflow - suitableNoteLength
                notesToAppendAfterMeasure += 1
            
            pitchTied = pitch + getNoteType(classified) + tie
            newStaffu += rest + getNoteType(classified) + space
            newStaffl += pitchTied
            for i in range(notesToFillMeasure-1):
                newStaffl += pitch + tie
                newStaffu += rest + getNoteType(classified) + space
            
            newStaffl += bar
            newStaffu += bar

            for i in range(notesToAppendAfterMeasure-1):
                newStaffl += pitch + tie
                newStaffu += rest + getNoteType(classified) + space
            newStaffl += pitch + space
            newStaffu += rest + getNoteType(classified) + space

        else: # An invalid measure that has yet to be filled up
            pitch = pitch + getNoteType(classified) + space
            newStaffl += pitch
            newStaffu += rest + getNoteType(classified) + space

    #If note is Octave 4 or higher
    else:
        #Append note to upper staff
        if fullMeasure:
            pitch = pitch + getNoteType(classified) + space
            #Append note to upper staff
            newStaffu += pitch
            #Otherwise append a rest to lower staff with corresponding duration
            newStaffl += rest + getNoteType(classified) + space
            #Append the bar to both staffs
            newStaffu += bar
            newStaffl += bar
            lengthCounter = 0
        elif exceedingMeasure:
            # Delete the current notes length from the counter
            # Find suitabe split so that the measure is valid
            notesToFillMeasure = 0
            notesToAppendAfterMeasure = 0

            validLengthCounter = lengthCounter - dLength
            # OVerflow amount
            overflow = lengthCounter - measureLength
            lengthCounter = overflow
            # Finding the suitable length to validate the measure  
            while True:
                done = False
                for i in range(16):
                    print('overflow',overflow, 'Original NL', dLength, 'ValidLC',validLengthCounter,'| noteType', getNoteType(classified), '| noteLength', ((i+1) * getNoteLength(int(getNoteType(classified)))), '| Total Length', validLengthCounter + ((i+1) * getNoteLength(int(getNoteType(classified)))))
                    if validLengthCounter + ((i+1) * getNoteLength(int(getNoteType(classified)))) == measureLength:
                        notesToFillMeasure = i+1
                        done = True
                        break
                if done:
                    break
                classified = classified / 2
            
            suitableNoteLength = getNoteLength(int(getNoteType(classified)))
            print(suitableNoteLength, validLengthCounter)

            while overflow != 0:
                overflow = overflow - suitableNoteLength
                notesToAppendAfterMeasure += 1
            
            pitchTied = pitch + getNoteType(classified) + tie
            newStaffl += rest + getNoteType(classified) + space
            newStaffu += pitchTied
            for i in range(notesToFillMeasure-1):
                newStaffu += pitch + tie
                newStaffl += rest + getNoteType(classified) + space
            
            newStaffu += bar
            newStaffl += bar

            for i in range(notesToAppendAfterMeasure-1):
                newStaffu += pitch + tie
                newStaffl += rest + getNoteType(classified) + space
            newStaffu += pitch + space
            newStaffl += rest + getNoteType(classified) + space
            
        else:
            pitch = pitch + getNoteType(classified) + space
            newStaffu += pitch
            newStaffl += rest + getNoteType(classified) + space

    
    


#prints correctly
print("after outlier removal and classifying duration")
for noteObj in new_my_notes:
    noteObj.printNote()

#following is correct
print("staff: ", staff)         #with duration 1 notes
print("newStaffu: ", newStaffu)   #staffs without duration 1 notes
print("newStaffl: ", newStaffl)

#copy newStaff into staff for convenience
staffu = newStaffu
staffl = newStaffl

print("=====FINAL RESULT=====")
#----------------------------------
# Debugging
print("sum", sumOfDuration)
print("quarter", q)
print("whole", w)
print("halfnote", hf)
print("eighth", e)
print("sixteenth", s)
#----------------------------------
print("staffu: ", staffu)         #without duration 1 notes
print("staffl: ", staffl)

# Open the file
fh = open('output.ly', "w")


# Setting up the ly file
v = "version"
vn = '"2.18.2"'
version = r"\{} {}".format(v, vn)
l = "language"
lang = '"english"'
language = r"\{} {}".format(l, lang)

# Writing setup into file
fh.write(version + "\n")
fh.write(language + "\n")

# Setting up header block (Inputs will be specified by GUI)
fbrac = '{'
bbrac = '}'
comm = '"'
songName = '"Song Name"'
composer = 'Username' 
tagLine = '"Copyright: '

title2 = r"""\header {}
    title = {}
    composer = {}{}{}
    tagline = {}{}{}
{}""".format(fbrac, songName, 
             comm, composer, comm, 
             tagLine, composer, comm,
             bbrac)


# Writing header into file
fh.write(title2 + "\n")

#Setting up 
relative = r"\{} {}".format("relative","c'")
#fh.write(relative + "\n")
#Will probably implement the use of another staff (bass clef)
staffh = "{\n\\new PianoStaff << \n"
staffh += "  \\new Staff { \clef treble " + staffu + r'\bar "|."' + "}\n"
staffh += "  \\new Staff { \clef bass " + staffl + r'\bar "|."' + "}\n"  #r prefix messed it up
staffh += ">>\n}\n"

fh.write(staffh + "\n")

# Closing file handling
fh.close()