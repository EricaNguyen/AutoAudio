#validateMeasures.py
import sys
import KeyChart
from noteClass import Note
from appendStaffs import appendLower, appendUpper, appendRests

wholeNote = '1'
halfNote = '2'
quarterNote = '4'
eighthNote = '8'
sixteenthNote = '16'

sixteenthNoteLength = .25
eighthNoteLength = .5
quarterNoteLength = 1
halfNoteLength = 2
wholeNoteLength = 4

def sumOfListDurations(noteList):
    sumOfDuration = 0
    for noteObj in noteList:
        sumOfDuration += noteObj.duration
    return sumOfDuration

def noteD(noteList):
    sumOfDuration = sumOfListDurations(noteList)
    try:
        q = sumOfDuration / len(noteList)
    except ZeroDivisionError:
        print("Nothing recorded. Program terminated prematurely")
        sys.exit()  
    #Whole Note
    w = q * 4
    #Half Note
    hf = q * 2
    #Eighth Note
    e = q / 2
    #Sixteenth Note
    s = q / 4
    return (q, w, hf, e, s)

def whichStaff(myString):
    commCount = 0
    aposCount = 0
    isRest = False
    for c in myString:
        if c == ',':
            commCount += 1
            break
        if c == "'":
            aposCount += 1
            break
        if c == 'r':
            isRest = True
    return (commCount, aposCount, isRest)

def getNoteLength(myInt):
    noteLength = 0
    if myInt == int(sixteenthNote):
        noteLength = sixteenthNoteLength
    elif myInt == int(eighthNote):
        noteLength = eighthNoteLength
    elif myInt == int(quarterNote):
        noteLength = quarterNoteLength
    elif myInt == int(halfNote):
        noteLength = halfNoteLength
    else:
        noteLength = wholeNoteLength
    return noteLength

def getNoteType(myInt, noteDurKeys):
    (s, e, q, hf, w) = noteDurKeys
    typeN = ''
    
    if myInt == s:
        typeN += sixteenthNote
    elif myInt == e:
        typeN += eighthNote
    elif myInt == hf:
        typeN += halfNote
    elif myInt == w:
        typeN += wholeNote
    elif myInt == q:
        typeN += quarterNote
    return typeN

def validate(new_my_notes):
    newStaffu = ""
    newStaffl = ""
    lengthCounter = 0
    #Assuming measures are 4/4
    measureLength = 4
    print("♩ Classifying note durations...............‖")
    print("♩ Validating measures......................‖")
    for noteObj in new_my_notes: 
        (q, w, hf, e, s) = noteD(new_my_notes)
        #Note Duration List
        noteDurKeys = (s, e, q, hf, w)
        # Classifying Note Durations
        classified = KeyChart.findNoteDuration(noteObj.duration, noteDurKeys)
        pitch = noteObj.pitch
        # Current notes length
        getType = int(getNoteType(classified, noteDurKeys))

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
        isRest = whichStaff(pitch)[2]

        notesToFillMeasure = 0
        notesToAppendAfterMeasure = 0

        # If valid measure
        if fullMeasure:
            lengthString = getNoteType(classified, noteDurKeys)
            #Reset counter
            lengthCounter = 0
        # If invalid measure and overflow
        elif exceedingMeasure:
            # Delete the current notes length from the counter
            # Find suitabe split so that the measure is valid
            validLengthCounter = lengthCounter - dLength
            # OVerflow amount
            overflow = lengthCounter - measureLength
            lengthCounter = overflow
            # Finding the suitable length to validate the measure  
            while True:
                done = False
                for i in range(16):
                    # Debugging: print('overflow',overflow, 'Original NL', dLength, 'ValidLC',validLengthCounter,'| noteType', getNoteType(classified, noteDurKeys), '| noteLength', ((i+1) * getNoteLength(int(getNoteType(classified, noteDurKeys)))), '| Total Length', validLengthCounter + ((i+1) * getNoteLength(int(getNoteType(classified, noteDurKeys)))))
                    if validLengthCounter + ((i+1) * getNoteLength(int(getNoteType(classified, noteDurKeys)))) == measureLength:
                        notesToFillMeasure = i+1
                        done = True
                        break
                if done:
                    break
                classified = classified / 2
            
            suitableNoteLength = getNoteLength(int(getNoteType(classified, noteDurKeys)))
            # print(suitableNoteLength, validLengthCounter)

            while overflow != 0:
                overflow = overflow - suitableNoteLength
                notesToAppendAfterMeasure += 1
            
            lengthString = getNoteType(classified, noteDurKeys)

        else: # An invalid measure that has yet to be filled up
            lengthString = getNoteType(classified, noteDurKeys)

        lowerOctaves = (numOfComm == 1 or numOfApos + numOfComm == 0) and not isRest
        upperOctaves = numOfApos == 1

        if lowerOctaves:
            (newStaffl, newStaffu) = appendLower(fullMeasure, exceedingMeasure, lengthString, pitch, notesToAppendAfterMeasure, notesToFillMeasure, newStaffl, newStaffu)
        elif upperOctaves:
            (newStaffl, newStaffu) = appendUpper(fullMeasure, exceedingMeasure, lengthString, pitch, notesToAppendAfterMeasure, notesToFillMeasure, newStaffl, newStaffu)
        elif isRest:
            (newStaffl, newStaffu) = appendRests(fullMeasure, exceedingMeasure, lengthString, pitch, notesToAppendAfterMeasure, notesToFillMeasure, newStaffl, newStaffu)
    print("♩ Splitting staffs.........................‖")
    # print("=====FINAL RESULT=====")
    #----------------------------------
    # Debugging
    # print("sum", sumOfListDurations(new_my_notes))
    # print("quarter", q)
    # print("whole", w)
    # print("halfnote", hf)
    # print("eighth", e)
    # print("sixteenth", s)
    #----------------------------------
    return (newStaffl, newStaffu)