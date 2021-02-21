from math import sin,cos,tan,radians,degrees,atan,sqrt
import numpy as np
import pandas as pd

class StarImage():

    #Default settings
    l = 3280
    w = 2464
    f = 0.00304
    myu = 1.12*(10**-6)
    star_catalogue_path = 'filtered_catalogue/Below_6.0_SAO.csv'

    def __init__(self,ra,de,roll):
        self.ra = ra
        self.de = de
        self.roll = roll


    def create_M_matrix(self):
        """[summary]

        Args:
            ra ([int]): [right ascension of sensor center]
            de ([int]): [declination of sensor center]
            roll ([int]): [roll angle of star sensor]
            method ([int]): [1 for method 1(Calculating each elements),2 for method 2(calculating rotation matrices)]
        """
        ra = self.ra
        de = self.de
        roll = self.roll
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
        return M
    


    def dir_vector_to_star_sensor(self,ra,de,M_transpose):
        """[Converts direction vector to star sensor coordinates]

        Args:
            ra ([int]): [right ascension of the object vector]
            de ([int]): [desclination of the object vector]
            M_transpose ([numpy array]): [rotation matrix from direction vector to star sensor transposed]
        """
        ra = self.ra
        de = self.de
        roll = self.roll    
        x_dir_vector = (cos(ra)*cos(de))
        y_dir_vector = (sin(ra)*cos(de))
        z_dir_vector = (sin(de))
        dir_vector_matrix = np.array([[x_dir_vector],[y_dir_vector],[z_dir_vector]])
        return M_transpose.dot(dir_vector_matrix)


    def draw_star(self,x,y,magnitude,gaussian,background,ROI=5):
        mag = abs(magnitude-7)
        radius = int(round((mag/9)*(5)+3))
        color = int(round((mag/0)*(155)+100))
        cv2.circle(background,(x,y),radius,color,thickness=-1)
        return background


    def add_noise(self,low,high,background):
        """[Adds noise to an image]

        Args:
            low ([int]): [lower threshold of the noise generated]
            high ([int]): [maximum pixel value of the noise generated]
            background ([numpy array]): [the image that is put noise on]
        """
        row,col = np.shape(background)
        background = background.astype(int)
        noise = np.random.randint(low,high=high,size=(row,col))
        noised_img = cv2.addWeighted(noise,0.1,background,0.9,0)
        return noised_img

    def create_star_image(self):
        ra = radians(float(self.ra))
        de = radians(float(self.de))
        roll = radians(float(self.roll))
        FOVy = degrees(2*atan((self.myu*self.w/2)/self.f))
        FOVx = degrees(2*atan((self.myu*self.l/2)/self.f))

        M = self.create_M_matrix()
        M_transpose = np.round(np.matrix.transpose(M),decimals=5)

        col_list = ["Star ID","RA","DE","Magnitude"]
        star_catalogue = pd.read_csv(self.star_catalogue_path,usecols=col_list)
        R = (sqrt((radians(FOVx)**2)+(radians(FOVy)**2))/2)
        alpha_start = (ra - (R/cos(de)))
        alpha_end = (ra + (R/cos(de)))
        delta_start = (de - R)
        delta_end = (de + R)
        star_within_ra_range = (alpha_start <= star_catalogue['RA']) & (star_catalogue['RA'] <= alpha_end)
        star_within_de_range = (delta_start <= star_catalogue['DE']) & (star_catalogue['DE'] <= delta_end)
        star_in_ra = star_catalogue[star_within_ra_range]
        star_in_de = star_catalogue[star_within_de_range]
        star_in_de = star_in_de[['Star ID']].copy()
        stars_within_FOV = pd.merge(star_in_ra,star_in_de,on="Star ID")

        #Converting to star sensor coordinate system
        ra_i = list(stars_within_FOV['RA'])
        de_i = list(stars_within_FOV['DE'])
        star_sensor_coordinates = []
        for i in range(len(ra_i)):
            coordinates = self.dir_vector_to_star_sensor(ra_i[i],de_i[i],M_transpose=M_transpose)
            star_sensor_coordinates.append(coordinates)

        #Conversion of star sensor coordinate system to image coordinate system
        star_loc = []
        for coord in star_sensor_coordinates:
            x = self.f*(coord[0]/coord[2])
            y = self.f*(coord[1]/coord[2])
            star_loc.append((x,y))

        xtot = 2*tan(radians(FOVx)/2)*self.f
        ytot = 2*tan(radians(FOVy)/2)*self.f
        xpixel = self.l/xtot
        ypixel = self.w/ytot

        magnitude_mv = list(stars_within_FOV['Magnitude'])
        filtered_magnitude = []

        #Rescaling to pixel sizes
        pixel_coordinates = []
        delete_indices = []
        for i,(x1,y1) in enumerate(star_loc):
            x1 = float(x1)
            y1 = float(y1)
            x1pixel = round(xpixel*x1)
            y1pixel = round(ypixel*y1)
            if abs(x1pixel) > self.l/2 or abs(y1pixel) > self.w/2:
                delete_indices.append(i)
                continue
            pixel_coordinates.append((x1pixel,y1pixel))
            filtered_magnitude.append(magnitude_mv[i])

        background = np.zeros((self.w,self.l))

        for i in range(len(filtered_magnitude)):
            x = round(self.l/2 + pixel_coordinates[i][0])
            y = round(self.w/2 - pixel_coordinates[i][1])
            background = self.draw_star(x,y,filtered_magnitude[i],False,background)

        #Adding noise
        background = add_noise(0,50,background=background)

        return background


image = StarImage(0,0,0)
image = image.create_star_image()
