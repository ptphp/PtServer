#!/usr/bin/env python
# -*- coding=utf-8 -*-
import sys
import os
import ConfigParser
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtNetwork import *
from PySide.QtWebKit import QWebView
from library.core.utils import loadUi,PtDebugView,debug
from library.core.controls import PortControl,PhpControl,NginxControl
from library.core.baseapp import BaseApp
from library.core.actions import BaseAction
from library.core.buttons import BaseButtons
from library.core.ptprocess import PtProcess

from library.core.ptwebview import PtWebView

import zipfile

ERROR, WARNING, INFO, DEBUG = range(4)

config = ConfigParser.RawConfigParser()
config_filename = "config.cfg"


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
    debug_edt = None
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
        self.webview = QWebView(self)

        self.setCentralWidget(self.webview)
        self.webview.load("http://theme.ptphp.net/theme/cleanzone/")

        #self.debugView = PtDebugView(self)

        self.controls = {
                'nginx' : NginxControl(self),
                'php' : PhpControl(self),
                'port' : PortControl(self),
                }
        #self.set_buttons()
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
