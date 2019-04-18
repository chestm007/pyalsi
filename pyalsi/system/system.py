import os
import math
from datetime import timedelta
from pyalsi.window_managers import window_manager_definitions


class System(object):
    distro = "unknown"
    friendly_distro = 'Unknown'
    distro_subclass_map = {}

    def __init__(self):
        for sub in System.__subclasses__():
            if sub.distro != 'unknown':
                self.distro_subclass_map[sub.distro] = sub
                if self.distro == sub.distro:
                    self.__class__ = sub
                for s in sub.__subclasses__():
                    self.distro_subclass_map[s.distro] = s
                    if self.distro == s.distro:
                        self.__class__ = s

        self.shell = os.readlink('/proc/%d/exe' % os.getppid())

    @property
    def distro(self):
        if hasattr(self, '_distro'):
            return self._distro
        try:
            for line in os.popen("cat /etc/*-release").read().splitlines():
                if line.startswith('NAME='):
                    return line.split('=')[1].strip('"')
        except IOError:
            return "Unknown"

    @property
    def uptime(self):
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            return timedelta(seconds=math.ceil(uptime_seconds))

    @property
    def window_manager(self):
        for proc in self.processes:
            wm = window_manager_definitions.get(proc)
            if wm:
                return wm

    @property
    def last_login(self):
        out = os.popen("last $USER -i | grep -E -v 'logged'").read()
        for o in out.splitlines():
            o = o.split()
            if len(o) > 1:
                if not o[-1] == 'in' and not o[0] == 'wtmp':
                    output_dict = {'name': o[0],
                                   'tty': o[1],
                                   'ip': o[2],
                                   'at': '{} {} {} {}:{}'.format(
                                       o[3], o[4], o[5], o[6], o[7].strip(':-'))}
                    return output_dict

    @property
    def processes(self):
        processes = os.popen('ps -A').read().splitlines()
        processes = [line.split()[3] for line in processes]
        return processes

    @property
    def package_stats(self):
        return {'Pending Updates': self._package_stats}

    @property
    def _package_stats(self):
        return 'no data'

    @property
    def num_packages(self):
        return 'no data'


class ArchLinuxSystem(System):
    distro = 'Arch'
    friendly_distro = 'Arch Linux'

    @property
    def num_packages(self):
        return Pacman().num_packages

    @property
    def _package_stats(self):
        return Pacman().package_stats


class ApricitySystem(ArchLinuxSystem):
    distro = 'Apricity OS'
    friendly_distro = 'Apricity OS'


class AntergosSystem(ArchLinuxSystem):
    distro = 'Antergos Linux'
    friendly_distro = 'Arch Linux'


class DebianSystem(System):
    distro = 'Debian'
    friendly_distro = distro

    @property
    def _num_packages(self):
        return Dpkg().num_packages


class UbuntuSystem(DebianSystem):
    distro = 'Ubuntu'
    friendly_distro = distro

    @property
    def package_stats(self):
        return Apt().package_stats


class FedoraSystem(System):
    distro = 'Fedora'
    friendly_distro = distro

    @property
    def num_packages(self):
        return Dpkg().num_packages


class Dpkg(object):
    @property
    def num_packages(self):
        for result in os.popen('dpkg -l |grep ^ii | wc -l').read().splitlines():
            if result:
                return result


class Apt(object):
    @property
    def package_stats(self):
        apt_output = os.popen('/usr/lib/update-notifier/apt-check --human-readable').read().splitlines()
        return apt_output[0].split()[0]


class Dnf(object):
    @property
    def package_stats(self):
        return

    @property
    def num_packages(self):
        return


class Pacman(object):
    @property
    def num_packages(self):
        return len([name for name in os.listdir('/var/lib/pacman/local')])

    @property
    def package_stats(self):
        pacman_output = os.popen('pacman -Qu').read().splitlines()
        return str(len(pacman_output))
