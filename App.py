#!/usr/bin/env python
# -*- coding=utf-8 -*-
import sys,os
from library.AppCore import *



if __name__ == "__main__":
    app = QSingleApplication(sys.argv)
    app.setApplicationName("PtProject V 1.0")
    win = MainWindow(debug_level=INFO,path = os.getcwd())
    app.singleStart(win)
    sys.exit(app.exec_())