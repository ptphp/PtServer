from PySide.QtCore import *
from utils import debug

class BaseButtons(QObject):
    def set_buttons(self):
        self.nginx_reload_btn.setEnabled(False)
        self.php_restart_btn.setDisabled(True)
        self.nginx_start_btn.clicked.connect(self._on_nginx_start)
        self.nginx_reload_btn.clicked.connect(self._on_nginx_reload)
        self.php_restart_btn.clicked.connect(self._on_php_restart)

        self.check_port_btn.clicked.connect(self._on_check_port)
        self.kill_port_btn.clicked.connect(self._on_kill_port)

    def _on_kill_port(self):
        self.kill_port_btn.setDisabled(True)
        self.controls['port'].action = "kill"
        self.controls['port'].start()

    def _on_check_port(self):
        self.check_port_btn.setDisabled(True)
        self.controls['port'].action = "check"
        self.controls['port'].start()


    def _on_nginx_start(self):
        self.nginx_start_btn.setDisabled(True)
        self.nginx_reload_btn.setDisabled(True)
        self.php_restart_btn.setDisabled(True)
        self.progressBar.show()
        if self.nginx_start_btn.text() == "stop":
            self.controls['nginx'].action = "stop"
            self.stat_timer("nginx_stop",10,1500)
        else:
            self.controls['nginx'].action = "start"
            self.stat_timer("nginx_start",10,1500)
            self._on_php_restart()
        self.controls['nginx'].start()

    def _on_nginx_reload(self):
        self.stat_timer("nginx_reload",10,1500)
        debug( "nginx reload")
        self.stat_timer("nginx",10,1500)
        self.nginx_start_btn.setDisabled(True)
        self.nginx_reload_btn.setDisabled(True)
        self.controls['nginx'].action = "reload"
        self.controls['nginx'].start()

    def _on_php_restart(self):
        self.php_restart_btn.setDisabled(True)
        debug( "php restart")
        self.controls['php'].action = "restart"
        self.controls['php'].start()

    def _on_env_btn_clicked(self):
        res = self.proc.cmd_out("SystemPropertiesAdvanced")
        self.debug("SystemPropertiesAdvanced","App")