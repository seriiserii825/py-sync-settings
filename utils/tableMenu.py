from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table


def tableMenu():
    table = Table(title="Star Wars Movies", row_styles=["none", "dim"])

    table.add_column("N%", justify="right", style="cyan", no_wrap=True)
    table.add_column("Title")

    table.add_row("1", "[green]feat(A new feature)")
    table.add_row("2", "[yellow]upd(An update to an existing feature)")
    table.add_row("3", "[red]bug-fix(A bug fix)")
    table.add_row("4", "[red]fix(A hotfix)")
    table.add_row("5", "[blue]core(An install a new package)")
    table.add_row("6", "[green]lazygit")
    table.add_row("7", "[red]exit(Exit the script)")
    console = Console()
    console.print(table)
    choose = Prompt.ask("Choose one", default="1")
    return choose
