"""
Scanner Module

Responsible for launching vulnerability scanners.

Runs:
    - Nuclei
    - Nikto
"""

from pathlib import Path
import json
import subprocess

import config
from core import utils

OUTPUT = Path(config.OUTPUT_DIR) / "scanner"


# ==========================================================
# PIPELINE
# ==========================================================

def run(scan, state):

    utils.create_directory(OUTPUT)

    target = scan["target"]

    state.add_event("[*] Starting Vulnerability Scan")
    state.set_stage_running("Vulnerability Detection")
    state.set_progress(55)

    nuclei_results = []
    nikto_results = ""

    # -------------------------------------------------
    # NUCLEI
    # -------------------------------------------------

    if scan.get("skip_nuclei", False):

        state.add_event("[*] Skipping Nuclei")

    else:

        nuclei_results = run_nuclei(target, state)

    state.set_progress(60)

    # -------------------------------------------------
    # NIKTO
    # -------------------------------------------------

    if scan.get("skip_nikto", False):

        state.add_event("[*] Skipping Nikto")

    else:

        nikto_results = run_nikto(target, state)

    state.set_progress(65)

    # -------------------------------------------------

    results = {
        "nuclei": nuclei_results,
        "nikto": nikto_results,
    }

    utils.save_json(
        OUTPUT / "scanner.json",
        results,
    )

    scan["scanner"] = results

    state.complete_stage("Vulnerability Detection")

    state.add_event("[+] Vulnerability Scan Completed")

    return scan


# ==========================================================
# NUCLEI
# ==========================================================

def run_nuclei(target, state):

    state.add_event("[*] Running Nuclei")

    output = OUTPUT / "nuclei.json"

    command = [
        "nuclei",
        "-u",
        f"http://{target}",
        "-jsonl",
        "-o",
        str(output),
    ]

    try:

        subprocess.run(
            command,
            timeout=600,
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    except subprocess.TimeoutExpired:

        state.add_event("[!] Nuclei Timed Out")

        return []

    except Exception as e:

        state.add_event(f"[!] Nuclei Error: {e}")

        return []

    findings = []

    if output.exists():

        for line in utils.read_lines(output):

            try:
                findings.append(json.loads(line))
            except Exception:
                continue

    state.set_finding(
        "CVEs",
        len(findings),
    )

    state.add_event(
        f"[+] Nuclei: {len(findings)} Findings"
    )

    return findings


# ==========================================================
# NIKTO
# ==========================================================

def run_nikto(target, state):

    state.add_event("[*] Running Nikto")

    output = OUTPUT / "nikto.txt"

    command = [
        "nikto",
        "-host",
        f"http://{target}",
        "-output",
        str(output),
    ]

    try:

        subprocess.run(
            command,
            timeout=90,
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    except subprocess.TimeoutExpired:

        state.add_event("[!] Nikto Timed Out")

        return ""

    except Exception as e:

        state.add_event(f"[!] Nikto Error: {e}")

        return ""

    if not output.exists():

        state.add_event("[!] Nikto Output Missing")

        return ""

    result = utils.read_text(output)

    state.add_event("[+] Nikto Completed")

    return result