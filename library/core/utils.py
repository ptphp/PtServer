from PySide.QtUiTools import QUiLoader
from PySide.QtCore import *
from PySide.QtGui import *
import datetime
import simplejson as json
import zipfile,os,shutil

def rmtree(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)

class UiLoader(QUiLoader):
    def __init__(self, baseinstance):
        QUiLoader.__init__(self, baseinstance)
        self.baseinstance = baseinstance

    def createWidget(self, class_name, parent=None, name=''):
        if parent is None and self.baseinstance:
            return self.baseinstance
        else:
            widget = QUiLoader.createWidget(self, class_name, parent, name)
            if self.baseinstance:
                setattr(self.baseinstance, name, widget)
            return widget

def loadUi(uifile, baseinstance=None):
    loader = UiLoader(baseinstance)
    widget = loader.load(uifile)
    QMetaObject.connectSlotsByName(widget)
    return widget


class PtDebugView(QObject):
    signal = None
    line_num = 0
    parent = None
    def __init__(self,parent):
        self.parent = parent
        self.signal = PtSignal()
        self.signal.type = 1
        self.signal.message.connect(self.logMsg, Qt.QueuedConnection)
        self.edit = parent.debug_edt
        font = QFont()
        font.setFamily("Helvetica")
        font.setFixedPitch(True)
        font.setPointSize(12)
        self.edit.setFont(font)
        self.edit.setReadOnly(True)

    @Slot(str)
    def logMsg(self, text):
        self.line_num = self.line_num +1
        if text[0] == "[" or text[0] == "{":
            m = json.loads(text)
        else:
            m = dict(
                msg = text,
                type = 'sys'
            )
        m['date'] = datetime.datetime.now().strftime('%H:%M:%S')

        for line in m['msg'].split("\n"):
            line = line.strip()
            msg = "{3} [{0}][{1}] {2}".format(m['date'],m['type'],line,str(self.line_num))
            self.edit.appendPlainText(msg)
            print msg
            #self.edit.moveCursor(QTextCursor.End)
            self.edit.verticalScrollBar().setValue(self.edit.verticalScrollBar().maximum())

    def clearLog(self):
        self.edit.clear()

def makeDir(path):
    path = os.path.abspath(path)

    if os.path.isfile(path):
        path = os.path.dirname(path)

    if os.path.isdir(path) == False:
        makeDir(os.path.dirname(path))
        return os.mkdir(path)
    return True
    
def unzip(file,output_dir = None):
    zfile = zipfile.ZipFile(file,'r')
    for name in zfile.namelist():
        (dirname, filename) = os.path.split(name)
        abs_dir_name = os.path.abspath(os.path.join(output_dir,dirname))
        if not os.path.exists(abs_dir_name):
            makeDir(abs_dir_name)
        print "unzip to : "+os.path.join(output_dir,name)
        zfile.extract(name, output_dir)
    zfile.close()


def compress_dir(dir,name,no_zip_res_plugin = []):
    print "compress to :"+name
    print "-"*40
    with zipfile.ZipFile(name, 'w') as izip:
        for root, dirs, files in os.walk(dir):
            for file in files:

                need_com = True
                abs_path =  os.path.abspath(os.path.join(dir,root,file))
                for nn in no_zip_res_plugin:
                    if abs_path.find(os.path.abspath(os.path.join(dir,nn))) >=0:
                        need_com = False
                if need_com:
                    print "compress ==>>",root+"\\"+file
                    izip.write(os.path.join(root, file))
                else:
                    print "filter ==>>",root+"\\"+file
        izip.close()
def debug(msg,type = "sys"):
    res = dict(
        type=type,
        msg = msg
    )
    emit_signal(json.dumps(res))

def emit_signal(msg):
    s = PtSignal()
    if s.type == 1:
        s.emits(msg)
    else:
        print msg

def ptston(cls, *args, **kw):
    """
    @ptston
    class Classname()
    """
    instances = {}
    def _ptston():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _ptston

@ptston
class PtSignal(QObject):
    """
    signal = PtSignal()
    signal.message.connect(self.logMsg, Qt.QueuedConnection)
    signal.emits('msg')
    """
    message = Signal(str)
    type = 0
    def emits(self,msg):
        if msg:
            msg = str(msg)
            self.message.emit(msg)
