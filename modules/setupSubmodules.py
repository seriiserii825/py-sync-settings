import os
import subprocess

from rich import print
from rich.panel import Panel


def _isRegistered(path):
    """True if path is already declared in .gitmodules."""
    if not os.path.exists(".gitmodules"):
        return False
    result = subprocess.run(
        ["git", "config", "-f", ".gitmodules", "--get-regexp", r"\.path$"],
        capture_output=True,
        text=True,
    )
    return any(
        line.split(maxsplit=1)[1] == path
        for line in result.stdout.splitlines()
        if " " in line
    )


def setupSubmodules():
    if not os.path.exists(".submodules"):
        return
    with open(".submodules") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    for line in lines:
        parts = line.split()
        if len(parts) != 2:
            print(f"[red]Invalid line in .submodules: {line}")
            continue
        url, path = parts
        # an existing but empty dir (e.g. created by `git pull`) is not a submodule yet
        if os.path.exists(os.path.join(path, ".git")):
            continue
        # already declared in .gitmodules: gitModules() clones it via `submodule update --init`
        if _isRegistered(path):
            continue
        if os.path.isdir(path):
            if os.listdir(path):
                print(f"[red]{path} exists and is not empty, cannot add submodule there")
                continue
            # `git submodule add` refuses even an empty existing dir
            os.rmdir(path)
        print(
            Panel(
                f"Adding missing submodule {path}",
                title="Submodule Setup",
                style="magenta",
            )
        )
        exit_code = os.system(f"git submodule add {url} {path}")
        if exit_code != 0:
            print(f"[red]Failed to add submodule {path}")
            continue
        if os.path.exists("pyproject.toml"):
            os.system(f"uv add --editable ./{path}")
