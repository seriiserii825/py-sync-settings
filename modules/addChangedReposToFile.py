import os
from libs.appendToFile import appendToFile
from libs.hasInFile import hasInFile
from modules.getCommits import getTodayProjects
from modules.gitPush import getExcludedDirs


project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
changed_file = os.path.join(project_root, "changed-repos.txt")


def addChangedReposToFile(file_path):
    today_projects = getTodayProjects(file_path)
    print(f"{today_projects}: today_projects")
    for project in today_projects:
        os.chdir(project)
        cwd = os.getcwd()
        excluded_dirs = getExcludedDirs()
        if (
            (cwd not in excluded_dirs)
            and ("py-sync-settings" not in cwd)
            and not hasInFile(changed_file, cwd)
        ):
            appendToFile(changed_file, cwd)
