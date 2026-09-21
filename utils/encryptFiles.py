import hashlib
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


def _hash_cache_path(source_path):
    return f"{source_path}.sha256"


def _file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _folder_hash(folder_path):
    h = hashlib.sha256()
    for root, _, files in os.walk(folder_path):
        for name in sorted(files):
            file_path = os.path.join(root, name)
            h.update(os.path.relpath(file_path, folder_path).encode())
            h.update(_file_hash(file_path).encode())
    return h.hexdigest()


def _needs_encryption(source_path, gpg_path, hash_fn):
    if not os.path.isfile(gpg_path):
        return True
    cache_path = _hash_cache_path(source_path)
    if not os.path.isfile(cache_path):
        return True
    with open(cache_path) as f:
        cached_hash = f.read().strip()
    return cached_hash != hash_fn(source_path)


def _write_hash_cache(source_path, hash_fn):
    cache_path = _hash_cache_path(source_path)
    with open(cache_path, "w") as f:
        f.write(hash_fn(source_path))
    addToGitIgnore(cache_path)


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
    addToGitIgnore(folder_name)
    removeFileFromGitCache(file_path=folder_name)
    if not _needs_encryption(folder_name, line, _folder_hash):
        print(f"[yellow]Folder {folder_name} unchanged, skipping encryption")
        return
    if os.path.isfile(line):
        os.system(f"rm {line}")
    os.system(f"zip -r {zip_path} {folder_name}")
    os.system(f"gpg -e -r {recipient} {zip_path}")
    os.system(f"rm {zip_path}")
    _write_hash_cache(folder_name, _folder_hash)
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
                    removeFileFromGitCache(file_path=file_without_gpg)
                    addToGitIgnore(file_without_gpg)
                    if not os.path.isfile(file_without_gpg):
                        print(f"[red]File not found: {file_without_gpg}")
                        continue
                    if not _needs_encryption(
                        file_without_gpg, line, _file_hash
                    ):
                        print(
                            f"[yellow]{file_without_gpg} unchanged, "
                            "skipping encryption"
                        )
                        continue
                    if os.path.isfile(line):
                        os.system(f"rm {line}")
                    os.system(f"gpg -e -r {recipient} {file_without_gpg}")
                    _write_hash_cache(file_without_gpg, _file_hash)
                except Exception as e:
                    print(f"[red]Error encrypting file: {line}")
                    print(e)
