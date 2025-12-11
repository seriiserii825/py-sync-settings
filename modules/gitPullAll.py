import os

from rich import print
from rich.panel import Panel

from classes.GitManager import GitManager
from modules.checkIfPullNeeded import checkIfPullNeeded
from modules.gitPull import gitPull


def gitPullAll(file_path):
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            os.chdir(line)
            git = GitManager(os.getcwd())
            if git.has_changes():
                print_repo()
                print(
                    "[yellow]Uncommitted changes detected. [/yellow]"
                )
                continue
            elif git.needs_pull():
                print_repo()
                print("[green]Remote changes detected. Pulling...[/green]")
                continue
            elif git.needs_push():
                print_repo()
                print("[cyan]Local changes detected. No pull needed.[/cyan]")
                continue
            else:
                continue
            # result = checkIfPullNeeded()
            # if result:
            #     gitPull()

def print_repo():
    print(Panel(f"Pulling from {os.getcwd()}", title="Git Pull", style="blue"))
