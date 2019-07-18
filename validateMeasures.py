#validateMeasures.py

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
    q = sumOfDuration / len(noteList)
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
    for c in myString:
        if c == ',':
            commCount += 1
            break
        if c == "'":
            aposCount += 1
            break
    return (commCount, aposCount)

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