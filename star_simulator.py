from math import radians,degrees,sin,cos,tan,sqrt,atan,pi,exp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2

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


def draw_star(x,y,magnitude,background):
    """[Draws the star in the background image]

    Args:
        x ([int]): [The x coordinate in the image coordinate system (starting from left to right)]
        y ([int]): [The y coordinate in the image coordinate system (starting from top to bottom)]
        magnitude ([float]): [The stellar magnitude]
        background ([numpy array]): [background image]
    """
    H = 1000*exp(-magnitude+1)
    (length,width) = np.shape(background)
    for u in range(length):
        for v in range(width):
            dist = sqrt(((u-x)**2)+((v-y)**2))
            if dist > 5:
                continue
            diff = (dist**2)/2
            exponent_exp = 1/(exp(diff))
            raw_intensity = (H/(2*pi))*exponent_exp
            background[u,v] = raw_intensity
    return background


def displayImg(img,cmap=None):
    """[Displays image]

    Args:
        img ([numpy array]): [the pixel values in the form of numpy array]
        cmap ([string], optional): [can be 'gray']. Defaults to None.
    """
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    fig = plt.figure(figsize=(12,10))
    ax = fig.add_subplot(111)
    ax.imshow(img,cmap)
    plt.show()


#Right ascension, declination and roll input prompt from user
ra = radians(float(input("Enter the right ascension angle in degrees:\n")))
de = radians(float(input("Enter the declination angle in degrees:\n")))
roll = radians(float(input("Enter the roll angle in degrees:\n")))

#length/pixel
myu = 3*(10**-6)

#Focal length prompt from user
f = 0.016

#Star sensor pixel
l = 1920
w = 1080
print("Resolution length: {}".format(l))
print("Resolution width: {}".format(w))

#Star sensor FOV
FOVy = degrees(2*atan((myu*w/2)/f))
FOVx = degrees(2*atan((myu*l/2)/f))
print("FOV y: {}".format(FOVy))
print("FOV x: {}".format(FOVx))

#STEP 1: CONVERSION OF CELESTIAL COORDINATE SYSTEM TO STAR SENSOR COORDINATE SYSTEM
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
print("*"*80)
print(f"Matrix M:\n {M}")

#Check if matrix is orthogonal
M_inverse = np.round(np.linalg.inv(M),decimals=5)
M_transpose = np.round(np.matrix.transpose(M),decimals=5)
orthogonal_check = []
for row in range(3):
    for column in range(3):
        element_check = M_inverse[row,column] == M_transpose[row,column]
        orthogonal_check.append(element_check)

if all(orthogonal_check):
    print("Matrix M is orthogonal...\nMoving on to next calculation\n")
else:
    print("WARNING: Matrix M is not orthogonal")

#Search for image-able stars
print("Reading in CSV file...\n")
col_list = ["Star ID","RA","DE","Magnitude"]
star_catalogue = pd.read_csv('Below_6.0_SAO.csv',usecols=col_list)
R = (sqrt((radians(FOVx)**2)+(radians(FOVy)**2))/2)
alpha_start = (ra - (R/cos(de)))
alpha_end = (ra + (R/cos(de)))
delta_start = (de - R)
delta_end = (de + R)
print("RA range: {0} to {1}".format(alpha_start,alpha_end))
print("DE range: {0} to {1}".format(delta_start,delta_end))
star_within_ra_range = (alpha_start <= star_catalogue['RA']) & (star_catalogue['RA'] <= alpha_end)
star_within_de_range = (delta_start <= star_catalogue['DE']) & (star_catalogue['DE'] <= delta_end)
star_in_ra = star_catalogue[star_within_ra_range]
star_in_de = star_catalogue[star_within_de_range]
star_in_de = star_in_de[['Star ID']].copy()
stars_within_FOV = pd.merge(star_in_ra,star_in_de,on="Star ID")
print(stars_within_FOV)

#Converting to star sensor coordinate system
ra_i = list(stars_within_FOV['RA'])
de_i = list(stars_within_FOV['DE'])
star_sensor_coordinates = []
print("Star sensor coordinates:\n")
for i in range(len(ra_i)):
    coordinates = dir_vector_to_star_sensor(ra_i[i],de_i[i],M_transpose=M_transpose)
    star_sensor_coordinates.append(coordinates)
    print(coordinates)

#Coordinates in image
star_loc = []
print("Image coordinates:\n")
for coord in star_sensor_coordinates:
    x = f*(coord[0]/coord[2])
    y = f*(coord[1]/coord[2])
    star_loc.append((x,y))
    print("X: {}".format(x))
    print("Y: {}".format(y))

xtot = 2*tan(radians(FOVx)/2)*f
ytot = 2*tan(radians(FOVy)/2)*f
xpixel = l/xtot
ypixel = w/ytot

magnitude_mv = list(stars_within_FOV['Magnitude'])

pixel_coordinates = []
print("*"*100)
print("Pixel coordinates:\n")
delete_indices = []
for i,(x1,y1) in enumerate(star_loc):
    x1 = float(x1)
    y1 = float(y1)
    if abs(x1) > l/2 or abs(y1) > w/2:
        delete_indices.append(i)
        continue
    x1pixel = round(xpixel*x1)
    y1pixel = round(ypixel*y1)
    pixel_coordinates.append((x1pixel,y1pixel))
    print("X: {}".format(x1pixel))
    print("Y: {}".format(y1pixel))

for index in delete_indices:
    del magnitude_mv[index]

background = np.zeros((w,l))

for i in range(len(magnitude_mv)):
    x = round(l/2 + pixel_coordinates[i][0])
    y = round(w/2 - pixel_coordinates[i][1])
    print("Drawing star {0} of {1}".format(i+1,len(magnitude_mv)))
    print("Location:\n X:{0}, Y:{1}".format(x,y))
    background = draw_star(x,y,magnitude=magnitude_mv[i],background=background)

cv2.imshow("Image",background)
cv2.waitKey(0)