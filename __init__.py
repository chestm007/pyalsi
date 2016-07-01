#! /usr/bin/python2

import os
import math
import click
import psutil
import cpuinfo
import platform
import arch_specific_functions
import ubuntu_specific_functions
from datetime import timedelta
from logos import logos
from colors import normal, bold
from window_managers import window_manager_definitions


@click.command()
@click.option('-n', '--normal-colour', default="white")
@click.option('-b', '--bold-colour', default="dgrey")
@click.option('-a', '--archie-logo', is_flag=True)
@click.option('-s', '--screenfetch-logo', is_flag=True)
@click.option('-l', '--info-below', is_flag=True)
@click.option('-d', '--distro', help="choose: " + ", ".join(logos.keys()))
@click.option('--logo', help="type 'pyAlsi --logo help' to see valid logos for your distro", default="Archey")
def main(normal_colour, bold_colour, archie_logo, screenfetch_logo, info_below, distro, logo):
    if not distro:
        distro = get_distro()

    if logo not in logos[distro]:
        valid_logos = "Please pick either: {}".format(", ".join(logos[distro].keys()))
        if logo != 'help':
            valid_logos = "Invalid logo. {}".format(valid_logos)
        raise click.UsageError(valid_logos)

    colors = {"c1": normal[normal_colour],
              "c2": bold[bold_colour],
              "low": bold["green"],
              "med": bold["yellow"],
              "high": bold["red"],
              "red": normal["red"]
              }

    if normal_colour not in normal or bold_colour not in bold:
        # if we were passed invalid colour parameters
        raise click.UsageError('color must be one of {}'.format(', '.join(normal)))

    # get RAM information
    ram_tot = str(math.ceil(psutil.virtual_memory().total / 1024 ** 2))
    ram_use = math.ceil(psutil.virtual_memory().used / 1024 ** 2)
    ram_pct = math.ceil(psutil.virtual_memory().percent)

    a = get_last_login()

    info = [colorize("OS", "{} {}".format(distro, platform.machine())),
            colorize("Hostname", platform.node())]

    info.append(colorize("Last Login From", '{} At {}'.format(a['ip'], a['at']))) if a else ""

    info.extend([colorize("Uptime", get_uptime()),
                 colorize("Kernel", platform.release()),
                 colorize("Shell", os.readlink('/proc/%d/exe' % os.getppid())),
                 colorize("Packages", count_packages(distro)),
                 colorize("Window Manager", get_window_manager()),
                 colorize("RAM", "{} ({})".format(colorize_usage(ram_use, ram_tot, ram_pct, "M"),
                                                  colorize_percent(ram_pct, "%"))),
                 colorize("CPU", get_cpu_info())
                 ])

    for card in get_vga_devices():
        info.append(colorize("VGA Cards", card))

    if distro == 'Arch Linux':
        info.extend(colorize(key, value) for key, value in arch_specific_functions.get_package_stats().iteritems())
    elif distro == 'Ubuntu':
        info.extend(colorize(key, value) for key, value in ubuntu_specific_functions.get_package_stats().iteritems())

    for disk in psutil.disk_partitions():
        disk_usage = psutil.disk_usage(disk.mountpoint)
        disk_used = math.ceil(disk_usage.used/1024**3)
        disk_total = math.ceil(disk_usage.total/1024**3)
        disk_percent = math.ceil(disk_usage.percent)
        disk_name = disk.mountpoint.split('/')[-1]

        info.append("{c2}{}: {} ({}) ({})".format(
                str.capitalize(disk_name) if disk_name != "" else "Root",
                colorize_usage(disk_used, disk_total, disk_percent,"G"),
                colorize_percent(disk_percent, "%"),
                disk.fstype, **colors))

    if info_below:
        click.echo("\n".join([line.format(**colors) for line in logos[distro][logo].splitlines()]))
        click.echo("\n\n")
        click.echo("\n".join(["   " + line.format(**colors) for line in info]))
    else:
        for i, line in enumerate((logos[distro][logo]).splitlines()):
            click.echo("{}".format(line + (info[i] if (i < len(info)) else "")).format(**colors))
    # print(logo.format(c1=color_one,c2=color_two, **info))


def get_cpu_info():
    cpu = cpuinfo.get_cpu_info_from_proc_cpuinfo()
    fmt = "{} cores" if cpu["count"] > 1 else "{} core"
    return "{} ({})".format(cpu["brand"], fmt.format(cpu["count"]))


def colorize(heading, value):
    """
    wrapper to colorize info lines
    :param heading: line heading (eg. "OS")
    :param value: line value (eg. "Arch Linux")
    :return: string (eg. "{c2}OS: {c1}Arch Linux")
    """
    return "{c2}" + heading + ": {c1}" + str(value)


def colorize_usage(use, total, percent, unit):
    """
    colorizes the passed string based on the percentage passed in
    :param use: output variable
    :param total: output variable
    :param percent: used to calculate the appropriate color
    :param unit: essentially a suffix to use and total (eg. "G | M")
    :return: string (eg. "{low}43G{c1} / 87G")
    """
    if percent <= 50:
        level = "{low}"
    elif percent > 50 and not percent > 80:
        level = "{med}"
    else:
        level = "{high}"
    return level + str(use) + unit + "{c1} / " + str(total) + unit


def colorize_percent(value, suffix=""):
    """
    as above but only takes one output variable
    :param value: the output variable
    :param suffix: string to put after value (eg. "%)
    :return: string (eg. "{low}15%{c1}")
    """
    if value <= 50:
        level = "{low}"
    elif value > 50 and not value > 80:
        level = "{med}"
    else:
        level = "{high}"
    return level + str(value) + suffix + "{c1}"


def count_packages(distro):
    if distro == 'Arch Linux':
        return len([name for name in os.listdir('/var/lib/pacman/local')])
    elif distro == 'Ubuntu':
        results = os.popen('dpkg -l |grep ^ii | wc -l').read().splitlines()
        for result in results:
            if result:
                return result

def get_uptime():
    """
    :return: uptime seconds as a human readable time
    """
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
        return str(timedelta(seconds=math.ceil(uptime_seconds)))


def get_distro():
    with open("/etc/issue") as f:
        v = f.read().split()
        if v[0] == 'Arch':
            return 'Arch Linux'
        elif v[0] == 'Apricity':
            return 'Apricity OS'
        elif v[0] == 'Ubuntu':
            return 'Ubuntu'


def get_window_manager():
    for proc in get_processes():
        if proc in window_manager_definitions.keys():
            return window_manager_definitions[proc]


def get_last_login():
    out = os.popen("last $USER -i | grep -E -v 'logged'").read()
    for o in out.splitlines():
        o = o.split()
        if len(o) > 1:
            if not o[-1] == 'in' and not o[0] == 'wtmp':
                output_dict = {'name': o[0],
                               'tty':  o[1],
                               'ip':   o[2],
                               'at': '{} {} {} {}:{}'.format(o[3], o[4], o[5], o[6], o[7].strip(':-'))}
                return output_dict
    return False


def get_processes():
    processes = os.popen('ps -A').read().splitlines()
    processes = [line.split()[3] for line in processes]
    return processes


def get_vga_devices():
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
    if len(cards) > 0:
        for k, v in cards.iteritems():
            output.append("{}{}".format(k, ("(x{})".format(v)) if v > 1 else ""))
    else:
        return False
    return output
if __name__ == "__main__":
    main()

