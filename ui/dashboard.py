"""
Live Dashboard
"""

import os
import time
import webbrowser
import subprocess

from rich.layout import Layout
from rich.live import Live

from ui.header import render as render_header
from ui.progress import render as render_progress
from ui.pipeline import render as render_pipeline
from ui.findings import render as render_findings
from ui.services import render as render_services
from ui.events import render as render_events
from ui.threat import render as render_threat
from ui.footer import render as render_footer


class Dashboard:

    def __init__(self, state):
        self.state = state

    # =====================================================
    # BUILD DASHBOARD
    # =====================================================

    def build(self):

        self.state.update_elapsed()

        layout = Layout(name="root")

        layout.split_column(
            Layout(name="header", size=5),
            Layout(name="progress", size=4),
            Layout(name="pipeline", size=12),
            Layout(name="middle", ratio=1),
            Layout(name="events", size=9),
            Layout(name="threat", size=9),
            Layout(name="footer", size=7),
        )

        layout["middle"].split_row(
            Layout(name="findings"),
            Layout(name="services"),
        )

        layout["header"].update(render_header(self.state))
        layout["progress"].update(render_progress(self.state))
        layout["pipeline"].update(render_pipeline(self.state))
        layout["findings"].update(render_findings(self.state))
        layout["services"].update(render_services(self.state))
        layout["events"].update(render_events(self.state))
        layout["threat"].update(render_threat(self.state))
        layout["footer"].update(render_footer(self.state))

        return layout

    # =====================================================
    # RUN
    # =====================================================

    def run(self):

        with Live(
            self.build(),
            refresh_per_second=10,
            screen=True,
            auto_refresh=False,
        ) as live:

            while not self.state.finished:

                live.update(
                    self.build(),
                    refresh=True,
                )

                time.sleep(0.1)

            live.update(
                self.build(),
                refresh=True,
            )

            while True:

                choice = input().strip().lower()

                if choice == "":

                    report = getattr(
                        self.state,
                        "report",
                        "Not Generated",
                    )

                    if report != "Not Generated":

                        try:

                            subprocess.Popen(
                                ["xdg-open", report],
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL,
                            )

                        except Exception:

                            pass

                elif choice == "q":

                    break