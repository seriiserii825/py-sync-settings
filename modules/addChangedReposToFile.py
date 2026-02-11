import os
from libs.appendToFile import appendToFile
from libs.hasInFile import hasInFile
from modules.getCommits import getTodayProjects
from modules.gitPush import getExcludedDirs


project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
changed_file = os.path.join(project_root, "changed-repos.txt")


def addChangedReposToFile(file_path):
    today_projects = getTodayProjects(file_path)
    excluded_dirs = getExcludedDirs()
    for project in today_projects:
        os.chdir(project)
        cwd = os.getcwd()
        is_excluded = any(excluded in cwd for excluded in excluded_dirs)
        if (
            not is_excluded
            and ("py-sync-settings" not in cwd)
            and not hasInFile(changed_file, cwd)
        ):
            appendToFile(changed_file, cwd)
