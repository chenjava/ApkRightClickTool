@echo off

@set file=%1

python %~dp0\ApkParse\apkInstaller.py decompile %file%

pause