"""
Dashboard Header
"""

from rich.panel import Panel
from rich.table import Table
from rich.text import Text


def render(state):

    table = Table.grid(expand=True)

    table.add_column(justify="left", ratio=1)
    table.add_column(justify="right", ratio=1)

    table.add_row(
        f"[bold cyan]Target :[/bold cyan] {state.target}",
        f"[bold cyan]Profile :[/bold cyan] {state.profile}",
    )

    table.add_row(
        f"[bold cyan]Started :[/bold cyan] {state.started}",
        f"[bold cyan]Elapsed :[/bold cyan] {state.elapsed}",
    )

    return Panel(
        table,
        title=Text(
            "V I G I L",
            justify="center",
            style="bold bright_cyan",
        ),
        border_style="bright_cyan",
        padding=(0, 2),
        expand=True,
    )