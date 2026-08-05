"""
Findings Panel
"""

from rich.panel import Panel
from rich.table import Table


def render(state):

    table = Table.grid(expand=True)

    table.add_column(
        justify="left",
        ratio=3,
    )

    table.add_column(
        justify="right",
        ratio=1,
    )

    for key, value in state.findings.items():

        table.add_row(

            f"[bold]{key}[/bold]",

            f"[bold bright_cyan]{value}[/bold bright_cyan]",

        )

    return Panel(

        table,

        title="[bold bright_white]Findings[/bold bright_white]",

        border_style="bright_cyan",

        padding=(0, 1),

        expand=True,

    )