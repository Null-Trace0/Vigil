"""
Vigil
Open Source Vulnerability Assessment Framework
"""

import argparse
import threading
import traceback

from core import (
    recon,
    enumeration,
    fingerprint,
    scanner,
    vulnerability,
    cve,
    risk,
    report,
    utils,
)

from ui.dashboard import Dashboard
from ui.state import state
from datetime import datetime


# ==========================================================
# Arguments
# ==========================================================

def parse_arguments():

    parser = argparse.ArgumentParser(
        prog="Vigil",
        description="Open Source Vulnerability Assessment Framework",
    )

    parser.add_argument(
        "-d",
        "--domain",
        required=True,
        help="Target domain",
    )

    parser.add_argument(
        "--skip-nuclei",
        action="store_true",
    )

    parser.add_argument(
        "--skip-nikto",
        action="store_true",
    )

    return parser.parse_args()


# ==========================================================
# Safe Module Runner
# ==========================================================

def execute(module, scan):

    try:
        return module(scan, state)

    except Exception as e:

        state.add_event(f"[!] {module.__module__}: {e}")

        traceback.print_exc()

        return scan


# ==========================================================
# Main
# ==========================================================

def main():

    args = parse_arguments()

    utils.check_dependencies()

    state.reset()
    state.target = args.domain
    start_time = datetime.now()

    dashboard = Dashboard(state)

    dashboard_thread = threading.Thread(
        target=dashboard.run,
        daemon=True,
    )

    dashboard_thread.start()

    scan = {

        "target": args.domain,

        "skip_nuclei": args.skip_nuclei,

        "skip_nikto": args.skip_nikto,

        "recon": {},

        "enumeration": {},

        "fingerprint": {},

        "scanner": {},

        "vulnerabilities": [],

        "risk": {},

        "report": {},

    }

    # -----------------------------
    # Pipeline
    # -----------------------------

    scan = execute(recon.run, scan)

    scan = execute(enumeration.run, scan)

    scan = execute(fingerprint.run, scan)

    scan = execute(scanner.run, scan)

    scan = execute(vulnerability.run, scan)

    scan = execute(cve.run, scan)

    scan = execute(risk.run, scan)

    end_time = datetime.now()

    scan["duration"] = str(
        end_time - start_time
    ).split(".")[0]


    scan = execute(report.run, scan)
   
    # -----------------------------
    # Finish Dashboard
    # -----------------------------

    state.finish()

    dashboard_thread.join()

    utils.success("Assessment Completed Successfully.")


if __name__ == "__main__":
    main()