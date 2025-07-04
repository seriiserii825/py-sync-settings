def getLocalProjects(projects):
    # print(f"projects: {projects}")
    items = []
    for project in projects:
        if "Local" in project:
            items.append(project)
    return items
