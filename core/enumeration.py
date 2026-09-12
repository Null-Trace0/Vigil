"""
Enumeration Module

Responsible for enumerating discovered hosts and services.
"""

from pathlib import Path
import xml.etree.ElementTree as ET

import config
from core import utils

OUTPUT = Path(config.OUTPUT_DIR) / "enumeration"


# ==========================================================
# ENUMERATION PIPELINE
# ==========================================================

def run(scan, state):

    utils.create_directory(OUTPUT)

    target = scan["target"]

    xml_file = OUTPUT / "scan.xml"

    state.add_event("[*] Starting Enumeration")
    state.set_stage_running("Enumeration")
    state.set_progress(20)

    success = run_nmap(
        target,
        xml_file,
        state,
    )

    if success:

        results = parse_nmap(
            xml_file,
            state,
        )

    else:

        results = {}

    scan["enumeration"] = results

    utils.save_json(
        OUTPUT / "enumeration.json",
        results,
    )

    state.complete_stage("Enumeration")

    state.add_event(
        "[+] Enumeration Completed"
    )

    state.set_progress(35)

    return scan


# ==========================================================
# NMAP
# ==========================================================

def run_nmap(
    target,
    xml_file,
    state,
):

    state.add_event(
        "[*] Running Nmap Service Discovery"
    )

    command = [
        "nmap",
        "-Pn",
        "-sV",
        "--version-light",
        "-oX",
        str(xml_file),
        target,
    ]

    output = utils.run_command(
        command,
        timeout=300,
    )

    if output is None:

        state.add_event(
            "[!] Nmap Scan Failed"
        )

        return False

    state.add_event(
        "[+] Nmap Scan Completed"
    )

    return True

# ==========================================================
# XML PARSER
# ==========================================================

def parse_nmap(
    xml_file,
    state,
):

    if not xml_file.exists():

        state.add_event(
            "[!] scan.xml not found"
        )

        return {}

    try:

        tree = ET.parse(xml_file)

    except Exception:

        state.add_event(
            "[!] Invalid Nmap XML"
        )

        return {}

    root = tree.getroot()

    data = {

        "host": "",

        "hostname": "",

        "state": "",

        "os": "Unknown",

        "ports": [],

        "services": [],

        "technologies": [],

        "open_ports": 0,

    }

    host = root.find("host")

    if host is None:

        return data

    # ======================================================
    # Host IP
    # ======================================================

    address = host.find("address")

    if address is not None:

        data["host"] = address.attrib.get(
            "addr",
            "",
        )

    # ======================================================
    # Hostname
    # ======================================================

    hostnames = host.find("hostnames")

    if hostnames is not None:

        hostname = hostnames.find("hostname")

        if hostname is not None:

            data["hostname"] = hostname.attrib.get(
                "name",
                "",
            )

    # ======================================================
    # Host State
    # ======================================================

    status = host.find("status")

    if status is not None:

        data["state"] = status.attrib.get(
            "state",
            "",
        )

    # ======================================================
    # OS Detection
    # ======================================================

    os_node = host.find("os")

    if os_node is not None:

        match = os_node.find("osmatch")

        if match is not None:

            data["os"] = match.attrib.get(
                "name",
                "VM",
            )

    # ======================================================
    # Ports
    # ======================================================

    ports = host.find("ports")

    if ports is None:

        return data

    open_ports = 0

    for port in ports.findall("port"):

        state_node = port.find("state")

        service = port.find("service")

        port_data = {

            "port": int(
                port.attrib["portid"]
            ),

            "protocol": port.attrib["protocol"],

            "state": "",

            "service": "",

            "product": "",

            "version": "",

            "extrainfo": "",

        }

        if state_node is not None:

            port_data["state"] = state_node.attrib.get(
                "state",
                "",
            )

        if service is not None:

            port_data["service"] = service.attrib.get(
                "name",
                "",
            )

            port_data["product"] = service.attrib.get(
                "product",
                "",
            )

            port_data["version"] = service.attrib.get(
                "version",
                "",
            )

            port_data["extrainfo"] = service.attrib.get(
                "extrainfo",
                "",
            )

        data["ports"].append(port_data)

        # --------------------------------------------------
        # Open Port
        # --------------------------------------------------

        if port_data["state"] == "open":

            open_ports += 1

            data["services"].append({

                "port": port_data["port"],

                "protocol": port_data["protocol"],

                "service": port_data["service"],

                "product": port_data["product"],

                "version": port_data["version"],

            })

            technology = " ".join(

                filter(

                    None,

                    [

                        port_data["product"],

                        port_data["version"],

                    ],

                )

            ).strip()

            if (

                technology

                and technology

                not in data["technologies"]

            ):

                data["technologies"].append(
                    technology
                )

            service_text = (

                f"{port_data['port']}/"

                f"{port_data['protocol']} "

                f"{port_data['service']} "

                f"{port_data['product']} "

                f"{port_data['version']}"

            ).strip()

            state.add_service(
                service_text
            )

    # ======================================================
    # Summary
    # ======================================================

    data["open_ports"] = open_ports

    state.set_finding(

        "Open Ports",

        open_ports,

    )

    state.add_event(

        f"[+] {open_ports} Open Ports Found"

    )

    if data["os"] != "Unknown":

        state.add_event(

            f"[+] OS Detected: {data['os']}"

        )

    if data["hostname"]:

        state.add_event(

            f"[+] Hostname: {data['hostname']}"

        )

    if data["technologies"]:

        state.set_finding(

            "Technologies",

            len(data["technologies"])

        )

    return data
