import os
import subprocess
import concurrent.futures

from rich import print
from rich.console import Console
from rich.panel import Panel

from classes.CsvHandler import CsvHandler

console = Console()

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ReposFiles:
    PUSH_FILE = os.path.join(os.path.expanduser("~"), "Documents", "push-repos.txt")
    PUT_FILE = os.path.join(os.path.expanduser("~"), "Documents", "pull-repos.txt")
    PUSH_FILE_GIT = os.path.join(PROJECT_ROOT, "push-repos.txt")
    PUT_FILE_GIT = os.path.join(PROJECT_ROOT, "pull-repos.txt")
    ALL_FILE_GIT = os.path.join(PROJECT_ROOT, "all-repos.txt")

    def __init__(self):
        self.csvHandler = CsvHandler()
        self.exclude_dirs = self.csvHandler.getExcludeDirs()
        self.exclude_for_pull = self.csvHandler.getExcludeForPull()

    def _read_existing(self, file_path):
        if not os.path.exists(file_path):
            return set()
        with open(file_path, "r") as f:
            return {line.strip() for line in f if line.strip()}

    def deleteFiles(self):
        delete_files = console.input("[green]Do you want to delete the files? (y/n): ")
        if delete_files.lower() != "y":
            print("[red]Files not deleted.")
            return

        old_push = self._read_existing(self.PUSH_FILE)
        old_pull = self._read_existing(self.PUT_FILE)

        os.system(f"rm -f {self.PUSH_FILE} {self.PUT_FILE}")

        old_all = self._read_existing(self.ALL_FILE_GIT)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            f_push = executor.submit(self.reposeWriteToFile, self.PUSH_FILE, self.exclude_dirs)
            f_pull = executor.submit(self.reposeWriteToFile, self.PUT_FILE, self.exclude_for_pull + self.exclude_dirs)
            f_all = executor.submit(self.reposeWriteToFile, self.ALL_FILE_GIT, [])
            new_push = f_push.result()
            new_pull = f_pull.result()
            new_all = f_all.result()

        self._print_diff("push-repos.txt", old_push, new_push)
        self._print_diff("pull-repos.txt", old_pull, new_pull)
        added_all = len(new_all - old_all)
        removed_all = len(old_all - new_all)
        if added_all or removed_all:
            print(f"[dim]all-repos.txt  [green]+{added_all}[/green] [red]-{removed_all}[/red]  total: {len(new_all)}[/dim]")
        else:
            print(f"[dim]all-repos.txt: no changes[/dim]")
        self._commit_to_git()

    def _print_diff(self, label, old, new):
        added = sorted(new - old)
        removed = sorted(old - new)

        if not added and not removed:
            print(f"[dim]{label}: no changes[/dim]")
            return

        lines = []
        for r in added:
            lines.append(f"  [green]+[/green] [green]{os.path.basename(r.rstrip('/'))}[/green]  [dim]{r}[/dim]")
        for r in removed:
            lines.append(f"  [red]-[/red] [red]{os.path.basename(r.rstrip('/'))}[/red]  [dim]{r}[/dim]")

        title = f"{label}  [green]+{len(added)}[/green] [red]-{len(removed)}[/red]  total: {len(new)}"
        print(Panel("\n".join(lines), title=title, style="dim"))

    def _commit_to_git(self):
        import shutil
        shutil.copy2(self.PUSH_FILE, self.PUSH_FILE_GIT)
        shutil.copy2(self.PUT_FILE, self.PUT_FILE_GIT)
        result = subprocess.run(
            ["git", "-C", PROJECT_ROOT, "diff", "--quiet", "push-repos.txt", "pull-repos.txt", "all-repos.txt"]
        )
        if result.returncode == 0:
            print("[dim]repos lists: no git changes[/dim]")
            return
        subprocess.run(["git", "-C", PROJECT_ROOT, "add", "push-repos.txt", "pull-repos.txt", "all-repos.txt"], check=True)
        subprocess.run(["git", "-C", PROJECT_ROOT, "commit", "-m", "upd: repos list"], check=True)
        print("[green]repos list committed to git[/green]")

    def reposeWriteToFile(self, file_path, exclude_dirs):
        base_command = [
            "find",
            os.path.expanduser("~"),
            "-maxdepth", "8",
            "-name", ".git",
            "-type", "d",
        ]
        for exclude in exclude_dirs:
            base_command.extend(["-not", "-path", f"*/{exclude}/*"])

        result = subprocess.run(base_command, stdout=subprocess.PIPE, text=True)

        git_paths = result.stdout.splitlines()
        filtered_paths = [path.replace(".git", "") for path in git_paths]

        with open(file_path, "w") as file:
            file.write("\n".join(filtered_paths))

        return set(filtered_paths)
