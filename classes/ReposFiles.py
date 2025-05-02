import os
import subprocess
from rich import print
from classes.CsvHandler import CsvHandler

class ReposFiles:
    PUSH_FILE = os.path.join(os.path.expanduser('~'), 'Documents', 'push-repos.txt')
    PUT_FILE = os.path.join(os.path.expanduser('~'), 'Documents', 'pull-repos.txt')
    def __init__(self):
        self.csvHandler = CsvHandler()
        self.exclude_dirs = self.csvHandler.getExcludeDirs()
        self.exclude_for_pull = self.csvHandler.getExcludeForPull()
        delete_files = input("[green]Do you want to delete the files? (y/n): ")
        if delete_files.lower() == 'y':
            self.deleteFiles()
            self.reposeWriteToFile(self.PUSH_FILE, self.exclude_dirs)
            self.reposeWriteToFile(self.PUT_FILE, self.exclude_for_pull + self.exclude_dirs)
        else:
            print("[red]Files not deleted.")

    def deleteFiles(self):
        os.system(f"rm {self.PUSH_FILE} {self.PUT_FILE}")

    def reposeWriteToFile(self, file_path, exclude_dirs):
        # Build the find command with exclusions
        base_command = ["find", os.path.expanduser("~"), "-maxdepth", "8", "-name", ".git", "-type", "d"]
        # pprint(exclude_dirs)
        for exclude in exclude_dirs:
            base_command.extend(["-not", "-path", f"*/{exclude}/*"])

        # Run the find command
        result = subprocess.run(base_command, stdout=subprocess.PIPE, text=True)

        # Process and write filtered paths
        git_paths = result.stdout.splitlines()
        filtered_paths = [path.replace(".git", "") for path in git_paths]
        with open(file_path, "w") as file:
            file.write("\n".join(filtered_paths))

        # file lines count
        print(f'[blue]Total repos found: {len(filtered_paths)}')
        # os.system(f"bat {file_push}")
