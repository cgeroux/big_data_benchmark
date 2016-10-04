from pyspark import SparkContext,SparkConf
import sys
import os

if len(sys.argv) > 1:
   inputFileName = sys.argv[1]
else:
   inputFileName = "./generated.txt"
#assert(os.path.exists(inputFileName))

conf=SparkConf().setAppName("wordCount")
sc = SparkContext(conf=conf)
file = sc.textFile(inputFileName)
counts = file.count()

