import os
import sys

from rich.console import Console

from libs.richTable import richTable
from modules.gitClone import gitClone
from modules.gitPull import gitPull
from modules.gitPush import gitPush
from modules.syncGit import syncGit

console = Console()


def menu():
    args = sys.argv
    args_str = ""
    # get args
    if len(args) > 1:
        for i in range(1, len(args)):
            args_str += args[i] + " "
        commit_message = args_str if args_str != "" else ""
    else:
        commit_message = ""

    table_title = "Choose an option"
    table_columns = ["Option", "Description"]
    table_rows = [
        ["[blue]1) Push[/]", "Push"],
        ["[green]2) Pull[/]", "Pull"],
        ["[yellow]3) Sync[/]", "Sync all repositories."],
        ["[green]4) Clone[/]", "Clone"],
        ["[red]5) Remove Sync files[/]", "Remove sync files."],
    ]
    richTable(table_title, table_columns, table_rows)
    action = console.input("[cyan]What would you like to do? ")
    if action == "1":
        gitPush(commit_message)
    elif action == "2":
        gitPull()
    elif action == "3":
        syncGit()
    elif action == "4":
        gitClone()
    elif action == "5":
        command = "rm -rf ~/Documents/push-repos.txt ~/Documents/pull-repos.txt"
        os.system(command)
    else:
        gitPush(commit_message)


menu()
