import psutil

from pyalsi.utils.types import Bytes
from pyalsi.utils.strings import colorize_usage, colorize_percent, Colors


class Disk(object):
    class Usage(object):
        def __init__(self, usage):
            self.used = Bytes(usage.used)
            self.total = Bytes(usage.total)
            self.percent = int(usage.percent)

    def __init__(self, disk):
        name = disk.mountpoint.split('/')[-1]
        self.usage = self.Usage(psutil.disk_usage(disk.mountpoint))
        self.name = name.capitalize() if name != "" else "Root"  # Type: str
        self.fstype = disk.fstype

    @property
    def info_string(self):
        used, unit = self.usage.used.to_human()
        total, unit = self.usage.total.to_human()

        return ("{}".format(self.name), " {} ({}) ({})".format(
            colorize_usage(used,
                           total,
                           self.usage.percent, unit.upper()),
            colorize_percent(self.usage.percent, "%"),
            self.fstype, **Colors.colors))


class DiskGroup(object):
    def __init__(self):
        self.disks = [Disk(disk) for disk in psutil.disk_partitions()]
