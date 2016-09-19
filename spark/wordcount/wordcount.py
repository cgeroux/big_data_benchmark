from pyspark import SparkContext,SparkConf
import sys
import os

if len(sys.argv) > 1:
   inputFileName = sys.argv[1]
else:
   inputFileName = "./generated.txt"
assert(os.path.exists(inputFileName))

if len(sys.argv) > 2:
   outputDirectoryName = sys.argv[2]
else:
   outputDirectoryName = "./wordcounts"
assert(not os.path.exists(outputDirectoryName))

conf=SparkConf().setAppName("wordCount")
sc = SparkContext(conf=conf)
file = sc.textFile(inputFileName)
counts = file.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a+b)
counts.saveAsTextFile(outputDirectoryName)  

#rdd = sc.textFile(inputFileName)\
#.flatMap(lambda line: line.split())\
#.map(lambda word: (word, 1))\
#.reduceByKey(lambda x, y: x + y, 3)\
#.collect()
