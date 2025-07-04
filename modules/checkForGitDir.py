import os

from rich import print


def checkForGitDir():
    if os.path.exists(".git"):
        return True
    if os.path.isdir(".git"):
        return True
    else:
        print(f"[blue]Current path: {os.getcwd()}")
        print("[red]This is not a git repository")
        exit()
