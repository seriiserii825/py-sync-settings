import os

from rich import print
from rich.panel import Panel

from modules.checkForGitDir import checkForGitDir
from modules.checkIfPullNeeded import checkIfPullNeeded
from modules.setupSubmodules import setupSubmodules
from utils.decryptFiles import decryptFiles


def gitModules():
    os.system("git submodule init")
    os.system("git submodule update")
    if not os.path.exists(".gitmodules"):
        return
    original_cwd = os.getcwd()
    with open(".gitmodules") as f:
        lines = f.readlines()
    for line in lines:
        if "path" not in line:
            continue
        path = line.split("=")[1].strip()
        if not os.path.exists(path):
            print(f"[red]Submodule path {path} not found")
            continue
        os.chdir(path)
        print(Panel(f"Pulling submodule {path}", title="Git Pull", style="yellow"))
        gitPull()
        os.chdir(original_cwd)


def gitPull(skip_fetch=False):
    print(Panel(f"Pulling from {os.getcwd()}", title="Git Pull", style="blue"))
    if checkForGitDir():
        setupSubmodules()
        if os.path.exists(".gitmodules"):
            gitModules()
        result = checkIfPullNeeded(skip_fetch=skip_fetch)
        if result:
            exit_code = os.system("git pull")
            if exit_code != 0:
                return False
        decryptFiles()
        return True
    return True
