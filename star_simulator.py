from math import radians,degrees,sin,cos,sqrt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def dir_vector_to_star_sensor(ra,de,M_transpose):
    """[summary]

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

#Right ascension, declination and roll input prompt from user
ra = radians(float(input("Enter the right ascension angle in degrees:\n")))
de = radians(float(input("Enter the declination angle in degrees:\n")))
roll = radians(float(input("Enter the roll angle in degrees:\n")))

#FOV prompt from user
x_fov = radians(float(input("Enter the X - axis FOV in degrees:\n")))
y_fov = radians(float(input("Enter the Y - axis FOV in degrees:\n")))

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
R = sqrt((x_fov**2)+(y_fov**2))/2
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
edges_coordinates = []
for ra,de in edges:
    coordinates = dir_vector_to_star_sensor(ra,de,M_transpose=M_transpose)
    edges_coordinates.append(coordinates)

#Converting to star sensor coordinate system
ra_i = list(stars_within_FOV['RA'])
de_i = list(stars_within_FOV['DE'])
star_sensor_coordinates = []
for i in range(len(ra_i)):
    coordinates = dir_vector_to_star_sensor(ra_i[i],de_i[i],M_transpose=M_transpose)
    star_sensor_coordinates.append(coordinates)

#Prompt Gaussian distribution parameters
mv_magnitude = list(stars_within_FOV['Magnitude'])
sigma = round(float(input("Input sigma:\n")))
K_1 = round(float(input("Input K1:\n")))
K_2 = round(float(input("Input K2:\n")))
K_3 = round(float(input("Input K3:\n")))

H = []
for magnitude in mv_magnitude:
    magnitude = float(magnitude)
    H.append(K_1**((-K_2*magnitude)+K_3))

f_intensity = []