@echo off

@set file=%1

python %~dp0\ApkParse\GetApkDetails.py %file%

pause