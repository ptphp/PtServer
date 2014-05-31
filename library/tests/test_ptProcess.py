from unittest import TestCase
from library.core.ptprocess import PtProcess
from PySide.QtCore import QProcess
import re,subprocess
from core.ptprocess import PtProcess

class TestPtProcess(TestCase):
    def setUp(self):
        self.proc = PtProcess()
        super(TestPtProcess, self).setUp()

    def tearDown(self):
        super(TestPtProcess, self).tearDown()

    def test_cmd(self):
        #subprocess.Popen("explorer.exe", shell=False,close_fds=True)
        #subprocess.Popen("ping www.baidu.com", shell=False,close_fds=True)
        subprocess.Popen("ping www.baidu.com ", shell=False,close_fds=True)
        subprocess.Popen("ping www.baidu.com ", shell=True,close_fds=True)

    def test_env(self):
        process = QProcess()
        env = QProcess.systemEnvironment()
        process.start("explorer.exe")
        process.kill()


    def test_nginx(self):
        cmd = 'D:\PtServer/usr/local/nginx/nginx.exe -p D:\PtServer -c D:\PtServer/etc/nginx_win/nginx.conf'
        #cmd = 'ls'
        builder = QProcess()
        builder.setProcessChannelMode(QProcess.MergedChannels)
        res = builder.start(cmd)
        import sys
        if not builder.waitForFinished():
            sys.stderr.write("Make failed:" + builder.errorString())
        else:
            sys.stderr.write("Make output:" + builder.readAll())

    def test_qprocess(self):
        builder = QProcess()
        builder.setProcessChannelMode(QProcess.MergedChannels)
        res = builder.start("ping www.baidu.com ")
        print res
        import sys
        if not builder.waitForFinished():
            sys.stderr.write("Make failed:" + builder.errorString())
        else:
            sys.stderr.write("Make output:" + builder.readAll())

    def test_qprocess1(self):
        builder = QProcess()
        builder.setProcessChannelMode(QProcess.MergedChannels)
        res = builder.startDetached("ping www.baidu.com ")
        print res
    def test_getpids(self):
        #print getPidByPort(80)
        #cmd_list_port = 'netstat -nao | findstr ":%d.*LISTENING"'
        cmd = "netstat -aon"
        builder = QProcess()
        builder.setProcessChannelMode(QProcess.MergedChannels)
        builder.start(cmd)
        if builder.waitForFinished():
            res = builder.readAll()
            print res.split("\r")

    def test_mysql_start(self):
        res = self.proc.cmd("net stop MySQL")
        print res
        #res = self.proc.sub_cmd("net stop MySQL")
        print res

    def test_task_kill(self):
        cmd = 'taskkill /F /IM PING.EXE > nul'
        subprocess.Popen(cmd, shell=True,close_fds=True)