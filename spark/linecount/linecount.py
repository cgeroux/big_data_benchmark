#!/bin/env python
from pyspark import SparkContext,SparkConf
import sys
import os
import time

if len(sys.argv) > 1:
   inputFileName = sys.argv[1]
else:
   inputFileName = "./generated.txt"
#assert(os.path.exists(inputFileName))

conf=SparkConf().setAppName("wordCount")
sc = SparkContext(conf=conf)

timeStart=time.time()
file = sc.textFile(inputFileName)
counts = file.count()
timeEnd=time.time()
dtRead=timeEnd-timeStart#time in seconds

#write out to a file
timeStart=time.time()
file.saveAsTextFile(inputFileName+"_tmp")
timeEnd=time.time()
dtWrite=timeEnd-timeStart#time in seconds

print("read+count time="+str(dtRead)+" s")
print("write time="+str(dtWrite)+" s")
print("number of lines="+str(counts))
print("num Partitions="+str(file.getNumPartitions()))
