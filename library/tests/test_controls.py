__author__ = 'Amy'
from library.TestApp import BaseTestCase
from library.core.controls import *


class TestApp(BaseTestCase):
    def setUp(self):
        super(TestApp, self).setUp()

    def tearDown(self):
        super(TestApp, self).tearDown()

    def test_unzip(self):
        p = PluginControl(self.win)

        plugins = [
            "memcached-1.2.4.zip",
            "mongodb-2.4.5.zip",
            "mysql-5.1.zip",
            "nginx-1.5.12.zip",
            "openssl.zip",
            "phing-2.6.1.zip",
            "php-5.3.8.zip",
            "php-5.5.11.zip",
            "phpunit-4.zip",
            "ssdb-bin.zip",
        ]
        for plugin in plugins:
            path = os.path.abspath(os.path.join(self.win.path,'usr','local',plugin))
            p.unzip_plugin('nginx-1.5.12',path)