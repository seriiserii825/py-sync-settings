import subprocess

from rich import print


def checkIfPullNeeded(skip_fetch=False):
    if not skip_fetch:
        result = subprocess.run(["git", "fetch"], check=True)
        if result.returncode != 0:
            print("[red]Error fetching the latest changes from the remote.")
            return False
    # Get the local and remote head commit hashes
    try:
        local_commit = subprocess.check_output(["git", "rev-parse", "HEAD"]).strip()
    except subprocess.CalledProcessError:
        print("[red]Error getting the local commit hash.")
        return False

    try:
        remote_commit = subprocess.check_output(["git", "rev-parse", "@{u}"]).strip()
    except subprocess.CalledProcessError:
        print("[red]Error getting the remote commit hash.")
        return False

    if remote_commit == b"":
        print("[red]Error getting the remote commit hash.")
        return False

    try:
        behind = subprocess.check_output(["git", "rev-list", "HEAD..@{u}", "--count"]).strip()
    except subprocess.CalledProcessError:
        print("[red]Error checking behind count.")
        return False

    if int(behind) > 0:
        print("[green]Pull needed. Your branch is behind the remote.")
        return True
    else:
        print("[red]Your branch is up to date with the remote.")
        return False
