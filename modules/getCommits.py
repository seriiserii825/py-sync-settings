import os
import subprocess
from datetime import datetime

from rich import print
from rich.panel import Panel

from libs.selectWithFzf import selectWithFzf
from modules.getLocalProjects import getLocalProjects
from modules.gitCommitToBuffer import gitCommitToBuffer


def getTodayProjects(file_path, projects=False):
    lines = []
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            lines.append(line)
    if projects:
        lines = getLocalProjects(lines)
    today_date = datetime.today().strftime("%Y-%m-%d")
    today_projects = []
    for line in lines:
        os.chdir(line)
        command = [
            "git",
            "log",
            f"--since={today_date} 00:00:00",
            f"--until={today_date} 23:59:59",
            "--pretty=format:%an: %cd: %s",
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.stdout:
            today_projects.append(line)
    return today_projects


def getCommits(file_path, projects=False):
    today_projects = getTodayProjects(file_path, projects)
    for line in today_projects:
        os.chdir(line)
        today_date = datetime.today().strftime("%Y-%m-%d")
        command = [
            "git",
            "log",
            f"--since={today_date} 00:00:00",
            f"--until={today_date} 23:59:59",
            "--pretty=format:%an: %cd: %s",
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.stdout:
            print(Panel(f"[green]{result.stdout}", title=line))
    copy_to_buffer = input(
        "Would you like to copy the commits to the clipboard? [y/n] "
    )
    if copy_to_buffer.lower() == "y":
        continue_commits = True
        while continue_commits:
            themes = []
            for line in today_projects:
                print(f"line: {line}")
                theme = line.split("/")[-2]
                print(f"theme: {theme}")
                themes.append(theme)
            choosed_theme = selectWithFzf(themes)
            print(f"choosed_theme: {choosed_theme}")
            for line in today_projects:
                if choosed_theme in line:
                    print(Panel(f"[blue]Changing directory to {line}"))
                    os.chdir(line)
                    gitCommitToBuffer()
                    continue_commits = input(
                        "Would you like to copy another commit to \
                                the clipboard? [y/n] "
                    )
                    if continue_commits.lower() == "n":
                        continue_commits = False
                        print("[red]Exiting...")
                        exit()
