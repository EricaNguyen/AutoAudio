#appendStaffs.py

rest = 'r'
bar = '| '
tie = '~ '
space = ' '
#---------------given---------given------------specified-----specified-------given---given---------------------given---------------given---given---
def appendLower(fullMeasure, exceedingMeasure, lengthString, pitch, notesToAppendAfterMeasure, notesToFillMeasure, staffl, staffu):
    if fullMeasure:
        pitch = pitch + lengthString + space
        #Append note to lower staff
        staffl += pitch
        #Otherwise append a rest to upper staff with corresponding duration
        staffu += rest + lengthString + space
        #Append the bar to both staffs to cut valid measure
        staffl += bar
        staffu += bar
    elif exceedingMeasure:
        pitchTied = pitch + lengthString + tie
        staffu += rest + lengthString + space
        staffl += pitchTied

        for _ in range(notesToFillMeasure-1):
            staffl += pitch + tie
            staffu += rest + lengthString + space

        staffl += bar
        staffu += bar

        for _ in range(notesToAppendAfterMeasure-1):
            staffl += pitch + tie
            staffu += rest + lengthString + space

        staffl += pitch + space
        staffu += rest + lengthString + space
    
    else: # An invalid measure that has yet to be filled up
        pitch = pitch + lengthString + space
        staffl += pitch
        staffu += rest + lengthString + space
    
    return (staffl, staffu)

def appendUpper(fullMeasure, exceedingMeasure, lengthString, pitch, notesToAppendAfterMeasure, notesToFillMeasure, staffl, staffu):
    if fullMeasure:
        pitch = pitch + lengthString + space
        #Append note to lower staff
        staffu += pitch
        #Otherwise append a rest to upper staff with corresponding duration
        staffl += rest + lengthString + space
        #Append the bar to both staffs to cut valid measure
        staffu += bar
        staffl += bar
    elif exceedingMeasure:
        pitchTied = pitch + lengthString + tie
        staffl += rest + lengthString + space
        staffu += pitchTied

        for _ in range(notesToFillMeasure-1):
            staffu += pitch + tie
            staffl += rest + lengthString + space

        staffl += bar
        staffu += bar

        for _ in range(notesToAppendAfterMeasure-1):
            staffu += pitch + tie
            staffl += rest + lengthString + space

        staffu += pitch + space
        staffl += rest + lengthString + space
    
    else: # An invalid measure that has yet to be filled up
        pitch = pitch + lengthString + space
        staffu += pitch
        staffl += rest + lengthString + space
    
    return (staffl, staffu)

def appendRests(fullMeasure, exceedingMeasure, lengthString, pitch, notesToAppendAfterMeasure, notesToFillMeasure, staffl, staffu):
    if fullMeasure:
        pitch = pitch + lengthString + space
        staffu += pitch
        staffl += pitch
        staffu += bar
        staffl += bar
    elif exceedingMeasure:
        for _ in range(notesToFillMeasure):
            staffl += pitch + lengthString + space
            staffu += pitch + lengthString + space
            
        staffl += bar
        staffu += bar

        for _ in range(notesToAppendAfterMeasure):
            staffl += pitch + lengthString + space
            staffu += pitch + lengthString + space
    else:
        pitch = pitch + lengthString + space
        staffu += pitch
        staffl += pitch

    return (staffl, staffu)
