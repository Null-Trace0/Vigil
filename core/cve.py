"""
CVE Module

Responsible for mapping findings to public CVEs.
"""

import re

from core import utils


# ==========================================================
# PIPELINE
# ==========================================================

def run(scan, state):

    state.add_event("[*] Mapping CVEs")
    state.set_stage_running("CVE Mapping")

    findings = scan.get(
        "vulnerabilities",
        [],
    )

    total_cves = 0

    for finding in findings:

        cves = []

        if isinstance(
            finding.get("cve"),
            list,
        ):

            cves.extend(
                finding["cve"]
            )

        matches = re.findall(

            r"CVE-\d{4}-\d+",

            finding.get(
                "description",
                "",
            ),

            flags=re.IGNORECASE,

        )

        for match in matches:

            match = match.upper()

            if match not in cves:

                cves.append(match)

        finding["cve"] = sorted(
            list(set(cves))
        )

        total_cves += len(finding["cve"])

        if finding.get("cvss") is None:

            finding["cvss"] = severity_to_cvss(
                finding["severity"]
            )

    scan["vulnerabilities"] = findings

    state.set_finding(
        "CVEs",
        total_cves,
    )

    state.add_event(
        f"[+] {total_cves} CVEs Mapped"
    )

    state.complete_stage("CVE Mapping")

    state.set_progress(88)

    return scan


# ==========================================================
# FALLBACK CVSS
# ==========================================================

def severity_to_cvss(severity):

    mapping = {

        "critical": 9.8,

        "high": 8.0,

        "medium": 5.5,

        "low": 3.1,

        "info": 0.0,

        "informational": 0.0,

    }

    return mapping.get(
        severity.lower(),
        0.0,
    )