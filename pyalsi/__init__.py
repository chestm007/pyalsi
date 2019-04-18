import click
import platform
import sys

from pyalsi.logos import logos
from pyalsi.colors import normal, bold
from pyalsi.hardware.disks.disk import DiskGroup
from pyalsi.hardware.vga.vga import Vga
from pyalsi.system.system import System
from pyalsi.utils.types import Bytes
from pyalsi.window_managers import window_manager_definitions
from pyalsi.hardware.cpu.cpu import Cpu
from pyalsi.hardware.ram.ram import Ram
from pyalsi.utils.strings import colorize, colorize_usage, colorize_percent, Colors

DEFAULT_DISTRO_LOGO = {'Arch Linux': 'Archey',
                       'Debian': 'Below',
                       'Fedora': 'Screenfetch',
                       'Apricity OS': 'Below',
                       'Ubuntu': 'Archey'}


@click.command()
@click.option('-n', '--normal-colour', default="white")
@click.option('-b', '--bold-colour', default="dgrey")
@click.option('-l', '--info-below', is_flag=True)
@click.option('-d', '--distro', help="choose: " + ", ".join(logos.keys()), default='Arch')
@click.option('--logo', help="type 'pyAlsi --logo help' to see valid logos for your distro", default=None)
def cli(normal_colour, bold_colour, info_below, distro, logo):
    for c, t in ((normal_colour, normal), (bold_colour, bold)):
        if c not in t:
            raise click.UsageError('color must be one of {}'.format(', '.join(normal)))

    colors = Colors(primary=normal[normal_colour], secondary=bold[bold_colour])

    cpu = Cpu()
    ram = Ram()
    system = System()
    vga = Vga()
    disks = DiskGroup()

    if distro is not None:
        if distro not in logos.keys():
            raise click.UsageError('distro must be one of ({})'.format('|'.join(logos.keys())))
        system._distro = distro
        system.friendly_distro = System.distro_subclass_map[distro].friendly_distro

    if logo is not None:
        if logo not in logos[system.distro]:
            valid_logos = "Please pick either: {}".format(", ".join(logos[system.distro].keys()))
            if logo != 'help':
                valid_logos = "Invalid logo. {}".format(valid_logos)
            raise click.UsageError(valid_logos)
    else:
        logo = DEFAULT_DISTRO_LOGO[system.friendly_distro]

    info_below = logo == 'Below'

    last_login = system.last_login
    info = [("OS", "{} {}".format(system.friendly_distro, platform.machine())),
            ("Hostname", platform.node()),
            ("Last Login From", ('{} At {}'.format(last_login['ip'], last_login['at'])) if last_login else 'Never'),
            ("Uptime", system.uptime),
            ("Kernel", platform.release()),
            ("Shell", system.shell),
            ("Packages", system.num_packages),
            ("Window Manager", system.window_manager),
            ("RAM", "{} ({})".format(
                colorize_usage(ram.used.megabytes, ram.total.megabytes, ram.percent, "M"),
                colorize_percent(ram.percent, "%"))),
            ("CPU", cpu.info_string)]

    info.extend(("VGA Cards", card) for card in vga.devices)
    info.extend((key, value) for key, value in system.package_stats.items())
    info.extend(disk.info_string for disk in disks.disks)

    if info_below:
        click.echo("\n".join([line.format(**colors.colors) for line in logos[system.distro][logo].replace('XX', '').splitlines()]))
        click.echo("\n\n")
        click.echo("\n".join(["   " + colorize(*line).format(**colors.colors) for line in info]))
    else:
        for i, line in enumerate((logos[system.distro][logo]).replace('XX', '').splitlines()):
            click.echo("{}".format(line + (colorize(*info[i]) if (i < len(info)) else "")).format(**colors.colors))
    click.echo('\x1b[0m')  # return terminal colour to normal


# compatibility for debugging in pyCharm.
if __name__ == '__main__':
    cli(sys.argv[1:])
