import os

LOCAL_SITES_DIR = os.path.join(os.path.expanduser("~"), "Local Sites")


def getLocalProjects(projects):
    items = []
    for project in projects:
        if project.startswith(LOCAL_SITES_DIR + os.sep):
            items.append(project)
    return items
