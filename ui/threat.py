from rich.console import Group
from rich.panel import Panel
from rich.progress_bar import ProgressBar
from rich.text import Text


LEVELS = [

    ("Critical", "red"),

    ("High", "dark_orange"),

    ("Medium", "yellow"),

    ("Low", "green"),

]


def render(state):
    """
    Threat Level Panel
    """

    components = []

    maximum = max(

        max(state.threat.values()),

        1,

    )

    for level, color in LEVELS:

        value = state.threat.get(
            level,
            0,
        )

        title = Text()

        title.append(
            f"{level:<10}",
            style=f"bold {color}",
        )

        title.append(
            f"{value}",
            style="bold white",
        )

        components.append(title)

        components.append(

            ProgressBar(

                total=maximum,

                completed=value,

                width=None,

            )

        )

        components.append(Text())

    return Panel(

        Group(*components),

        title="[bold bright_white]Threat Overview[/bold bright_white]",

        border_style="cyan",

        padding=(0, 1),

    )