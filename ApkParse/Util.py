#!/usr/bin/env python
#coding:utf-8 
# --*-- encoding:utf-8 --*--
'''
Created on 2014-10-20

@author: chenjava
'''

import sys
import os
import md5
import re

def convertFilePath(path):
    path = path.replace('(', '\(')
    path = path.replace(' ', '\ ')
    path = path.replace(')', '\)')

    return path

def getRunPath ():
    temppath = os.path.split( os.path.realpath( sys.argv[0] ) )[0]
    if temppath[-1] == os.path.sep:
        temppath = temppath[:-1]
    return temppath

def getCmdoutput(cmd):  
    text = ''      
    pipe = os.popen(cmd)
    text = pipe.read()
    sts = pipe.close()        
    return text

def getTempPath (): 
    temppath = os.path.split( os.path.realpath( sys.argv[0] ) )[0]
    if temppath[-1] == os.path.sep:
        temppath = temppath + "temp" +os.path.sep
    else:
        temppath = temppath +os.path.sep+ "temp" +os.path.sep
    return temppath

def getFileMd5(filename): 
    fileMd5=''
    try:
        fobj = file(filename, 'rb')   
        if fobj != None:
            m = md5.new()
            while True:
                d = fobj.read(8096)
                if not d:
                    break
                m.update(d)
            fobj.close()
            fileMd5 = m.hexdigest()
    except Exception,e:
        print e
        print "cal file md5 error:%s"%filename
    return fileMd5

def getStringMd5(strName):  
    m = md5.new()
    m.update(strName)
    return m.hexdigest()

def getFileSize (apkFilePath):
    fileSize = os.path.getsize(apkFilePath)
    return int(fileSize)


def styleFileCorrect (filename):
    bCorrect=False
    fp = file(filename)
    lines=fp.readlines()
    newLines=''
    pattern = '\s+name="(do|if)"'
    pattern2 = '>@\w+?/(do|if)</item'
    for line in lines:
        m = re.search(pattern,line)
        if m!=None:
            pos = line.find('name="')
            newLine = line[:pos+7]+'_'+line[pos+7:]
            newLines=newLines+newLine
            bCorrect = True
        else:
            m = re.search(pattern2,line)
            if m!=None:
                pos = line.find('</item')
                newLine = line[:pos-1]+'_'+line[pos-1:]
                newLines=newLines+newLine
                bCorrect = True
            else:
                newLines=newLines+line
    fp.close()
    fwp=open(filename,'w')
    fwp.write(newLines)
    fwp.close()
    if bCorrect == True:
        print "%s include do|if"%filename
    return bCorrect


def fileCorrectValueName (filename):
    bCorrect=False
    fp = file(filename)
    lines=fp.readlines()
    newLines=''
    pattern = '\s+name="(do|if)"'
    for line in lines:
        m = re.search(pattern,line)
        if m!=None:
            pos = line.find('name="')
            newLine = line[:pos+7]+'_'+line[pos+7:]
            newLines=newLines+newLine
            bCorrect = True
        else:
            newLines=newLines+line
    fp.close()
    fwp=open(filename,'w')
    fwp.write(newLines)
    fwp.close()
    if bCorrect == True:
        print "%s include do|if"%filename
    return bCorrect

def correctValueName(resDir):    
    publicFile = resDir+os.sep+"values"+os.sep+"public.xml"    
    if fileCorrectValueName(publicFile) == False:
        print "public.xml not include do|if"
        return
    print "public.xml include do|if"
    list_dirs = os.walk(resDir) 
    for root, dirs, files in list_dirs:     
        for f in files: 
            filename = os.path.join(root, f) 
            if filename[-4:]=='.xml' and filename!=publicFile:
                if filename[-10:]=='styles.xml':
                    styleFileCorrect(filename)
                else:
                    fileCorrectValueName(filename)



