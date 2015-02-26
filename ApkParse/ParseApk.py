#!/usr/bin/env python
#coding:utf-8 
# --*-- encoding:utf-8 --*--
'''
Created on 2014-7-30

@author: chenjava
'''


import re
import os
import zipfile
from Util import * 


class ApkParser:
    def __init__(self,apkFilePath):          
        self.apkFilePath = apkFilePath
        self.output = self.getAAPTinfo()
        self.tempPath = getTempPath()


    def getAAPTinfo (self):
        localPath = getRunPath()
        command = '%s/lib/apktool/aapt.exe dump  badging %s'%(localPath,self.apkFilePath)
        output = getCmdoutput(command) 
        return output

    def getAPKSignInfo (self):
        localPath = getRunPath()
        sigCommand = 'java -jar %s/lib/getapksign/getapksign.jar %s' % (localPath,self.apkFilePath)
        output = getCmdoutput(sigCommand) 
        signList = output.split('\n')
        signMd5=''
        signCN=''
        if len(signList)>1:
            signMd5 = signList[0]
            signCN = signList[1]
        return (signMd5,signCN)



    def getPackageName (self):
        packName = ''
        m = re.search("package: name='([\w\.]+)'",self.output)
        if m != None:
            packName = m.group(1)                    
        return packName

    def getVersionCode (self):
        packName = '0'
        m = re.search("versionCode='(\d+)'",self.output)
        if m != None:
            tempList = m.groups()                
            packName = tempList[0]        
        return packName

    def getVersionName(self):
        packName = ''
        m = re.search("versionName='(.+?)'",self.output)
        if m != None:
            tempList = m.groups()           
            packName = tempList[0]            
        return packName

    def getAppLabel(self):
        appLabel = ''
        m = re.search("application-label:'(.+?)'",self.output)
        if m != None:
            appLabel = m.group(1)                               
        return appLabel

    def getMinSdkVersion(self):
        sdkVersion = '0'
        m = re.search("sdkVersion:'(\d+)'",self.output)
        if m != None:
            tempList = m.groups()           
            sdkVersion = tempList[0]
        print    "minSdkVersion:%s"%sdkVersion           
        return sdkVersion

    def getTargetSdkVersion(self):
        targetSdkVersion = '0'
        m = re.search("targetSdkVersion:'(\d+)'",self.output)
        if m != None:
            tempList = m.groups()           
            targetSdkVersion = tempList[0]        
        print    "targetSdkVersion:%s"%targetSdkVersion           
        return targetSdkVersion

    def getNativeCode(self):
        NativeCode = ''
        m = re.search("native-code:(.+?)\n",self.output)
        if m != None:
            NativeCode = m.group(1)
        return NativeCode
     
    def getLanguageCount (self):
        nCount = 0
        m = re.search("locales:.+?\n",self.output)
        if m != None:
            localeList = re.findall("'(.+?)'",m.group(0))
            nCount = len(localeList)
        return nCount


    def getApkFileSize (self):
        return getFileSize(self.apkFilePath)

    def getApkFileMd5(self):
        return getFileMd5(self.apkFilePath)

