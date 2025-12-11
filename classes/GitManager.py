from git import Repo, GitError
from typing import Optional


class GitManager:
    def __init__(self, path: str = "."):
        try:
            self.repo = Repo(path)
        except GitError:
            raise Exception(f"Directory '{path}' is not a git repository")

    # --- Basic operations ---

    def has_changes(self) -> bool:
        """Return True if there are uncommitted changes."""
        return self.repo.is_dirty(untracked_files=True)

    def add_all(self):
        """git add ."""
        self.repo.git.add(A=True)

    def commit(self, message: str):
        """git commit -m message"""
        if not self.has_changes():
            return False
        self.repo.index.commit(message)
        return True

    def push(self, remote_name: str = "origin", branch: Optional[str] = None):
        """git push"""
        remote = self.repo.remote(remote_name)
        if branch:
            remote.push(branch)
        else:
            remote.push()

    def fetch(self, remote_name: str = "origin"):
        """git fetch"""
        remote = self.repo.remote(remote_name)
        remote.fetch()

    def pull(self, remote_name: str = "origin", branch: Optional[str] = None):
        """git pull"""
        remote = self.repo.remote(remote_name)
        if branch:
            remote.pull(branch)
        else:
            remote.pull()

    # --- Advanced checks for pull/push ---

    def local_head(self) -> str:
        """Return local commit hash."""
        return self.repo.head.commit.hexsha

    def remote_head(self, remote_name: str = "origin", branch: str = "HEAD") -> Optional[str]:
        """Return remote commit hash."""
        remote = self.repo.remote(remote_name)
        for ref in remote.refs:
            if ref.name.endswith(branch):
                return ref.commit.hexsha
        return None

    def needs_pull(self, remote_name: str = "origin", branch: str = "main") -> bool:
        """Check if local branch is behind remote."""
        self.fetch(remote_name)
        try:
            local = self.local_head()
            remote = self.remote_head(remote_name, branch)
            return local != remote
        except Exception:
            return False

    def needs_push(self) -> bool:
        """Check if there are commits ahead of remote."""
        try:
            return bool(list(self.repo.iter_commits('@{0}..@{u}')))
        except Exception:
            return False

    # --- Utility ---

    def status(self) -> str:
        """Human-readable git status."""
        return self.repo.git.status()
