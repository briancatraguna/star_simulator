import nested_function as nf

#User defines the initial attitude
ra = float(input("Input right ascension:\n"))
de = float(input("Input declination:\n"))
roll = float(input("Input roll:\n"))

#Angular rate prompt
direction_sensor = input("Input direction:\n(X for +X)\n(Y for +Y)\n(R for +ROLL)\n")
omega = float(input("Input angular rate in degrees: "))

#Frames per second
fps = 30
duration = int(input("Enter the duration of the video in seconds:\n"))

#Creating images
images = []
angle_increment = omega/fps
total_frames = fps*duration
if direction_sensor.lower() == "x":
    ra_list = [ra]
    for i in range(total_frames):
        ra_append = round(ra_list[-1] + angle_increment,3)
        ra_list.append(ra_append)
    
    for ra_step in ra_list:
        images.append(nf.create_star_image(ra_step,de,roll))

elif direction_sensor.lower() == "y":
    de_list = [de]
    for i in range(total_frames):
        de_append = round(de_list[-1] + angle_increment,3)
        de_list.append(de_append)
    
    for de_step in de_list:
        images.append(nf.create_star_image(ra,de_step,roll))

elif direction_sensor.lower() == "z":
    roll_list = [roll]
    for i in range(total_frames):
        roll_append = round(roll_list[-1] + angle_increment,3)
        roll_list.append(roll_append)
    
    for roll_step in roll_list:
        images.append(nf.create_star_image(ra,de,roll_step))
    