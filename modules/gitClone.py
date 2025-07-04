import os
import subprocess


def gitClone():
    clipboard = subprocess.check_output(
        "xclip -o -selection clipboard", shell=True, text=True
    ).strip()
    urls = ("github.com", "bitbucket.org", "gitlab.com", "repo clone")
    if any(url in clipboard for url in urls):
        print(clipboard)

        git_command = f"{clipboard} --single-branch"
        if "github.com" in clipboard:
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
