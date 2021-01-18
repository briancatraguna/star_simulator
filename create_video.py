import numpy as np
import cv2


images = []
for i in range(100):
    image = np.random.randint(255,size=(200,100))
    images.append(image)
    
fps = 30.0
width,height = images[0].shape
print(width,height)

def create_video(images,fps):
    out = cv2.VideoWriter('project.mp4',cv2.VideoWriter_fourcc(*'mp4v'), fps, (height,width), False)

    for i in range(len(images)):
        out.write(images[i])

    out.release()

create_video(images,fps)
