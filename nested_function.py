from math import radians,degrees,sin,cos,tan,sqrt,atan,pi,exp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2

def displayImg(img,cmap='gray'):
    """[Displays image]

    Args:
        img ([numpy array]): [the pixel values in the form of numpy array]
        cmap ([string], optional): [can be 'gray']. Defaults to None.
    """
    fig = plt.figure(figsize=(12,10))
    ax = fig.add_subplot(111)
    ax.imshow(img,cmap)
    plt.show()

def create_star_image(ra,de,roll):
    """[summary]

    Args:
        ra ([float]): [right ascension in degrees]
        de ([float]): [declination in degrees]
        roll ([float]): [roll in degrees]
    """


    def create_M_matrix(ra,de,roll,method=2):
        """[summary]

        Args:
            ra ([int]): [right ascension of sensor center]
            de ([int]): [declination of sensor center]
            roll ([int]): [roll angle of star sensor]
            method ([int]): [1 for method 1(Calculating each elements),2 for method 2(calculating rotation matrices)]
        """
        if method == 1:
            a1 = (sin(ra)*cos(roll)) - (cos(ra)*sin(de)*sin(roll))
            a2 = -(sin(ra)*sin(roll)) - (cos(ra)*sin(de)*cos(roll))
            a3 = -(cos(ra)*cos(de))
            b1 = -(cos(ra)*cos(roll)) - (sin(ra)*sin(de)*sin(roll))
            b2 = (cos(ra)*sin(roll)) - (sin(ra)*sin(de)*cos(roll))
            b3 = -(sin(ra)*cos(de))
            c1 = (cos(ra)*sin(roll))
            c2 = (cos(ra)*cos(roll))
            c3 = -(sin(de))
            M = np.array([[a1,a2,a3],[b1,b2,b3],[c1,c2,c3]])
        if method == 2:
            ra_exp = ra - (pi/2)
            de_exp = de + (pi/2)
            M1 = np.array([[cos(ra_exp),-sin(ra_exp),0],[sin(ra_exp),cos(ra_exp),0],[0,0,1]])
            M2 = np.array([[1,0,0],[0,cos(de_exp),-sin(de_exp)],[0,sin(de_exp),cos(de_exp)]])
            M3 = np.array([[cos(roll),-sin(roll),0],[sin(roll),cos(roll),0],[0,0,1]])
            first_second = np.matmul(M1,M2)
            M = np.matmul(first_second,M3)
        return M


    def dir_vector_to_star_sensor(ra,de,M_transpose):
        """[Converts direction vector to star sensor coordinates]

        Args:
            ra ([int]): [right ascension of the object vector]
            de ([int]): [desclination of the object vector]
            M_transpose ([numpy array]): [rotation matrix from direction vector to star sensor transposed]
        """    
        x_dir_vector = (cos(ra)*cos(de))
        y_dir_vector = (sin(ra)*cos(de))
        z_dir_vector = (sin(de))
        dir_vector_matrix = np.array([[x_dir_vector],[y_dir_vector],[z_dir_vector]])
        return M_transpose.dot(dir_vector_matrix)


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
                    background[v,u] = raw_intensity
        else:
            mag = abs(magnitude-7) #1 until 9
            radius = int(round((mag/9)*(5)+2))
            color = int(round((mag/9)*(155)+100))
            cv2.circle(background,(x,y),radius,color,thickness=-1)
        return background

    def add_noise(low,high,background):
        """[Adds noise to an image]

        Args:
            low ([int]): [lower threshold of the noise generated]
            high ([int]): [maximum pixel value of the noise generated]
            background ([numpy array]): [the image that is put noise on]
        """
        row,col = np.shape(background)
        background = background.astype(int)
        noise = np.random.randint(low,high=high,size=(row,col))
        noised_img = cv2.addWeighted(noise,0.1,background,0.9,0)
        return noised_img


    #Right ascension, declination and roll
    ra = radians(float(ra))
    de = radians(float(de))
    roll = radians(float(roll))

    #length/pixel
    myu = 3*(10**-6)

    #Focal length prompt from user
    f = 0.016

    #Star sensor pixel
    l = 1920
    w = 1080

    #Star sensor FOV
    FOVy = degrees(2*atan((myu*w/2)/f))
    FOVx = degrees(2*atan((myu*l/2)/f))

    #STEP 1: CONVERSION OF CELESTIAL COORDINATE SYSTEM TO STAR SENSOR COORDINATE SYSTEM
    M = create_M_matrix(ra,de,roll)
    M_transpose = np.round(np.matrix.transpose(M),decimals=5)

    #Search for image-able stars
    col_list = ["Star ID","RA","DE","Magnitude"]
    star_catalogue = pd.read_csv('Below_6.0_SAO.csv',usecols=col_list)
    R = (sqrt((radians(FOVx)**2)+(radians(FOVy)**2))/2)
    alpha_start = (ra - (R/cos(de)))
    alpha_end = (ra + (R/cos(de)))
    delta_start = (de - R)
    delta_end = (de + R)
    star_within_ra_range = (alpha_start <= star_catalogue['RA']) & (star_catalogue['RA'] <= alpha_end)
    star_within_de_range = (delta_start <= star_catalogue['DE']) & (star_catalogue['DE'] <= delta_end)
    star_in_ra = star_catalogue[star_within_ra_range]
    star_in_de = star_catalogue[star_within_de_range]
    star_in_de = star_in_de[['Star ID']].copy()
    stars_within_FOV = pd.merge(star_in_ra,star_in_de,on="Star ID")

    #Converting to star sensor coordinate system
    ra_i = list(stars_within_FOV['RA'])
    de_i = list(stars_within_FOV['DE'])
    star_sensor_coordinates = []
    for i in range(len(ra_i)):
        coordinates = dir_vector_to_star_sensor(ra_i[i],de_i[i],M_transpose=M_transpose)
        star_sensor_coordinates.append(coordinates)

    #STEP 2: CONVERSION OF STAR SENSOR COORDINATE SYSTEM TO IMAGE COORDINATE SYSTEM
    star_loc = []
    for coord in star_sensor_coordinates:
        x = f*(coord[0]/coord[2])
        y = f*(coord[1]/coord[2])
        star_loc.append((x,y))

    xtot = 2*tan(radians(FOVx)/2)*f
    ytot = 2*tan(radians(FOVy)/2)*f
    xpixel = l/xtot
    ypixel = w/ytot

    magnitude_mv = list(stars_within_FOV['Magnitude'])
    filtered_magnitude = []

    #Rescaling to pixel sizes
    pixel_coordinates = []
    delete_indices = []
    for i,(x1,y1) in enumerate(star_loc):
        x1 = float(x1)
        y1 = float(y1)
        x1pixel = round(xpixel*x1)
        y1pixel = round(ypixel*y1)
        if abs(x1pixel) > l/2 or abs(y1pixel) > w/2:
            delete_indices.append(i)
            continue
        pixel_coordinates.append((x1pixel,y1pixel))
        filtered_magnitude.append(magnitude_mv[i])

    background = np.zeros((w,l))

    for i in range(len(filtered_magnitude)):
        x = round(l/2 + pixel_coordinates[i][0])
        y = round(w/2 - pixel_coordinates[i][1])
        background = draw_star(x,y,filtered_magnitude[i],False,background)

    #Adding noise
    background = add_noise(0,50,background=background)

    return background