import os
from pyfzf.pyfzf import FzfPrompt
from rich import print
from rich.console import Console
console = Console()
fzf = FzfPrompt()
def createDir(basepath):
    dirs = []
    with os.scandir(basepath) as entries:
        for entry in entries:
            if entry.is_dir():
                dirs.append(entry.name)
    for dir in dirs:
        print(dir)
    choose = console.input("[green]Create or select directory, c/s: ")
    if choose == "c":
        new_dir = console.input("[gren]Enter new directory name: ")
        if new_dir in dirs:
            print("[red]Directory already exists, try again.")
            exit()
        os.mkdir(basepath + "/" + new_dir)
        return basepath + "/" + new_dir
    elif choose == "s":
        selected_dir = fzf.prompt(dirs)
        if selected_dir:
            print(f"[blue]selected_dir[0]: {selected_dir[0]}")
            return basepath + "/" + selected_dir[0]
        else:
            print("[red]No directory selected, try again.")
            createDir(basepath)
    else:
        print("[red]Invalid console.input, try again.")
        createDir(basepath)
