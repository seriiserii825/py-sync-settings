import os
import subprocess

from rich import print
from rich.panel import Panel
from rich.prompt import Prompt

from classes.ReposFiles import ReposFiles
from modules.checkForGitDir import checkForGitDir
from modules.checkIfPullNeeded import checkIfPullNeeded
from modules.checkIfPushNeeded import checkIfPushNeeded
from utils.decryptFiles import decryptFiles
from utils.encryptFiles import encryptFiles
from utils.tableMenu import tableMenu

user = os.getlogin()

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

commands = {
    "1": "feat",
    "2": "upd",
    "3": "bug-fix",
    "4": "fix",
    "5": "core",
}


def getExcludedDirs():
    repos_files = ReposFiles()
    exclude_dirs = repos_files.exclude_dirs
    exclude_for_pull = repos_files.exclude_for_pull
    total_exclude = exclude_dirs + exclude_for_pull
    return total_exclude


def pushChanges(commit_message_param=""):
    # show current path
    print(f"[green]Current path: {os.getcwd()}")
    choose = tableMenu()
    if choose in ["1", "2", "3", "4", "5"]:
        if commit_message_param == "":
            os.system("lazygit")
        if commit_message_param == "" and not checkIfPushNeeded():
            os.system("git push")
            print("[green]Done")
            decryptFiles()
            return
        commit_message = (
            commit_message_param
            if commit_message_param != ""
            else Prompt.ask("Commit message: ")
        )
        if commit_message == "":
            print("[red]Commit message is required")
            gitPush()
        git_command = "git add ."
        git_command += f' && git commit -m "{commands[choose]}: {commit_message}"'
        git_command += " && git push"
        os.system(git_command)
        print("[green]Done")
        decryptFiles()
    else:
        if choose == "6":
            os.system("lazygit")
            gitPush()
        elif choose == "7":
            print("[red]Bye")
            exit()
        else:
            print("[red]Invalid option")
            gitPush()


def gitModules():
    if not os.path.exists(".gitmodules"):
        return
    original_cwd = os.getcwd()
    with open(".gitmodules") as f:
        lines = f.readlines()
    for line in lines:
        if "path" not in line:
            continue
        path = line.split("=")[1].strip()
        if not os.path.exists(path):
            print(f"[red]Submodule path {path} not found")
            continue
        os.chdir(path)
        print(Panel(f"Pushing submodule {path}", title="Git Push", style="cyan"))
        if checkForGitDir():
            if checkIfPushNeeded():
                pushChanges()
            else:
                print("[red]No changes to commit")
        else:
            print("[red]No git dir found")
        os.chdir(original_cwd)


def getSubmodulePaths():
    if not os.path.exists(".gitmodules"):
        return set()
    with open(".gitmodules") as f:
        return {
            line.split("=")[1].strip()
            for line in f
            if line.strip().startswith("path")
        }


def onlySubmodulesChanged():
    submodule_paths = getSubmodulePaths()
    if not submodule_paths:
        return False
    result = subprocess.run(
        ["git", "status", "--porcelain"], capture_output=True, text=True
    )
    changed = [line[3:] for line in result.stdout.splitlines() if line]
    return bool(changed) and all(path in submodule_paths for path in changed)


def pushSubmodulesUpdate():
    print("[green]Only submodules changed, auto-committing")
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "feat: libs updated"], check=True)
    subprocess.run(["git", "push"], check=True)
    print("[green]Done")
    decryptFiles()


def gitPush(commit_message=""):
    print(Panel(f"Pushing from {os.getcwd()}", title="Git Push", style="blue"))
    if checkForGitDir():
        os.system("git status")
        gitModules()
        if checkIfPullNeeded():
            print("[red]Pull needed. Run git pull first.")
            return True
        if os.path.exists(".gpgrc"):
            encryptFiles()
            if onlySubmodulesChanged():
                pushSubmodulesUpdate()
            elif checkIfPushNeeded():
                pushChanges(commit_message_param=commit_message)
            else:
                print("[red]No changes to commit")
        else:
            if onlySubmodulesChanged():
                pushSubmodulesUpdate()
            elif checkIfPushNeeded():
                pushChanges(commit_message_param=commit_message)
            else:
                print("[red]No changes to commit")
