from nose.plugins.attrib import attr

from pyalsi.tests.base_test import BaseTest
from pyalsi.utils.types import Bytes, Gigabyte, Megabyte


@attr('small', 'hardware', 'unit', 'disk')
class TestUtilsUnit(BaseTest):

    def test_types(self):
        megabyte = Bytes(1048576)
        gigabyte = Bytes(1073741824)
        self.assertEqual(Megabyte(1024).gigabytes, 1)
        self.assertEqual(Megabyte(1).bytes, 1048576)
        self.assertEqual(megabyte.megabytes, 1)
        self.assertEqual(gigabyte.gigabytes, 1)
        self.assertEqual(Gigabyte(1).bytes, 1073741824)
        self.assertEqual(Gigabyte(1).megabytes, 1024)
