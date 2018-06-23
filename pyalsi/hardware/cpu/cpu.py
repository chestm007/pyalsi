import cpuinfo


class Cpu(object):
    def __init__(self):
        info = cpuinfo.get_cpu_info()
        self.count = info.get('count')
        self.brand = info.get('brand')

    def to_info_string(self):
        fmt = "{} cores" if self.count > 1 else "{} core"
        return "{} ({})".format(self.brand, fmt.format(self.count))
