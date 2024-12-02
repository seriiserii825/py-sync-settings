import git
from rich import print

def removeFileFromGitCache(repo_path='.', file_path=''):
    repo = git.Repo(repo_path)
    
    # Check if the file is in the Git index (staged for commit)
    if file_path in repo.index.entries:
        print(f"[blue]{file_path}[/] is in cache. Removing from cache...")
        
        # Remove the file from the Git index (equivalent to `git rm --cached file`)
        repo.index.remove([file_path], working_tree=False)
        repo.index.write()  # Save the updated index
        print(f"[blue]{file_path}[/] [red]removed from cache.")
    else:
        print(f"[blue]{file_path}[/] [green]is not in cache.")

