#!/bin/env python
from pyspark import SparkContext, SparkConf

import random
import optparse as op

def addParserOptions(parser):
  """Adds command line options
  """
  
  #these options apply globally
  parser.add_option("--line-length",dest="lineLength",type="int",default=80
    ,help="Set the length of lines in the file [default: %default]")
  parser.add_option("--lines-split",dest="splitLines",default=True
    ,action="store_true"
    ,help="Separate file into lines of length LINELENGTH or less [default].")
  parser.add_option("--lines-not-split",dest="splitLines",default=True
    ,action="store_false"
    ,help="File will be a single line [not default].")
  parser.add_option("--file-size",dest="fileSize",type="int",default=1000
    ,help="The size of the file in bytes [default: %default bytes]")
  parser.add_option("-o",dest="outputFileName",type="string"
    ,default="generated.txt"
    ,help="Specify the name of the output file [default: \"%default\"].")
  parser.add_option("--seed-file",dest="seedFile",default=1,help="Seed used "
    +"for randomly choosing words from the dictionary [default: %default].")
  parser.add_option("--dictionary-file",dest="dictionaryFile",type="string"
    ,default="english-wordlist.txt"
    ,help="Specify a file containing a list of words separated by newlines "
    +"to be used as the language dictionary. This option has no effect if "
    +"the option --randomly-generate-dict is specified "
    +"[default: \"%default\"].")
  parser.add_option("--randomly-generate-dict",dest="genDict",default=False
    ,action="store_true",help="If set will create a dictionary by selecting"
    +" random letters for NUMWORDS words of a randomly chosen word length "
    +"between MINWORDLENGTH and MAXWORDLENGTH. See \"Randomly generated "
    +"dictionary options\" [default: %default].")
    
  randDictGroup=op.OptionGroup(parser,"Randomly generated dictionary options")
  randDictGroup.add_option("--min-word-length",dest="minWordLength",default=1
    ,type="int",help="Sets the minimum word length [default: %default].")
  randDictGroup.add_option("--max-word-length",dest="maxWordLength",default=10
    ,type="int",help="Sets the maximum word length [default: %default].")
  randDictGroup.add_option("--num-words",dest="numWords",default=1000
    ,type="int",help="Sets the maximum word length [default: %default].")
  randDictGroup.add_option("--seed-dict",dest="seedDict",default=1,help="Seed used "
    +"for randomly generating dictionary [default: %default].")
  parser.add_option_group(randDictGroup)
def parseOptions():
  """Parses command line options
  
  """
  
  parser=op.OptionParser(usage="Usage: %prog [options]"
    ,version="%prog 1.0",description=r"Randomly generates the content of a text file.")
  
  #add options
  addParserOptions(parser)
  
  #parse command line options
  return parser.parse_args()
def createGiberishDict(numWords,minWordLength,maxWordLength,seed=1):
  """Creates a dictionary of numWords created by randomly selecting a word 
  length between minWordLength and maxWordLength and the populating it with 
  randomly selected lower case letters.
  """
  
  characterLow=97
  characterHigh=122
  random.seed(seed)
  
  #create a dictionary of words
  dictionary={}
  for i in range(numWords):
    length=random.randint(minWordLength,maxWordLength)
    word=""
    for j in range(length):
      character=chr(random.randint(characterLow,characterHigh))
      word+=character
    dictionary[i]=word
  return dictionary
def loadDictFromFile(fileName):
  """Loads a dicionary from a file containing words seperated by newline 
  characters.
  """
  
  dictionary={}
  count=0
  for line in open(fileName,'r'):
    line=line.strip()
    line=line.replace("(a)","")
    if len(line)>0:
      dictionary[count]=line.strip()
      count+=1
  return dictionary
def main():
  
  conf=SparkConf().setAppName("create_text_spark")
  sc=SparkContext(conf=conf)
  
  print("hello world")
  
  #parse command line options
  #(options,args)=parseOptions()
  
  '''
  #create a dictionary to use to construct the file
  if options.genDict:
    dictionary=createGiberishDict(options.numWords
      ,options.minWordLength,options.maxWordLength
      ,seed=options.seedDict)
  else:
    dictionary=loadDictFromFile(options.dictionaryFile)
   
  #create file from the dictionary
  size=0
  f=open(options.outputFileName,'w')
  lenDict=len(dictionary.keys())-1
  random.seed(options.seedFile)
  while(size<options.fileSize):
    
    line=""
    lineLen=0
    while(True):
      wordKey=random.randint(0,lenDict)
      word=dictionary[wordKey]
      lineLen+=len(word)+1
      if lineLen<options.lineLength:
        line+=word+" "
      else:
        break
    if options.splitLines:
      line+="\n"
    f.write(line)
    size+=len(line)
  
  f.close()
  '''
if __name__ == "__main__":
  main()