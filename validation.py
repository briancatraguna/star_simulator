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

print(data)