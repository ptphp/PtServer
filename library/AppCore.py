#!/usr/bin/env python
# -*- coding=utf-8 -*-
import sys
import os
import ConfigParser
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtNetwork import *
from library.core.utils import loadUi,PtDebugView,debug
from library.core.controls import PortControl,PhpControl,NginxControl
from library.core.baseapp import BaseApp
from library.core.actions import BaseAction
from library.core.buttons import BaseButtons
from library.core.ptprocess import PtProcess
import zipfile

ERROR, WARNING, INFO, DEBUG = range(4)

config = ConfigParser.RawConfigParser()
config_filename = "config.cfg"

dirs = [
            "logs",
            "var/logs/nginx",
            "var/logs/mysql",
            "var/logs/mongodb",
            "var/data/mongodb",
            "var/data/ssdb",
            "var/data/mysql",
            "temp/client_body_temp",
            "temp/fastcgi_temp",
            "temp/fastcgi_temp",
            "temp/uwsgi_temp",
        ]



def makeDir(path):
    path = os.path.abspath(path)

    if os.path.isfile(path):
        path = os.path.dirname(path)

    if os.path.isdir(path) == False:
        makeDir(os.path.dirname(path))
        return os.mkdir(path)
    return True

class MainWindow(QMainWindow,BaseApp,BaseAction,BaseButtons):
    path = None

    def __init__(self,debug_level=ERROR,debug_stream = sys.stderr,path = "",test = False):
        super(MainWindow, self).__init__()
        self.path = path
        self.path_root = os.path.dirname(self.path)
        self.test = test
        self.make_dirs()

        self.proc = PtProcess()
        loadUi(self.path + "/var/res/ui/win.ui",self)
        self.setWindowTitle("PtServer")
        self.debug_level = debug_level
        self.debug_stream = debug_stream
        self.debugView = PtDebugView(self)
        self.controls = {
                'nginx' : NginxControl(self),
                'php' : PhpControl(self),
                'port' : PortControl(self),
                }
        self.set_buttons()
        self.icon = QIcon()
        icon_path = os.path.join(self.path,"var",'res','title.png')
        self.icon.addPixmap(QPixmap(icon_path),QIcon.Normal,QIcon.Off)
        self.setWindowIcon(self.icon)

        self.set_actions()
        self.addTray()
        self.set_status_bar()

        self.timer_list = {}


    def debug(self,msg,type="sys"):
        print msg
        debug(msg.strip(),type)

    def config(self):
        config.read(self.path+"/"+config_filename)
        return config
    def closeEvent(self, event):
        reply = QMessageBox.Yes
        if self.test == False:
            reply = QMessageBox.question(self, 'Message',
                        "Are you sure to quit?", QMessageBox.Yes |
                        QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            for control in self.controls:
                if self.controls[control].isRunning():
                    print control+"kill"
                    self.controls[control].terminate()
            event.accept()
        else:
            if self.trayIcon.isVisible():
                self.showMessage(u"提示信息",u"最小化")
                self.hide()
                event.ignore()
    def make_dirs(self):
        return
        for dir in dirs:
            makeDir(os.path.join(self.path,dir))
        mysql_data_path = os.path.join(self.path,"var/data/mysql/mysql")

        if False == os.path.isdir(mysql_data_path):
            mysql_ini_path = os.path.join(self.path,"usr/local/mysql/my.ini")
            f = open(mysql_ini_path)
            _ini_content = ''
            for line in f.read().split("\n"):
                if line.startswith("log-error="):
                    line = "log-error={0}/var/logs/mysql/error.log".format(self.path.replace("\\","/"))
                if line.startswith("log="):
                    line = "log-error={0}/var/logs/mysql/mysql.log".format(self.path.replace("\\","/"))
                if line.startswith("log-slow-queries="):
                    line = "log-error={0}/var/logs/mysql/slowquery.log".format(self.path.replace("\\","/"))
                if line.startswith("basedir"):
                    line = "basedir={0}/usr/local/mysql".format(self.path.replace("\\","/"))
                if line.startswith("datadir"):
                    line = "datadir={0}/var/data/mysql".format(self.path.replace("\\","/"))

                _ini_content += line+"\n"
            f.close()
            f = open(mysql_ini_path,"w")
            f.write(_ini_content)
            f.close()

            zfile = zipfile.ZipFile(os.path.join(self.path,"var/data/mysql/mysql.zip"),'r')
            for name in zfile.namelist():
                (dirname, filename) = os.path.split(name)
                dirname = os.path.join(self.path,"var/data/mysql/")
                self.debug("Decompressing " + filename + " on " + dirname,"app")
                if not os.path.exists(dirname):
                    os.makedirs(dirname)
                zfile.extract(name, dirname)


class QSingleApplication(QApplication):
    def singleStart(self, mainWindow):
        self.mainWindow = mainWindow
        # Socket
        self.m_socket = QLocalSocket()
        self.m_socket.connected.connect(self.connectToExistingApp)
        self.m_socket.error.connect(self.startApplication)
        self.m_socket.connectToServer(self.applicationName(), QIODevice.WriteOnly)
    def connectToExistingApp(self):
        if len(sys.argv)>1 and sys.argv[1] is not None:
            self.m_socket.write(sys.argv[1])
            self.m_socket.bytesWritten.connect(self.quit)
        else:
            QMessageBox.warning(None, self.tr("Already running"), self.tr("The program is already running."))
            # Quit application in 250 ms
            QTimer.singleShot(250, self.quit)
    def startApplication(self):
        self.m_server = QLocalServer()
        if self.m_server.listen(self.applicationName()):
            self.m_server.newConnection.connect(self.getNewConnection)
            self.mainWindow.show()
        else:
            QMessageBox.critical(None, self.tr("Error"), self.tr("Error listening the socket."))
    def getNewConnection(self):
        self.new_socket = self.m_server.nextPendingConnection()
        self.new_socket.readyRead.connect(self.readSocket)
    def readSocket(self):
        f = self.new_socket.readLine()
        self.mainWindow.getArgsFromOtherInstance(str(f))
        self.mainWindow.activateWindow()
        self.mainWindow.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    path = os.path.dirname(os.getcwd())
    win = MainWindow(debug_level=INFO,path = path)
    #win.start_nginx_php()
    win.show()
    sys.exit(app.exec_())
