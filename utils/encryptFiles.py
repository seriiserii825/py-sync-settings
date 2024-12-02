import os
from rich import print

from modules.removeFileFromGitCache import removeFileFromGitCache
user = os.getlogin()

def addToGitIgnore(filename):
    with open('.gitignore', 'r') as file:
        file.seek(0)
        lines = file.readlines()
        lines = [line.replace('\n', '') for line in lines]
    if filename not in lines:
        command = f'echo {filename} >> .gitignore'
        os.system(command)

def encryptFiles():
    if os.path.isfile('.gpgrc'):
        print(f'[green]Encrypting files')
        with open('.gpgrc', 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.replace('\n', '')
                print(f"line: {line}")
                file_without_gpg = line.replace('.gpg', '')
                print(f"file_without_gpg: {file_without_gpg}")
                if os.path.isfile(line):
                    os.system(f'rm {line}')
                removeFileFromGitCache(file_path=file_without_gpg)
                addToGitIgnore(file_without_gpg)
                file_without_gpg = line.replace('.gpg', '')
                os.system(f'gpg -e -r {user} {file_without_gpg}')
