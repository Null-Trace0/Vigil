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

    subdomains = subfinder(target, state)
    state.add_event(
        f"[+] {len(subdomains)} Subdomains Found"
    )

    state.set_progress(5)

    # ------------------------------------------------------

    alive = httpx(state)

    state.set_progress(10)

    state.add_event(
        f"[+] {len(alive)} Alive Hosts"
    )

    # ------------------------------------------------------

    dns = dnsx(state)

    state.set_progress(15)

    state.add_event("[+] DNS Enumeration Finished")

    # ------------------------------------------------------

    whois_data = whois(target, state)

    state.set_progress(20)

    # ------------------------------------------------------

    scan["recon"] = {

        "subdomains": subdomains,

        "alive_hosts": alive,

        "dns": dns,

        "whois": whois_data,

    }

    utils.save_json(

        OUTPUT / "recon.json",

        scan["recon"]

    )

    # ------------------------------------------------------

    state.complete_stage("Recon")

    state.add_event("[+] Recon Completed")

    return scan


# ==========================================================
# SUBFINDER
# ==========================================================

def subfinder(target, state):

    output = OUTPUT / "subdomains.txt"

    command = (

        f"subfinder "

        f"-d {target} "

        f"-silent "

        f"-o {output}"

    )

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

    command = (

        f"httpx "

        f"-silent "

        f"-l {input_file} "

        f"-o {output_file}"

    )

    utils.run_command(command)

    alive = utils.read_lines(output_file)

    state.add_event(

        f"[+] {len(alive)} Alive Hosts"

    )

    return alive


# ==========================================================
# DNSX
# ==========================================================

def dnsx(state):

    input_file = OUTPUT / "subdomains.txt"

    output_file = OUTPUT / "dns.txt"

    command = (

        f"dnsx "

        f"-silent "

        f"-resp "

        f"-a "

        f"-aaaa "

        f"-cname "

        f"-mx "

        f"-ns "

        f"-l {input_file} "

        f"-o {output_file}"

    )

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

    output = utils.run_command(

        f"whois {target}"

    )

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