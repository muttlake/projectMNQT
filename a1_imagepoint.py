# This class holds image points information
class ImagePoint:
    def __init__(self, x, y, i):
        self.x = x
        self.y = y
        self.i = i
    def __str__(self):
        return "Image Point Object: x: " +  str(self.x) + ", y:" +  str(self.y) +  ", i:" +  str(self.i)