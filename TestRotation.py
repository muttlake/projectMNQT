import numpy as np
import cv2
import printImage as pim


class Coord:
    """Coordinate class"""
    x = None
    y = None

    def __init__(self, xValue, yValue):
        self.x = xValue
        self.y = yValue

    def __str__(self):
        """return string of coord"""
        #formatted_X = "%02d" % x
        return "( %.2f" % self.x + ", %.2f" % self.y + ")"


def getCentroid(image):
    """Return center of image"""
    centerX = 0.0
    centerY = 0.0
    (N, M) = lenna.shape
    for x in range(M):
        centerX = centerX + x
    centerX = centerX / M
    for y in range(N):
        centerY = centerY + y
    centerY = centerY / N
    return(centerX, centerY)


def rotateVector(vector, angle):
    """Rotates counter clockwise vector by angle"""
    angleRad = np.deg2rad(angle)
    RotationMatrix = np.matrix([[np.cos(angleRad), -1 * np.sin(angleRad)], [np.sin(angleRad), np.cos(angleRad)]])
    outputVector = RotationMatrix * vector
    return outputVector


def makeVector(x, y, centroid):
    """Return a vector of x and y"""
    (centerX, centerY) = centroid
    xV = x - centerX
    yV = centerY - y
    return [[xV], [yV]]

def initializeCoordMatrix(image):
    coordMatrix = []
    (N, M) = image.shape
    for ii in range(N):
        newline = []
        for jj in range(M):
            newline.append(Coord(ii, jj))
        coordMatrix.append(newline)
    return coordMatrix

def printImageCoordMatrix(imageCoordMatrix):
    """ Image Coord Matrix is 2D matrix """
    print("\n\n")
    N = len(imageCoordMatrix)
    for ii in range(N):
        M = len(imageCoordMatrix[ii])
        eachLine = imageCoordMatrix[ii]
        for jj in range(M):
            print(eachLine[jj], end="\t")
        print("", end="\n")

def getRotatedCoordMatrix(image, angle):
    """ Get Rotated Coords as Coord Matrix """

    input_coords = initializeCoordMatrix(image)
    rotated_coords = []
    centroid = getCentroid(image)
    N = len(input_coords)
    for ii in range(N):
        M = len(input_coords[ii])
        eachInputLine = input_coords[ii]
        eachRotatedLine = []
        for jj in range(M):
            x = eachInputLine[jj].x
            y = eachInputLine[jj].y
            vec = makeVector(x, y, centroid)
            rotvec = rotateVector(vec, angle)
            rotX = float(rotvec[0][0])
            rotY = float(rotvec[1][0])
            eachRotatedLine.append(Coord(centroid[0] + rotX , centroid[1] - rotY))
        rotated_coords.append(eachRotatedLine)
    return rotated_coords



lenna = cv2.imread("lennaGreySmall.png")
lenna = cv2.cvtColor(lenna, cv2.COLOR_RGB2GRAY)

print("Lenna shape: ", lenna.shape)
cv2.imshow("Input Image", lenna)
cv2.waitKey()

print("Centroid of image: ", getCentroid(lenna))

pim.printUnsignedImage(lenna)

inputCoordMatrix = initializeCoordMatrix(lenna)

printImageCoordMatrix(inputCoordMatrix)

rotatedCoordMatrix = getRotatedCoordMatrix(lenna, 45) # positive angle is counter clockwise

printImageCoordMatrix(rotatedCoordMatrix)






