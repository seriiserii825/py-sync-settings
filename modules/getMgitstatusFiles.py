from classes.Mgitstatus import Mgitstatus


def getMgitstatusFiles():
    ms = Mgitstatus()
    # ms.get_all_repos()
    ms.exclude_repos()
