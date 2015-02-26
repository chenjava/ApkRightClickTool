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
