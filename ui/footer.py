from pathlib import Path

from rich.panel import Panel
from rich.table import Table


def render(state):

    table = Table.grid(expand=True)
    table.add_column()

    if state.finished:

        report_name = "Not Generated"

        if getattr(state, "report", "Not Generated") != "Not Generated":
            report_name = Path(state.report).name

        table.add_row(
            "[bold green]✓ Assessment Completed[/bold green]"
        )

        table.add_row("")

        table.add_row(
            f"[bold cyan]📄 Report:[/bold cyan] [bold white]{report_name}[/bold white]"
        )

        table.add_row("")

        table.add_row(
            "[bright_cyan]▸[/bright_cyan] "
            "[bold black on bright_green] ENTER [/bold black on bright_green] "
            "[bold white]Launch Report[/bold white]"
        )

        table.add_row("")

        table.add_row(
            "[bright_cyan]▸[/bright_cyan] "
            "[bold black on bright_red]  Q  [/bold black on bright_red] "
            "[white]Exit Vigil[/white]"
        )

    else:

        table.add_row(
            "[bold cyan]Status:[/bold cyan] Running"
        )

        table.add_row(
            f"[bold cyan]Stage:[/bold cyan] {state.current_stage}"
        )

    return Panel(
        table,
        title="[bold cyan]VIGIL[/bold cyan]",
        border_style="bright_black",
        padding=(0, 1),
    )