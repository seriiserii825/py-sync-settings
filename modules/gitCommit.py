import os
from rich import print


def gitCommit():
    user = os.getenv('USER')
    print('[blue]Committing')
    os.system(f'/home/{user}/Documents/python/py-lf/venv/bin/python /home/{user}/Documents/python/py-lf/main.py')
    return

