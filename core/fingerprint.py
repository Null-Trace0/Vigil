"""
Fingerprint Module

Responsible for identifying technologies used by the target.
"""

from pathlib import Path
import re

import config
from core import utils

OUTPUT = Path(config.OUTPUT_DIR) / "fingerprint"


# ==========================================================
# PIPELINE
# ==========================================================

def run(scan, state):

    utils.create_directory(OUTPUT)

    target = scan["target"]

    state.add_event("[*] Starting Fingerprinting")
    state.set_stage_running("Fingerprinting")
    state.set_progress(35)

    # ------------------------------------------------------

    whatweb = run_whatweb(target, state)

    state.set_progress(40)

    # ------------------------------------------------------

    headers = get_headers(target, state)

    state.set_progress(45)

    # ------------------------------------------------------

    technologies = extract_technologies(
        whatweb,
        headers,
        state,
    )

    results = {

        "whatweb": whatweb,

        "headers": headers,

        "technologies": technologies,

    }

    utils.save_json(
        OUTPUT / "fingerprint.json",
        results,
    )

    scan["fingerprint"] = results

    state.complete_stage("Fingerprinting")

    state.add_event("[+] Fingerprinting Completed")

    state.set_progress(50)

    return scan


# ==========================================================
# WHATWEB
# ==========================================================

def run_whatweb(target, state):

    state.add_event("[*] Running WhatWeb")

    output_file = OUTPUT / "whatweb.txt"

    command = (
        f"whatweb "
        f"--no-errors "
        f"--log-brief={output_file} "
        f"http://{target}"
    )

    output = utils.run_command(
        command,
        timeout=180,
    )

    if output is None:

        state.add_event("[!] WhatWeb Timed Out")

        return ""

    if not output_file.exists():

        utils.save_text(output_file, output)

    state.add_event("[+] WhatWeb Finished")

    return utils.read_text(output_file)


# ==========================================================
# HTTP HEADERS
# ==========================================================

def get_headers(target, state):

    state.add_event("[*] Collecting HTTP Headers")

    command = (
        f"curl "
        f"-I "
        f"-L "
        f"-s "
        f"--max-time 20 "
        f"http://{target}"
    )

    output = utils.run_command(
        command,
        timeout=30,
    )

    if output is None:

        state.add_event("[!] Failed To Collect Headers")

        return {}

    utils.save_text(
        OUTPUT / "headers.txt",
        output,
    )

    headers = {}

    for line in output.splitlines():

        if ":" not in line:

            continue

        key, value = line.split(":", 1)

        headers[key.strip()] = value.strip()

    state.add_event(
        f"[+] {len(headers)} Headers Collected"
    )

    return headers


# ==========================================================
# TECHNOLOGY EXTRACTION
# ==========================================================

def extract_technologies(
    whatweb,
    headers,
    state,
):

    technologies = []

    patterns = [

        "Apache",
        "Nginx",
        "LiteSpeed",
        "PHP",
        "WordPress",
        "Drupal",
        "Joomla",
        "Laravel",
        "Cloudflare",
        "OpenResty",
        "MySQL",
        "MariaDB",
        "Bootstrap",
        "jQuery",
        "React",
        "Vue",
        "Angular",

    ]

    text = whatweb + "\n"

    for key, value in headers.items():

        text += f"{key}: {value}\n"

    for pattern in patterns:

        if re.search(
            pattern,
            text,
            re.IGNORECASE,
        ):

            technologies.append(pattern)

    technologies = sorted(set(technologies))

    for tech in technologies:

        state.add_event(f"[+] {tech} Detected")

    state.set_finding(
        "Technologies",
        len(technologies),
    )

    return technologies