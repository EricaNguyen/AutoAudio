from tkinter import *
import tkinter as tk
import os
import sys
import signal
import subprocess

#pyinstaller --onefile --hidden-import tkinter -F src/AutoAudio.py

bool = 0 #used for record button functions. 0 means not recording, 1 means recording

class App(tk.Frame): #class for making the window
    
    def __init__(self, master=None): #where info on what the window displays is defined
        super().__init__(master)
        
        self.pack() #where user input and instructions go

        #makes a control panel within the window. We will use this to hold the buttons
        controlPanel = LabelFrame(self, text = 'Control Panel') 
        controlPanel.config(height = '250', width = '400') 
        controlPanel.pack(side = LEFT)
        self.create_controls_widgets(controlPanel)
        
        #makes an instructions panel within the window.
        instrPanel = LabelFrame(self, text = 'Instructions') 
        instrPanel.config(height = '250', width = '400') 
        instrPanel.pack(side = LEFT)
        self.create_instructions(instrPanel)
        
    def create_controls_widgets(self, panel): #where info displayed in control panel is defined
        #global e1
        #global e2
        #global e3
        
        #button images
        global photo
        global photo2
        
        #display status for recording/not recording
        label = Label(panel, text="Not Recording", font=("Helvetica", 12), fg="red", bg="light gray")
        label.place(x=220, y=45, anchor="w")
        
        '''Label of fileName entry field (does not work)
        Label(panel, text="Put Output Filename Here:").place(x=20, y=60, anchor="w")
        e1 = Entry(panel)
        e1.place(x=170, y=60, anchor="w")
        Label(panel, text="Put the Song Name Here:").place(x=20, y=90, anchor="w")
        e2 = Entry(panel)
        e2.place(x=165, y=90, anchor="w")
        Label(panel, text="Put the Song Writer's Name Here:").place(x=20, y=120, anchor="w")
        e3 = Entry(panel)
        e3.place(x=205, y=120, anchor="w")
        default name
        fileName = "NoteSheet"
        authorName = "Author"
        songName = "My Song 1"'''
        
        #buttons for control panel
        location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(sys.argv[0])))
        photo = PhotoImage(file = os.path.join(location,'startbutton.png'))
        button = Button(panel, text="Start Recording", command = self.record, image = photo, compound=TOP, bd=0)
        button.place(x=20, y=20, anchor="nw")
        photo2 = PhotoImage(file = os.path.join(location,'stopbutton.png'))
        button2 = Button(panel, text="Stop Recording", command = self.stopR, image = photo2, compound=TOP, bd=0)
        button2.place(x=120, y=20, anchor="nw")
        button3 = Button(panel, text="Quit AutoAudio", command = self.quit)
        button3.place(x=20, y=190, anchor="w")
        
    def create_instructions(self, panel): #the text that goes inside the instructions panel  
        instrText = Message(panel, text="Welcome to AutoAudio!\n\nThis program uses the LilyPond music engraving program to help YOU write your own sheet music!\nNo need to understand complex music theory!\nJust hit “Start Recording” and start singing, playing your favorite instrument, or just making sounds.\nWhen you’re done expressing yourself, press “Stop Recording” and your song will be written for you.\nCheck the src folder and double-click on “ouput.pdf” to see your sheet music!\nNow anyone can be a music composer! Hit “Start” and have fun!\n\nInstall LilyPond: lilypond.org", font=("Helvetica", 8)) #replace with instructions text
        instrText.config(width = '350')
        instrText.place(x=20, y=0, anchor='nw')
       
    def record(self): #records the user's sound
        global p
        global bool
        if bool == 0: #check if user is not already recording
            label = Label(self, text="    Recording   ", font=("Helvetica", 12), fg="green", bg="light gray")
            label.place(x=222, y=61, anchor="w")
            subprocess.call(r'.\scripts\cleaner.sh',shell = True)
            p = subprocess.Popen([r'python', r'.\core\main.py'])
        bool = 1
        
    def stopR(self): #stops recording
        global fileName
        global songName
        global authorName
        global bool
        if bool == 1: #check if user was recording
            pid = p.pid
            os.kill(pid, signal.CTRL_C_EVENT) #ends recording and saves input
            bool = 0
            label = Label(self, text="Not Recording", font=("Helvetica", 12), fg="red", bg="light gray")
            label.place(x=222, y=61, anchor="w")
            try:
                subprocess.call(r'.\scripts\finished.sh', shell = True)
            except:
                pass
            #open("output.pdf")
            # if e1.get() != "":
                # fileName = e1.get()
            # if e2.get() != "":
                # songName = e2.get()
            # if e3.get() != "":
                # authorName = e3.get()
            #check if there was any recording done
            #pass filename into lilypond or freqAnalyzer
        bool = 0
		    
    def quit(self): #exits the program
        if bool == 1:
            App.stopR(self)
        sys.exit()
        
    def getFName():
        global fileName
        return fileName

    def getAName():
        global authorName
        return authorName

    def getSName():
        global songName
        return songName
        
# create the application for the user to see
myapp = App()

myapp.master.title("AutoAudio")
myapp.master.geometry('800x250')

# start the program
myapp.mainloop()