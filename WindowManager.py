from tkinter import *
import tkinter as tk
import os
import signal
import subprocess

#p = subprocess.Popen(['head', 'README.txt'])
#command definitions
#record button functions, aka button
bool = 0

class App(tk.Frame):
    def __init__(self, master=None): #where info on what the window displays is defined
        super().__init__(master)
        self.pack() #where user input and instructions go

        #makes a control panel within the window. We will use this to hold the buttons
        controlPanel = LabelFrame(self, text = 'Control Panel') 
        controlPanel.config(bg='lightgreen', height = '200', width = '400') 
        controlPanel.pack(side = LEFT)
        
        #buttons
        button = Button(controlPanel, text="Start Recording", command = self.record)
        button.place(x=20, y=20, anchor="w")
        button2 = Button(controlPanel, text="Stop Recording", command = self.stopR)
        button2.place(x=20, y=40, anchor="w")
        button3 = Button(controlPanel, text="Quit", command = self.quit)
        button3.place(x=20, y=60, anchor="w")

        #T = Text(master, height=1, width=20)
        #T.pack();
        #T.insert(END, "Put File Name Here")

        #Label of fileName entry field
        Label(controlPanel, text="Put Output Filename Here").place(x=20, y=90, anchor="w")
        e1 = Entry(controlPanel)
        e1.place(x=20, y=80, anchor="w")
        #default name
        fileName = "NoteSheet";
        #label for recording/not recording
        label = Label(controlPanel, text="Not Recording", font=("Helvetica", 12), fg="black")
        label.place(x=20, y=100, anchor="w")
        
        #makes an instructions panel within the window.
        instrPanel = LabelFrame(self, text = 'Instructions go here') 
        instrPanel.config(bg='pink', height = '200', width = '400') 
        instrPanel.pack(side = LEFT, fill = X)
        #the text that goes inside the instructions panel
        instrText = Message(instrPanel, text="inside text") #replace with instructions text
        instrText.config(bg='pink')
        instrText.place(x=20, y=20, anchor="w")
        
        #makes output panel
        outputPanel = LabelFrame(master, text = 'Output:') 
        outputPanel.config(bg='white', height = '400', width = '800') 
        #outputPanel.place(x=0, y=400, anchor="w")
        outputPanel.pack()
        #scrollbar
        scrollbar = Scrollbar(outputPanel)
        scrollbar.pack( side = RIGHT, fill = Y )
        #output listed here
        mylist = Listbox(outputPanel, yscrollcommand = scrollbar.set )
        #mylist = Text(outputPanel, yscrollcommand = scrollbar.set )
        for line in range(100): #replace with music note output
           mylist.insert(END, "This is line number " + str(line))
        mylist.config(height = '400', width = '800')
        mylist.pack( side = LEFT, fill = BOTH )
        scrollbar.config( command = mylist.yview )
        
    def record(self):
        global p
        global bool
        #T.delete('1.0', END)
        #T.insert(END,"Recording")
        label = Label(self, text="Not Recording", font=("Helvetica", 12), fg="black")
        label.place(x = 40, y = 120)
        label.config(text="Recording")
        p = subprocess.Popen(['python', 'freqAnalyzer.py'])
        #test code, use instead of subprocess if thing don't work
        #p = subprocess.Popen(['python', 'runTheThing.py'])
        bool = 1;
        #print(fileName)
        
    #stop record button functions, aka button 2
    def stopR(self):
        global fileName
        global bool
        p.kill()
        #T.delete('1.0', END)
        #T.insert(END,"Not Recording")
        label = Label(self, text="Not Recording", font=("Helvetica", 12), fg="black")
        label.place(x = 40, y = 120)
        label.config(text="Not Recording")
        fileName = e1.get()
        #check if there was any recording done
        if bool == 1:
            #pass filename into lilypond or freqAnalyzer
            bool = 0
        

    #quitting the program, aka button 3
    def quit(self):
        exit()
        
# create the application
myapp = App()

myapp.master.title("AutoAudio")
myapp.master.geometry('800x600')

# start the program
myapp.mainloop()