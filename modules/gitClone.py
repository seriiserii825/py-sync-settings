import os
import subprocess

from libs.buffer import getFromClipboard


def gitClone():
    clipboard = getFromClipboard()

    urls = (
        "github.com",
        "bitbucket.org",
        "gitlab.com",
        "git.bludelego.com",
        "repo clone",
    )
    # Hosts whose copied URL is bare (without the "git clone" prefix)
    bare_url_hosts = ("github.com", "git.bludelego.com")
    if any(url in clipboard for url in urls):
        print(clipboard)

        if any(host in clipboard for host in bare_url_hosts):
            git_command = f"git clone {clipboard}"
        else:
            git_command = f"{clipboard}"
        subprocess.run(git_command, shell=True, check=True)

        # Change directory to the cloned repo
        repo_name = os.path.basename(clipboard).replace(".git", "")
        os.chdir(repo_name)

        # Check for and update submodules if present
        if os.path.isfile(".gitmodules"):
            subprocess.run(
                "git submodule update --init --recursive", shell=True, check=True
            )
            subprocess.run(
                "git submodule foreach 'branch=$(git branch -r | \
                        grep -m1 origin/HEAD | sed \"s/.*origin\\///\") \
                        && git checkout $branch && git pull origin $branch'",
                shell=True,
                check=True,
            )
    else:
        print("Clipboard does not contain a Git repository URL.")
