"""
core/utils.py

Common helper functions used throughout Vigil.
"""

import json
import shutil
import subprocess
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

import config


console = Console(stderr=True)


# =====================================================
# Banner
# =====================================================

def banner():
    """        ╱──────────────╲
          ╱────                ────╲
      ╱───                          ───╲

               ⟨  V I G I L  ⟩

      ╲───                          ───╱
          ╲────                ────╱
               ╲──────────────╱"""

    title = Text(config.APP_NAME, style="bold cyan")
    version = Text(f"Version {config.VERSION}", style="green")

    console.print(
        Panel.fit(
            f"""
Open Source Vulnerability Assessment Framework

""",
            title=title,
            subtitle=version,
            border_style="cyan",
        )
    )


# =====================================================
# Logging
# =====================================================

def info(message):
    console.print(f"[cyan][INFO][/cyan] {message}")


def success(message):
    console.print(f"[green][SUCCESS][/green] {message}")


def warning(message):
    console.print(f"[yellow][WARNING][/yellow] {message}")


def error(message):
    console.print(f"[bold red][ERROR][/bold red] {message}")


# =====================================================
# Directory Helpers
# =====================================================

def create_directory(path):
    """Create directory if it doesn't exist."""

    Path(path).mkdir(
        parents=True,
        exist_ok=True,
    )


def create_output_folders():

    folders = [
        "output",
        "output/recon",
        "output/enumeration",
        "output/fingerprint",
        "output/scanner",
        "output/vulnerability",
        "reports",
        "logs",
    ]

    for folder in folders:
        create_directory(folder)


# =====================================================
# File Helpers
# =====================================================

def save_text(path, text):

    with open(path, "w") as file:
        file.write(text)


def append_text(path, text):

    with open(path, "a") as file:
        file.write(text)


def read_text(path):

    with open(path, "r") as file:
        return file.read()


def read_lines(path):

    if not Path(path).exists():
        return []

    with open(path, "r") as file:

        return [
            line.strip()
            for line in file
            if line.strip()
        ]


# =====================================================
# JSON
# =====================================================

def save_json(path, data):

    with open(path, "w") as file:

        json.dump(
            data,
            file,
            indent=4,
        )


def load_json(path):

    with open(path, "r") as file:

        return json.load(file)


# =====================================================
# Command Runner
# =====================================================

def run_command(command, timeout=120):

    try:

        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

    except subprocess.TimeoutExpired:

        error(f"Command timed out ({timeout}s)")
        return None

    except KeyboardInterrupt:

        warning("Interrupted by user.")
        return None

    except Exception as e:

        error(str(e))
        return None

    if process.returncode != 0:

        if process.stderr.strip():

            error(process.stderr.strip())

        return None

    return process.stdout

# =====================================================
# Dependency Checker
# =====================================================

def check_dependencies():

    missing = []

    for tool in config.REQUIRED_TOOLS:

        if shutil.which(tool) is None:

            missing.append(tool)

    if missing:

        console.print()

        error("Missing Dependencies")

        for tool in missing:

            console.print(f"   - {tool}")

        raise SystemExit(1)

    console.print(
    "[bold green]✓[/bold green] All dependencies installed."
    )


# =====================================================
# Statistics
# =====================================================

def count_lines(path):

    return len(read_lines(path))


# =====================================================
# Generic Parser
# =====================================================

def command_output_to_list(command):

    output = run_command(command)

    if output is None:
        return []

    return [

        line.strip()

        for line in output.splitlines()

        if line.strip()

    ]