from unittest import TestCase
from library.core.dist_zip import *
from library.core.utils import makeDir,rmtree,compress_dir

__author__ = 'Amy'


class TestDistZip(TestCase):
    def setUp(self):
        pass
    def test_check_zip_version(self):
        dir = "tmp"
        rmtree(dir)
        makeDir(dir)
        name = "php-1.1.1"
        self.assertEqual(1,get_zip_version(name,dir))
        open("tmp/php-1.1.1-1.zip","w")
        open("tmp/php-1.1.1-2.zip","w")
        open("tmp/php-1.1.1-3.zip","w")
        self.assertEqual(4,get_zip_version(name,dir))
        rmtree(dir)
    def test_zip_local_all(self):
        dir = "D:\\usr"
        zip_local_all(dir)

    def test_zip_local(self):
        dir = "D:\\usr"
        name = "mysql-5.1"
        zip_local(dir,name)

    def test_unzip_local(self):
        zip_name = "D:\\usr\\local_zip\\mysql-5.1-1.zip"
        dir = "D:\\usr\\local"
        unzip_local(dir,zip_name)
