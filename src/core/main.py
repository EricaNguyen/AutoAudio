#main.py
import sys
import pyaudio
import aubio
import math
import time
import numpy as np 
import subprocess
import warnings
warnings.simplefilter("ignore", DeprecationWarning)

#linking together
from noteClass import Note
from freqAnalyzer import getFreq
from validateMeasures import sumOfListDurations, noteD, whichStaff, getNoteLength, getNoteType, validate
from createLily import createFile
import KeyChart
import filterList
import removeEdges

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

print("===========================================")
print("*♩* RECORDING..............................‖")
print("===========================================")
(staff, my_notes) = getFreq(stream, CHUNK, fDetection, outputsink)

# Closing stream
stream.stop_stream()
stream.close()
p.terminate()
print("===========================================")
print("*♩* RECORDING STOPPED......................‖")
print("===========================================")

#CODE TO REMOVE OUTLIER FREQUENCIES

print("♩ Removing extra rests.....................‖")
#remove edges
edgeless_my_notes = removeEdges.removeEdges(my_notes)

print("♩ Joining notes............................‖")
# for noteObj in my_notes:
#    noteObj.printNote()

#New algorithm:
#first loop through and join split up notes
fixed_my_notes = filterList.fixDuration(edgeless_my_notes)

#NOW remove all recorded notes with duration of 1
#insert all with duration > 1 into new_my_notes
#the total duration is also calculated

print("♩ Removing spikes..........................‖")
(tempq, tempw, temphf, tempe, temps) = noteD(fixed_my_notes)
new_my_notes = filterList.outlierRemoval(fixed_my_notes, tempe)

# #prints correctly
# print("after outlier removal and classifying duration")
# for noteObj in new_my_notes:
#     noteObj.printNote()

#Validating Measures
(newStaffl, newStaffu) = validate(new_my_notes)

#following is correct
# print("staff: ", staff)         #with duration 1 notes

#copy newStaff into staff for convenience
staffu = newStaffu
staffl = newStaffl

# print("staffu: ", staffu)         #without duration 1 notes
# print("staffl: ", staffl)

# Create the Lilypond input file
print("♩ Creating Lilypond input file.............‖")
createFile(staffu, staffl)
print("===========================================")
print("Running Lilypond...")
print("===========================================")
subprocess.call(['lilypond', 'output.ly'])
print("===========================================")

#---------------------------------------------------------------------------
print("\n")
print("Debugging purposes:")
print("staffu: ", staffu)         #without duration 1 notes
print("staffl: ", staffl)
