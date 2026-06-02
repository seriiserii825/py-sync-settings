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


def _encrypt_folder(line, recipient):
    zip_path = line.replace(".gpg", "")       # http.zip
    folder_name = zip_path.replace(".zip", "") # http
    if not os.path.isdir(folder_name):
        print(f"[red]Folder not found: {folder_name}")
        return
    if os.path.isfile(line):
        os.system(f"rm {line}")
    os.system(f"zip -r {zip_path} {folder_name}")
    os.system(f"gpg -e -r {recipient} {zip_path}")
    os.system(f"rm {zip_path}")
    addToGitIgnore(folder_name)
    removeFileFromGitCache(file_path=folder_name)
    print(f"[green]Folder {folder_name} encrypted → {line}")


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
                    if line.endswith(".zip.gpg"):
                        _encrypt_folder(line, recipient)
                        continue
                    file_without_gpg = line.replace(".gpg", "")
                    print(f"file_without_gpg: {file_without_gpg}")
                    if os.path.isfile(line):
                        os.system(f"rm {line}")
                    removeFileFromGitCache(file_path=file_without_gpg)
                    addToGitIgnore(file_without_gpg)
                    os.system(f"gpg -e -r {recipient} {file_without_gpg}")
                except Exception as e:
                    print(f"[red]Error encrypting file: {line}")
                    print(e)
