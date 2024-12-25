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
        self.readExcludeDirs()

    def readCsv(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                self.exclude_dirs.append(line.strip())

    def readExcludeDirs(self):
        self.readCsv(self.EXCLUDE_DIRS_FILE)
        self.readCsv(self.EXCLUDE_FOR_PULL_FILE)
        
    def getExcludeDirs(self):
        return self.exclude_dirs

    def getExcludeForPull(self):
        return self.exclude_for_pull
