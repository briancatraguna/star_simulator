from tkinter import *

mainWindow = Tk()
mainWindow.title("Star Simulator")
mainWindow.geometry("1000x750+8+8")
Label(mainWindow,text="Created by Brian Mohammed Catraguna, Flight Physics Laboratory, ITB 2020").grid(row=0,column=0)

#INPUT FRAME
inputframe = Frame(mainWindow)
inputframe.grid(row=1,column=0,sticky='w')

#Configure grids in input frame
inputframe.columnconfigure(0,weight=1)
inputframe.columnconfigure(1,weight=1)
inputframe.columnconfigure(2,weight=1)

ra_input_label = Label(inputframe,text="Right Ascension Input (Degrees): ")
ra_input_label.grid(row=0,column=0)
ra_input = Entry(inputframe)
ra_input.grid(row=0,column=1)

de_input_label = Label(inputframe,text="Declination Input (Degrees): ")
de_input_label.grid(row=0,column=2)
    

mainWindow.mainloop()