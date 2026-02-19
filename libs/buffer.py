import os
import subprocess

import plyer
import pyperclip


def _is_wayland():
    return bool(os.getenv("WAYLAND_DISPLAY"))


def _is_x11():
    return bool(os.getenv("DISPLAY"))


def addToClipboard(text: str):
    text = text.strip()

    try:
        if _is_wayland():
            subprocess.run(
                ["wl-copy"],
                input=text.encode(),
                check=True
            )
        elif _is_x11():
            subprocess.run(
                ["xclip", "-selection", "clipboard"],
                input=text.encode(),
                check=True
            )
        else:
            pyperclip.copy(text)
    except Exception:
        pyperclip.copy(text)

    plyer.notification.notify(
        title="Buffer",
        message=text,
        app_name="Buffer",
        timeout=5
    )


def addToClipboardFile(file: str):
    try:
        if _is_wayland():
            cmd = ["wl-copy"]
        elif _is_x11():
            cmd = ["xclip", "-selection", "clipboard"]
        else:
            raise RuntimeError("No GUI session")

        with open(file, "rb") as f:
            subprocess.run(cmd, stdin=f, check=True)

    except Exception as e:
        raise RuntimeError(f"Clipboard copy failed: {e}")


def getFromClipboard() -> str:
    try:
        if _is_wayland():
            return subprocess.check_output(["wl-paste"]).decode().strip()
        elif _is_x11():
            return subprocess.check_output(
                ["xclip", "-o", "-selection", "clipboard"]
            ).decode().strip()
        else:
            return pyperclip.paste().strip()
    except Exception:
        return pyperclip.paste().strip()
