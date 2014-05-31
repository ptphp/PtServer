from AppCore import  *
import unittest
from PySide.QtGui import *
_instance = None
print  __file__
class BaseTestCase(unittest.TestCase):
    def setUp(self):
        super(BaseTestCase, self).setUp()
        global _instance
        if _instance is None:
            _instance = QApplication([])
        self.app = _instance
        path = os.path.dirname(os.path.dirname(__file__))
        self.win = MainWindow(debug_level=INFO,path = path ,test = True)
    def tearDown(self):
        super(BaseTestCase, self).tearDown()
        self.win.close()
        del self.app

class TestApp(BaseTestCase):
    def setUp(self):
        super(TestApp, self).setUp()

    def tearDown(self):
        super(TestApp, self).tearDown()
    def test_win(self):
        self.win.show()


if __name__ == '__main__':
    unittest.main()