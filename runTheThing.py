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
	#print(p)
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
master.grid()
controlFrame = Frame(master)
controlFrame.config(bg='green', height = '200', width = '400')
controlFrame.grid(row=0, column=0)
#button definitions
button = Button(controlFrame, text="Start Recording", command = record)
button.grid(row=0)
button2 = Button(controlFrame, text="Stop Recording", command = stopR)
button2.grid(row=2)
button3 = Button(controlFrame, text="Quit", command = quit)
button3.grid(row=4)

#T = Text(master, height=1, width=20)
#T.pack()
#T.insert(END, "Put File Name Here")

#Label of fileName entry field
Label(controlFrame, text="Put Output Filename Here").grid(row=0, column=1)
e1 = Entry(controlFrame)
e1.grid(row=1, column=1)
Label(controlFrame, text="Put the Song Name Here").grid(row=2, column=1)
e2 = Entry(controlFrame)
e2.grid(row=3, column=1)
Label(controlFrame, text="Put the Song Writer's Name Here").grid(row=4, column=1)
e3 = Entry(controlFrame)
e3.grid(row=5, column=1)
#default name
fileName = "NoteSheet"
authorName = "Author"
songName = "My Song 1"
#label for recording/not recording
label = Label(controlFrame, text="Not Recording", font=("Helvetica", 12), fg="black")
label.grid(row=6, column=0)

#makes an instructions panel within the window.
instrPanel = LabelFrame(master, text = 'Instructions go here') 
instrPanel.config(bg='pink', height = '200', width = '400') 
instrPanel.grid(row=0, column=1)
#the text that goes inside the instructions panel
instrText = Message(instrPanel, text="inside text") #replace with instructions text
instrText.config(bg='pink')
instrText.grid(row=1, column=0)

#makes output panel
outputPanel = LabelFrame(master, text = 'Output:') 
outputPanel.config(bg='white', height = '400', width = '800') 
#outputPanel.place(x=0, y=400, anchor="w")
outputPanel.grid(row=3, column = 0, columnspan=2)
#scrollbar
scrollbar = Scrollbar(outputPanel)
scrollbar.pack( side = RIGHT, fill = Y )
#output listed here
mylist = Listbox(outputPanel, yscrollcommand = scrollbar.set )
#mylist = Text(outputPanel, yscrollcommand = scrollbar.set )
for line in range(100): #replace with music note output
	mylist.insert(END, "This is line number " + str(line))
mylist.config(height = '200', width = '200')
mylist.pack( side = LEFT, fill = BOTH )
scrollbar.config( command = mylist.yview )

mainloop()