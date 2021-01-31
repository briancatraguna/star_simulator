from tkinter import *

mainWindow = Tk()
mainWindow.title("Star Simulator")
mainWindow.geometry("1000x750+8+8")
Label(mainWindow,text="Created by Author").grid(row=0,column=0)

mainWindow.columnconfigure(0,weight=1)
mainWindow.columnconfigure(1,weight=5)

#INPUT FRAME
inputframe = Frame(mainWindow)
inputframe.grid(row=1,column=0,sticky='n')
inputframe.config(relief='sunken',borderwidth=2)

#Attitude Sub - Frame
attitudeframe = LabelFrame(inputframe,text="Attitude")
attitudeframe.grid(row=0,column=0,sticky='w')

ra_input_label = Label(attitudeframe,text="Right Ascension α (degrees): ")
ra_input_label.grid(row=0,column=0)
ra_input = Spinbox(attitudeframe,width=10,values=tuple(range(-180,180)))
ra_input.grid(row=0,column=1)

de_input_label = Label(attitudeframe,text="Declination δ (degrees): ")
de_input_label.grid(row=1,column=0)
de_input = Spinbox(attitudeframe,width=10,values=tuple(range(-90,90)))
de_input.grid(row=1,column=1)

roll_input_label = Label(attitudeframe,text="Roll φ (degrees): ")
roll_input_label.grid(row=2,column=0)
roll_input = Spinbox(attitudeframe,width=10,values=tuple(range(0,360)))
roll_input.grid(row=2,column=1)

#Sensor Settings Sub - Frame
settingsframe = LabelFrame(inputframe,text="Sensor Settings")
settingsframe.grid(row=0,column=1,sticky='e')

focal_length_label = Label(settingsframe,text="Focal Length f (mm): ")
focal_length_label.grid(row=0,column=0)
focal_length = Entry(settingsframe)
focal_length.grid(row=0,column=1)

miu_label = Label(settingsframe,text="Length per Pixel μ (μm): ")
miu_label.grid(row=1,column=0)
miu = Entry(settingsframe)
miu.grid(row=1,column=1)

res_l_label = Label(settingsframe,text="Horizontal Resolution (pixels): ")
res_l_label.grid(row=2,column=0)
res = Entry(settingsframe)
res.grid(row=2,column=1)

res_h_label = Label(settingsframe,text="Vertical Resolution (pixels): ")
res_h_label.grid(row=3,column=0)
res_h = Entry(settingsframe)
res_h.grid(row=3,column=1)

mainWindow.mainloop()