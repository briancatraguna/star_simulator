#Right ascension, declination and roll input prompt from user
ra = round(float(input("Enter the right ascension angle in degrees:\n")))
de = round(float(input("Enter the declination angle in degrees:\n")))
roll = round(float(input("Enter the roll angle in degrees:\n")))
print(type(ra),type(de),type(roll))
#Conversion of celestial coordinate system to star sensor coordinate system
