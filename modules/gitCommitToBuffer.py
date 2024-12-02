import git
from datetime import datetime

from libs.buffer import addToClipBoard
def gitCommitToBuffer():
# Open the existing git repository
    repo = git.Repo('.')

# Define the time (you mentioned 3am, so we'll assume today at 3am)
    since_time = datetime.now().replace(hour=3, minute=0, second=0, microsecond=0)

# Get the git log messages since 3am, in reverse order
    commits = repo.iter_commits(since=since_time, reverse=True)

# Collect commit messages
    commit_messages = [commit.message.strip() for commit in commits]
    #remove feat: from commit_messages
    clear_messages = []
    for message in commit_messages:
        clear_messages.append(message.replace('feat:',''))

# Print the commit messages
    print("Commit messages since 3am:")
    message_text = '\n'.join(clear_messages)
    addToClipBoard(message_text)
