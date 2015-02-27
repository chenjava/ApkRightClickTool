@echo off
reg add HKCR\.apk /ve /t reg_sz /d "" /f
set WINRAR="C:\Program Files (x86)\WinRAR\WinRAR.exe"
set tool=apk_Winrar
set toolDes=apkWinrar
set toolPath=apkWinrar.bat
call :SetApkRightClickDirect %tool% "%toolDes%" %WINRAR%

set tool=apk_details
set toolDes=ApkDetails
set toolPath=getapkdetails.bat
call :SetApkRightClick %tool% "%toolDes%" "%toolPath%"

set tool=apkinstaller
set toolDes=ApkInstall
set toolPath=apkinstall.bat
call :SetApkRightClick %tool% "%toolDes%" "%toolPath%"

set tool=apk_Decompile
set toolDes=apkDecompile
set toolPath=apkDecompile.bat
call :SetApkRightClick %tool% "%toolDes%" "%toolPath%"

set tool=apk_Netbeans
set toolDes=apkNetbeans
set toolPath=apkNetbeans.bat
call :SetApkRightClick %tool% "%toolDes%" "%toolPath%"

set tool=apkRepack
set toolDes=apkRepack
set toolPath=apkRepack.bat
call :SetDirectoryRightClick %tool% "%toolDes%" "%toolPath%"

set tool=apkNetbeansRepack
set toolDes=apkNetbeansRepack
set toolPath=apkPackNetbeans.bat
call :SetDirectoryRightClick %tool% "%toolDes%" "%toolPath%"

pause>nul
goto :eof
:SetApkRightClick
echo %1
echo %2
echo %3
echo %0
set "regname=HKEY_CLASSES_ROOT\.apk\shell\%1"
set "regpath=HKEY_CLASSES_ROOT\.apk\shell\%1\command"
echo %regname%
echo %regpath%
set toolPath=%~dp0\%3 ""%%1""
echo %toolPath%
reg add "%regname%" /ve /t reg_sz /d "%2" /f
reg add "%regpath%" /ve /t reg_sz /d "%toolPath%" /f  
exit /b 0
:SetDirectoryRightClick
echo %1
echo %2
echo %3
echo %0
set "regname=HKEY_CLASSES_ROOT\Directory\shell\%1"
set "regpath=HKEY_CLASSES_ROOT\Directory\shell\%1\command"
echo %regname%
echo %regpath%
set toolPath=%~dp0\%3 ""%%1""
echo %toolPath%
reg add "%regname%" /ve /t reg_sz /d "%2" /f
reg add "%regpath%" /ve /t reg_sz /d "%toolPath%" /f  
exit /b 0
:SetApkRightClickDirect
echo %1
echo %2
echo %3
echo %0
set "regname=HKEY_CLASSES_ROOT\.apk\shell\%1"
set "regpath=HKEY_CLASSES_ROOT\.apk\shell\%1\command"
echo %regname%
echo %3%
set toolPath=%3
set setpath=%toolPath:~,-1% \"%%1\""
echo %setpath%
reg add "%regname%" /ve /t reg_sz /d "%2" /f
reg add "%regpath%" /ve /t reg_sz /d %setpath% /f  
exit /b 0
