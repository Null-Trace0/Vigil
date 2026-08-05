from rich.console import Group
from rich.progress_bar import ProgressBar
from rich.text import Text


def render(state):
    """
    Overall Scan Progress
    """

    progress = ProgressBar(
        total=100,
        completed=state.progress,
        width=None,
    )

    return Group(

        Text(
            "Overall Scan Progress",
            style="bold cyan",
        ),

        progress,

        Text(
            f"{state.progress}% Complete",
            style="bold white",
        ),

    )