@echo off

@set file=%1

python %~dp0\ApkParse\apkInstaller.py rebuild %file%

pause