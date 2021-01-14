from math import radians,degrees,sin,cos,tan,sqrt,atan,pi,exp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2

def draw_star(x,y,magnitude,gaussian,background,ROI=5):
    """[Draws the star in the background image]

    Args:
        x ([int]): [The x coordinate in the image coordinate system (starting from left to right)]
        y ([int]): [The y coordinate in the image coordinate system (starting from top to bottom)]
        magnitude ([float]): [The stellar magnitude]
        gaussian ([bool]): [True if using the gaussian function, false if using own function]
        background ([numpy array]): [background image]
        ROI ([int]): [The ROI of each star in pixel radius]
    """
    if gaussian:
        H = 2000*exp(-magnitude+1)
        sigma = 5
        for u in range(x-ROI,x+ROI+1):
            for v in range(y-ROI,y+ROI+1):
                dist = ((u-x)**2)+((v-y)**2)
                diff = (dist)/(2*(sigma**2))
                exponent_exp = 1/(exp(diff))
                raw_intensity = int(round((H/(2*pi*(sigma**2)))*exponent_exp))
                if u == x and v == y:
                    print(raw_intensity)
                background[v,u] = raw_intensity
    else:
        # mag = abs(magnitude-7) #1 until 9
        # radius = 
        # color = 
        # cv2.circle(background,(x,y),radius,color,thickness=-1)
        cv2.circle(background,(x,y),2,255,thickness=-1)

    return background


def displayImg(img,cmap=None):
    """[Displays image]

    Args:
        img ([numpy array]): [the pixel values in the form of numpy array]
        cmap ([string], optional): [can be 'gray']. Defaults to None.
    """
    fig = plt.figure(figsize=(12,10))
    ax = fig.add_subplot(111)
    ax.imshow(img,cmap)
    plt.show()


background = np.zeros((1080,1920))
background = draw_star(100,100,2,False,background)

displayImg(background,cmap='gray')
