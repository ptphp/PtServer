import os
from PySide.QtCore import QObject,QThread
from .ptprocess import PtProcess
from .utils import PtSignal,makeDir,unzip
from PySide.QtCore import *
import zipfile
cmd_list_port = 'netstat -nao | findstr ":%d.*LISTENING"'
cmd_kill_port = "taskkill /PID %d /F"
cmd_chek_running = 'tasklist /FO csv /FI "IMAGENAME eq %s"'


class BaseControl(QThread):
    parent = None
    proc = None
    action = None
    process_value_signal = Signal(str)
    process_hide = Signal(str)
    def __init__(self, parent = None):
        QThread.__init__(self, parent)
        self.parent = parent
        self.path = self.parent.path
        self.proc = self.parent.proc
        self.process_value_signal.connect(self.parent.process_setValue, Qt.QueuedConnection)
        self.process_hide.connect(self.parent.process_hide, Qt.QueuedConnection)
    def run(self):
        print "run in base test"

    def terminate(self):
        super(BaseControl, self).terminate()
        for p in self.proc.list:
            if p.waitForFinished(1) == False:
                print "kill process"
                p.kill()
                p.waitForFinished(1)


class NginxControl(BaseControl):
    processName = "nginx.exe"
    def __init__(self,parent = None):
        super(NginxControl, self).__init__(parent)

    def _do_start(self):
        self.parent.nginx_start_btn.setText("starting...")

        path = self.parent.config().get("nginx","path")
        path_work = self.parent.config().get("nginx","path_work")

        dirs = [
            'temp/client_body_temp',
            'temp/client_body_temp',
            'logs'
        ]

        path_conf = self.parent.config().get("nginx","path_conf")

        nginx_exe_path = os.path.abspath(os.path.join(self.path,path,self.processName))
        root_path = os.path.abspath(os.path.join(self.path,path_work))
        conf_path = os.path.abspath(os.path.join(self.path,path_conf))

        for dir in dirs:
            t_dir = os.path.join(root_path,dir)
            if os.path.isdir(t_dir) == False:
                makeDir(t_dir)

        cmd = "{0} -p {1} -c {2}".format(nginx_exe_path,root_path,conf_path)

        self.parent.debug(cmd,"nginx")
        res = self.proc.cmd(cmd,"nginx")
        self.process_hide.emit("ok")
        if res['error'] == 1:
            if "Process operation timed out" not in res['result']:
                self.parent.debug("nginx start failed:"+res['result'],"nginx")
                self.parent.nginx_start_btn.setText("start")
                self.parent.nginx_reload_btn.setDisabled(True)
                self.parent.php_restart_btn.setDisabled(True)
            else:
                #todo cheeck nginx pid
                self.parent.nginx_start_btn.setText("stop")
                self.parent.debug("nginx started","nginx")
                self.parent.nginx_reload_btn.setDisabled(False)
                self.parent.php_restart_btn.setDisabled(False)

            self.parent.nginx_start_btn.setDisabled(False)
        else:
            self.parent.nginx_start_btn.setDisabled(False)
            print res['result']
            if "emerg" in res['result']:
                self.parent.nginx_start_btn.setText("start")
                self.parent.debug("nginx start failed","nginx")
                self.parent.debug(res['result'],"nginx")
                self.parent.nginx_reload_btn.setDisabled(True)
                self.parent.php_restart_btn.setDisabled(True)
            else:
                self.parent.nginx_start_btn.setText("stop")
                self.parent.debug("nginx started","nginx")
                self.parent.nginx_reload_btn.setDisabled(False)
                self.parent.php_restart_btn.setDisabled(False)

    def _do_reload(self):

        self._do_stop()
        self._do_start()
        return
        self.parent.nginx_start_btn.setText("Reloading")

        path = self.parent.config().get("nginx","path")
        path_work = self.parent.config().get("nginx","path_work")
        path_conf = self.parent.config().get("nginx","path_conf")

        nginx_exe_path = os.path.abspath(os.path.join(self.path,path,self.processName))
        root_path = os.path.abspath(os.path.join(self.path,path_work))
        conf_path = os.path.abspath(os.path.join(self.path,path_conf))



        cmd="{0} -s reload -p {1} -c {2}".format(nginx_exe_path,root_path,conf_path)
        self.parent.debug(cmd,"nginx")
        res = self.proc.cmd(cmd,"nginx")




        self.parent.nginx_reload_btn.setDisabled(False)
        self.parent.nginx_start_btn.setDisabled(False)
        self.parent.nginx_reload_btn.setText("Reload Nginx")
        self.parent.debug("nginx reloaded","nginx")

    def _do_stop(self):
        self.parent.nginx_start_btn.setText("stopping ...")
        cmd = 'taskkill /F /IM '+self.processName
        self.parent.debug(cmd,"nginx")
        self.process_hide.emit("ok")
        res = self.proc.cmd(cmd,"nginx",1500)
        self.parent.nginx_start_btn.setDisabled(False)
        self.parent.nginx_reload_btn.setDisabled(True)
        self.parent.nginx_start_btn.setText("start")

        self.parent.debug(res['result'],"nginx")
        self.parent.debug("nginx stoped","nginx")

    def run(self):
        if self.action == "stop":
            self._do_stop()
        elif self.action == "reload":
            self._do_reload()
        elif self.action == "start":
            self._do_start()
        else:
            pass
        self.action == ""

class PortControl(BaseControl):
    def __init__(self,parent = None):
        super(PortControl, self).__init__(parent)

    def _do_check(self):
        ports = {}
        ports['php_port'] = self.parent.config().get("php","port")
        ports['http_port'] = self.parent.config().get("nginx","http_port")
        ports['https_port'] = self.parent.config().get("nginx","https_port")

        for key in ports:
            port = ports[key]
            pid = self.proc.get_pid_by_port(port)
            name = None
            if pid:
                info = self.proc.get_process_info_by_pid(pid)
                name = info['Image_name']
            #print key,pid,name
            self.parent.debug("{0} => port:{1} name:{2} pid:{3}".format(key,port,name,pid),"check ports")
        self.parent.check_port_btn.setDisabled(False)

    def _do_kill(self):
        ports = {}
        ports['php_port'] = self.parent.config().get("php","port")
        ports['http_port'] = self.parent.config().get("nginx","http_port")
        ports['https_port'] = self.parent.config().get("nginx","https_port")

        for key in ports:
            pid = self.proc.get_pid_by_port(ports[key])
            r = None
            if pid:
                res = self.proc.kill_process_by_im(pid)
                r = str(res['result'])
            self.parent.debug("pid: {0} => {1}".format(pid,r),"kill ports")
        self.parent.kill_port_btn.setDisabled(False)
    def run(self):
        if self.action == "check":
            self._do_check()
        elif self.action == "kill":
            self._do_kill()
        else:
            pass
        self.action == ""

class PhpControl(BaseControl):
    processName = "php-cgi.exe"
    def __init__(self,parent = None):
        super(PhpControl, self).__init__(parent)

    def _do_restart(self):

        cmd = 'taskkill /F /IM '+self.processName
        res = self.proc.cmd(cmd,"nginx",1500)
        print res
        port = self.parent.config().get("php","port")
        ip = self.parent.config().get("php","ip")
        path = self.parent.config().get("php","path")
        php_ini = self.parent.config().get("php","php_ini")


        path_php_exe = os.path.abspath(os.path.join(self.path,path,self.processName))

        host = "{0}:{1}".format(ip,port)
        path_php_ini = os.path.abspath(os.path.join(self.path,php_ini))
        cmd = "{0} -b {1} -c {2}".format(path_php_exe,host,path_php_ini)

        self.parent.debug(cmd,"php")
        res = self.proc.cmd(cmd,"php",2000,{'PHP_FCGI_MAX_REQUESTS':'1000'})
        print res
        self.parent.php_restart_btn.setDisabled(False)

    def run(self):
        if self.action == "restart":
            self._do_restart()
        else:
            pass
        self.action == ""


class PluginControl(BaseControl):
    def __init__(self,parent = None):
        super(PluginControl, self).__init__(parent)

    def unzip_plugin(self,name,zip_path):
        path_local = os.path.abspath(os.path.join(self.parent.path_root,'usr','local'))

        #if os.path.isdir(path_local):
        #    return

        zfile = zipfile.ZipFile(zip_path,'r')
        for file_name in zfile.namelist():
            file_path = os.path.join(path_local,file_name)
            print file_path
            dirname= os.path.dirname(file_path)
            if not os.path.exists(dirname):
                makeDir(dirname)
            zfile.extract(file_name, path_local)
        return

    def run(self):
        print 1