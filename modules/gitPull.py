import os
from rich import print
from modules.checkForGitDir import checkForGitDir
from modules.checkIfPullNeeded import checkIfPullNeeded
from rich.panel import Panel

from utils.decryptFiles import decryptFiles

def gitModules():
    os.system('git submodule init')
    os.system('git submodule update')
    # get submodule dirs from .gitmodules
    with open('.gitmodules') as f:
        lines = f.readlines()
        for line in lines:
            if 'path' in line:
                print(Panel(f"Pulling from {os.getcwd()}", title="Git Pull", style="yellow"))
                path = line.split('=')[1].strip()
                if path == 'libs':
                    os.chdir(path)
                    gitPull()
                    os.chdir('..')
                else:
                    print(f'[red]Error: libs not found')
                    os.chdir('..')

def gitPull():
    print(Panel(f"Pulling from {os.getcwd()}", title="Git Pull", style="blue"))
    if checkForGitDir():
        if os.path.exists('.gitmodules'):
            gitModules()
        result = checkIfPullNeeded()
        if result:
            os.system('git pull')
            decryptFiles()


