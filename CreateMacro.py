import os

def createMacro(nameMacroFile,sourcesNameFile):
    file = open(nameMacroFile, 'w')
    sourcesFile = open(sourcesNameFile, 'w')
    file.write('//setTool("oval");\n')
    file.write('run("Colors...", "foreground=black background=white selection=green");\n')
    sourcesFile.write('ID,RA,DEC,X,Y,FLUX_AUTO\n')

    os.chdir('./sextractor')
    with open('out.cat') as f:
        content = f.readlines()
        for i in range(21,len(content)):
            items = [x for x in content[i].split(' ') if x]
            x = int(float(items[13][0:len(items[13])-1]))-8
            y = ((int(float(items[14][0:len(items[14])-1]))+8)-1024)*-1
            file.write('makeOval('+str(x)+','+str(y)+',16, 16);\n')
            file.write('roiManager("Add");\n')

            it = [x for x in items[16].split(',') if x]
            a = str(i-21+1) + "," + it[1] + "," + it[2] + ","+ items[13]+items[14]+ items[1][:-1]+ "\n"
            sourcesFile.write(a)

    file.write('run("ROI Manager...");\n')
    file.write('roiManager("Show All");\n')
    file.close()
    sourcesFile.close()

createMacro("macro.ijm","sources.csv")