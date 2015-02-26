#!/usr/bin/env python
#coding:utf-8 
# --*-- encoding:utf-8 --*--
'''
Created on 2014-10-20
@author: chenjava

'''

import sys

from ParseApk import ApkParser 
from Util import * 


class apkParse:    
    def __init__(self,apkFilePath):  
        self.apkFilePath = apkFilePath    #apk file path
        self.unpackPath = ''     #apk unpack file path            

    
    def getAPKDetails(self):        
        apkFilePath = self.apkFilePath
        self.parser = ApkParser(apkFilePath)    
        packageName = self.parser.getPackageName()
        print "packName:%s"%packageName
        versionCode = self.parser.getVersionCode()
        print "versionCode:%s"%versionCode
        versionName = self.parser.getVersionName()
        print "versionName:%s"%versionName
        appLabel = self.parser.getAppLabel()        
        printappLabel = appLabel.decode("utf-8").encode("gbk")
        print "appName:%s"%printappLabel
        nativeCode = self.parser.getNativeCode()
        print "nativeCode:%s"%nativeCode
        minSdkVersion = self.parser.getMinSdkVersion()
        targetSdkVersion = self.parser.getTargetSdkVersion()
        languageCount = self.parser.getLanguageCount()
        print "minSDKV:%s targetSDKV:%s languangeCount:%d"%(minSdkVersion,targetSdkVersion,languageCount)
        fileSize = self.parser.getApkFileSize()
        fileMd5 = self.parser.getApkFileMd5()
        print "fileSize:%d\nfileMd5:%s"%(fileSize,fileMd5)
        (sign,company) =  self.parser.getAPKSignInfo()
        print "signMd5:%s"%sign
        print "subjectInfo:%s"%company

def main(argv):        
    if(len(argv)>1):
        print "apkFile:%s"%argv[1]
        parse = apkParse(argv[1])
        parse.getAPKDetails()    

if __name__ == '__main__':
  main(sys.argv)

