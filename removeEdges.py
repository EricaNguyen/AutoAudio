#remove rests at start and beginning of recording

def removeEdges(noteList):
   del noteList[0]
   del noteList[len(noteList)-1]

   return noteList
