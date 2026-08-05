"""
Services Panel
"""

from rich.panel import Panel
from rich.table import Table


MAX_SERVICES = 8


def render(state):

    table = Table.grid(expand=True)

    table.add_column()

    services = state.services[:MAX_SERVICES]

    if not services:

        table.add_row(
            "[bright_black]Waiting for service detection...[/bright_black]"
        )

    else:

        for service in services:

            table.add_row(
                f"[bold green]•[/bold green] {service}"
            )

    remaining = len(state.services) - MAX_SERVICES

    if remaining > 0:

        table.add_row("")

        table.add_row(
            f"[bright_black]+ {remaining} more...[/bright_black]"
        )

    return Panel(

        table,

        title="[bold bright_white]Services[/bold bright_white]",

        border_style="bright_cyan",

        padding=(0, 1),

        expand=True,

    )