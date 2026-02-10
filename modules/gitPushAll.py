import os

from rich import print

from libs.appendToFile import appendToFile
from modules.checkIfPushNeeded import checkIfPushNeeded
from modules.gitPush import gitPush

changed_file = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "changed-repos.txt"
)


def gitPushAll(file_path):
    print("[blue]Pushing")
    if os.path.exists(changed_file):
        os.remove(changed_file)
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            print(f"Pushing {line}")
            os.chdir(line)
            if checkIfPushNeeded():
                gitPush()
                appendToFile(changed_file, line)
