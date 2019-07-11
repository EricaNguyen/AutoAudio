from tkinter import *
import tkinter as tk

class App(tk.Frame):
    def __init__(self, master=None): #where info on what the window displays is defined
        super().__init__(master)
        self.pack() #where user input and instructions go

        #makes a control panel within the window. We will use this to hold the buttons
        controlPanel = LabelFrame(self, text = 'Control Panel') 
        controlPanel.config(bg='lightgreen', height = '200', width = '400') 
        controlPanel.pack(side = LEFT)
        
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
        for line in range(100): #replace with music note output
           mylist.insert(END, "This is line number " + str(line))
        mylist.config(height = '400', width = '800')
        mylist.pack( side = LEFT, fill = BOTH )
        scrollbar.config( command = mylist.yview )
        
# create the application
myapp = App()

myapp.master.title("AutoAudio")
myapp.master.geometry('800x600')

# start the program
myapp.mainloop()