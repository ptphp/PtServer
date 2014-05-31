__author__ = 'Amy'

import os,zipfile
from .utils import makeDir

from library.core.utils import compress_dir,unzip
def get_zip_version(name,dir):
    path = os.path.join(dir,name)
    print "get version :" + path
    versions = []
    for file in os.listdir(dir):
        if name in file and ".zip" in file:
            versions.append(int(file.replace(name+"-","").replace(".zip","")))
    if versions:
        v = sorted(versions,reverse = True)[0]
    else:
        v = 0

    return v+1

def zip_local_all(dir):
    dir_local = os.path.join(dir,"local")
    for plugin_name in os.listdir(dir_local):
        zip_local(dir,plugin_name)

no_zip_res = {
    'mongodb-2.4.5':[
        "data/",
        "logs/",
    ],
    "mysql-5.1":[
        'data/',
    ],
    "openssl-1.9.8":[
        'certs/',
    ]
}


def zip_local(dir,name):
    no_zip_res_plugin = []
    if name in no_zip_res.keys():
        print name
        no_zip_res_plugin = no_zip_res[name]
    dir_local = os.path.join(dir,"local")
    dir_local_zip = os.path.join(dir,"local_zip")
    version = get_zip_version(name,dir_local_zip)
    plugin_name_zip_file_name = name+"-"+str(version)+".zip"
    print plugin_name_zip_file_name
    plugin_name_zip_file_name_path = os.path.join(dir_local_zip,plugin_name_zip_file_name)
    path_root = os.path.join(dir_local,name)

    if False == os.path.isdir(path_root):
        print "no exists : " + path_root
        return

    os.chdir(path_root)
    compress_dir("./",plugin_name_zip_file_name_path,no_zip_res_plugin)

def unzip_local(dir,zip_name):
    (dirname,filename) = os.path.split(zip_name)
    print (dirname,filename)
    dir = os.path.join(dir,filename.replace(".zip",""))
    print dir
    if os.path.exists(dir):
        print "exists : "+ dir
        return
    if os.path.exists(zip_name) == True:
        unzip(zip_name,dir)
    else:
        print "no exsits : "+zip_name

