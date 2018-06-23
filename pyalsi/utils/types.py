class Bytes:
    factorial = 0
    factorials = {'bytes': 0,
                  'kilobytes': 1,
                  'megabytes': 2,
                  'gigabytes': 3,
                  'terrabytes': 4}

    mappings = ['b', 'kb', 'mb', 'gb', 'tb']

    # these are only here for autocomplete
    kilobytes = None
    megabytes = None
    gigabytes = None
    terrabytes = None

    def __init__(self, in_int):
        if self.factorial > 0:
            self.real = in_int * 1024 ** self.factorial
        else:
            self.real = in_int

    def __int__(self):
        return self.real

    def __lt__(self, other):
        return self.real < other

    def __getattribute__(self, item):
        if item not in ('real', 'factorials', 'factorial', 'mappings'):
            if item in self.factorials.keys():
                factorial = self.factorials[item]
                if factorial > 0:
                    return int(self.real / 1024 ** int(factorial))
                else:
                    return self.real
        return object.__getattribute__(self, item)

    def to_human(self):
        i = 0
        while True:
            cur = self.real / 1024 ** i
            if cur < 1024:
                return int(cur), self.mappings[i]
            i += 1


class Megabyte(Bytes):
    factorial = 2


class Gigabyte(Bytes):
    factorial = 3


class Terrabyte(Bytes):
    factorial = 4
