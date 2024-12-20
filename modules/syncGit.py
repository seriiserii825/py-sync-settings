import os
from rich.console import Console

from libs.richTable import richTable
from modules.getCommits import getCommits
from modules.gitPullAll import gitPullAll
from modules.gitPushAll import gitPushAll
from modules.reposToFile import reposToFile

file_push = os.path.join(os.path.expanduser('~'), 'Downloads', 'push-repos.txt')
file_pull = os.path.join(os.path.expanduser('~'), 'Downloads', 'pull-repos.txt')
console = Console()

def syncGit():
    reposToFile(file_push, file_pull)
    table_title = "Git Repository Manager"
    table_columns = ["Option", "Description"]
    table_rows = [
        ["1) [blue]push[/]", "Push changes to the remote repository."],
        ["2) [red]pull[/]", "Pull changes from the remote repository."],
        ["3) [green]commits_all[/]", "Push changes to the remote repository."],
        ["4) [blue]commits_projects[/]", "Push changes to the remote repository."],
    ]
    richTable(table_title, table_columns, table_rows)
    action = console.input("[cyan]What would you like to do? ")
    if action == "1":
        gitPushAll(file_push)
    elif action == "2":
        gitPullAll(file_pull)
    elif action == "3":
        getCommits(file_push)
    elif action == "4":
        getCommits(file_push, projects=True)
    else:
        console.print("[red]Invalid option. Please try again.")
        exit()
