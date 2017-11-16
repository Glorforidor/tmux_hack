#!/usr/bin/env python3
"""
Since lastest update for tmux, tmux on my system does not inherit enviroment
variables from caller on server start. It will inherit enviroment variables
after a server shutdown but then my session saved with resurrect is broken.
It seems tmux-resurrect saves a broken session after shutdown of tmux,
but this can be fixed by deleting the last saved session
and replace it with second last session.

So this script is to start the tmux server, kill it again, delete the last
saved session and point tmux-resurrect 'last' to second last saved session.
"""

import os
import subprocess
import time
from threading import Thread
from typing import List


def kill_tmux():
    time.sleep(2)
    print('Kill tmux server')
    subprocess.call(['tmux', 'kill-server'])


print('Start tmux server')
subprocess.call(['tmux', 'start-server'])
t = Thread(target=kill_tmux)
t.start()
subprocess.call(['tmux'])
t.join()  # Wait for tmux to exit
# maybe tmux saves a session after exit. Wait for it to be saved.
time.sleep(2)

home = os.getenv('HOME')
tmux_resurrect_path = f'{home}/.tmux/resurrect/'
files: List[str] = sorted(os.listdir(tmux_resurrect_path))

print('Delete broken session:', files[-1])
os.remove(tmux_resurrect_path+files[-1])
print('Delete old link:', files[files.index('last')])
os.remove(tmux_resurrect_path+files[files.index('last')])
print(f'Link second lastest file: {files[-2]} session as last')
os.symlink(tmux_resurrect_path+files[-2], tmux_resurrect_path+'last')
