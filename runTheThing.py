from tkinter import *
import os
import signal
import subprocess

#import freqAnalyzer

p = subprocess.Popen(['head', 'README.txt'])
#command definitions
#record button functions, aka button
bool = 0;
def record():
	global p
	global bool
	#T.delete('1.0', END)
	#T.insert(END,"Recording")
	label.config(text="Recording")
	p = subprocess.Popen(['python', 'freqAnalyzer.py'])
	#test code, use instead of subprocess if thing don't work
	#p = subprocess.Popen(['python', 'runTheThing.py'])
	bool = 1;
	#print(fileName)
	
#stop record button functions, aka button 2
def stopR():
	global fileName
	global bool
	p.kill()
	#T.delete('1.0', END)
	#T.insert(END,"Not Recording")
	label.config(text="Not Recording")
	fileName = e1.get()
	#check if there was any recording done
	if bool == 1:
		#pass filename into lilypond or freqAnalyzer
		bool = 0;
	

#quitting the program, aka button 3
def quit():
	exit()
	
master = Tk()
master.title("AutoAudio")
frame = Frame(master)
frame.grid()
#button definitions
button = Button(master, text="Start Recording", command = record)
button.grid(row=0)
button2 = Button(master, text="Stop Recording", command = stopR)
button2.grid(row=1)
button3 = Button(master, text="Quit", command = quit)
button3.grid(row=2)

#T = Text(master, height=1, width=20)
#T.pack();
#T.insert(END, "Put File Name Here")

#Label of fileName entry field
Label(master, text="Put Output Filename Here").grid(row=0, column=1)
e1 = Entry(master)
e1.grid(row=1, column=1)
#default name
fileName = "NoteSheet";
#label for recording/not recording
label = Label(master, text="Not Recording", font=("Helvetica", 12), fg="black")
label.grid(row=2, column=1)
mainloop()