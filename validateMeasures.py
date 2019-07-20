#validateMeasures.py
import sys

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


def noteD(sumOfDuration, noteList):
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

def validate(classified, measureLength, dLength, lengthCounter, noteDurKeys):
    overflow = lengthCounter - measureLength
    lengthCounter = overflow
    validLengthCounter = lengthCounter - dLength
    notesToFillMeasure = 0
    notesToAppendAfterMeasure = 0
    # Finding the suitable length to validate the measure  
    while True:
        done = False
        for i in range(16):
            # Debugging: print('overflow',overflow, 'Original NL', dLength, 'ValidLC',validLengthCounter,'| noteType', getNoteType(classified), '| noteLength', ((i+1) * getNoteLength(int(getNoteType(classified)))), '| Total Length', validLengthCounter + ((i+1) * getNoteLength(int(getNoteType(classified)))))
            if validLengthCounter + ((i+1) * getNoteLength(int(getNoteType(classified, noteDurKeys)))) == measureLength:
                notesToFillMeasure = i+1
                done = True
                break
        if done:
            break
        classified = classified / 2

    suitableNoteString = getNoteType(classified, noteDurKeys)
    suitableNoteLength = getNoteLength(int(suitableNoteString))

    while overflow != 0:
        overflow = overflow - suitableNoteLength
        notesToAppendAfterMeasure += 1

    return (classified, notesToFillMeasure, notesToAppendAfterMeasure, suitableNoteString, lengthCounter)
