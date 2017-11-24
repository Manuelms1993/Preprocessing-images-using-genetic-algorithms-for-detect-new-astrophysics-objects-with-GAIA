import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.wcs import WCS
from astropy.utils.data import get_pkg_data_filename
import pyfits
import os

def createFits(data, headername, name='finalImage.fits'):
    inhdulist = pyfits.open(headername)
    inhdulist[0].data = data
    hdulist = pyfits.HDUList(inhdulist)
    if os.path.exists(name): os.remove(name)
    hdulist.writeto(name)

class fitsLibrary:

    fitsName = None
    fitsHeader = None
    imageData = None
    inhdulist = None
    data = None

    def __init__(self, infits):

        self.fitsName = get_pkg_data_filename(infits)
        self.inhdulist = fits.open(self.fitsName)[0]
        self.wcs = WCS(self.inhdulist.header)
        self.fitsHeader = self.inhdulist.header
        self.imageData = self.inhdulist.data

        # Print information about the image
        print 'Image read! (',infits,')'

    def showTheImage(self):
        fig = plt.figure()
        fig.add_subplot(111, projection=self.wcs)
        plt.imshow(self.inhdulist.data, origin='lower', cmap=plt.cm.gray)
        plt.xlabel('RA')
        plt.ylabel('Dec')
        plt.show()

    def saveImage(self, name= "fig.png"):
        fig = plt.figure()
        fig.add_subplot(111, projection=self.wcs)
        plt.imshow(self.inhdulist.data, origin='lower', cmap=plt.cm.gray)
        plt.xlabel('RA')
        plt.ylabel('Dec')
        fig.savefig("imgTest/"+name)

    def closeImage(self):
        self.inhdulist.close()
