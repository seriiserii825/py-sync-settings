import os
import subprocess

from rich import print
from rich.panel import Panel


def _decrypt_folder(line):
    zip_path = line.replace(".gpg", "")       # http.zip
    folder_name = zip_path.replace(".zip", "") # http
    if not os.path.isfile(line):
        print(f"[red]GPG file not found: {line}")
        return
    result = subprocess.run(
        ["gpg", "--output", zip_path, "--yes", "--decrypt", line]
    )
    if result.returncode != 0:
        print(f"[red]Failed to decrypt: {line}")
        return
    os.system(f"unzip -o {zip_path}")
    os.system(f"rm {zip_path}")
    print(f"[green]Folder {folder_name} decrypted from {line}")


def decryptFiles():
    if os.path.isfile(".gpgrc"):
        print("[green]Decrypting files")
        with open(".gpgrc", "r") as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                print(Panel(f"[blue]decrypt line: {line}"))
                if line.endswith(".zip.gpg"):
                    _decrypt_folder(line)
                    continue
                file_without_gpg = line.replace(".gpg", "")
                if not os.path.isfile(line):
                    print(f"[red]GPG file not found: {line}")
                    continue
                result = subprocess.run(
                    ["gpg", "--output", file_without_gpg, "--yes", "--decrypt", line]
                )
                if result.returncode != 0:
                    print(f"[red]Failed to decrypt: {line}")
