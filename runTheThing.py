from tkinter import *
import os
import signal
import subprocess

#import freqAnalyzer

p = subprocess.Popen(['head', 'README.txt'])
#command definitions
def record():
	global p
	T.delete('1.0', END)
	T.insert(END,"Recording")
	p = subprocess.Popen(['python', 'freqAnalyzer.py'])
	#test code, use instead of subprocess if thing don't work
	#p = subprocess.Popen('ls')
	
def stopR():
	#will not work with test code, as p will terminate on its own very quick,
	p.kill()
	T.delete('1.0', END)
	T.insert(END,"Not Recording")

def quit():
	exit()
	
master = Tk()
frame = Frame(master)
frame.pack()
#button definitions
button = Button(master, text="Start Recording", command = record)
button.pack(side=LEFT)
button2 = Button(master, text="Stop Recording", command = stopR)
button2.pack(side=LEFT)
button3 = Button(master, text="Quit", command = quit)
button3.pack(side=LEFT)
T = Text(master, height=1, width=14)
T.pack();
T.insert(END, "Not Recording")
mainloop()