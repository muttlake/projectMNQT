import numpy as np
import cv2
import printImage as pim

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

# def rotateImage(image):
#     (N, M) = image.shape
#     centroid = getCentroid(image)
#     for y in range(M):
#         for x in range(N):
#             vec = makeVector(x, y, centroid)
#             rotvec = rotateVector(vec, 45)
#             print("\n(X = ", x, " Y = ", y, ")")
#             print("Vec: ", vec)
#             print("Vec Rotated 45°:", rotvec)

lenna = cv2.imread("lennaGreySmall.png")
lenna = cv2.cvtColor(lenna, cv2.COLOR_RGB2GRAY)

print("Lenna shape: ", lenna.shape)
cv2.imshow("Input Image", lenna)
cv2.waitKey()

print("Centroid of image: ", getCentroid(lenna))

pim.printUnsignedImage(lenna)

(N, M) = lenna.shape
centroid = getCentroid(lenna)
for y in range(M):
    for x in range(N):
        vec = makeVector(x, y, centroid)
        rotvec = rotateVector(vec, 45)
        print("\n(X = ", x, " Y = ", y, ")")
        print("Vec: ", vec)
        print("Vec Rotated 45°:", rotvec)



