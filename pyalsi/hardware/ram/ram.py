import psutil
from pyalsi.utils import types


class Ram(object):
    def __init__(self):
        mem_info = psutil.virtual_memory()
        self.percent = mem_info.percent
        self.total = types.Bytes(mem_info.total)
        self.used = types.Bytes(mem_info.used)
