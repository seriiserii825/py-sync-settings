import os
import sys

from rich.console import Console

from libs.Menu import Menu
from modules.autoCommit import autoCommit
from modules.gitClone import gitClone
from modules.gitPull import gitPull
from modules.gitPush import gitPush
from modules.syncGit import syncGit

console = Console()


def menu():
    args = sys.argv

    if len(args) > 1 and args[1] == "pull":
        gitPull()
        return

    if len(args) == 1 and autoCommit():
        return

    args_str = ""
    # get args
    if len(args) > 1:
        for i in range(1, len(args)):
            args_str += args[i] + " "
        commit_message = args_str if args_str != "" else ""
    else:
        commit_message = ""

    action = Menu.select_fzf_menu([
        "[blue]Push",
        "[green]Pull",
        "[yellow]Sync all repositories",
        "[green]Clone",
        "[red]Remove sync files",
    ])
    if not action:
        console.print("[red]Bye")
        exit()
    elif action == 1:
        gitPush(commit_message)
    elif action == 2:
        gitPull()
    elif action == 3:
        syncGit()
    elif action == 4:
        gitClone()
    elif action == 5:
        docs = os.path.expanduser("~/Documents")
        command = f"rm -rf {docs}/push-repos.txt {docs}/pull-repos.txt"
        os.system(command)
    elif action == "6":
        console.print("[red]Bye")
        exit()
    else:
        gitPush(commit_message)


menu()
