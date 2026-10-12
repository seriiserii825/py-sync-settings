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

user = os.getlogin()

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def detectCommitType(message):
    lower = message.lower()
    if "conflict" in lower:
        return "merge-conflict"
    if "upd" in lower:
        return "upd"
    if "bug" in lower:
        return "bug-fix"
    if "fix" in lower:
        return "fix"
    if "install" in lower:
        return "core"
    return "feat"


def getExcludedDirs():
    repos_files = ReposFiles()
    exclude_dirs = repos_files.exclude_dirs
    exclude_for_pull = repos_files.exclude_for_pull
    total_exclude = exclude_dirs + exclude_for_pull
    return total_exclude


def pushChanges(commit_message_param=""):
    # show current path
    print(f"[green]Current path: {os.getcwd()}")
    if commit_message_param == "":
        os.system("lazygit")
        if not checkIfPushNeeded():
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
        return
    commit_type = detectCommitType(commit_message)
    git_command = "git add ."
    git_command += f' && git commit -m "{commit_type}: {commit_message}"'
    git_command += " && git push"
    os.system(git_command)
    print("[green]Done")
    decryptFiles()


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


def getPyLibsSubmodulePaths():
    if not os.path.exists(".gitmodules"):
        return set()
    result = subprocess.run(
        [
            "git", "config", "-f", ".gitmodules",
            "--get-regexp", r"^submodule\..*\.(path|url)$",
        ],
        capture_output=True,
        text=True,
    )
    paths = {}
    urls = {}
    for line in result.stdout.splitlines():
        key, _, value = line.partition(" ")
        name, _, field = key[len("submodule."):].rpartition(".")
        (paths if field == "path" else urls)[name] = value.strip()
    return {
        path
        for name, path in paths.items()
        if urls.get(name, "").removesuffix(".git").endswith("/py-libs")
    }


def onlySubmodulesChanged():
    submodule_paths = getPyLibsSubmodulePaths()
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
