import os


def get_package_stats():
    apt_output = os.popen('/usr/lib/update-notifier/apt-check --human-readable').read().splitlines()
    apt_pending_update_count = apt_output[0].split()[0]
    return {'Pending Updates': apt_pending_update_count}


