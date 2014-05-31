#!/usr/bin/env python
# -*- coding: utf-8 -*-
#http://stackoverflow.com/questions/4629595/using-pysides-qtwebkit-under-windows-with-py2exe
#http://qt-project.org/wiki/Packaging_PySide_applications_on_Windows
from glob import glob
from distutils.core import setup  
import py2exe  
import sys
import os

if len(sys.argv) == 1:
    sys.argv.append("py2exe")
    sys.argv.append("-q")

sys.path.append(os.path.join(os.getcwd(),"Microsoft.VC90.CRT"))
data_files = []
INCLUDES = ["encodings","encodings.*","subprocess","PySide.QtNetwork","PySide.QtXml"]

dll_excludes = ['msvcm90.dll','msvcp90.dll','msvcr90.dll']

options = {
            "py2exe":{
                    "compressed" : 1,
                    "optimize" : 2,
                    "bundle_files" : 1,
                    "includes" : INCLUDES,
                    "excludes" : [],
                    "dll_excludes": dll_excludes
                    }
          }

windows = [
            {
              "script": "App.py",
              "icon_resources": [(0, "var/res/fav.ico")],
            }
          ]
setup(
  name = "PtServer",
  version = "1.0",
  description = "PtServer",
  author = "joseph",
  author_email ="joseph@ptphp.com",
  maintainer = "Joseph",
  maintainer_email = "joseph@ptphp.com",
  license = "BSD Licence",
  url = "http://www.ptphp.com",
  data_files = data_files,
  zipfile = None,
  options = options,
  windows = windows,
)
