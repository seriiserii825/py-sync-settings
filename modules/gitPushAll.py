import os

from rich import print

from modules.checkIfPushNeeded import checkIfPushNeeded
from modules.gitPush import gitPush


def gitPushAll(file_path):
    print("[blue]Pushing")
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            print(f"Pushing {line}")
            os.chdir(line)
            if checkIfPushNeeded():
                gitPush()
