import os
import subprocess
from rich import print

def reposToFile(file_path):
    os.system(f"rm {file_path}")

  # Directories to exclude
    exclude_dirs = [
            "yay", 
            "cache",
            "autoload",
            "oh-my-zsh",
            "powerlevel10k",
            "Trash",
            "advanced-custom-fields-wpcli",
            "settingsSync",
            "oh-my-zsh",
            ".oh-my-zsh",
            "mysql",
            "Local Sites"
            ]

    # Remove the old file if it exists
    if os.path.exists(file_path):
        os.remove(file_path)

    # Build the find command with exclusions
    base_command = ["find", os.path.expanduser("~"), "-maxdepth", "8", "-name", ".git", "-type", "d"]
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

    # os.system(f"bat {file_path}")
