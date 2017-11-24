import numpy as np

size = 40

def createGaussian(MaxValue, fwhm, xoffset, yoffset, xFactor, yFactor, reductionFactor):
    x0 = (size / 2) + xoffset
    y0 = (size / 2) + yoffset
    x = np.arange(0, size, 1, float)
    y = x[:,np.newaxis]
    star = MaxValue * np.exp(reductionFactor *
                                   ((xFactor*(x-x0))**2 + (yFactor*(y-y0))**2) / 2*fwhm**2)
    return -1*star