from rich.panel import Panel
from rich.table import Table


ICONS = {
    "pending": "[bright_black]○[/bright_black]",
    "running": "[bold yellow]▶[/bold yellow]",
    "done": "[bold green]✓[/bold green]",
}


def render(state):
    """
    Scan Pipeline
    """

    table = Table.grid(expand=True)
    table.add_column()

    for stage in state.pipeline:

        icon = ICONS.get(
            stage["status"],
            "[bright_black]○[/bright_black]"
        )

        text = f"{icon} {stage['name']}"

        if stage["status"] == "running":
            text += " [yellow](Running)[/yellow]"

        table.add_row(text)

    return Panel(
        table,
        title="[bold bright_white]Pipeline[/bold bright_white]",
        border_style="cyan",
        padding=(0, 1),
    )