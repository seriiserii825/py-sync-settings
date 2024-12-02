import os

from rich import print
from rich.panel import Panel

from modules.checkIfPullNeeded import checkIfPullNeeded
from modules.gitPull import gitPull
def gitPullAll(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            os.chdir(line)
            print(Panel(f"Pulling from {os.getcwd()}", title="Git Pull", style="blue"))
            result = checkIfPullNeeded()
            if result:
                gitPull()
