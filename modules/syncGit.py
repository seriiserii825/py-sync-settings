import os
from rich.console import Console

from classes.ReposFiles import ReposFiles
from libs.richTable import richTable
from modules.getCommits import getCommits
from modules.gitPullAll import gitPullAll
from modules.gitPushAll import gitPushAll



def syncGit():
    console = Console()
    ReposFiles()
    file_push = os.path.join(os.path.expanduser('~'), 'Documents', 'push-repos.txt')
    file_pull = os.path.join(os.path.expanduser('~'), 'Documents', 'pull-repos.txt')
    table_title = "Git Repository Manager"
    table_columns = ["Option", "Description"]
    table_rows = [
        ["1) [blue]push[/]", "Push changes to the remote repository."],
        ["2) [red]pull[/]", "Pull changes from the remote repository."],
        ["3) [green]commits_all[/]", "Push changes to the remote repository."],
    ]
    richTable(table_title, table_columns, table_rows)
    action = console.input("[cyan]What would you like to do? ")
    if action == "1":
        gitPushAll(file_push)
    elif action == "2":
        gitPullAll(file_pull)
    elif action == "3":
        getCommits(file_push)
    else:
        console.print("[red]Invalid option. Please try again.")
        exit()
