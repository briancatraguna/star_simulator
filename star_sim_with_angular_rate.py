import nested_function as nf

#User defines the initial attitude
ra = float(input("Input right ascension:\n"))
de = float(input("Input declination:\n"))
roll = float(input("Input roll:\n"))

#Angular rate prompt
direction_sensor = input("Input direction:\n(X for +RA)\n(Y for +DE)\n(R for +ROLL)\n")
omega = float(input("Input angular rate: "))

#Frames per second
fps = 30


img = nf.create_star_image(ra,de,roll)
nf.displayImg(img)