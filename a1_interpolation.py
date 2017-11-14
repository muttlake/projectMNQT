from .imagepoint import ImagePoint

# class used for bilinear interpolation algorithm
class interpolation:

    def linear_interpolation(self, pt1, pt2, unknownLoc):
        """Computes the linear interpolation for the unknown values using pt1 and pt2 take as input pt1: known point pt1 and f(pt1) or intensity value pt2: known point pt2 and f(pt2) or intensity value unknown: take and unknown location return the f(unknown) or intentity at unknown"""
        # Write your code for linear interpolation here
        # assume pt1 and pt2 are of the form (location, intensity)
        loc1 = pt1[0]
        loc2 = pt2[0]
        distance = loc2 - loc1
        intensity1 = pt1[1]
        intensity2 = pt2[1]
        unknownIntensity = (intensity1 * (loc2 - unknownLoc) / distance ) + (intensity2 * (unknownLoc - loc1) / distance )
        return unknownIntensity

    def linear_interpolation_x(self, pt1, pt2, unknown):
        """Computes the linear interpolation for the unknown values using pt1 and pt2 take as input pt1: known point pt1 and f(pt1) or intensity value pt2: known point pt2 and f(pt2) or intensity value unknown: take and unknown location return the f(unknown) or intentity at unknown"""
        # Write your code for linear interpolation here
        temporaryPointX = ImagePoint(unknown.x, pt1.y, None)
        # xDistance = pt2.x - pt1.x
        # temporaryPointX.i = ( pt1.i * ((pt2.x - temporaryPointX.x)/xDistance) ) + ( pt2.i * ((temporaryPointX.x - pt1.x)/xDistance) )
        temporaryPointX.i = self.linear_interpolation((pt1.x, pt1.i), (pt2.x, pt2.i), temporaryPointX.x)
        return temporaryPointX

    def linear_interpolation_y(self, pt1, pt2, unknown):
        """Computes the linear interpolation for the unknown values using pt1 and pt2 take as input pt1: known point pt1 and f(pt1) or intensity value pt2: known point pt2 and f(pt2) or intensity value unknown: take and unknown location return the f(unknown) or intentity at unknown"""
        # Write your code for linear interpolation here
        temporaryPointY = ImagePoint(pt1.x, unknown.y, None)
        # yDistance = pt2.y - pt1.y
        # temporaryPointY.i = ( pt1.i * ((pt2.y - temporaryPointY.y)/yDistance) ) + ( pt2.i * ((temporaryPointY.y - pt1.y)/ yDistance) )
        # if temporaryPointY.i > 255 or temporaryPointY.i < 0:
        #     print("Bad interpolation: (pt1, pt2, unknown): ", pt1, pt2, unknown)
        temporaryPointY.i = self.linear_interpolation((pt1.y, pt1.i), (pt2.y, pt2.i), temporaryPointY.y)
        return temporaryPointY

    def bilinear_interpolation(self, pt1, pt2, pt3, pt4, unknown):
        """Computes the linear interpolation for the unknown values using pt1 and pt2 take as input pt1: known point pt1 and f(pt1) or intensity value pt2: known point pt2 and f(pt2) or intensity value pt3: known point pt3 and f(pt3) or intensity value pt4: known point pt4 and f(pt4) or intensity value unknown: take and unknown location return the f(unknown) or intentity at unknown"""
        # Write your code for bilinear interpolation here
        # May be you can reuse or call linear interpolation method to compute this task
        savedValidIntensity = 0
        for point in [pt1, pt2, pt3, pt4]:
            if point.i is not None:
                savedValidIntensity = point.i
        for point in [pt1, pt2, pt3, pt4]:
            if point.i is None:  # for edge cases put a valid intensity value, should only happen where computed row or column is outside 0,0 and originalRows, originalCols
                point.i = savedValidIntensity # This only happens for images output larger than original image
        temporaryPointX1 = self.linear_interpolation_x(pt1, pt2, unknown)
        temporaryPointX2 = self.linear_interpolation_x(pt3, pt4, unknown)
        unknownXYinterp = self.linear_interpolation_y(temporaryPointX1, temporaryPointX2, unknown)
        return unknownXYinterp
