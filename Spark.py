from __future__ import print_function

import sys
from operator import add
import fnmatch
import os
import fitsLibrary as fl
import numpy as np

from pyspark.sql import SparkSession

if __name__ == "__main__":

    files = []
    for root, dirnames, filenames in os.walk('transneptunian3Days'):
        for filename in fnmatch.filter(filenames, '*.fts'):
            files.append(os.path.join(root, filename))
    print(len(files)," files detected")

    virtual = fl.fitsLibrary("virtual.fits").imageData
    files = files[1:10]

    spark = SparkSession\
        .builder\
        .appName("IAA Spark")\
        .getOrCreate()

    partitions = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    n = int(np.floor(len(files)/partitions) * partitions)
    print(n)

    def f(x):
        image = fl.fitsLibrary(files[x]).imageData
        value = 2 # np.absolute(np.array(virtual) - np.array(image))
        return [files[x],value]

    count = spark.sparkContext.parallelize(range(1, n + 1), partitions).map(lambda x: f(x)).reduce(add)

    outfile = open('data.txt', 'w')
    for item in count:
        outfile.write("%s\n" % item)

    spark.stop()