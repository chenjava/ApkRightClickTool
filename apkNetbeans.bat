@echo off

@set file=%1

python %~dp0\ApkParse\netbeans.py bin %file%

pause