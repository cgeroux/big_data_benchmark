#!/usr/bin/env python

import random
import optparse as op
from subprocess import Popen, PIPE,list2cmdline
import os

def addParserOptions(parser):
  """Adds command line options
  """
  
  #these options apply globally
  parser.add_option("-f",dest="forceOverwrite",default=False,action="store_true"
    ,help="Forces overwriting of an existing output file [not default].")
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
    ,default="generated.txt",help="Specify the name of the output file "
    +"and path within HDFS [default: \"%default\"].")
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
  parser.add_option("--hdfs-upload-size",dest="hdfsUploadSize",type="int"
    ,default=100000000
    ,help="Size in bytes between uploads to HDFS [default: %default].")
    
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
    ,version="%prog 1.0",description=r"Randomly generates the content of a text file in HDFS.")
  
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
def performCommand(cmd,throwOnError=True):
  #upload file to HDFS
  process=Popen(cmd,stdout=PIPE,stderr=PIPE)
  stdout,stderr=process.communicate()
  returnCode=process.returncode
  if throwOnError:
    if (returnCode!=0):
      raise Exception("error encounter while executing command "
        +str(cmd)+" got stdout=\""+str(stdout)+"\" and stderr=\""
        +str(stderr)+"\" and return code="+str(returnCode))
  
  return returnCode
def main():
  
  #parse command line options
  (options,args)=parseOptions()
  
  #create a dictionary to use to construct the file
  if options.genDict:
    dictionary=createGiberishDict(options.numWords
      ,options.minWordLength,options.maxWordLength
      ,seed=options.seedDict)
  else:
    dictionary=loadDictFromFile(options.dictionaryFile)
  
  #should check if the hdfs file is there and remove it if it is
  cmd=["hdfs","dfs","-stat",options.outputFileName]
  returnCode=performCommand(cmd,throwOnError=False)#throwOnError=False since we will handle the error here
  
  if(returnCode==0):
    overwrite=False
    if not options.forceOverwrite:
      
      #check if we should overwrite it
      overWriteResponse=raw_input("File exists, overwrite? (y/n)")
      if overWriteResponse in ["y","Y","Yes","T","True","1"]:
        overwrite=True
    else:
      overwrite=True
    
    #remove the file
    if overwrite:
      cmd=["hdfs","dfs","-rm",options.outputFileName]
      performCommand(cmd)
    else:
      print "Not overwriting pre-existing file in HDFS \"" \
        +options.outputFileName+"\""
      quit()
  
  #create the command to upload to HDFS
  tempFileName="tmp.txt"
  cmd=["hdfs","dfs","-appendToFile",tempFileName,options.outputFileName]
  
  #create file from the dictionary
  sizeTotal=0
  sizeToUpload=0
  f=open(tempFileName,'w')
  lenDict=len(dictionary.keys())-1
  random.seed(options.seedFile)
  sizePerHDFAppend=options.hdfsUploadSize
  while(sizeTotal<options.fileSize):
    
    #create a line to add to the file
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
    
    #write the line to the file
    if options.splitLines:
      line+="\n"
    f.write(line)
    sizeTotal+=len(line)
    sizeToUpload+=len(line)
    
    #if temporary file big enough upload to HDFS
    if sizeToUpload>=sizePerHDFAppend:
      
      print "uploading "+str(sizeToUpload)+" bytes to hdfs"
      
      #close the file
      f.close()
      
      #upload file to HDFS
      performCommand(cmd)
      
      #remove file after upload and open a new file for the next chunk
      os.remove(tempFileName)
      f=open(tempFileName,'w')
      sizeToUpload=0
  
  #close the temporary file
  f.close()
  
  #upload any extra content written to the temporary file since last upload
  if sizeToUpload>0:
    print "uploading remaining "+str(sizeToUpload)+" bytes to hdfs"
    performCommand(cmd)
  
  #remove temporary file
  os.remove(tempFileName)
if __name__ == "__main__":
  main()