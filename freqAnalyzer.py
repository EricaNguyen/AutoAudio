import sys
import pyaudio
import aubio
import numpy as np 
import warnings
warnings.simplefilter("ignore", DeprecationWarning)

#linking together
from noteClass import Note
import KeyChart
import filterList

# POTATO
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


#while stream.is_active()
def getFreq(stream, CHUNK, fDetection, outputsink):
    staff = ""
    prev_note = ""
    my_notes = []
    while True:
        try:
            data = stream.read(CHUNK)

            samples = np.fromstring(data, dtype = aubio.float_type)

            freq = fDetection(samples)[0]
            confidence = fDetection.get_confidence()
            fConfidence = '{:.2f}'.format(confidence)
            
            # if confidence < 0.5:
            #     freq = 0
            
            #IT IS ALSO CONVERTED INTO DECIBEL 
            #I commented it out originally because the outputs didn't make sense
            #Maybe you can make some sense out of it

            #decibel = 20 * np.log10(rms) #dB = 20 * log10(Amp)
            #print(decibel)

            #MAX THE linear VARIABLE HAS THE SOUND PRESSURE LEVELS
            #aubio:
            linear = '{:.4f}'.format(aubio.level_lin(samples)) #seems to make more sense
            decibels = '{:.4f}'.format(aubio.db_spl(samples))
            #Ive been testing it and it seems like 
            #it's outputting negative decibels
            #the closer to 0, the louder
            
            #uncomment to print original stuff
            #print("{} / {}".format(freq, confidence))


            if outputsink:
                outputsink(samples, len(samples))
        
            # if note is too low, don't print
            if(freq > 25.0):
                #call KeyChart
                idx = KeyChart.findNote(freq)
                #note name
                (nn, regular) = KeyChart.alternate(idx)
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
            return (staff, my_notes)
            


