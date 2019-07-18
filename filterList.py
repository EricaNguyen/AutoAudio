# filterList.py
# This file is responsible for filtering the raw notes that are produced by
# the audio (e.g outlier notes) and fixing the aftereffects caused by them

from noteClass import Note

def fixDuration(noteList):
    #New algorithm:
    #first loop through and join split up notes
    for i in range(len(noteList)):
        #avoid segfault
        if i > 0 and i < len(noteList)-1 and noteList[i].duration == 1:
            #check if other sies of duration 1 note are same pitch
            if noteList[i-1].pitch == noteList[i+1].pitch:
                #add durations together and delete one
                noteList[i-1].duration += noteList[i+1].duration
                del noteList[i+1]
    
    return noteList

def outlierRemoval(noteList, eighthnote):
    #insert all with duration > 1 into new_my_notes
    new_my_notes = []
    sumOfDuration = 0
    for noteObj in noteList:
        #also remove rests TODO remove that
        if noteObj.duration > 1 and noteObj.pitch != 'r':
            sumOfDuration += noteObj.duration
            new_my_notes.append(noteObj)
        elif noteObj.pitch == 'r' and noteObj.duration > eighthnote:
            sumOfDuration += noteObj.duration
            new_my_notes.append(noteObj)

    return (new_my_notes, sumOfDuration)

    
