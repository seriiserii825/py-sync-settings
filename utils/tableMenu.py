from libs.Menu import Menu

EXIT_CHOICE = "7"


def tableMenu():
    """Commit type menu; returns "1".."6" for an item, "7" for Exit / Esc."""
    choice = Menu.select_fzf_menu(
        [
            "[green]feat[/] (A new feature)",
            "[yellow]upd[/] (An update to an existing feature)",
            "[red]bug-fix[/] (A bug fix)",
            "[red]fix[/] (A hotfix)",
            "[blue]core[/] (An install a new package)",
            "[green]lazygit",
        ],
        title="Commit type",
    )
    return str(choice) if choice else EXIT_CHOICE
