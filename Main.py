
import GAIAFile as GDB
DBobject = GDB.GAIAFile("result.csv", 1, 2)

import SyntheticImage as VI
VI.createSyntheticImage("header.fit", "negative.fit", DBobject.database, sizeX=1024, sizeY=1024)

# os.system('~/spark-2.1.1-bin-hadoop2.7/bin/spark-submit ~/PycharmProjects/TFM/Spark.py 5')