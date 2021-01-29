from tkinter import *

mainWindow = Tk()
mainWindow.title("Star Simulator")
mainWindow.geometry("1000x750+8+8")
Label(mainWindow,text="Created by Brian Mohammed Catraguna, Flight Physics Laboratory, ITB 2020").grid(row=0,column=0)

inputframe = Frame(mainWindow)
inputframe.grid(row=1,column=0)
ra_input_label = Label(inputframe,text="RA Input (Degrees): ")
ra_input_label.grid(row=0,column=0)
ra_input = Entry(inputframe)
ra_input.grid(row=0,column=1)     
    

mainWindow.mainloop()