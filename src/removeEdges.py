#remove rests at start and beginning of recording

def removeEdges(noteList):
    if noteList[0].pitch == 'r':
        del noteList[0]
    if noteList[len(noteList)-1].pitch == 'r':
        del noteList[len(noteList)-1]

    return noteList
