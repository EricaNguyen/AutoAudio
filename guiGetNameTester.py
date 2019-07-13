from tkinter import *
import os
import signal
import subprocess

#import freqAnalyzer
#subprocess that starts everything
p = subprocess.Popen(['head', 'README.txt'])
#command definitions
bool = 0;
#record button functions, aka button
def record():
	global p
	global bool
	if bool == 0:
		#T.delete('1.0', END)
		#T.insert(END,"Recording")
		label.config(text="Recording")
		temp = subprocess.call('cleaner.sh',shell = True)
		p = subprocess.call(['python', 'freqAnalyzer.py'])
		#test code, use instead of subprocess if thing don't work
		#p = subprocess.Popen(['python', 'runTheThing.py'])
	bool = 1
	#print(fileName)
	
#stop record button functions, aka button 2
def stopR():
	global fileName
	global songName
	global authorName
	global bool
	if bool == 1:
		p.terminate()
		#T.delete('1.0', END)
		#T.insert(END,"Not Recording")
		label.config(text="Not Recording")
		if e1.get() != "":
			fileName = e1.get()
		if e2.get() != "":
			songName = e2.get()
		if e3.get() != "":
			authorName = e3.get()
		#check if there was any recording done
		#pass filename into lilypond or freqAnalyzer
	bool = 0
	

#quitting the program, aka button 3
def quit():
	if bool == 1:
		p.terminate()
	exit()

def getFName():
	global fileName
	return fileName

def getAName():
	global authorName
	return authorName

def getSName():
	global songName
	return songName

master = Tk()
master.title("AutoAudio")
frame = Frame(master)
frame.grid()
#button definitions
button = Button(master, text="Start Recording", command = record)
button.grid(row=0)
button2 = Button(master, text="Stop Recording", command = stopR)
button2.grid(row=2)
button3 = Button(master, text="Quit", command = quit)
button3.grid(row=4)

#T = Text(master, height=1, width=20)
#T.pack()
#T.insert(END, "Put File Name Here")

#Label of fileName entry field
Label(master, text="Put Output Filename Here").grid(row=0, column=1)
e1 = Entry(master)
e1.grid(row=1, column=1)
Label(master, text="Put the Song Name Here").grid(row=2, column=1)
e2 = Entry(master)
e2.grid(row=3, column=1)
Label(master, text="Put the Song Writer's Name Here").grid(row=4, column=1)
e3 = Entry(master)
e3.grid(row=5, column=1)
#default name
fileName = "NoteSheet"
authorName = "Author"
songName = "My Song 1"
#label for recording/not recording
label = Label(master, text="Not Recording", font=("Helvetica", 12), fg="black")
label.grid(row=6, column=0)
mainloop()