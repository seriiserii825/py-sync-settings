import os
import subprocess

from rich import print
from rich.panel import Panel


def decryptFiles():
    if os.path.isfile(".gpgrc"):
        print("[green]Decrypting files")
        with open(".gpgrc", "r") as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                print(Panel(f"[blue]decrypt line: {line}"))
                file_without_gpg = line.replace(".gpg", "")
                if not os.path.isfile(line):
                    print(f"[red]GPG file not found: {line}")
                    continue
                result = subprocess.run(
                    ["gpg", "--output", file_without_gpg, "--yes", "--decrypt", line]
                )
                if result.returncode != 0:
                    print(f"[red]Failed to decrypt: {line}")
