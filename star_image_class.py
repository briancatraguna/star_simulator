class StarImage:
    def __init__(self,ra,de,roll):
        self.ra = ra
        self.de = de
        self.roll = roll

image = StarImage(0,0,0)
print(image.ra)