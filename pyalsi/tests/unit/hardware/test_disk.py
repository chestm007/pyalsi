from pyalsi.hardware.disks.disk import Disk, DiskGroup
from nose.plugins.attrib import attr

from pyalsi.tests.base_test import BaseTest
from pyalsi.utils.strings import Colors


@attr('small', 'hardware', 'unit', 'disk')
class TestDiskUnit(BaseTest):

    def test_diskgroup(self):

        Colors.colors['c2'] = ''
        group = DiskGroup()
        self.assertIsInstance(group, DiskGroup)
        self.assertIsInstance(group.disks, list)
        for disk in group.disks:
            self.assertIsInstance(disk, Disk)
