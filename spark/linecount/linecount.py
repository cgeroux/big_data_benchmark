#!/bin/env python
from __future__ import print_function
from pyspark import SparkContext,SparkConf
import sys
import os
import time
import optparse as op

def addParserOptions(parser):
  """Adds command line options
  """
  
  parser.add_option("--num-partitions",dest="numPartitions",type="int",default=None
    ,help="Number of partitions to split the data into. If not set it chooses "
    +"a number based on the file size and the default Spark parallelism, "
    +"usually the number of cores on a node, multiplied by a factor "
    +"(usually 2).")
def parseOptions():
  """Parses command line options
  
  """
  
  parser=op.OptionParser(usage="Usage: %prog [options] INPUTFILE OUTPUTFILE"
    ,version="%prog 1.0",description=r"times reading and writing a file or file set.")
  
  #add options
  addParserOptions(parser)
  
  #parse command line options
  return parser.parse_args()
def main():
  
  #parse command line options
  (options,args)=parseOptions()
  
  if len(args) != 2:
   raise Exception("need an input file and an output path")
  
  #set number of file partitions/parallelism
  if options.numPartitions==None:
    #pick number of partitions based on default amount of parallelism and filesize
    partFactor=1#how many times the default parallelism. Defaul Parallelism is 
      #related to the number of cores on the machine.
    numPartitions=sc.defaultParallelism*partFactor
  else:
    numPartitions=options.numPartitions
  
  conf=SparkConf().setAppName("wordCount").setMaster("local["+str(numPartitions)+"]")
  sc = SparkContext(conf=conf)
  conf=sc.getConf()
  print("conf="+str(conf.getAll()))
  print("defaultMinPartitions="+str(sc.defaultMinPartitions))
  print("defaultParallelism="+str(sc.defaultParallelism))
  
  inputFileName = args[0]
  outputFileName= args[1]
  
  timeStart=time.time()
  file = sc.textFile(inputFileName,minPartitions=numPartitions)
  counts = file.count()
  timeEnd=time.time()
  dtRead=timeEnd-timeStart#time in seconds
  
  #write out to a file
  timeStart=time.time()
  file.saveAsTextFile(outputFileName)
  timeEnd=time.time()
  dtWrite=timeEnd-timeStart#time in seconds
  
  print("read+count time="+str(dtRead)+" s")
  print("write time="+str(dtWrite)+" s")
  print("number of lines="+str(counts))
  print("num Partitions="+str(file.getNumPartitions()))
if __name__ == "__main__":
  main()
