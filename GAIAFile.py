import numpy as np

class GAIAFile:

    database = []

    def __init__(self, CSVname, raPos, decPos):
        db = np.genfromtxt(CSVname, delimiter=',', skip_header=True)
        self.database = np.zeros((db.shape[0],2))
        self.database[:,0] = db[:,raPos]
        self.database[:,1] = db[:,decPos]
        print "File read correctly!"

