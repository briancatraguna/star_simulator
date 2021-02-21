from math import sin,cos
import numpy as np

class StarImage():


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

    

image = StarImage(0,0,0)
M = image.create_M_matrix()
print(M)