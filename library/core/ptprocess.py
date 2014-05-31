import subprocess
from PySide.QtCore import *
from .utils import debug,PtSignal

cmd_list_port = 'netstat -nao | findstr ":%d.*LISTENING"'
cmd_kill_port = "taskkill /PID %d /F"
cmd_chek_running = 'tasklist /FO csv /FI "IMAGENAME eq %s"'

class PtProcess(QObject):
    list = []
    type = "sys"
    def _on_output(self):
        res = str(self.proc_cur.readAll())
        debug(res.strip(),self.type)
    def _do_start(self,proc,cmd):
        proc.setProcessChannelMode(QProcess.MergedChannels)
        proc.start(cmd,QIODevice.ReadOnly)
        #proc.readyReadStandardOutput.connect(self._on_output)
    def _get_res(self,proc,timeout):
        if proc.waitForFinished(timeout):
            res = {
                "error":0,
                "result":str(proc.readAll()).strip()
            }
        else:
            res = {
                "error":1,
                "result":str(proc.errorString()).strip()
            }
        return res
    def cmd(self,cmd,type="sys",timeout = 2000,env_dict = {}):
        debug(cmd)
        self.type = type
        self.proc_cur = proc = QProcess()
        env = QProcessEnvironment.systemEnvironment()
        for key in env_dict:
            env.insert(key, env_dict[key])
            #env.insert("PATH", env.value("Path") + ";C:\\Bin")
        proc.setProcessEnvironment(env)
        self.list.append(proc)
        self._do_start(proc,cmd)
        return self._get_res(proc,timeout)
    def cmd_out(self,cmd):
        debug(cmd)
        proc = QProcess()
        self.list.append(proc)
        proc.startDetached(cmd)

    def kill_process_by_im(self,name):
        cmd = "taskkill /f /im "+name
        res = self.cmd(cmd)
        return res

    def kill_process_by_im(self,pid):
        cmd = "taskkill /f /pid "+str(pid)
        res = self.cmd(cmd)
        return res
    def get_pid_by_port(self,port):
        cmd = "netstat -aon -p TCP"
        res = self.cmd(cmd)
        res =  res['result']
        pid = None
        for row in str(res).split("\r\n"):
            row1 = []
            for i in row.split(" "):
                if i :
                    row1.append(i)
            if row1 and row1[0] == "TCP" and row1[3] == "LISTENING" and row1[1].split(":")[1] == str(port):
                pid = row1[4]
        return pid
    #tasklist /fi "imagename eq imageName"
    def get_process_info_by_pid(self,pid):
        pid = str(pid)
        cmd = 'tasklist /fi "pid eq '+pid+'"'
        res = self.cmd(cmd)
        res = res['result']
        info = {}
        for row in str(res).split("\r\n"):
            row1 = []
            for i in row.split(" "):
                if i :
                    row1.append(i)

            if row1:
                if row1[1] == pid:
                    info = dict(
                                Image_name = row1[0],
                                PID = row1[1],
                                Session_name = row1[2],
                                Session = row1[3],
                                Mem = row1[4],
                                Usage= row1[5],
                                )
        return info

    def sub_cmd(self,cmd,shell=True):
        subprocess.call(cmd, shell=shell,close_fds=True)