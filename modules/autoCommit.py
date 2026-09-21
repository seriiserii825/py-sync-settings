import csv
import os
import subprocess
import sys

from rich import print
from rich.panel import Panel

from modules.checkIfPullNeeded import checkIfPullNeeded
from modules.checkIfPushNeeded import checkIfPushNeeded
from utils.decryptFiles import decryptFiles
from utils.encryptFiles import encryptFiles

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUTO_COMMIT_FILE = os.path.join(PROJECT_ROOT, "auto-commit.csv")


def getAutoCommitMessage():
    if not os.path.isfile(AUTO_COMMIT_FILE):
        return None
    cwd = os.path.realpath(os.getcwd())
    with open(AUTO_COMMIT_FILE, newline="") as file:
        for row in csv.DictReader(file):
            path = (row.get("path") or "").strip()
            message = (row.get("message") or "").strip()
            if path and os.path.realpath(os.path.expanduser(path)) == cwd:
                return message
    return None


def autoCommit():
    message = getAutoCommitMessage()
    if message is None:
        return False

    if not os.path.isdir(".git"):
        return False

    title = "Auto Commit"
    print(Panel(f"Auto-committing {os.getcwd()}", title=title, style="blue"))

    if checkIfPullNeeded():
        print(f"[red]Aborting: {os.getcwd()} needs a pull first.")
        sys.exit(1)

    has_gpgrc = os.path.isfile(".gpgrc")
    if has_gpgrc:
        encryptFiles()

    if not checkIfPushNeeded():
        print("[red]No changes to commit")
        if has_gpgrc:
            decryptFiles()
        return True

    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", f"feat: {message}"], check=True)
    subprocess.run(["git", "push"], check=True)
    print("[green]Done")

    if has_gpgrc:
        decryptFiles()

    return True
