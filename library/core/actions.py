import os,webbrowser
from PySide.QtCore import *
from PySide.QtGui import *
from .utils import loadUi,debug

bin_path = "usr/bin"
class BaseAction(QObject):
    def set_actions(self):
        self.actionHosts.triggered.connect(self._on_act_hosts_triggered)
        self.actionPutty.triggered.connect(self._on_act_putty_triggered)
        self.actionWinscp.triggered.connect(self._on_act_winscp_triggered)
        self.actionCertmgr.triggered.connect(self._on_act_certmgr_triggered)

        self.actionError_log.triggered.connect(self._on_act_nginx_error_triggered)
        self.actionAccess_log.triggered.connect(self._on_act_nginx_access_triggered)

        self.actionNginx_conf.triggered.connect(self._on_act_nginx_conf_triggered)
        self.actionSites_conf.triggered.connect(self._on_act_sites_conf_triggered)
        self.actionPtserver.triggered.connect(self._on_act_ptserver_conf_triggered)
        self.actionPhpIni.triggered.connect(self._on_act_phpini_conf_triggered)

        self.actionLocalhost.triggered.connect(self._on_act_localhost_triggered)
        self.actionPyside.triggered.connect(self._on_act_pyside_triggered)

        self.actionPtServer.triggered.connect(self._on_act_ptserver_triggered)
        self.actionWebroot.triggered.connect(self._on_act_webroot_triggered)

        self.actionEnv.triggered.connect(self._on_act_evn_triggered)

        self.ptserver_config_win = env_win = QMdiSubWindow()
        loadUi(self.path +"/var/res/ui/config.ui",self.ptserver_config_win)
        self.ptserver_config_win.saveConfigBtn.clicked.connect(self._on_save_config_btn_clicked)

        self.env_win = QMdiSubWindow()
        loadUi(self.path +"/var/res/ui/env.ui",self.env_win)

        self.env_win.envBtn.clicked.connect(self._on_env_btn_clicked)
        self.env_win.convertBtn.clicked.connect(self._on_convert_btn_clicked)



        self.mem_start_act.triggered.connect(self._on_mem_start_act)
        self.mem_stop_act.triggered.connect(self._on_mem_stop_act)
        self.mem_install_act.triggered.connect(self._on_mem_install_act)

        self.mysql_start_act.triggered.connect(self._on_mysql_start_act)
        self.mysql_stop_act.triggered.connect(self._on_mysql_stop_act)
        self.mysql_install_act.triggered.connect(self._on_mysql_install_act)

        self.mongodb_start_act.triggered.connect(self._on_mongodb_start_act)
        self.mongodb_stop_act.triggered.connect(self._on_mongodb_stop_act)
        self.mongodb_install_act.triggered.connect(self._on_mongodb_install_act)


    def _on_mem_start_act(self):
        path = os.path.join(self.path,'usr/local/memcached/memcached.exe')
        cmd = path + " -d start"
        res = self.proc.cmd(cmd)
        self.debug(res['result'])

    def _on_mem_stop_act(self):
        path = os.path.join(self.path,'usr/local/memcached/memcached.exe')
        cmd = path + " -d stop"
        res = self.proc.cmd(cmd)
        self.debug(res['result'])
    def _on_mem_install_act(self):
        path = os.path.join(self.path,'usr/local/memcached/memcached.exe')
        cmd = path + " -d install"
        res = self.proc.cmd(cmd)
        self.debug(res['result'])

    def _on_mysql_start_act(self):
        res = self.proc.cmd("net start MySQL")
        self.debug(res['result'])


    def _on_mysql_stop_act(self):
        res = self.proc.cmd("net stop MySQL")
        self.debug(res['result'])

    def _on_mysql_install_act(self):
        path = os.path.join(self.path,r'usr\local\mysql\bin\mysqld')
        path_ini = os.path.join(self.path,r'usr\local\mysql\my.ini')
        cmd = path + " --install MySQL --defaults-file="+path_ini
        self.debug(cmd)
        res = self.proc.cmd(cmd)
        self.debug(res['result'])

    def _on_mongodb_install_act(self):
        data_path = os.path.join(self.path,"var\\data\\mongodb\\")
        log_path = os.path.join(self.path,"var\\logs\\mongodb\\mongodb.log")
        path = os.path.join(self.path,'usr/local/mongodb/mongod.exe')
        cmd =  "{0} --dbpath={1} --logpath={2} --install".format(path,data_path,log_path)
        res = self.proc.cmd(cmd)
        self.debug(res['result'])

    def _on_mongodb_start_act(self):
        res = self.proc.cmd("net start MongoDB")
        self.debug(res['result'])

    def _on_mongodb_stop_act(self):
        res = self.proc.cmd("net stop MongoDB")
        self.debug(res['result'])


    def _on_save_config_btn_clicked(self):
        debug("save config btn clicked")
        c = self.ptserver_config_win.ConfigPTedt.toPlainText()
        conf_path = os.path.relpath(os.path.join(self.path,"config.cfg"))
        f = open(conf_path,"w")
        f.write(c)
        f.close()


    def _on_act_ptserver_conf_triggered(self):
        self.ptserver_config_win.show()
        debug("ptsever config trigger")
        conf_path = os.path.relpath(os.path.join(self.path,"config.cfg"))
        f = open(conf_path)
        c = f.read()
        self.ptserver_config_win.ConfigPTedt.setPlainText(c)
        f.close()

    def _on_act_evn_triggered(self):
        env_win = self.env_win
        debug("env trigger")
        path =  os.environ.get("PATH").split(";")
        for p in path:
            #debug(p)
            env_win.envEdt.insertPlainText(p+"\n")
        env_win.envEdt.moveCursor(QTextCursor.End)
        env_win.show()
    def _on_convert_btn_clicked(self):
        content = self.env_win.envEdt.toPlainText().strip()
        if "\n" in content:
            content = content.replace("\n",";")
        else:
            content = content.replace(";","\n")
        self.env_win.envEdt.setPlainText(content+"\n")

    def _on_act_ptserver_triggered(self):
        self.proc.cmd_out("explorer.exe " +self.path)

    def _on_act_webroot_triggered(self):
        self.proc.cmd_out("explorer.exe " +os.path.relpath(os.path.join(self.path,"var/www")))

    def _on_act_localhost_triggered(self):
        webbrowser.open("http://127.0.0.1")

    def _on_act_pyside_triggered(self):
        webbrowser.open("http://pyside.github.io/docs/pyside/")

    def _on_act_certmgr_triggered(self):
        self.proc.sub_cmd(self.get_bin_path("certmgr"),)

    def _on_act_hosts_triggered(self):
        self.proc.cmd_out(self.get_bin_path("hosts"))

    def _on_act_putty_triggered(self):
        self.proc.cmd_out(self.get_bin_path("putty"))

    def _on_act_winscp_triggered(self):
        self.proc.cmd_out(self.get_bin_path("winscp"))

    def vi_exe_path(self):
        return self.get_bin_path("vi.exe")
    def get_bin_path(self,name):
        path =  os.path.abspath(os.path.join(self.path,bin_path,name))
        #self.debug(path)
        return path
        
    def _on_act_nginx_error_triggered(self):
        self.nginx_error_log_path = os.path.abspath(os.path.join(self.path,self.config().get("nginx","error_log")))
        self.proc.cmd_out(self.vi_exe_path() + " "+self.nginx_error_log_path)

    def _on_act_nginx_access_triggered(self):
        self.nginx_access_log_path = os.path.abspath(os.path.join(self.path,self.config().get("nginx","access_log")))
        self.proc.cmd_out(self.vi_exe_path() + " "+self.nginx_access_log_path)


    def _on_act_nginx_conf_triggered(self):
        self.nginx_path_conf_path = os.path.abspath(os.path.join(self.path,self.config().get("nginx","path_conf")))
        self.proc.cmd_out(self.vi_exe_path() + " "+self.nginx_path_conf_path)

    def _on_act_sites_conf_triggered(self):
        self.nginx_path_conf_sites_path = os.path.abspath(os.path.join(self.path,self.config().get("nginx","path_conf_sites")))
        self.proc.cmd_out(self.vi_exe_path() + " "+self.nginx_path_conf_sites_path)

    def _on_act_phpini_conf_triggered(self):
        self.php_ini_path = os.path.abspath(os.path.join(self.path,self.config().get("php","php_ini")))
        self.proc.cmd_out(self.vi_exe_path() + " "+self.php_ini_path)

