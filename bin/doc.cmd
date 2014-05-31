@echo off 
echo %%~dp0 is "%~dp0"
echo %%0 is "%0"
echo %%~dpnx0 is "%~dpnx0"



set REL_PATH=..\..\
set ABS_PATH=

rem // save current directory and change to target directory
pushd %REL_PATH%
rem // save value of CD variable (current directory)
set ABS_PATH=%CD%
rem // restore original directory
popd

echo Relative path : %REL_PATH%
echo Maps to path  : %ABS_PATH%

pause