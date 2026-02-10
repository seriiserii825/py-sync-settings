import os

from rich import print

from libs.appendToFile import appendToFile
from modules.checkIfPushNeeded import checkIfPushNeeded
from modules.gitPush import gitPush

project_root = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)
changed_file = os.path.join(project_root, "changed-repos.txt")


def gitPushAll(file_path):
    print("[blue]Pushing")
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            print(f"Pushing {line}")
            os.chdir(line)
            if checkIfPushNeeded():
                gitPush()
                appendToFile(changed_file, line)
    if os.path.exists(changed_file):
        os.chdir(project_root)
        os.system(
            'git add changed-repos.txt'
            ' && git commit -m "upd: changed-repos"'
            ' && git push'
        )
        print("[green]changed-repos.txt committed")
