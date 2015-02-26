#!/usr/bin/env python2.7
#coding:utf-8 
# --*-- encoding:utf-8 --*--

import os
import shutil
import sys
import zipfile
import time
import shutil
 

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
    os.system(sigCommand)
    return signApkName


def enableDebug (apkpath):
    xmlName = apkpath+os.path.sep + "AndroidManifest.xml"
    fr = open(xmlName)
    lines = fr.readlines()
    newlines = []
    for line in lines:
        tmpIndex = line.find('<application ')
        if tmpIndex>-1:
            if line.find("android:debuggable=\"false\"")>-1:
                line = line.replace("android:debuggable=\"false\"","android:debuggable=\"true\"")
            elif line.find("android:debuggable=\"true\"")>-1:
                print "debug true already"
            else:
                useIndex = tmpIndex + len('<application ')
                line =  line[:useIndex] + "android:debuggable=\"true\" " + line[useIndex:]
        newlines.append(line)
    fr.close()
    fw = open(xmlName,'w')
    for line in newlines:
        fw.write(line)
    fw.close()


def reverseApk (apkName):
    extIndex = apkName.find('.apk')
    apkPath = ''
    reversedApkName = ''
    signApkName = ''
    if extIndex > 0:
        apkPath = apkName[:extIndex]
        reversedApkName = apkName[:extIndex] + '_newReversed.apk'        
        signApkName = apkName[:extIndex] + '_netbeans.apk'        
    libpath = getLibPath()
    print "start unpack apk"
    Command = 'java -jar %s/apktool/apktool.jar  d -d %s -o  %s' % (libpath,apkName,apkPath)    
    os.system(Command)
#   time.sleep(50)
    print "start pack apk"
    enableDebug(apkPath)
    Command = 'java -jar %s/apktool/apktool.jar  b -d %s -o  %s' % (libpath,apkPath,reversedApkName)
    os.system(Command)

    if  os.path.exists(reversedApkName)==False:
        print "pack apk error"
        return
    Command = 'java -jar %s/autosign/signapk.jar %s/autosign/testkey.x509.pem %s/autosign/testkey.pk8 %s %s' % (libpath,libpath,libpath,reversedApkName,signApkName)
    print "start resign apk"
    os.system(Command)

    if  os.path.exists(signApkName)==False:
        print "resign apk error"
        return
    else:
        os.remove(reversedApkName)
#   remove build dir
    shutil.rmtree(apkPath+os.path.sep+"build")
    print "start install apk"
    os.system('adb install -r '+signApkName)

    #原有的netbeans解包重新打包
def rebuildNetbeans (apkPath):
    reversedApkName = apkPath+"_pack.apk"
    signApkName = apkPath + '_netbeans_repack.apk'    
    libpath = getLibPath()
       
    Command = 'java -jar %s/apktool/apktool.jar  b -d %s -o  %s' % (libpath,apkPath,reversedApkName)
    os.system(Command)

    if  os.path.exists(reversedApkName)==False:
        print "pack apk error"
        return
    Command = 'java -jar %s/autosign/signapk.jar %s/autosign/testkey.x509.pem %s/autosign/testkey.pk8 %s %s' % (libpath,libpath,libpath,reversedApkName,signApkName)
    print "start resign apk"
    os.system(Command)

    if  os.path.exists(signApkName)==False:
        print "resign apk error"
        return
    else:
        os.remove(reversedApkName)
#   remove build dir
    shutil.rmtree(apkPath+os.path.sep+"build")
    print "start install apk"
    os.system('adb install -r '+signApkName)

def main(argv):
  """
  A command line google safe browsing client. Usage:
    client.py <APIKey> [check <URLs>]
  """  
  if(len(argv)>2):
      if argv[1]=='bin':
          reverseApk(argv[2])     
      if argv[1]=='pack':
          rebuildNetbeans(argv[2])  
  else:
      print "please input apk file"


if __name__ == '__main__':
  main(sys.argv)
