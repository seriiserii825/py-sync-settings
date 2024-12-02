import os
from pyfzf.pyfzf import FzfPrompt
from rich import print
from rich.console import Console
console = Console()
fzf = FzfPrompt()
def createFile(basepath, ext, placeholder=None):
    files = []
    with os.scandir(basepath) as entries:
        for entry in entries:
            if entry.is_file():
                files.append(entry.name)
    for file in files:
        print(f"[blue]{file}")
    if placeholder:
        print(f"[green]Create file: {placeholder}")
    else:
        print("[green]Create file: ")
    new_file = console.input("[green]Enter new filename: ")
    if new_file in files:
        print("[red]File already exists, try again.")
        createFile(basepath, ext)
    os.system(f"touch {basepath}/{new_file}.{ext}")
    return basepath + "/" + new_file + "." + ext
