@echo "����CMD"
@echo "1����ӡPATH"
@echo "2���˳�"
@echo off
:choose
set /p st="ģʽѡ��"
if /i "%st%"=="1" goto echo_path
if /i "%st%"=="2" goto exit
:echo_path
echo %PATH%
goto choose
:exit
exit