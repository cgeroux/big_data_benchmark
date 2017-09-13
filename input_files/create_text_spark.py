#!/bin/env python
from pyspark import SparkContext, SparkConf
import optparse as op
import os
import random
import glob
import time

def addParserOptions(parser):
  """Adds command line options
  """
  
  #these options apply globally
  parser.add_option("--line-length",dest="lineLength",type="int",default=80
    ,help="Set the length of lines in the file [default: %default]")
  parser.add_option("--file-size",dest="fileSize",type="int",default=10000
    ,help="The size of the file in bytes [default: %default bytes]")
  parser.add_option("-o",dest="outputDirName",type="string"
    ,default="generated_txt"
    ,help="Specify the name of the output file [default: \"%default\"].")
  parser.add_option("--seed",dest="seed",default=1,help="Seed used "
    +"for randomly choosing words from the dictionary [default: %default].")
  parser.add_option("--num-partitions",dest="numPartitions",type="int",default=None
    ,help="Number of partitions to split the data into. If not set it chooses "
    +"a number based on the file size and the default Spark parallelism, "
    +"usually the number of cores on a node, multiplied by a factor "
    +"(usually 2).")
  dictPath=os.path.dirname(os.path.realpath(__file__))
  parser.add_option("--dictionary-file",dest="dictionaryFile",type="string"
    ,default=os.path.join(dictPath,"english-wordlist.txt")
    ,help="Specify a file containing a list of words separated by newlines "
    +"to be used as the language dictionary. This option has no effect if "
    +"the option --randomly-generate-dict is specified "
    +"[default: \"%default\"].")
def parseOptions():
  """Parses command line options
  
  """
  
  parser=op.OptionParser(usage="Usage: %prog [options]"
    ,version="%prog 1.0",description=r"Randomly generates the content of a text file.")
  
  #add options
  addParserOptions(parser)
  
  #parse command line options
  return parser.parse_args()
def loadDictFromFile(sc,fileName):
  """Loads a dictionary from a file containing words separated by newline 
  characters.
  """
  
  dictionary=[]
  #file=sc.textFile(fileName)
  #file=file.collect()
  file=open(fileName,"r")
  
  for line in file:
    line=line.strip()
    line=line.replace("(a)","")
    if len(line)>0:
      dictionary.append(line.strip())
  return dictionary
def toLines(x,lineLen):
  line=""
  for word in x:
    line+=word+" "
    if len(line)>=lineLen:
      yield line
def sizePartition(splitIndex,iterator):
  numChars=0
  for x in iterator:
    numChars+=len(x)
  yield numChars
def createWords(splitIndex,iterator,seed,dictionary,partSizes):
  random.seed(splitIndex+seed)
  dictSize=len(dictionary)
  numChars=0
  while numChars<partSizes[splitIndex]:
    n=random.randint(0,dictSize-1)
    word=dictionary[n]+" "#add a space between words
    numChars+=len(word)
    yield word
def combineWordsIntoLines(splitIndex,iterator,lineLength):
  line=""
  curLineLength=0
  for word in iterator:
    wordLen=len(word)
    if curLineLength+wordLen>lineLength:
      yield line
      line=word
      curLineLength=wordLen
    else:
      line+=word
      curLineLength+=wordLen
  yield line
def main():
  
  #parse command line options
  (options,args)=parseOptions()
  
  conf=SparkConf().setAppName("create_text_spark")
  #conf.set("spark.executor.instances",str(options.numExe))
  sc=SparkContext(conf=conf)
  conf=sc.getConf()
  print("conf="+str(conf.getAll()))
  print("defaultMinPartitions="+str(sc.defaultMinPartitions))
  print("defaultParallelism="+str(sc.defaultParallelism))
  
  #load dictionary
  dictionary=loadDictFromFile(sc,options.dictionaryFile)
  
  #set number of file partitions/parallelism
  if options.numPartitions==None:
    #pick number of partitions based on default amount of parallelism and filesize
    partFactor=2#how many times the default parallelism. Defaul Parallelism is 
      #related to the number of cores on the machine.
    numPartitions=sc.defaultParallelism*partFactor
    #Decrease the number of partitions if size of file per partition is too small 
    #(e.g. less than 1KB)
    while int(options.fileSize/numPartitions)<1000 and numPartitions!=1:
      numPartitions=int(numPartitions/2)
  else:
    numPartitions=options.numPartitions
  
  #create an RDD with the given number of partitions
  rdd=sc.parallelize([],numPartitions)#create an RDD with a given number of partitions
  print("num Partitions="+str(rdd.getNumPartitions()))
  
  #determine how many characters per partition
  sizePartMin=int(float(options.fileSize)/float(numPartitions))
  partSizes=[]
  for i in range(numPartitions):
    partSizes.append(sizePartMin)
  leftOver=options.fileSize-sizePartMin*numPartitions
  i=0
  while leftOver>0:
    partSizes[i]+=1
    leftOver-=1
    i+=1
  print("partSizes="+str(partSizes))
  
  #pick words randomly from dictionary
  f=lambda x,y: createWords(x,y,options.seed,dictionary,partSizes)
  result=rdd.mapPartitionsWithIndex(f)
  
  #print result
  #print(result.collect())
  
  #Check total size
  #print("total number of characters="+str(result.mapPartitionsWithIndex(sizePartition).sum()))
  
  #combine words into lines
  f=lambda x,y: combineWordsIntoLines(x,y,options.lineLength)
  lines=result.mapPartitionsWithIndex(f)
  #lines.cache()#this maybe helpful for timing IO
  numLines=lines.count()#count the lines so we can compare with line count and to force
    #evaluation of previous mappings to ensure that the below is just measuring
    #write time and not evaluation times.
  
  #save files
  timeStartWrite=time.time()
  lines.saveAsTextFile(options.outputDirName)
  timeEndWrite=time.time()
  dt=timeEndWrite-timeStartWrite
  print("write time="+str(dt)+" s")
  print("number of lines="+str(numLines))
if __name__ == "__main__":
  main()