"""
Copy of py_libs.Menu.select_fzf_menu (py-libs is not a dependency here).
"""
import subprocess
from typing import List, Optional

from rich.console import Console
from rich.text import Text

INDEX_COLOR = "magenta"


def _markup_to_ansi(label: str) -> str:
    console = Console(force_terminal=True, color_system="standard")
    with console.capture() as capture:
        console.print(Text.from_markup(label), end="")
    return capture.get()


class Menu:
    @classmethod
    def select_fzf_menu(
        cls,
        labels: List[str],
        title: Optional[str] = None,
        exit_label: Optional[str] = "[red]Exit",
    ) -> Optional[int]:
        """
        Colored fzf menu with indexes:
            01) [green]First
            02) [blue]Second
            00) [red]Exit

        labels may contain rich markup ("[green]ACF").
        Filter by text, or type an index and press Enter.
        Returns 1..len(labels) for an item, 0 for the exit item
        (exit_label=None hides it), None on Esc/Ctrl-C.
        """
        lines = [
            _markup_to_ansi(f"[{INDEX_COLOR}]{i:02d})[/] {label}")
            for i, label in enumerate(labels, start=1)
        ]
        if exit_label:
            exit_line = f"[{INDEX_COLOR}]00)[/] {exit_label}"
            lines.append(_markup_to_ansi(exit_line))
        cmd = [
            "fzf", "--ansi", "--reverse", "--no-mouse", "--no-sort",
            "--height", "50%", "--print-query",
        ]
        if title:
            cmd += ["--header", title]
        result = subprocess.run(
            cmd, input="\n".join(lines).encode(), stdout=subprocess.PIPE
        )
        if result.returncode not in (0, 1):
            return None
        output = result.stdout.decode().split("\n")
        query = output[0].strip()
        max_index = len(labels)
        if query.isdigit() and int(query) <= max_index:
            if int(query) or exit_label:
                return int(query)
        if len(output) > 1 and output[1].strip():
            return int(output[1].split(")", 1)[0])
        return None
