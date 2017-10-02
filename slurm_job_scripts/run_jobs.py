#!/bin/env python
from __future__ import print_function
import sys
import subprocess as sp
import optparse as op
import os
import copy
from lxml import etree
import logging
logger=logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO
  ,format="%(levelname)s:%(name)s:%(filename)s:%(funcName)s:%(lineno)d:%(message)s")

__version__="1.0"

def addParserOptions(parser):
  """Adds command line options
  """
  pass
def parseOptions():
  """Parses command line options
  
  """
  
  parser=op.OptionParser(usage="Usage: %prog [options] SETTINGS.xml"
    ,version="%prog "+__version__,description="")
  
  #add options
  addParserOptions(parser)
  
  #parse command line options
  return parser.parse_args()
def getListOfChildValues(node):
  tmpList=[]
  for child in node:
    tmp={"text":child.text,"name":child.attrib["name"],"timeMult":child.attrib["timeMult"]}
    tmpList.append(tmp)
  return tmpList
def parseSettings(fileName
  ,variableElementNames=["spark-partitions-list","lustre-stripes-list"
  ,"data-sizes-list"]):
  
  #load schema to validate against
  schemaFileName=os.path.join(os.path.dirname(__file__)
    ,"run_jobs_settings.xsd")
  schema=etree.XMLSchema(file=schemaFileName)
  
  #parse xml file
  tree=etree.parse(fileName)
  
  #strip out any comments in xml
  comments=tree.xpath('//comment()')
  for c in comments:
    p=c.getparent()
    p.remove(c)
  
  #validate against schema
  schema.assertValid(tree)
  
  settings={}
  root=tree.getroot()
  
  #get paths to template job scripts
  templateJobScriptsNode=root.find("template-job-scripts")
  createInputJobScriptNode=templateJobScriptsNode.find("create-input")
  runBenchmarkJobScriptNode=templateJobScriptsNode.find("run-benchmark")
  settings["create-input"]={
    "baseJobTime":createInputJobScriptNode.attrib["baseJobTime"]
    ,"text":createInputJobScriptNode.text
    ,"skip":createInputJobScriptNode.attrib["skip"] in ["true",1]}
  settings["run-benchmark"]={
    "baseJobTime":runBenchmarkJobScriptNode.attrib["baseJobTime"]
    ,"text":runBenchmarkJobScriptNode.text
    ,"numRuns":runBenchmarkJobScriptNode.attrib["numRuns"]
    ,"skip":runBenchmarkJobScriptNode.attrib["skip"] in ["true",1]}
  
  settings["parameters"]={}
  variablesNode=root.find("parameters")
  
  #Get variable data
  for child in variablesNode:
    settings["parameters"][child.tag]=getListOfChildValues(child)

  return settings
def makeJobScript(templateFileName,outFileName,replaces):
  
  #read in template
  templateFile=open(templateFileName,'r')
  templateText=templateFile.read()
  templateFile.close()
  
  #do replaces
  script=templateText
  logger.debug(str(replaces))
  for replace in replaces:
    script=script.replace(replace[0],replace[1])
  
  #write out
  outFile=open(outFileName,"w")
  outFile.write(script)
  outFile.close()
def getTestCases(p,depth=0,keys=None,parentParams={},testCases=[]):
  if keys==None:#need to pass keys down to child calls to keep consistent 
    #ordering, since dictionaries are not ordered
    keys=p.keys()
  key=keys[depth]
  for i in range(len(p[key])):
    #print("depth="+str(depth)+" i="+str(i))
    #print("p[depth][i]="+str(p[depth][i]))
    params=copy.deepcopy(parentParams)
    params[key]=p[key][i]
    if depth+1<len(keys):
      getTestCases(p,depth=depth+1,keys=keys,parentParams=params
        ,testCases=testCases)
    else:#test case completed
      #print("adding "+str(params)+" test case")
      testCases.append(params)
  return testCases
def makeStringReplacementsForTestCase(testCase):
  replacements=[]
  logger.debug(testCase)
  for key in testCase.keys():
    logger.debug(str(key)+":"+str(testCase[key]))
    for subkey in testCase[key].keys():
      replacements.append( ("<"+str(key)+"."+str(subkey)+">",str(testCase[key][subkey])))
  logger.debug(replacements)
  return replacements
def makeJobScriptName(prefix,testCase):
  fileName=prefix
  for key in testCase.keys():
    fileName+="_"+testCase[key]["name"]
  return fileName+".sh"
def createJobTimeStr(baseJobTime,testCase):
  jobTime=float(baseJobTime)#should be a string of job time in seconds
  for key in testCase.keys():
    jobTime=jobTime*float(testCase[key]["timeMult"])
  
  #convert to a HH:MM:SS string
  minutes=int(jobTime)
  if minutes<1:#minimum job times appears to be 1 min, 
    #at least can't be 0 mins or fractions of mins.
    minutes=1
  return str(minutes)
def submitJob(pathToJobScript,options=[]):
  cmd=["sbatch"]+options+[pathToJobScript]
  logger.debug("cmd="+str(cmd))
  process=sp.Popen(cmd,stdout=sp.PIPE,stderr=sp.PIPE)
  stdout,stderr=process.communicate()
  returnCode=process.returncode
  jobID=None
  if returnCode==0:
    splits=stdout.split(' ')
    jobID=splits[len(splits)-1]
    logger.debug("jobID="+str(jobID))
  else:
    logger.info("problem submitting the job, stdout, stderr, and return code "
      +"to follow:")
    logger.debug("stdout="+str(stdout))
    logger.debug("stderr="+str(stderr))
    logger.debug("returnCode="+str(returnCode))
  return jobID.strip()
def main():
  
  #parse command line options
  (options,args)=parseOptions()
  
  if len(args)!=1:
    raise Exception("need to specify a settings file")
  
  #parse settings
  variableElementNames=["spark-partitions-list","lustre-stripes-list"
  ,"data-sizes-list"]
  settings=parseSettings(args[0],variableElementNames=variableElementNames)
  logger.debug(settings)
  
  #create settings for test cases to run (all permutations of the parameters)
  testCases=getTestCases(settings["parameters"])
  
  for testCase in testCases:
    logger.debug(testCase)
    
    replaces=makeStringReplacementsForTestCase(testCase)
    
    #create data
    jobID=None
    if not settings["create-input"]["skip"]:
      jobScriptFileName=makeJobScriptName("./create-input",testCase)
      jobTimeStr=createJobTimeStr(settings["create-input"]["baseJobTime"],testCase)
      replaces.append(("<job-time>",jobTimeStr))
      makeJobScript(settings["create-input"]["text"],jobScriptFileName,replaces)
      
      #submit create date job and get job ID
      print("submitting job "+jobScriptFileName+" ...")
      jobID=submitJob(jobScriptFileName)
    
    #run benchmarks
    if not settings["run-benchmark"]["skip"]:
      del replaces[-1]#remove last job time
      jobTimeStr=createJobTimeStr(settings["run-benchmark"]["baseJobTime"],testCase)
      replaces.append(("<job-time>",jobTimeStr))
      jobScriptFileName=makeJobScriptName("./run_read-write-benchmark",testCase)
      makeJobScript(settings["run-benchmark"]["text"],jobScriptFileName,replaces)
      for i in range(int(settings["run-benchmark"]["numRuns"])):
        print("submitting job "+jobScriptFileName+" ...")
        if jobID==None:
          jobID=submitJob(jobScriptFileName)
        else:
          jobID=submitJob(jobScriptFileName,options=["--dependency=afterany:"+str(jobID)])
    
if __name__=="__main__":
  main()