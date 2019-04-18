import os


class VgaCard(object):
    pass


class Vga(object):
    @property
    def devices(self):
        out = os.popen("lspci | grep VGA").read().splitlines()
        cards = {}
        for line in out:
            line = line.split(":")[-1]
            if line in cards.keys():
                count = cards[line]
                cards.pop(line)
                cards[line] = count + 1
            else:
                cards[line] = 1
        output = []
        for k, v in cards.items():
            output.append("{}{}".format(k, ("(x{})".format(v)) if v > 1 else ""))
        return output
