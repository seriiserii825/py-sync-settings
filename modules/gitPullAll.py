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
    total = 0
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total += 1
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

    success_count = total - len(failed)
    failed_count = len(failed)

    if failed:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(FAILED_LOG, "a") as log:
            log.write(f"\n--- {timestamp} ---\n")
            for repo in failed:
                log.write(f"{repo}\n")
        print(f"[red]Failed repos written to {FAILED_LOG}")

    summary_color = "green" if failed_count == 0 else "yellow"
    print(Panel(
        f"[green]Success: {success_count}[/green]  [red]Failed: {failed_count}[/red]  Total: {total}",
        title="Pull Summary",
        style=summary_color,
    ))
    subprocess.run(
        ["notify-send", f"Git Pull Done — {success_count}/{total} succeeded",
         f"Failed: {failed_count}" if failed_count else "All repos pulled successfully"],
        check=False,
    )


def _notify_fail(repo):
    name = os.path.basename(repo.rstrip("/"))
    subprocess.run(
        ["notify-send", "-u", "critical", "Git Pull Failed", f"Repo: {name}\n{repo}"],
        check=False,
    )
