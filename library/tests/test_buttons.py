__author__ = 'Amy'
from library.TestApp import BaseTestCase
from library.core.controls import NginxControl,PhpControl

class TestApp(BaseTestCase):
    def setUp(self):
        super(TestApp, self).setUp()

    def tearDown(self):
        super(TestApp, self).tearDown()

    def test_nginx_start(self):
        nginx = NginxControl(self.win)
        nginx._do_stop()
        nginx._do_start()

    def test_nginx_reload(self):
        nginx = NginxControl(self.win)
        nginx._do_reload()

    def test_php_reload(self):
        php = PhpControl(self.win)
        php._do_restart()


