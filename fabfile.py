#!/usr/bin/env python
# -*- coding=utf-8 -*-

from fabric.api import run,put,cd,env,local
import shutil,os
import py_compile

__author__ = 'Joseph'

UpxEXE = os.path.join(os.getcwd(),"usr/bin/upx.exe")
SevenZipEXE = os.path.join(os.getcwd(),"usr/bin/7z.exe")
dist_dir = os.path.join(os.getcwd(),"dist")
pro_dir = os.getcwd()

setup_name = "PtServer-1.0.2"
setup_script = "setup_script.iss"
DefaultDirName = "C:\\PtServer"

dirs = [
        'imageformats',
        'Microsoft.VC90.CRT',
        'var/res',
        'var/www',
        'etc/nginx_win',
        'etc/php53_win',
        'usr/bin',
        'usr/local/php/53',
        'usr/local/mysql',
        'usr/local/nginx',
        'usr/local/openssl',
        'usr/local/memcached',
        'usr/local/mongodb',
        'usr/local/ssdb-bin',
    ]

files = [
    'config.cfg',
	'var/data/mysql/mysql.zip',
]
files_setup = [
    "App.exe",
    "w9xpopen.exe",	
]

def makeDir(path):
    path = os.path.abspath(path)

    if os.path.isfile(path):
        path = os.path.dirname(path)

    if os.path.isdir(path) == False:
        makeDir(os.path.dirname(path))
        return os.mkdir(path)
    return True


def unzip(zip_file,out_dir):
    local(SevenZipEXE+' -aoa x "'+zip_file+'" -o "'+out_dir+'"')


def upx(dir,files = "*.*"):
    print "upx ... "+dir
    os.chdir(dir)
    local(UpxEXE+" --best "+files)

def copydir(dir):
    from_dir = os.path.join(pro_dir,dir)
    to_dir = os.path.join(dist_dir,dir)
    print "copy dir from :"+ from_dir + " to :" +to_dir
    shutil.copytree(from_dir,to_dir)

def copyfile(file):
    from_dir = os.path.join(pro_dir,file)
    to_dir = os.path.join(dist_dir,file)
    if os.path.isdir(os.path.dirname(to_dir)) == False:
        makeDir(os.path.dirname(to_dir))

    print "copy file from :"+ from_dir + " to :" +to_dir

    shutil.copy(from_dir,to_dir)

def build_pyc():
    py_compile.compile('library/AppCore.py')
    py_compile.compile('library/__init__.py')
    py_compile.compile('App.py')

def pre_build():
    if os.path.isdir(os.path.join(pro_dir,"build")):
        print "delete ./build"
        shutil.rmtree(os.path.join(pro_dir,"build"))
    if os.path.isdir(os.path.join(pro_dir,"dist")):
        print "delete ./dist"
        shutil.rmtree(os.path.join(pro_dir,"dist"))


def compress():
    os.chdir(dist_dir)
    output_zip = os.path.join(pro_dir,"Output/"+setup_name+".zip")
    if os.path.isfile(output_zip):
        os.remove(output_zip)
    if os.path.isdir(os.path.dirname(output_zip)) == False:
        os.mkdir(os.path.dirname(output_zip))
    print "compress " +dist_dir+" to " + output_zip
    local(SevenZipEXE + ' a -tzip -mx9 "'+output_zip+'" -r')

def package_to_setup():
    #http://www.jrsoftware.org/ishelp/index.php?topic=compilercmdline
    os.chdir(pro_dir)
    path = os.path.join(pro_dir,"library/version_tmplate")
    f = open(path,'r')
    template = f.read()
    Files = ""
    for file in files+files_setup:
        file_path = dist_dir +"\\" +file
        Files += 'Source: "'+file_path+'"; DestDir: "{app}"; Flags: ignoreversion'+ "\n"
    for dir in dirs:
        dir = dir.replace("/","\\")
        file_path = dist_dir +"\\" +dir
        Files += 'Source: "'+file_path+'\*"; DestDir: "{app}\\'+dir+'"; Flags: ignoreversion recursesubdirs createallsubdirs'+ "\n"
    iss = template.replace("#Files#",Files)

    iss = iss.replace("#setup_name#",setup_name)
    iss = iss.replace("#DefaultDirName#",DefaultDirName)

    f = open("setup_script.iss","w")
    f.write(iss)
    f.close()
    if os.path.isfile(pro_dir+"/Output/"+setup_name):
        os.remove(pro_dir+"/Output/"+setup_name)

    local("iscc "+setup_script)
    os.remove(setup_script)

def build_copy_exe_to_pro_dir():
    shutil.copy(dist_dir+"/App.exe",pro_dir+"/App.exe")
    os.chdir(pro_dir)
    local(pro_dir+"/App.exe")


def build_exe():
    pre_build()
    print "build ptserver"
    local("python build_run.py py2exe")
    upx(dist_dir,"*.exe")
    build_copy_exe_to_pro_dir()


def test_build_copy_files():
    os.chdir(pro_dir)
    if os.path.isdir("dist"):
        shutil.rmtree("dist")
    os.mkdir("dist")
    copyfile("App.exe")
    build_copy_files()
    os.chdir(dist_dir)
    local(dist_dir+"/App.exe")


def build_copy_files():
    for file in files:
        copyfile(file)
    for dir in dirs:
        copydir(dir)
    path = os.path.join(dist_dir,"usr/bin/winscp.ini")
    if os.path.isfile(path):
        os.remove(path)

    dirs1 = [
        'etc/nginx_win/certs_tmp',
        'etc/nginx_win/ssl_tmp',
        'etc/nginx_win/sites_tmp',
    ]
    for dir in dirs1:
        path = os.path.join(dist_dir,"etc/nginx_win/sites_tmp")
        if os.path.isdir(path):
            shutil.rmtree(path)

def build():
    build_exe()
    build_copy_files()
    handle_sites_conf()
    gen_htpasswd()
    compress()
    package_to_setup()
    gitpush()


def gitpush():
    local("git add --all")
    local("git commit -m 'deploy'")
    local("git push origin master")

def handle_sites_conf():
    path = os.path.join(dist_dir,"etc/nginx_win/sites.conf")
    f = open(path,"w")
    f.write("include sites-available/*.conf;")
    f.close()

def gen_htpasswd():
    #htpasswd passwordfile username
    import subprocess
    path = os.path.join(dist_dir,"etc/nginx_win/htpasswd")
    os.remove(path)
    subprocess.call("./usr/bin/htpasswd -c "+path+" ptserver")