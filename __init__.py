#! /usr/bin/python2

import os
import math
import click
import psutil
import cpuinfo
import platform
from datetime import timedelta
from logos import logos
from colors import normal, bold
from window_managers import window_manager_definitions


@click.command()
@click.option('-n', '--normal-colour')
@click.option('-b', '--bold-colour')
@click.option('-a', '--archie-logo', is_flag=True)
@click.option('-s', '--screenfetch-logo', is_flag=True)
@click.option('-l', '--info-below', is_flag=True)
def main(normal_colour, bold_colour, archie_logo, screenfetch_logo, info_below):

    # default if no logo selected
    if not archie_logo and not screenfetch_logo and not info_below:
        archie_logo = True

    if not normal_colour:
        normal_colour = "white"
    if not bold_colour:
        bold_colour = "dgrey"
    colors = {"c1": normal[normal_colour],
              "c2": bold[bold_colour],
              "low": normal["green"],
              "med": normal["yellow"],
              "high": normal["red"]
              }

    if screenfetch_logo:
        logo = 'Screenfetch'
    elif archie_logo:
        logo = 'Archie'
    elif info_below:
        logo = 'Below'

    if normal_colour not in normal or bold_colour not in bold:
        # if we were passed invalid colour parameters
        raise click.UsageError('color must be one of {}'.format(', '.join(normal)))

    # get RAM information
    ram_tot = str(math.ceil(psutil.virtual_memory().total / 1024 ** 2))
    ram_use = math.ceil(psutil.virtual_memory().used / 1024 ** 2)
    ram_pct = math.ceil(psutil.virtual_memory().percent)

    os_info = "{} {}".format(get_distro(), platform.machine())

    info = [colorize("OS", os_info),
            colorize("Hostname", platform.node()),
            colorize("Uptime", get_uptime()),
            colorize("Kernel", platform.release()),
            colorize("Shell", os.readlink('/proc/%d/exe' % os.getppid())),
            colorize("Packages", len([name for name in os.listdir('/var/lib/pacman/local')])),
            colorize("Window Manager", get_window_manager()),
            colorize("RAM", "{} ({})".format(colorize_usage(ram_use, ram_tot, ram_pct, "M"),
                                             colorize_percent(ram_pct, "%"))),
            colorize("CPU", cpuinfo.get_cpu_info_from_proc_cpuinfo()["brand"]),
            ]

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
        click.echo("\n".join([line.format(**colors) for line in logos[logo].splitlines()]))
        click.echo("\n\n")
        click.echo("\n".join(["   " + line.format(**colors) for line in info]))
    else:
        for i, line in enumerate((logos[logo]).splitlines()):
            click.echo("{}".format(line + (info[i] if (i < len(info)) else "")).format(**colors))
    # print(logo.format(c1=color_one,c2=color_two, **info))


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


def get_uptime():
    """
    :return: uptime seconds as a human readable time
    """
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
        return str(timedelta(seconds=math.ceil(uptime_seconds)))


def get_distro():
    """
    :return: first 2 words from /etc/issue
    """
    with open("/etc/issue") as f:
        v = f.read().split()
        return '{} {}'.format(v[0], v[1])


def get_window_manager():
    for proc in get_processes():
        if proc in window_manager_definitions.keys():
            return window_manager_definitions[proc]


def get_processes():
    processes = os.popen('ps -A').read().splitlines()
    processes = [line.split()[3] for line in processes]
    return processes

if __name__ == "__main__":
    main()

