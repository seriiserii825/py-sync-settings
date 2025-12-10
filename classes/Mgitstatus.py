import os
import subprocess

from classes.ReposFiles import ReposFiles


class Mgitstatus:
    def __init__(self):
        self.all_repos = []

    def get_all_repos(self):
        home_dir = os.path.expanduser("~")

        result = subprocess.run(
            ["mgitstatus", "-e", "-d", "4", "--no-stashes"],
            cwd=home_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Print full output
        print(result.stdout)

    def exclude_repos(self):
        rf = ReposFiles()
        exclude_pull_dirs = rf.get_exclude_for_pull_rows()
        ms_repos = self.get_all_repos_list()
        ms_to_exclude = []
        for repo in ms_repos:
            for exclude in exclude_pull_dirs:
                if exclude in repo:
                    ms_to_exclude.append(repo)
        print(f"{ms_to_exclude}: ms_to_exclude")

    def get_all_repos_list(self):
        home_dir = os.path.expanduser("~")

        result = subprocess.run(
            ["mgitstatus", "-d", "4"],
            cwd=home_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Extract and process paths into array
        repo_paths = []
        for line in result.stdout.splitlines():
            # Split at colon and take first part
            if ":" in line:
                path = line.split(":", 1)[0].strip()

                # Replace leading ./ with ~/
                if path.startswith("./"):
                    path = "~/" + path[2:]

                repo_paths.append(path)
        return repo_paths
