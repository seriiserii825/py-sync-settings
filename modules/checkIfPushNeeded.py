import git


def checkIfPushNeeded():
    # if exists .gpgrc and it's not empty
    my_repo = git.Repo('.')
    if my_repo.is_dirty(untracked_files=True):
        return True
    else:
        return False
