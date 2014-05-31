@echo "测试CMD"
@echo "1、打印PATH"
@echo "2、退出"
@echo off
:choose
set /p st="模式选择："
if /i "%st%"=="1" goto echo_path
if /i "%st%"=="2" goto exit
:echo_path
echo %PATH%
goto choose
:exit
exit