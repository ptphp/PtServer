@echo off 
echo deleting service
echo =================
echo sc delete MySQL5.1
net stop MySQL5.1
sc delete MySQL5.1
echo ------------
echo sc delete MongoDB
net stop MongoDB
sc delete MongoDB
echo ------------
echo sc delete redis
net stop redis
sc delete redis
echo =================
pause
