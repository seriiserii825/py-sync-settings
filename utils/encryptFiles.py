import os

from rich import print

from modules.removeFileFromGitCache import removeFileFromGitCache

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_BLUELINE_CSV = os.path.join(_PROJECT_ROOT, "blueline.csv")


def _load_blueline_paths():
    if not os.path.isfile(_BLUELINE_CSV):
        return set()
    with open(_BLUELINE_CSV, "r") as f:
        return {os.path.expanduser(line.strip()) for line in f if line.strip()}


def _get_recipient():
    blueline_paths = _load_blueline_paths()
    cwd = os.getcwd()
    if cwd in blueline_paths:
        return "blueline"
    return os.getlogin()


def addToGitIgnore(filename):
    if os.path.isfile(".gitignore"):
        with open(".gitignore", "r") as file:
            lines = [line.replace("\n", "") for line in file.readlines()]
    else:
        lines = []
    if filename not in lines:
        with open(".gitignore", "a") as file:
            file.write(f"{filename}\n")


def encryptFiles():
    if os.path.isfile(".gpgrc"):
        print("[green]Encrypting files")
        recipient = _get_recipient()
        with open(".gpgrc", "r") as file:
            lines = file.readlines()
            for line in lines:
                try:
                    line = line.replace("\n", "")
                    print(f"line: {line}")
                    file_without_gpg = line.replace(".gpg", "")
                    print(f"file_without_gpg: {file_without_gpg}")
                    if os.path.isfile(line):
                        os.system(f"rm {line}")
                    removeFileFromGitCache(file_path=file_without_gpg)
                    addToGitIgnore(file_without_gpg)
                    file_without_gpg = line.replace(".gpg", "")
                    os.system(f"gpg -e -r {recipient} {file_without_gpg}")
                except Exception as e:
                    print(f"[red]Error encrypting file: {line}")
                    print(e)
