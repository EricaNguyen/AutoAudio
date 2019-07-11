from tkinter import *
import os
import signal
import subprocess

#import freqAnalyzer

p = subprocess.Popen(['head', 'README.txt'])
#command definitions
#record button functions, aka button
def record():
	global p
	#T.delete('1.0', END)
	#T.insert(END,"Recording")
	label.config(text="Recording")
	#p = subprocess.Popen(['python', 'freqAnalyzer.py'])
	#test code, use instead of subprocess if thing don't work
	#p = subprocess.Popen(['python', 'runTheThing.py'])
	
#stop record button functions, aka button 2
def stopR():
	p.kill()
	T.delete('1.0', END)
	#T.insert(END,"Not Recording")
	label.config(text="Not Recording")

#quitting the program, aka button 3
def quit():
	exit()
	
master = Tk()
master.title("AutoAudio")
frame = Frame(master)
frame.pack()
#button definitions
button = Button(master, text="Start Recording", command = record)
button.pack(side=LEFT)
button2 = Button(master, text="Stop Recording", command = stopR)
button2.pack(side=LEFT)
button3 = Button(master, text="Quit", command = quit)
button3.pack(side=LEFT)
T = Text(master, height=1, width=20)
T.pack();
T.insert(END, "Put File Name Here")
label = Label(master, text="Not Recording", font=("Helvetica", 12), fg="black")
label.pack()
mainloop(
)