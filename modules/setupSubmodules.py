import os

from rich import print
from rich.panel import Panel


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
        if os.path.exists(path):
            continue
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
