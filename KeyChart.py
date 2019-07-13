# KeyChart.py
# Written by Jeffrey Ng
# for use in UC Santa Cruz, CMPS115, Summer 2019
# Team: The Awesome Team
# Project: Auto Audio
# Description: Simple algorithm designed to calculate which
#     key on a piano best matches a sound frequency

# Pre-set piano key frequencies stored in a Tuple. They should
#     remain consistent for the entire project.



# Change the value of "frequency" to test different numbers
#frequency = 4200

import os.path
from os import path
import itertools

keys = (27.50000,
        29.13524,
        30.86771,
        32.70320,
        34.64783,
        36.70810,
        38.89087,
        41.20344,
        43.65353,
        46.24930,
        48.99943,
        51.91309,
        55.00000,
        58.27047,
        61.73541,
        65.40639,
        69.29566,
        73.41619,
        77.78175,
        82.40689,
        87.30706,
        92.49861,
        97.99886,
        103.8262,
        110.0000,
        116.5409,
        123.4708,
        130.8128,
        138.5913,
        146.8324,
        155.5635,
        164.8138,
        174.6141,
        184.9972,
        195.9977,
        207.6523,
        220.0000,
        233.0819,
        246.9417,
        261.6256,
        277.1826,
        293.6648,
        311.1270,
        329.6276,
        349.2282,
        369.9944,
        391.9954,
        415.3047,
        440.0000,
        466.1638,
        493.8833,
        523.2511,
        554.3653,
        587.3295,
        622.2540,
        659.2551,
        698.4565,
        739.9888,
        783.9909,
        830.6094,
        880.0000,
        932.3275,
        987.7666,
        1046.502,
        1108.731,
        1174.659,
        1244.508,
        1318.510,
        1396.913,
        1479.978,
        1567.982,
        1661.219,
        1760.000,
        1864.655,
        1975.533,
        2093.005,
        2217.461,
        2349.318,
        2489.016,
        2637.020,
        2793.826,
        2959.955,
        3135.963,
        3322.438,
        3520.000,
        3729.310,
        3951.066
        )
		
# This script is designed to return the
#     tuple index of the closest-matching frequency value
# Also included in this script is an alternate algorithm,
#     which returns the note "name" as a string

# function findNote:
# Takes a frequency value (should be a float)
# Iterates through "keys" tuple, finds which value
#     in tuple is closest to the given frequency by
#     taking the average of every adjacent pair in the tuple and
#     comparing each average to the given frequency
# Returns which index in the tuple the best-matching value is at
# If no matching value is found, function should return maximum index: 87
# If value is smaller than minimum value (27.5 Hz), returns 0
def findNote(freq):
    for x in range(0, 86):
        #this loop should go from 0 to 86
        #that is just how Python works
        avg = keys[x] + keys[x+1]
        avg = avg / 2
        if freq < avg:
            #print("index: ")
            #print(x)
            return x
    #print("index: ")
    #print("87")
    return 86

#''' --------------------------------------------------------------------------
# comment/uncomment this block for alternate algorithm
# (sixteenth, eighth, quarterNote, halfnote, wholenote)

def findNoteDuration(duration, myList):
    for x in range(len(myList)-1):
        #this loop should go from 0 to 86
        #that is just how Python works
        avg = myList[x] + myList[x+1]
        avg = avg / 2
        if duration < avg:
            #print("index: ")
            #print(x)
            return myList[x]
    #print("index: ")
    #print("87")
    return myList[(len(myList))-1]

# another tuple that stores the note names
notes = ("A", "Bf", "B", "C", "Cs", "D", "Ef", "E", "F", "Fs", "G", "Gs")

#loc is location local var
def alternate(loc):
   
   noteName = notes[loc % 12]
   #print("Note: ")
   #print(noteName)

   #add one, subtract later if A, Bb, or B.
   octave = (loc / 12) + 1

   # 0 is notes before first C, 8 is highest note on piano (C)
   if (noteName == "A" or noteName == "Bf" or noteName == "B"):
      octave = octave - 1

   #convert to int (for printing)
   iOctave = (int(octave))
   #convert to string (for concatenation)
   sOctave = (str(iOctave))
   #concatenate

   # Octave logic
   # c in LilyPond syntax is c2 so middle C is c'
   # Octaves (Middle C and above): 4 = c' 5 = c'' 6 = c''' 7 = c''''
   
   #Octave -1: c,,,, d,,,, e,,,, f,,,, g,,,, a,,,, b,,,,
   #Octave 0: c,,, d,,, e,,, f,,, g,,, a,,, b,,, 
   #Octave 1: c,, d,, e,, f,, g,, a,, b,, 
   #Octave 2: c, d, e, f, g, a, b, 
   #Octave 3: c d e f g a b  
   #Octave 4: c' d' e' f' g' a' b'  
   #Octave 5: c'' d'' e'' f'' g'' a'' b''
   #Octave 6: c''' d''' e''' f''' g''' a''' b''' 
   #Octave 7: c'''' d'''' e'''' f'''' g'''' a'''' b'''' 


   lilyOc = ""
   apos = "'"
   if iOctave >= 4:
      for _ in itertools.repeat(None, int(octave)-3):
         lilyOc += apos
   # Octaves below Middle C: 2 = c, 1 = c,,
   elif iOctave < 4:
      if iOctave == 1:
              lilyOc = ",,"
      elif iOctave == 2:
              lilyOc = ','
      else:
              lilyOc


   #pianoKey = noteName + sOctave
   #print(pianoKey)
   return noteName.lower() + lilyOc

   #print("Octave you are in: ")
   # Range from 0 to 8
   #print(int(octave))

   #print("Key on keyboard: ")
   # Base index is 0. Add 1 to index, so it's easier for user to see
   # Range from 1 - 88
   #print(loc + 1)

#comment out when done testing:
#location = findNote(frequency)
#print (location)
#alternate(location)
