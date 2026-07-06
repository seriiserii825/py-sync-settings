import os

from rich.console import Console
from rich.panel import Panel

from classes.Command import Command
from classes.ReposFiles import ReposFiles
from libs.richTable import richTable
from modules.addChangedReposToFile import addChangedReposToFile
from modules.getCommits import getCommits
from modules.gitPullAll import LAST_MODIFIED_FILE, gitPullAll
from modules.gitPushAll import gitPushAll


def syncGit():
    console = Console()
    repos_files = ReposFiles()
    repos_files.deleteFiles()
    docs = os.path.join(os.path.expanduser("~"), "Documents")
    file_push = os.path.join(docs, "push-repos.txt")
    file_pull = os.path.join(docs, "pull-repos.txt")
    table_title = "Git Repository Manager"
    table_columns = ["Option", "Description"]
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_changed = os.path.join(project_root, "changed-repos.txt")
    table_rows = [
        ["1) [blue]push all[/]", "Push changes to the remote repository."],
        ["2) [red]pull all[/]", "Pull changes from the remote repository."],
        ["3) [green]commits_all[/]", "Push changes to the remote repository."],
        ["4) [yellow]pull_changed[/]", "Pull only repos changed in last push."],
        ["5) [green]repos_to_changed_repos[/]", "Copy repos to changed-repos.txt."],
        ["6) [magenta]clear_changed[/]", "Clear changed-repos.txt."],
        ["7) [cyan]last_modified[/]", "Show repos changed in the last pull all."],
        ["8) [red]exit[/]", "Exit."],
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
        if os.path.exists(file_changed):
            gitPullAll(file_changed)
        else:
            console.print("[red]No changed-repos.txt found. Push first.")
    elif action == "5":
        addChangedReposToFile(file_push)
    elif action == "6":
        if os.path.exists(file_changed):
            # make file empty
            Command.run_quiet(f"echo '' > {file_changed}")
            console.print("[green]changed-repos.txt empty.")
        else:
            console.print("[red]No changed-repos.txt to make empty.")
    elif action == "7":
        if os.path.exists(LAST_MODIFIED_FILE):
            with open(LAST_MODIFIED_FILE, "r") as f:
                content = f.read().strip()
            if content:
                console.print(Panel(content, title="Last modified dirs", style="cyan"))
            else:
                console.print("[yellow]No repos changed in the last pull.")
        else:
            console.print("[red]No last-modified-dirs.txt found. Run pull all first.")
    elif action == "8":
        exit()
    else:
        console.print("[red]Invalid option. Please try again.")
        exit()
