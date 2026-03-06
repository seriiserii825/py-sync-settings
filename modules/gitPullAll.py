import os
import subprocess
from datetime import datetime

from rich import print
from rich.panel import Panel

from modules.checkIfPullNeeded import checkIfPullNeeded
from modules.gitPull import gitPull

FAILED_LOG = os.path.expanduser("~/Downloads/pull-failed.txt")


def gitPullAll(file_path):
    failed = []
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if not os.path.exists(line):
                print(f"[red]Error: {line} does not exist")
                failed.append(line)
                _notify_fail(line)
                continue
            os.chdir(line)
            print(Panel(f"Pulling from {os.getcwd()}", title="Git Pull", style="blue"))
            result = checkIfPullNeeded()
            if result:
                success = gitPull()
                if success is False:
                    failed.append(line)
                    _notify_fail(line)

    if failed:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(FAILED_LOG, "a") as log:
            log.write(f"\n--- {timestamp} ---\n")
            for repo in failed:
                log.write(f"{repo}\n")
        print(f"[red]Failed repos written to {FAILED_LOG}")


def _notify_fail(repo):
    name = os.path.basename(repo.rstrip("/"))
    subprocess.run(
        ["notify-send", "-u", "critical", "Git Pull Failed", f"Repo: {name}\n{repo}"],
        check=False,
    )
