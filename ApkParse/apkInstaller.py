#!/usr/bin/env python2.7
#coding:utf-8 
# --*-- encoding:utf-8 --*--

import os
import sys
import zipfile
import time
import shutil
import re
from Util import *  

urlSidList = []

def getLibPath ():
    temppath = os.path.split( os.path.realpath( sys.argv[0] ) )[0]
    if temppath[-1] == os.path.sep:
        temppath = temppath + "lib"
    else:
        temppath = temppath +os.path.sep+ "lib"    
    return temppath

def getTempPath (): 
    temppath = os.path.split( os.path.realpath( sys.argv[0] ) )[0]
    if temppath[-1] == os.path.sep:
        temppath = temppath + "temp" +os.path.sep
    else:
        temppath = temppath +os.path.sep+ "temp" +os.path.sep
    return temppath


def reSignApk (apkName):
    extIndex = apkName.find('.apk')
    signApkName = ''
    if extIndex > 0:
        signApkName = apkName[:extIndex] + '_newSigned.apk'        
    libpath = getLibPath()
    sigCommand = 'java -jar %s/autosign/signapk.jar %s/autosign/testkey.x509.pem %s/autosign/testkey.pk8 %s %s' % (libpath,libpath,libpath,apkName,signApkName)
#   sigCommand = 'java -jar %s/autosign/signapk.jar %s/autosign/debug.x509.pem %s/autosign/debug.pk8 %s %s' % (libpath,libpath,libpath,apkName,signApkName)
    os.system(sigCommand)
    return signApkName

def reTestSignApk (apkName):
    extIndex = apkName.find('.apk')
    signApkName = ''
    if extIndex > 0:
        signApkName = apkName[:extIndex] + '_newSigned.apk'        
    libpath = getLibPath()
    sigCommand = 'java -jar %s/autosign/signapk.jar %s/autosign/shared.x509.pem %s/autosign/shared.pk8 %s %s' % (libpath,libpath,libpath,apkName,signApkName)
    os.system(sigCommand)
    return signApkName

def reBuildApk (apkpath):
    libpath = getLibPath()
    outFile = apkpath+"_pack.apk"
    sigCommand = '%s\\apktool\\apktool.bat b %s -o %s' % (libpath,apkpath,outFile)
#   print sigCommand
    print "start rebuild apk:%s"%outFile
    os.system(sigCommand)
    if  os.path.exists(outFile)==False:
        print "rebuild error"
        return
    else:        
        print "start resign apk"
        signed_apk = reSignApk(outFile)
        if  os.path.exists(signed_apk)==False:
            print "resign error"
            return
        else:
            os.remove(outFile)
#   print "start install apk"
#   os.system('adb install -r '+signed_apk)

def decompilAPK (apkpath):
    libpath = getLibPath()    
    sigCommand = '%s/apktool/apktool.bat d %s' % (libpath,apkpath)
    print "start decomile apk"
    os.system(sigCommand)

def getDevices ():
    devices=[]
    command="adb devices"
    out = getCmdoutput(command)
    lines = out.split('\n')
    for line in lines:        
        if line[-6:]=='device':
            pattern="(.+?)\s+"
            m = re.match(pattern,line)
            if m!=None:
                devices.append(m.group(1))
    return devices

def apkInstall (apkName):
    devices=getDevices ()
    if len(devices)==0:
        print "no android device"
    elif len(devices)==1:
        command="adb install -r %s"%apkName
        os.system(command)
    else:
        print "one more devices"
        devIndex=1
        selectDir={}
        for device in devices:
            print "%d   %s"%(devIndex,device)
            selectDir[devIndex]=device
            devIndex = devIndex + 1
        select_num = raw_input("select install device(input num): ")
        print select_num
        if selectDir.has_key(int(select_num)):
            useDev = selectDir[int(select_num)]
            print "selected device:%s"%useDev            
            command="adb -s %s install -r %s"%(useDev,apkName)
#           print command
            os.system(command)
        else:
            print "select device error"

        

def main(argv):
    """
    A command line google safe browsing client. Usage:
    client.py <APIKey> [check <URLs>]
    """  
    if(len(argv)>2):        
        if argv[1]=='install':
            apkInstall(argv[2])
        elif argv[1]=='decompile':
            decompilAPK(argv[2])
        elif argv[1]=='rebuild':
            reBuildApk(argv[2])
    else:
      print "please input apk file"


if __name__ == '__main__':
  main(sys.argv)
