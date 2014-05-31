#!/usr/bin/env python
# -*- coding=utf-8 -*-
import os
from PySide.QtCore import *
from PySide.QtGui import *
import sys

class BaseApp(QObject):
    def quit(self):
        sys.exit()
    def trayMenu(self):
        self.minimizeAction = QAction(u"最小化", self,triggered=self.hide)
        #self.maximizeAction = QAction(u"最大化",self,triggered=self.showMaximized)
        self.restoreAction = QAction(u"还原", self,triggered=self.showNormal)
        self.quitAction = QAction(u"直接退出", self,triggered=self.quit)
        self.trayIconMenu = QMenu(self)
        self.trayIconMenu.addAction(self.minimizeAction)
        #self.trayIconMenu.addAction(self.maximizeAction)
        self.trayIconMenu.addAction(self.restoreAction)
        self.trayIconMenu.addSeparator() #间隔线
        self.trayIconMenu.addAction(self.quitAction)
        self.trayIcon.setContextMenu(self.trayIconMenu) #右击托盘
    def addTray(self):
        self.isWindow()
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(self.icon)
        self.trayIcon.show()
        self.trayIcon.activated.connect(self.trayClick)
        self.trayIcon.setToolTip(u"PtServer 开发工具\nv 1.0 ")
        self.trayMenu()

    def set_status_bar(self):
        statusBar = self.statusBar = QStatusBar(self)
        self.progressBar = QProgressBar()
        self.progressBar.valueChanged.connect(self._progress_bar_changed)
        statusBar.addWidget(self.progressBar)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(0)
        self.setStatusBar(statusBar)
        self.progressBar.hide()
    def _progress_bar_changed(self,value):
        if int(value) == 100:
            for key in self.timer_list:
                self.timer_list[key]['thread'].stop()

    @Slot(str)
    def process_setValue(self, value):
        self.progressBar.setValue(int(value))

    @Slot(str)
    def process_hide(self, ok):
        self.progressBar.hide()
        self.progressBar.setValue(0)
        for key in self.timer_list:
            self.timer_list[key]['thread'].stop()
    @Slot()
    def process_setValue_by_timer(self):
        for key in self.timer_list:
            self.timer_list[key]['num'] = self.timer_list[key]['num'] +1
            v = int((self.timer_list[key]['num']*self.timer_list[key]['unit']*100)/self.timer_list[key]['total'])

        self.progressBar.setValue(v)

    def stat_timer(self,name,unit,total):
        self.timer_list[name] = dict(
            thread =QTimer(),
            num =0,
            total =total,
            unit =unit,
        )
        self.timer_list[name]['thread'].timeout.connect(self.process_setValue_by_timer)
        self.timer_list[name]['thread'].start(unit)

    def showMessage(self,title,content,icon=QSystemTrayIcon.Information):
        self.trayIcon.showMessage(title,content,icon)

    def trayClick(self,reason):
        if reason==QSystemTrayIcon.DoubleClick: #双击
            self.showNormal()
        elif reason==QSystemTrayIcon.MiddleClick: #中击
            self.showMessage(u"提示信息",u"中击")
        else:
            pass


    def status_bar_show(self,msg):
        self.statusBar().showMessage(msg)

    def start_nginx_php(self):
        import threading
        t1 = threading.Thread(target=self._on_nginx_start)
        t1.start()
        t1.join()