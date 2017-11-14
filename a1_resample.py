import numpy as np
from .imagepoint import ImagePoint
from .interpolation import interpolation

class resample:

    def resize(self, image, fx = None, fy = None, interpolation = None):
        """calls the appropriate funciton to resample an image based on the interpolation method
        image: the image to be resampled
        fx: scale along x direction (eg. 0.5, 1.5, 2.5)
        fx: scale along y direction (eg. 0.5, 1.5, 2.5)
        interpolation: method used for interpolation ('either bilinear or nearest_neighbor)
        returns a resized image based on the interpolation method
        """

        if interpolation == 'bilinear':
            return self.bilinear_interpolation(image, fx, fy)

        elif interpolation == 'nearest_neighbor':
            return self.nearest_neighbor(image, fx, fy)

    #
    # We are editing the methods below this comment
    #

    def nearest_neighbor(self, image, fx, fy):
        """resizes an image using bilinear interpolation approximation for resampling image: the image to be resampled fx: scale along x direction (eg. 0.5, 1.5, 2.5) fy: scale along y direction (eg. 0.5, 1.5, 2.5) returns a resized image based on the nearest neighbor interpolation method """
        # Write your code for nearest neighbor interpolation here
        (originalRows, originalCols) = image.shape
        print("Original Image Size: ", str((originalRows, originalCols)), "with rows [0," + str(originalRows - 1) + "] and columns [0,", str(originalCols - 1) + "]")
        newImage = self.getNewImage(image, fx, fy)
        (newRows, newCols) = newImage.shape
        print("New Image Size: ", str((newRows, newCols)), "with rows [0," + str(newRows - 1) + "] and columns [0,", str(newCols - 1) + "]")
        self.printOriginalImageXYGrid(originalRows, originalCols)
        for row in range(newRows):
            for col in range(newCols):
                interpIntensity = self.getNearestNeighborImageValue(image, originalRows, originalCols, newRows, newCols, row, col)
                newImage[row][col] = interpIntensity
        image = newImage
        return image

    def bilinear_interpolation(self, image, fx, fy):
        """resizes an image using bilinear interpolation approximation for resampling image: the image to be resampled, fx: scale along x direction (eg. 0.5, 1.5, 2.5), fy: scale along y direction (eg. 0.5, 1.5, 2.5) returns a resized image based on the bilinear interpolation method """
        # Write your code for bilinear interpolation here
        (originalRows, originalCols) = image.shape
        print("Original Image Size: ", str((originalRows, originalCols)), "with rows [0," + str(originalRows - 1) + "] and columns [0,", str(originalCols - 1) + "]")
        newImage = self.getNewImage(image, fx, fy)
        (newRows, newCols) = newImage.shape
        print("New Image Size: ", str((newRows, newCols)), "with rows [0," + str(newRows - 1) + "] and columns [0,", str(newCols - 1) + "]")
        self.printOriginalImageXYGrid(originalRows, originalCols)
        for row in range(newRows):
            for col in range(newCols):
                imageInterpLocation = self.getInterpLocation(originalRows, originalCols, newRows, newCols, row, col)
                fourSurroundingPoints = self.getFourSurroundingPoints(image, imageInterpLocation)
                interpolator = interpolation()
                bilinearInterpolatedImagePoint = interpolator.bilinear_interpolation(fourSurroundingPoints[0], fourSurroundingPoints[1], fourSurroundingPoints[2], fourSurroundingPoints[3], imageInterpLocation)
                newImage[row][col] = bilinearInterpolatedImagePoint.i
                # print information to check bilinear interpolation
                if (row == 0 and col == 0) or (row == int(newRows / 2) and col == int(newCols / 2)) or (row == newRows - 1 and col == newCols - 1):
                    print("\n", end="")
                    print("newImage Row,", str(row), " newImage Col,", str(col), " maps onto original image at:", str((imageInterpLocation.x, imageInterpLocation.y)), end="")
                    print(", that is originalImage Row", str(imageInterpLocation.y), "and originalImage Col", str(imageInterpLocation.x))
                    print("Four surrounding points:", end="")
                    for point in fourSurroundingPoints:
                        print(" " + str((point.x, point.y)) + " has i = " + str(point.i) + ",", end="")
                    print("\n", end="")
                    print("Bilinear interpolated image point:", bilinearInterpolatedImagePoint)
        return newImage

    #
    # New methods created by me are below this comment
    #
    def getNewImage(self, originalImage, fx, fy):
        """return image of new size for originalImage scaled by fx and fy"""
        (originalRows, originalCols) = originalImage.shape
        scalex = float(fx)
        scaley = float(fy)
        newRows = round(originalRows * scaley)  # Rows correspond to the Y-direction
        newCols = round(originalCols * scalex)  # Columns correspond to the X-direction
        newImage = self.createBlackImage(newRows, newCols)
        return newImage

    def createBlackImage(self, rows, columns):
        """return black image of size rows x columns."""
        blackImage = np.zeros((rows, columns), np.uint8)
        return blackImage

    def getInterpLocation(self, originalRows, originalCols, newRows, newCols, inputRow, inputCol):
        """Imagine the original image has points on a 2d plane with column value in the x direction increasing positive right and row value in the y direction increasing positive down, Get X location of new image for that grid."""

        originalGridNewImageXbinStep = float(originalCols) / float(newCols) # X direction corresponds to columns
        originalGridNewImageXStartingPoint = -.5 + .5 * originalGridNewImageXbinStep  # Imagine grid starting at -.5, -.5 so that pixel 0,0 is at center of a 1x1 bin from x = -0.5 to 0.5

        originalGridNewImageYbinStep = float(originalRows) / float(newRows) # Y direction corresponds to rows
        originalGridNewImageYStartingPoint = -.5 + .5 * originalGridNewImageYbinStep

        interpLocX = originalGridNewImageXbinStep * inputCol + originalGridNewImageXStartingPoint  # X direction corresponds to columns
        interpLocY = originalGridNewImageYbinStep * inputRow + originalGridNewImageYStartingPoint  # Y direction corresponds to rows

        newImageLocation = ImagePoint(interpLocX, interpLocY, None)
        return newImageLocation

    def getFourSurroundingPoints(self, originalImage, newImageLocation):
        if newImageLocation.x.is_integer():  # Have to do this because before linear interpolation was causing division by zero when both ceil and floor gave the same values for pt1 and pt2
            newImageLocation.x += 0.1
        if newImageLocation.y.is_integer():
            newImageLocation.y += 0.1
        ptUL = ImagePoint(np.floor(newImageLocation.x), np.floor(newImageLocation.y), None)
        ptUL.i = self.getCorrespondingImageValue(ptUL.x, ptUL.y, originalImage)
        ptUR = ImagePoint(np.ceil(newImageLocation.x), np.floor(newImageLocation.y), None)
        ptUR.i = self.getCorrespondingImageValue(ptUR.x, ptUR.y, originalImage)
        ptLL = ImagePoint(np.floor(newImageLocation.x), np.ceil(newImageLocation.y), None)
        ptLL.i = self.getCorrespondingImageValue(ptLL.x, ptLL.y, originalImage)
        ptLR = ImagePoint(np.ceil(newImageLocation.x), np.ceil(newImageLocation.y), None)
        ptLR.i = self.getCorrespondingImageValue(ptLR.x, ptLR.y, originalImage)
        fourSurroundingPoints = [ptUL, ptUR, ptLL, ptLR]
        return fourSurroundingPoints

    def getCorrespondingImageValue(self, imageLocationX, imageLocationY, originalImage):
        (originalRows, originalCols) = originalImage.shape
        locationLessThanZero = imageLocationX < 0 or imageLocationY < 0
        locationGreaterThanDimensions = imageLocationX >= originalCols or imageLocationY >= originalRows
        imageValue = None
        if not locationLessThanZero and not locationGreaterThanDimensions:
            imageValue = originalImage[int(imageLocationY)][int(imageLocationX)]
        return imageValue

    def getDistanceTwoPoints(self, pt1, pt2):
        xDiff = pt1.x - pt2.x
        yDiff = pt1.y - pt2.y
        sumOfSquares = xDiff * xDiff + yDiff * yDiff
        return np.sqrt(sumOfSquares)

    def findNearestNeighbor(self, fourSurroundingPoints, location):
        nearestNeighbor = fourSurroundingPoints[0]
        nearestNeighborDistance = self.getDistanceTwoPoints(nearestNeighbor, location)
        for neighboringPt in fourSurroundingPoints:
            neighboringPtDistance = self.getDistanceTwoPoints(neighboringPt, location)
            if neighboringPtDistance < nearestNeighborDistance:
                nearestNeighbor = neighboringPt
                nearestNeighborDistance = neighboringPtDistance
        return nearestNeighbor

    def getNearestNeighborImageValue(self, originalImage, originalRows, originalCols, newRows, newCols, inputRow, inputCol):

        newImageLocation = self.getInterpLocation(originalRows, originalCols, newRows, newCols, inputRow, inputCol)
        fourSurroundingPoints = self.getFourSurroundingPoints(originalImage, newImageLocation)
        nearestNeighbor = self.findNearestNeighbor(fourSurroundingPoints, newImageLocation)
        imageRow = int(nearestNeighbor.y)  # Y direction corresponds to rows
        imageCol = int(nearestNeighbor.x)  # X direction corresponds to columns

        # check that it is working
        if (inputRow == 0 and inputCol == 0) or (inputRow == int(newRows/2) and inputCol == int(newCols/2)) or (inputRow == newRows -1 and inputCol == newCols - 1):
            print("\n", end="")
            print("newImage Row,", str(inputRow), " newImage Col,", str(inputCol), " maps onto original image at:", str((newImageLocation.x, newImageLocation.y)), end="")
            print(", that is originalImage Row", str(newImageLocation.y), "and originalImage Col", str(newImageLocation.x))
            print("Four surrounding points:", end="")
            for point in fourSurroundingPoints:
                print(" " + str((point.x, point.y)) + ",", end="")
            print("\n", end="")
            print("nearestNeighbor:", nearestNeighbor, " , nearestNeighborDistance:", self.getDistanceTwoPoints(nearestNeighbor, newImageLocation),"return image value:", originalImage[imageRow][imageCol])

        return originalImage[imageRow][imageCol]

    def printOriginalImageXYGrid(self, originalRows, originalCols):
        """Print the grid to which the resize image is mapping to in order to find the image intensity value."""
        print("\nOriginal Image XY Grid:")
        print("(-0.5. -0.5) -----------------------", str((originalCols - 0.5, 0.5)))
        for i in range(5):
            print("         |                             |")
        print(str((-0.5, originalRows - 0.5)),  "----------------------", str((originalCols - 0.5, originalRows - 0.5)) + "\n")
