from math import radians,degrees,sin,cos,tan,sqrt,atan,pi,exp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2

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
# a1 = (sin(ra)*cos(roll)) - (cos(ra)*sin(de)*sin(roll))
# a2 = -(sin(ra)*sin(roll)) - (cos(ra)*sin(de)*cos(roll))
# a3 = -(cos(ra)*cos(de))
# b1 = -(cos(ra)*cos(roll)) - (sin(ra)*sin(de)*sin(roll))
# b2 = (cos(ra)*sin(roll)) - (sin(ra)*sin(de)*cos(roll))
# b3 = -(sin(ra)*cos(de))
# c1 = (cos(ra)*sin(roll))
# c2 = (cos(ra)*cos(roll))
# c3 = -(sin(de))
# M = np.array([[a1,a2,a3],[b1,b2,b3],[c1,c2,c3]])
ra_exp = ra - (pi/2)
de_exp = de + (pi/2)
M1 = np.array([[cos(ra_exp),-sin(ra_exp),0],[sin(ra_exp),cos(ra_exp),0],[0,0,1]])
M2 = np.array([[1,0,0],[0,cos(de_exp),-sin(de_exp)],[0,sin(de_exp),cos(de_exp)]])
M3 = np.array([[cos(roll),-sin(roll),0],[sin(roll),cos(roll),0],[0,0,1]])
first_second = np.matmul(M1,M2)
M = np.matmul(first_second,M3)

print("*"*80)
print(f"Matrix M:\n {M}")

#Check if matrix is orthogonal
M_inverse = np.round(np.linalg.inv(M),decimals=5)
M_transpose = np.round(np.matrix.transpose(M),decimals=5)
print(M_inverse)
print(M_transpose)
orthogonal_check = []
for row in range(3):
    for column in range(3):
        element_check = M_inverse[row,column] == M_transpose[row,column]
        orthogonal_check.append(element_check)

if all(orthogonal_check):
    print("Matrix M is orthogonal...\nMoving on to next calculation\n")
else:
    print("WARNING: Matrix M is not orthogonal")