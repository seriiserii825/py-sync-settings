import os
import subprocess
import concurrent.futures
from datetime import datetime

from rich import print
from rich.panel import Panel
from rich.prompt import Confirm

from modules.gitPull import gitPull

FAILED_LOG = os.path.expanduser("~/Downloads/pull-failed.txt")


def _fetch(repo):
    subprocess.run(["git", "-C", repo, "fetch", "-q"], capture_output=True)


def _needs_pull(repo):
    try:
        count = subprocess.check_output(
            ["git", "-C", repo, "rev-list", "HEAD..@{u}", "--count"],
            stderr=subprocess.DEVNULL,
        ).strip()
        return int(count) > 0
    except (subprocess.CalledProcessError, ValueError):
        return False


def gitPullAll(file_path):
    repos = []
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if not os.path.exists(line):
                print(f"[red]Not found: {line}")
                continue
            repos.append(line)

    print(Panel(f"Fetching [bold]{len(repos)}[/bold] repos in parallel...", style="cyan"))
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(_fetch, repos)

    needs_pull = [r for r in repos if _needs_pull(r)]

    if not needs_pull:
        print(Panel("All repos are up to date.", style="green"))
        return

    lines = [f"  [cyan]{os.path.basename(r.rstrip('/'))}[/cyan]  [dim]{r}[/dim]" for r in needs_pull]
    print(Panel("\n".join(lines), title=f"Need pull ({len(needs_pull)})", style="yellow"))

    if not Confirm.ask("Pull all?"):
        return

    failed = []
    changed = []
    for repo in needs_pull:
        os.chdir(repo)
        success = gitPull(skip_fetch=True)
        if success is False:
            failed.append(repo)
            _notify_fail(repo)
        else:
            changed.append(repo)

    failed_count = len(failed)
    success_count = len(changed)
    total = len(needs_pull)

    if failed:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(FAILED_LOG, "a") as log:
            log.write(f"\n--- {timestamp} ---\n")
            for repo in failed:
                log.write(f"{repo}\n")
        print(f"[red]Failed repos written to {FAILED_LOG}")

    summary_lines = [
        f"[green]Success: {success_count}[/green]  [red]Failed: {failed_count}[/red]  Total: {total}"
    ]
    if failed_count > 0:
        summary_lines.append("\n[bold]Failed:[/bold]")
        for repo in failed:
            summary_lines.append(f"  [red]{os.path.basename(repo.rstrip('/'))}[/red]  [dim]{repo}[/dim]")

    print(Panel(
        "\n".join(summary_lines),
        title="Pull Summary",
        style="green" if failed_count == 0 else "yellow",
    ))
    subprocess.run(
        [
            "notify-send",
            f"Git Pull Done — {success_count}/{total} succeeded",
            f"Failed: {failed_count}" if failed_count else "All repos pulled successfully",
        ],
        check=False,
    )


def _notify_fail(repo):
    name = os.path.basename(repo.rstrip("/"))
    subprocess.run(
        ["notify-send", "-u", "critical", "Git Pull Failed", f"Repo: {name}\n{repo}"],
        check=False,
    )
