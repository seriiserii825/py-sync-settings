import os
import subprocess

from rich import print
from rich.panel import Panel

from modules.checkForGitDir import checkForGitDir
from modules.checkIfPullNeeded import checkIfPullNeeded
from modules.setupSubmodules import setupSubmodules
from utils.decryptFiles import decryptFiles


def getSubmodulePaths():
    result = subprocess.run(
        ["git", "config", "-f", ".gitmodules", "--get-regexp", r"\.path$"],
        capture_output=True,
        text=True,
    )
    return [line.split(maxsplit=1)[1]
            for line in result.stdout.splitlines() if " " in line]


def initSubmodule(path):
    """Clone/checkout submodule if it's missing or empty (not initialized)."""
    if os.path.exists(os.path.join(path, ".git")):
        return True
    print(
        Panel(
            f"Initializing missing submodule {path}",
            title="Git Pull",
            style="magenta"))
    exit_code = os.system(f"git submodule update --init --recursive -- {path}")
    if exit_code != 0 or not os.path.exists(os.path.join(path, ".git")):
        print(f"[red]Failed to initialize submodule {path}")
        return False
    return True


def attachSubmoduleBranch():
    """`git submodule update` leaves a detached HEAD, which has no upstream to pull from.
    Switch to the remote default branch so it can be pulled."""
    head = subprocess.run(
        ["git", "symbolic-ref", "-q", "HEAD"], capture_output=True, text=True
    )
    if head.returncode == 0:
        return
    remote_head = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "origin/HEAD"], capture_output=True, text=True
    )
    branch = remote_head.stdout.strip().removeprefix("origin/")
    if remote_head.returncode != 0 or not branch:
        branch = "main"
    print(f"[yellow]Detached HEAD, switching to branch {branch}")
    if os.system(f"git checkout {branch}") != 0:
        print(f"[red]Failed to checkout branch {branch}")


def gitModules():
    if not os.path.exists(".gitmodules"):
        return
    os.system("git submodule sync --quiet")
    original_cwd = os.getcwd()
    for path in getSubmodulePaths():
        if not initSubmodule(path):
            continue
        os.chdir(path)
        print(
            Panel(
                f"Pulling submodule {path}",
                title="Git Pull",
                style="yellow"))
        attachSubmoduleBranch()
        gitPull()
        os.chdir(original_cwd)
    # submodules are often uv workspace members: install them into .venv
    if os.path.exists("pyproject.toml"):
        os.system("uv sync --quiet")


def gitPull(skip_fetch=False):
    print(Panel(f"Pulling from {os.getcwd()}", title="Git Pull", style="blue"))
    if checkForGitDir():
        setupSubmodules()
        if os.path.exists(".gitmodules"):
            gitModules()
        result = checkIfPullNeeded(skip_fetch=skip_fetch)
        if result:
            exit_code = os.system("git pull")
            if exit_code != 0:
                return False
        decryptFiles()
        return True
    return True
