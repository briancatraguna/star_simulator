from tkinter import *
from PIL import ImageTk,Image
import cv2
import nested_function as nf

def rescale_image(image,percentage=25):
    """[resizes image]

    Args:
        image ([numpy array]): [image to be rescaled]
    """
    scale_percent = percentage
    width = int(image.shape[1] * scale_percent/100)
    height = int(image.shape[0] * scale_percent/100)
    dsize = (width,height)
    output = cv2.resize(image,dsize)
    return output


def create_star_image(ra,de,roll,f,myu):
    """[create star image command when button is pressed]

    Args:
        ra ([int]): [right ascension from the spinner]
        de ([int]): [declination from the spinner]
        roll ([int]): [roll from the spinner]
        f ([float]): [focal length from the entry]
        myu ([float]): [length per pixel from the entry]
    """
    ra_calc = (ra.get())
    de_calc = (de.get())
    roll_calc = (roll.get())
    f_calc = float((f.get()))
    myu_calc = float((myu.get()))
    star_image = nf.create_star_image(ra_calc,de_calc,roll_calc,f_calc,myu_calc)



mainWindow = Tk()
mainWindow.title("Star Simulator")
mainWindow.geometry("1000x780+8+8")
mainWindow.configure(bg='gray')
created_label = Label(mainWindow,text="Created by Brian Mohammed Catraguna, Flight Physics Laboratory, Faculty of Mechanical and Aerospace Engineering, Bandung Institue of Technology")
created_label.grid(row=0,column=0,sticky='nsew',columnspan=3)

mainWindow.columnconfigure(0,weight=1)

#INPUT FRAME
inputframe = Frame(mainWindow,width=1000)
inputframe.grid(row=1,column=0,sticky='n')
inputframe.config(relief='sunken',borderwidth=3)

#Attitude Sub - Frame
attitudeframe = LabelFrame(inputframe,text="Attitude")
attitudeframe.grid(row=0,column=0)

ra = IntVar()
de = IntVar()
roll = IntVar()

f = StringVar()
myu = StringVar()

ra_input_label = Label(attitudeframe,text="Right Ascension α (degrees): ")
ra_input_label.grid(row=0,column=0)
ra_input = Spinbox(attitudeframe,width=10,values=tuple(range(-180,180)),textvariable=ra)
ra_input.grid(row=0,column=1)

de_input_label = Label(attitudeframe,text="Declination δ (degrees): ")
de_input_label.grid(row=1,column=0)
de_input = Spinbox(attitudeframe,width=10,values=tuple(range(-90,90)),textvariable=de)
de_input.grid(row=1,column=1)

roll_input_label = Label(attitudeframe,text="Roll φ (degrees): ")
roll_input_label.grid(row=2,column=0)
roll_input = Spinbox(attitudeframe,width=10,values=tuple(range(0,360)),textvariable=roll)
roll_input.grid(row=2,column=1)

#Sensor Settings Sub - Frame
settingsframe = LabelFrame(inputframe,text="Sensor Settings")
settingsframe.grid(row=0,column=1)

focal_length_label = Label(settingsframe,text="Focal Length f (mm): ")
focal_length_label.grid(row=0,column=0)
focal_length = Entry(settingsframe,textvariable=f)
focal_length.grid(row=0,column=1)

miu_label = Label(settingsframe,text="Length per Pixel μ (μm): ")
miu_label.grid(row=1,column=0)
miu = Entry(settingsframe,textvariable=myu)
miu.grid(row=1,column=1)

#Generate Star Image Button
generate_button = Button(inputframe,text="Generate Star Image!")
generate_button.grid(row=0,column=2)

#OUTPUT FRAME
outputframe = Frame(mainWindow,width=1000)
outputframe.grid(row=2,column=0,sticky='s')
outputframe.config(relief='ridge',borderwidth=3)

#Creating Canvas for Showing Image
canvas = Canvas(outputframe,width=850,height=700)
canvas.grid(row=0,column=0,sticky='nsew')

my_image = cv2.imread("ra0_de0_roll0.jpg")
my_image = rescale_image(my_image,25)
img =  ImageTk.PhotoImage(image=Image.fromarray(my_image))
canvas.create_image(20,20,anchor=NW,image=img)

mainWindow.mainloop()