
@echo off

rem # bitsadmin /create indir
rem # bitsadmin /addfile indir https://www.python.org/ftp/python/2.7.11/Python-2.7.11.tgz C:\Users\bkorayoz\Desktop\pags_client\pitonyukleme
rem # bitsadmin /getstate indir
rem # bitsadmin /resume indir
rem # bitsadmin /getstate indir
rem # bitsadmin /complete indir
rem # tar -xzf Python-2.7.11.tgz  
rem # cd Python-2.7.11

set way=%cd%
START /WAIT bitsadmin.exe /transfer "Python Downloading" https://www.python.org/ftp/python/3.5.3/python-3.5.3.exe %way%/python-3.5.3.exe
START /WAIT python-3.5.3.exe /quiet InstallAllUsers=1 PrependPath=1

START /WAIT pip3 install requests
START /WAIT pip3 install pypiwin32
START /WAIT pip3 install wmi

START /WAIT python getHardwareInfo.py

start http://www.localhost:5000/profile
pause