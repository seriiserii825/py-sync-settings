import os
import subprocess
from rich import print

def reposToFile(file_push, file_pull):
    os.system(f"rm {file_push} {file_pull}")

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
            ]
    exclude_for_pull = [
            "Local Sites",
            "wp-projects",
            "laravel",
            "vue",
            "nuxt",
            "nvim-coc",
            "mjml",
            "php-oop"
            ]

    # Remove the old file if it exists
    if os.path.exists(file_push):
        os.remove(file_push)

    if os.path.exists(file_pull):
        os.remove(file_pull)


    def reposeWriteToFile(file_path, exclude_dirs):
        # Build the find command with exclusions
        base_command = ["find", os.path.expanduser("~"), "-maxdepth", "8", "-name", ".git", "-type", "d"]
        for exclude in exclude_dirs:
            base_command.extend(["-not", "-path", f"*/{exclude}/*"])

        # Run the find command
        result = subprocess.run(base_command, stdout=subprocess.PIPE, text=True)

        # Process and write filtered paths
        git_paths = result.stdout.splitlines()
        filtered_paths = [path.replace(".git", "") for path in git_paths]
        with open(file_push, "w") as file:
            file.write("\n".join(filtered_paths))

        # file lines count
        print(f'[blue]Total repos found: {len(filtered_paths)}')
        # os.system(f"bat {file_push}")

    reposeWriteToFile(file_push, exclude_dirs)
    reposeWriteToFile(file_pull, exclude_for_pull + exclude_dirs)
