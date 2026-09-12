"""
core/recon.py

Reconnaissance Module
"""

from pathlib import Path

import config
from core import utils


OUTPUT = Path(config.OUTPUT_DIR) / "recon"


# ==========================================================
# RECON PIPELINE
# ==========================================================

def run(scan, state):
    """
    Recon Pipeline
    """

    utils.create_directory(OUTPUT)

    target = scan["target"]

    state.add_event("[*] Starting Recon")
    state.set_stage_running("Recon")

    # ------------------------------------------------------
    # SUBFINDER
    # ------------------------------------------------------

    subdomains = subfinder(target, state)

    state.set_progress(5)

    # ------------------------------------------------------
    # HTTPX
    # ------------------------------------------------------

    alive = httpx(state)

    state.set_progress(10)

    # ------------------------------------------------------
    # KATANA
    # ------------------------------------------------------

    katana_urls = katana(state)

    state.set_progress(13)

    # ------------------------------------------------------
    # DNSX
    # ------------------------------------------------------

    dns = dnsx(state)

    state.set_progress(15)

    # ------------------------------------------------------
    # WHOIS
    # ------------------------------------------------------

    whois_data = whois(target, state)

    state.set_progress(20)

    # ------------------------------------------------------
    # SAVE RESULTS
    # ------------------------------------------------------

    scan["recon"] = {
        "subdomains": subdomains,
        "alive_hosts": alive,
        "katana_urls": katana_urls,
        "dns": dns,
        "whois": whois_data,
    }

    utils.save_json(
        OUTPUT / "recon.json",
        scan["recon"],
    )

    state.complete_stage("Recon")

    state.add_event("[+] Recon Completed")

    return scan


# ==========================================================
# SUBFINDER
# ==========================================================

def subfinder(target, state):

    output = OUTPUT / "subdomains.txt"

    command = [
        "subfinder",
        "-d",
        target,
        "-silent",
        "-o",
        str(output),
    ]

    utils.run_command(command)

    subdomains = utils.read_lines(output)

    state.add_event(
        f"[+] {len(subdomains)} Subdomains Found"
    )

    return subdomains


# ==========================================================
# HTTPX
# ==========================================================

def httpx(state):

    input_file = OUTPUT / "subdomains.txt"
    output_file = OUTPUT / "alive.txt"

    command = [
        "httpx",
        "-silent",
        "-l",
        str(input_file),
        "-o",
        str(output_file),
    ]

    utils.run_command(command)

    alive = utils.read_lines(output_file)

    state.add_event(
        f"[+] {len(alive)} Alive Hosts"
    )

    return alive


# ==========================================================
# KATANA
# ==========================================================

def katana(state):

    input_file = OUTPUT / "alive.txt"
    output_file = OUTPUT / "katana.txt"

    if not input_file.exists():

        state.add_event("[!] Katana Input Missing")

        return []

    command = [
        "katana",
        "-list",
        str(input_file),
        "-silent",
        "-o",
        str(output_file),
    ]

    utils.run_command(
        command,
        timeout=300,
    )

    urls = utils.read_lines(output_file)

    state.add_event(
        f"[+] {len(urls)} URLs Discovered"
    )

    return urls


# ==========================================================
# DNSX
# ==========================================================

def dnsx(state):

    input_file = OUTPUT / "subdomains.txt"
    output_file = OUTPUT / "dns.txt"

    command = [
        "dnsx",
        "-silent",
        "-resp",
        "-a",
        "-aaaa",
        "-cname",
        "-mx",
        "-ns",
        "-l",
        str(input_file),
        "-o",
        str(output_file),
    ]

    utils.run_command(command)

    dns = utils.read_lines(output_file)

    state.add_event(
        f"[+] {len(dns)} DNS Records"
    )

    return dns


# ==========================================================
# WHOIS
# ==========================================================

def whois(target, state):

    command = [
        "whois",
        target,
    ]

    output = utils.run_command(command)

    if output is None:
        output = ""

    utils.save_text(
        OUTPUT / "whois.txt",
        output,
    )

    state.add_event(
        "[+] WHOIS Collected"
    )

    return output