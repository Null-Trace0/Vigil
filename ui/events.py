from rich.panel import Panel
from rich.table import Table

MAX_EVENTS = 8


def render(state):
    """
    Live Events Panel
    """

    table = Table.grid(expand=True)
    table.add_column()

    if not state.events:

        table.add_row(
            "[bright_black]Waiting for events...[/bright_black]"
        )

    else:

        for event in state.events[-MAX_EVENTS:]:

            style = "white"

            if "[+]" in event:
                style = "green"

            elif "[!]" in event:
                style = "red"

            elif "[*]" in event:
                style = "yellow"

            table.add_row(
                f"[{style}]{event}[/{style}]"
            )

    return Panel(
        table,
        title="[bold bright_white]Live Events[/bold bright_white]",
        border_style="cyan",
        padding=(0, 1),
    )