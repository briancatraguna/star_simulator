import numpy as np
import nested_function_for_validation as nf
import cv2
import pandas as pd

#Create the star image with ra,de,roll = 0
image,stars_within_FOV,star_id_list,star_sensor_coordinates,star_loc,dir_vectors = nf.create_star_image(0,0,0)
height,length = image.shape
star_id_list = stars_within_FOV['Star ID']
ra_list = stars_within_FOV['RA']
de_list = stars_within_FOV['DE']
f=0.00304

#Create dataframe
data = {
    'Star ID'       :[],
    'RA'            :[],
    'DE'            :[],
    'Dir Vector'   :[],
    'Image Coor'    :[]
}

#get index of unphotographed star images
indexes = []
pixel_size = 1.12*(10**-6)
for i,(x,y) in enumerate(star_loc):
    x,y = (x,y)
    x = float(x)
    y = float(y)
    x_pixel = int(round(x/pixel_size))
    y_pixel = int(round(y/pixel_size))
    if x_pixel>=length/2 or y_pixel>=height/2:
        continue
    else:
        indexes.append(i)

#Append the star id with the indexes obtained
for index in indexes:
    data['Star ID'].append(star_id_list[index])
    data['RA'].append(ra_list[index])
    data['DE'].append(de_list[index])
    data['Dir Vector'].append(dir_vectors[index])
    data['Image Coor'].append(star_loc[index])

data = pd.DataFrame(
    data,
    columns=['Star ID','RA','DE','Dir Vector','Image Coor'])

error_calculation = {
    'Star ID'   :[],
    'Ideal Distance 1':[],
    'Distance After Image 1':[],
    'Error 1':[],
    'Ideal Distance 2':[],
    'Distance After Image 2':[],
    'Error 2':[],
    'Ideal Distance 3':[],
    'Distance After Image 3':[],
    'Error 3':[],
}

from math import acos,sqrt,degrees
image_coor_list = list(data['Image Coor'])
for coordinate1 in image_coor_list:
    x,y = coordinate1
    x1 = float(x)
    y1 = float(y)
    for j,coordinate2 in enumerate(image_coor_list):
        bin_name = 'Distance After Image ' + str(j+1)
        x2 = float(coordinate2[0])
        y2 = float(coordinate2[1])
        numerator = (x1*x2)+(y1*y2)+(f**2)
        denominator1 = sqrt(x1**2+y1**2+f**2)
        denominator2 = sqrt(x2**2+y2**2+f**2)
        denominator = denominator1*denominator2
        division = numerator/denominator
        if division>1:
            division = 1
        angular_distance = degrees(acos(division))
        error_calculation[bin_name].append(angular_distance)
        if j == 2:
            break

from math import asin
star_ID_list = list(data['Star ID'])
dir_vectors = list(data['Dir Vector'])
for id in star_ID_list:
    error_calculation['Star ID'].append(id)
for i,coordinate1 in enumerate(dir_vectors):
    index = i
    x1 = coordinate1[0]
    y1 = coordinate1[1]
    z1 = coordinate1[2]
    for j,coordinate2 in enumerate(dir_vectors):
        bin_name = 'Ideal Distance ' + str(j+1)
        x2 = coordinate2[0]
        y2 = coordinate2[1]
        z2 = coordinate2[2]
        resultant = abs((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)/2
        angular_distance = degrees(2*asin(resultant))
        error_calculation[bin_name].append(angular_distance)
        if j==2:
            break



ideal_distance_list_1 = error_calculation['Ideal Distance 1']
ideal_distance_list_2 = error_calculation['Ideal Distance 2']
ideal_distance_list_3 = error_calculation['Ideal Distance 3']
image_distance_list_1 = error_calculation['Distance After Image 1']
image_distance_list_2 = error_calculation['Distance After Image 2']
image_distance_list_3 = error_calculation['Distance After Image 3']
for i in range(len(star_ID_list)):
    index = i
    error1 = abs(ideal_distance_list_1[index] - image_distance_list_1[index])
    error_calculation['Error 1'].append(error1)
    error2 = abs(ideal_distance_list_2[index] - image_distance_list_2[index])
    error_calculation['Error 2'].append(error2)
    error3 = abs(ideal_distance_list_3[index] - image_distance_list_3[index])
    error_calculation['Error 3'].append(error3)


print(len(error_calculation['Star ID']))
print(len(error_calculation['Ideal Distance 1']))
print(len(error_calculation['Distance After Image 1']))
print(len(error_calculation['Error 1']))
print(len(error_calculation['Ideal Distance 2']))
print(len(error_calculation['Distance After Image 2']))
print(len(error_calculation['Error 2']))
print(len(error_calculation['Ideal Distance 3']))
print(len(error_calculation['Distance After Image 3']))
print(len(error_calculation['Error 3']))


error = pd.DataFrame(
    error_calculation,
    columns=['Star ID','Ideal Distance 1','Distance After Image 1','Error 1','Ideal Distance 2','Distance After Image 2','Error 2','Ideal Distance 3','Distance After Image 3','Error 3']
)

print(error)

error.to_excel('Validation Error Degrees.xlsx')