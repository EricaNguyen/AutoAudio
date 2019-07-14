import sys
import pyaudio
import aubio
import audioop
import math
import numpy as np 
import warnings
warnings.simplefilter("ignore", DeprecationWarning)

#linking together
import KeyChart

#-----------------------------------------------------------
# LILYPOND SYNTAX (Taken from documentation)
# For future use. Once we want to implement other properties
# ♩ = note eg: a, b, c

# Durations: note<duration> 
#   ♩1 (Whole Note)
#   ♩2 (Half Note)
#   ♩8 (Eighth Note)
#   ♩16 (Sixteenth Note)

# Rests: r<duration>
#   r1 (Whole Rest)
#   r2 (Half Rest)
#   r4 (Quarter Rest)
#   r8 (Eighth Rest)
#   r16 (Sixteenth Rest)
#   r32 (x2)
#   r64 (x2)
#   r128 (x2)

# Beams: note<duration>[note]
#   ♩8[♩]

# Articulations: note->
#   ♩-> 

# Staccato: note-.
#   ♩-.

# Dynamics: note\<dynamic>
#   ♩\ppp
#   ♩\ff
# Crescendo: note\< note note\!
#   ♩\< ♩ ♩\!
# Decrescendo: note\> note note\!
#   ♩/> ♩ ♩\!

# Chords: < notes >
#   <♩' ♩'>




FRAME_SIZE = 1024 * 2
FRAMES_PER_FFT = 16 # FFT = Fast Fourier Transform
# FORMAT = pyaudio.paInt16 # Bytes per sample
#FORMAT = pyaudio.paInt16
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100 # Samples per second
CHUNK = 1024 # Number of data samples (Bytes)
#CHUNK = 2048
RECORD_SECONDS = 5
TOLERANCE = 0.8
WAVE_OUTPUT_NAME = "def_output.wav"

class Note(object):
    def __init__(self, pitch, duration, durationNote, soundPressureLevel):
        self.pitch = pitch
        self.duration = duration
        self.soundPressureLevel = soundPressureLevel
        self.durationNote = durationNote

    def printNote(self):
        print("Pitch: ", self.pitch, "| Duration :", self.duration, "| Duration Note:", self.durationNote, "| Sound Pressure Level:", self.soundPressureLevel)

# I don't really understand FFT 
'''
SAMPLES_PER_FFT = FRAME_SIZE * FRAMES_PER_FFT
FREQ_STEP = float(RATE) / SAMPLES_PER_FFT 
'''

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

#NUM_CHUNKS = int((RATE / CHUNK) * RECORD_SECONDS)

'''
# RATE * TIME_RECORDED / CHUNKS = NUM CHUNKS
for i in range(0, NUM_CHUNKS): 
    data = stream.read(CHUNK)
    frames.append(data)
'''

staff = ""
prev_note = ""
my_notes = []

#while stream.is_active()
while True:
    try:
        data = stream.read(CHUNK)

        samples = np.fromstring(data, dtype = aubio.float_type)

        freq = fDetection(samples)[0]
        confidence = fDetection.get_confidence()
        fConfidence = '{:.2f}'.format(confidence)
        
        # if confidence < 0.5:
        #     freq = 0
        
        #MAX THE VARIABLE rms HAS THE AMPLITUDE
        #IT IS ALSO CONVERTED INTO DECIBEL 
        #I commented it out originally because the outputs didn't make sense
        #Maybe you can make some sense out of it

        rms = audioop.rms(data,2)
        #decibel = 20 * np.log10(rms) #dB = 20 * log10(Amp)
        #print(decibel)

        #aubio:
        linear = '{:.4f}'.format(aubio.level_lin(samples)) #seems to make more sense
        decibels = '{:.4f}'.format(aubio.db_spl(samples))
        #Ive been testing it and it seems like 
        #it's outputting negative decibels
        #the closer to 0, the louder, which doesn't make sense
        
        #uncomment to print original stuff
        #print("{} / {}".format(freq, confidence))


        if outputsink:
            outputsink(samples, len(samples))
        
        # if note is too low, don't print
        if(freq > 25.0):
           #call KeyChart
           idx = KeyChart.findNote(freq)
           #note name
           nn = KeyChart.alternate(idx)
           print("all :", nn, "| confidence", fConfidence)

           #if new note
           if (nn != prev_note):
              prev_note = nn
              
              #create new note
              newNote = Note(nn, 1, 'TBD', linear)
              #append to list of notes
              my_notes.append(newNote)
              #note name formated (added space)
              nnf = nn + " " 
              # Adding the notes to the string
              staff += nnf
              #print(nn)

           #else if same note
           else:
              #increment current note's duration
              my_notes[len(my_notes)-1].duration += 1              
              
        #else it's a rest
        else:
           #if last note was not a rest
           if prev_note != "REST":
              prev_note = "REST"
              newRest = Note("REST", 1, 'TBD', linear)
              my_notes.append(newRest)
           #else last note was a rest
           else: 
              my_notes[len(my_notes)-1].duration += 1              

    except KeyboardInterrupt:
        print ("User Ctrl+C. Exiting...")
        break

print("* RECORDING STOPPED")


#CODE TO REMOVE OUTLIER FREQUENCIES

newStaffu = ""
newStaffl = ""

#print all recorded notes (shortened)
print("before joining")
for noteObj in my_notes:
   noteObj.printNote()

#New algorithm:
#first loop through and join split up notes
for i in range(len(my_notes)):
    #avoid segfault
    if i > 0 and i < len(my_notes)-1 and my_notes[i].duration == 1:
       #check if other sies of duration 1 note are same pitch
       if my_notes[i-1].pitch == my_notes[i+1].pitch:
          #add durations together and delete one
          my_notes[i-1].duration += my_notes[i+1].duration
          del my_notes[i+1]


#prints correctly
print("after joining ||| before outlier removal")
for noteObj in my_notes:
   noteObj.printNote()

#NOW remove all recorded notes with duration of 1
new_my_notes = []

#LilyPond durations
sumOfDuration = 0

wholeNote = '1'
halfNote = '2'
quarterNote = '4'
eighthNote = '8'
sixteenthNote = '16'

rest = 'r'

#insert all with duration > 1 into new_my_notes
for noteObj in my_notes:
   #also remove rests TODO remove that
   if noteObj.duration > 1 and noteObj.pitch != "REST":
      sumOfDuration += noteObj.duration
      new_my_notes.append(noteObj)

#Determining Note Type using holistic perspective

#Quarter Note
q = sumOfDuration / len(new_my_notes)
#Whole Note
w = q * 4
#Half Note
hf = q * 2
#Eighth Note
e = q / 2
#Sixteenth Note
s = q / 4

#Note Duration List
noteDurKeys = (s, e, q, hf, w)

def whichStaff(myString):
    commCount = 0
    aposCount = 0

    for c in myString:
        if c == ',':
            commCount += 1
            break
        if c == "'":
            aposCount += 1
            break
    return (commCount, aposCount)

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
    noteObj.durationNote = classified
    noteObj.pitch = noteObj.pitch + getNoteType(classified) + " "

    #if getNoteType(classified) == wholeNote and noteObj.duration > w + hf:
        
    #Spliting into upper and lower staff
    #If note is Octave 3 or lower
    numOfApos = whichStaff(noteObj.pitch)[1]
    numOfComm = whichStaff(noteObj.pitch)[0]

    if numOfComm == 1 or numOfApos + numOfComm == 0:
        #Append note to lower staff
        newStaffl += noteObj.pitch
        #Otherwise append a rest to upper staff with corresponding duration
        newStaffu += rest + getNoteType(classified) + " "
    else:
        #Append note to upper staff
        newStaffu += noteObj.pitch
        #Or rest
        newStaffl += rest + getNoteType(classified) + " "
    


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

# Closing stream
stream.stop_stream()
stream.close()
p.terminate()

# Closing file handling
fh.close()
