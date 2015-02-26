@echo off

@set file=%1

python %~dp0\ApkParse\netbeans.py pack %file%

pause