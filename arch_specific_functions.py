import os


def get_package_stats():
    pacman_output = os.popen('pacman -Qu').read().splitlines()
    pacman_pending_update_count = len(pacman_output)
    return {'Pending Updates': pacman_pending_update_count}
