from scipy import ndimage
import numpy as np
import astropy.io.fits
from astropy import wcs
import GaussianCreator
import subprocess
import GeneticAlgorithm
import fitsLibrary as fl

def createSyntheticImage(headerName, finalImageName, database, sizeX=1024, sizeY=1024):

    def exportFits(image, headerName, name):
        fl.createFits(image, headerName, name)

    def cleanImage(imageData, synthetic):
        sub = imageData + 0
        padding = 30
        for i in range(imageData.shape[0]):
            for j in range(imageData.shape[1]):
                if synthetic[i, j] < -1e-20:
                    boxXL = padding if i > padding else i
                    boxXR = padding if i < 1024 - padding else 1024 - i
                    boxYL = padding if j > padding else j
                    boxYR = padding if j < 1024 - padding else 1024 - j
                    (values, counts) = np.unique(np.squeeze(imageData[i-boxXL:i+boxXR,j-boxYL:j+boxYR]), return_counts=True)
                    skyFlux = values[np.argmax(counts)]
                    sub[i,j] = np.random.randint(skyFlux-100,skyFlux+100) + 32768
                else: sub[i,j] += 32768

        return sub

    def RaDec2Pixels():
        for i in range(database.shape[0]):
            cmd = ['sky2xy', headerName, str(database[i, 0]), str(database[i, 1])]
            output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
            output = output[0:len(output)-2]
            items = [x for x in output.split(' ') if x]
            database[i, 1] = int(float(items[4]))
            database[i, 0] = int(float(items[5]))

    imagelist = headerName
    hdulist = astropy.io.fits.open(imagelist)
    w = wcs.WCS(hdulist[0].header)
    imageData = hdulist[0].data
    (values, counts) = np.unique(np.squeeze(imageData), return_counts=True)
    skyFlux = values[np.argmax(counts)]
    offset = 2000
    area = GaussianCreator.size
    image = np.zeros( (sizeX+offset, sizeY+offset) )
    imageWithoutSkyFlux = np.zeros( (sizeX+offset, sizeY+offset) )
    RaDec2Pixels()

    for i in range(database.shape[0]):

        print "Training star" ,i, "-->",database[i, 0],database[i, 1], "..."
        if database[i, 0] > 0 and database[i, 0] < sizeX and database[i, 1] > 0 and database[i, 1] < sizeY:
            x = int(database[i, 0] + offset / 2)
            y = int(database[i, 1] + offset / 2)
            params = GeneticAlgorithm.run(database[i, 0], database[i, 1], headerName, 10, 250, 3)
            star = GaussianCreator.createGaussian(params[0], params[1], params[2], params[3], params[4], params[5], params[6])
            imageWithoutSkyFlux[int(x-(area/2)):int(x+(area/2)),int(y-(area/2)):int(y+(area/2))] += -1*star
            image[int(x-(area/2)):int(x+(area/2)),int(y-(area/2)):int(y+(area/2))] += star

        else: print "Star" ,i, "OUT OF RANGE!"

    imageWithoutSkyFlux = imageWithoutSkyFlux[offset/2:sizeX+offset/2,offset/2:sizeY+offset/2]
    image = image[offset/2:sizeX+offset/2,offset/2:sizeY+offset/2]
    sub = cleanImage(imageData,image)

    for i in range(sub.shape[0]):
        for j in range(sub.shape[1]):
            imageWithoutSkyFlux[i,j] += 32768
            if imageWithoutSkyFlux[i,j] > 55000: imageWithoutSkyFlux[i,j] = 50000

    sub = sub.astype(np.int16)
    imageWithoutSkyFlux = imageWithoutSkyFlux.astype(np.int16)

    exportFits(imageWithoutSkyFlux, headerName, 'synthetic.fits')
    exportFits(sub, headerName, finalImageName)