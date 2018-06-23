from pyalsi.colors import bold, normal


class Colors(object):
    colors = {"low": bold["green"],
              "med": bold["yellow"],
              "high": bold["red"],
              "red": normal["red"]
              }

    def __init__(self, *_, primary='white', secondary='dgrey'):
        self.colors.update({'c1': primary, 'c2': secondary})

    def set_primary(self, v):
        self.colors['c1'] = v

    def set_secondary(self, v):
        self.colors['c2'] = v


def colorize(heading, value):
    """
    wrapper to colorize info lines
    :param heading: line heading (eg. "OS")
    :param value: line value (eg. "Arch Linux")
    :return: string (eg. "{c2}OS: {c1}Arch Linux")
    """
    return "{c2} %(heading)s: {c1} %(value)s" % {'heading': heading, 'value': value}


def colorize_usage(use, total, percent, unit):
    """
    colorizes the passed string based on the percentage passed in
    :param use: output variable
    :param total: output variable
    :param percent: used to calculate the appropriate color
    :param unit: essentially a suffix to use and total (eg. "G | M")
    :return: string (eg. "{low}43G{c1} / 87G")
    """
    return '%(level)s%(use)s%(unit)s{c1} / %(total)s%(unit)s' % {'level': get_warning_level(percent),
                                                                 'use': use,
                                                                 'unit': unit,
                                                                 'total': total}


def colorize_percent(value, suffix=""):
    """
    as above but only takes one output variable
    :param value: the output variable
    :param suffix: string to put after value (eg. "%)
    :return: string (eg. "{low}15%{c1}")
    """
    return '%(level)s%(value)s%(suffix)s{c1}' % {'level': get_warning_level(value),
                                                 'value': value,
                                                 'suffix': suffix}


def get_warning_level(val):
    return '{low}' if val <= 50 else '{med}' if val < 80 else '{high}'

