import psutil
from pyalsi.utils import types


class Ram(object):
    def __init__(self):
        mem_info = psutil.virtual_memory()
        self.percent = mem_info.percent
        self.total = mem_info.total
        self.used = mem_info.used

    def get_total(self):
        return types.Bytes(self.total)

    def get_used(self):
        return types.Bytes(self.used)
