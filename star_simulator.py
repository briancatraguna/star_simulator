from math import radians,sin,cos
import numpy as np

#Right ascension, declination and roll input prompt from user
ra = radians(float(input("Enter the right ascension angle in degrees:\n")))
de = radians(float(input("Enter the declination angle in degrees:\n")))
roll = radians(float(input("Enter the roll angle in degrees:\n")))

#Conversion of celestial coordinate system to star sensor coordinate system
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
    print("Matrix is orthogonal...\nMoving on to next calculation")
else:
    print("WARNING: Matrix is not orthogonal")