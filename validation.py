import numpy as np
import nested_function_for_validation as nf
import cv2
import pandas as pd

#Create the star image with ra,de,roll = 0
image,stars_within_FOV,star_id_list,star_sensor_coordinates,star_loc = nf.create_star_image(0,0,0)
height,length = image.shape
star_id_list = stars_within_FOV['Star ID']
ra_list = stars_within_FOV['RA']
de_list = stars_within_FOV['DE']

#Create dataframe
data = {
    'Star ID'       :[],
    'RA'            :[],
    'DE'            :[],
    'Sensor Coor'   :[],
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
    data['Sensor Coor'].append(star_sensor_coordinates[index])
    data['Image Coor'].append(star_loc[index])

data = pd.DataFrame(
    data,
    columns=['Star ID','RA','DE','Sensor Coor','Image Coor'])

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

from math import asin
star_ID_list = list(data['Star ID'])
sensor_coord_list = list(data['Sensor Coor'])
for coordinate1 in sensor_coord_list:
    x1 = coordinate1[0]
    y1 = coordinate1[1]
    z1 = coordinate1[2]
    for i,coordinate2 in enumerate(sensor_coord_list):
        x2 = coordinate2[0]
        y2 = coordinate2[1]
        z2 = coordinate2[2]
        resultant = abs((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)/2
        angular_distance = 2*asin(resultant)
        if i==2:
            break
