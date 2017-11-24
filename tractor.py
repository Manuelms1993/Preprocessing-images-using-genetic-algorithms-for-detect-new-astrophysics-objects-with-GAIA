import astropy.io.fits
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

def createMacro(nameMacroFile,sourcesNameFile):
    file = open(nameMacroFile, 'w')
    sourcesFile = open(sourcesNameFile, 'w')
    file.write('//setTool("oval");\n')
    file.write('run("Colors...", "foreground=black background=white selection=green");\n')
    sourcesFile.write('ID,RA,DEC,X,Y,FLUX_AUTO\n')

    imagelist = "subtract.fits"
    hdulist = astropy.io.fits.open(imagelist)
    imageData = hdulist[0].data

    (values, counts) = np.unique(np.squeeze(imageData), return_counts=True)
    skyFlux = values[np.argmax(counts)]

    implot = plt.imshow(imageData, cmap='gist_heat',interpolation="none")

    n = 0
    pad = 3
    lasti, lastj = 0,0
    for i in range(pad,imageData.shape[0]-pad):
        for j in range(pad,imageData.shape[1]-pad):

            flag=1
            for k in range(i-pad,i+pad):
                if flag == 0: break
                for l in range(j-pad,j+pad):
                    if imageData[i,j]<imageData[k,l]: flag=0;break

            if flag==1 and imageData[i,j]>skyFlux+200 and np.absolute(lasti-i)>3 and np.absolute(lastj-j)>3:
                file.write('makeOval(' + str(j-9) + ',' + str(i-9) + ',16, 16);\n')
                file.write('roiManager("Add");\n')
                lasti = i
                lastj = j
                n+=1

    file.write('run("ROI Manager...");\n')
    file.write('roiManager("Show All");\n')
    file.close()
    sourcesFile.close()
    print n

createMacro("macro.ijm","sources.csv")

