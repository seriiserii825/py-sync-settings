import os


class CsvHandler():
    ROOT_DIR = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
    EXCLUDE_DIRS_FILE = f'{ROOT_DIR}/exclude-dirs.csv'
    EXCLUDE_FOR_PULL_FILE = f'{ROOT_DIR}/exclude-for-pull.csv'
    def __init__(self):
        self.exclude_dirs = []
        self.exclude_for_pull = []
        self.readExcludeDirs(self.EXCLUDE_DIRS_FILE)
        self.readExcludeDirsForPull(self.EXCLUDE_FOR_PULL_FILE)


    def readExcludeDirs(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                self.exclude_dirs.append(line.strip())

    def readExcludeDirsForPull(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                self.exclude_for_pull.append(line.strip())
        
    def getExcludeDirs(self):
        return self.exclude_dirs

    def getExcludeForPull(self):
        return self.exclude_for_pull
