import psutil
from pyalsi.utils import types


class Ram(object):
    def __init__(self):
        self.percent = None
        self.total = None
        self.used = None
#        svmem(total=16721362944, available=11914027008, percent=28.7, used=4403113984, free=8754683904, active=4450758656,
#              inactive=3089240064, buffers=216772608, cached=3346792448, shared=721403904, slab=255266816)
        self.__dict__.update(psutil.virtual_memory()._asdict())

    def get_total(self):
        return types.Bytes(self.total)

    def get_used(self):
        return types.Bytes(self.used)
