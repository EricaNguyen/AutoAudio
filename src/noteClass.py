class Note(object):
    def __init__(self, pitch, duration, durationLength, soundPressureLevel):
        self.pitch = pitch
        self.duration = duration
        self.soundPressureLevel = soundPressureLevel
        self.durationLength = durationLength

    def printNote(self):
        print("Pitch: ", self.pitch, "| Duration :", self.duration, "| Duration Note:", self.durationLength, "| Sound Pressure Level:", self.soundPressureLevel)