from math import radians,degrees,sin,cos,tan,sqrt,atan,pi
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

def find_edges(arr):
    """[Finds the respective edges]

    Args:
        arr ([arr]): [array of arrays containing x and y of the edges]

    Returns:
        [tuple]: [tuple of coordinates including top left, top right, bottom left, bottom right respectively]
    """
    x = arr[:][0]
    y = arr[:][1]
    top_left = (min(x),max(y))
    top_right = (max(x),max(y))
    bottom_left = (min(x),min(y))
    bottom_right = (max(x),min(y))
    return top_left,top_right,bottom_left,bottom_right

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
myu = 0.25*(10**-6)

#Focal length prompt from user
f = 0.003044898

#Star sensor pixel
l = 3280
w = 2464

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
star_within_ra_range = ((ra - (R/cos(de))) <= star_catalogue['RA']) & (star_catalogue['RA'] <= (ra + (R/cos(de))))
star_within_de_range = ((de - R) <= star_catalogue['DE']) & (star_catalogue['DE'] <= (de + R))
star_in_ra = star_catalogue[star_within_ra_range]
star_in_de = star_catalogue[star_within_de_range]
star_in_de = star_in_de[['Star ID']].copy()
stars_within_FOV = pd.merge(star_in_ra,star_in_de,on="Star ID")

#Find A,B,C,D
A = ((ra - (R/cos(de))),(de - R)) #Bottom left
B = ((ra + (R/cos(de))),(de - R)) #Bottom right
C = ((ra + (R/cos(de))),(de + R)) #Top right
D = ((ra - (R/cos(de))),(de + R)) #Top left
edges = [A,B,C,D]
print("Edges:\n")
for ra,de in edges:
    print(degrees(ra),degrees(de))
edges_coordinates = []
for ra,de in edges:
    coordinates = dir_vector_to_star_sensor(ra,de,M_transpose=M_transpose)
    edges_coordinates.append(coordinates)

#Converting to star sensor coordinate system
ra_i = list(stars_within_FOV['RA'])
de_i = list(stars_within_FOV['DE'])
print("Length of RA:{}".format(len(ra_i)))
for ra in ra_i:
    print(degrees(ra))
print("Length of DE:{}".format(len(de_i)))
for de in de_i:
    print(degrees(de))
star_sensor_coordinates = []
for i in range(len(ra_i)):
    coordinates = dir_vector_to_star_sensor(ra_i[i],de_i[i],M_transpose=M_transpose)
    star_sensor_coordinates.append(coordinates)
    print(coordinates)

#Coordinates in image
image_edges = []
for coord in edges_coordinates:
    x = f*(coord[0]/coord[2])
    y = f*(coord[1]/coord[2])
    image_edges.append((x,y))

star_loc = []
for coord in star_sensor_coordinates:
    x = f*(coord[0]/coord[2])
    y = f*(coord[1]/coord[2])
    star_loc.append((x,y))
    print(x,y)

xtot = 2*tan(radians(FOVx)/2)*f
ytot = 2*tan(radians(FOVy)/2)*f
xpixel = l/xtot
ypixel = w/ytot

edge_pixel_coordinates = []
for x1,y1 in image_edges:
    x1 = float(x1)
    y1 = float(y1)
    x1pixel = round(xpixel*x1)
    y1pixel = round(ypixel*y1)
    edge_pixel_coordinates.append((x1pixel,y1pixel))

pixel_coordinates = []
for x1,y1 in star_loc:
    x1 = float(x1)
    y1 = float(y1)
    x1pixel = round(xpixel*x1)
    y1pixel = round(ypixel*y1)
    pixel_coordinates.append((x1pixel,y1pixel))

background = np.zeros((w,l))
for x,y in pixel_coordinates:
    print(x,y)

print("Edges coordinates:\n")
for coord in edge_pixel_coordinates:
    print(coord[0],coord[1])