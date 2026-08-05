"""
Risk Assessment Module

Responsible for calculating overall risk.
"""

SEVERITY_WEIGHT = {
    "critical": 10,
    "high": 7,
    "medium": 4,
    "low": 2,
    "info": 1,
    "informational": 1,
}


def run(scan, state):

    state.add_event("[*] Calculating Risk Score")
    state.set_stage_running("Risk Analysis")

    findings = scan.get("vulnerabilities", [])

    summary = {
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
        "info": 0,
    }

    score = 0

    for finding in findings:

        severity = finding.get("severity", "info").lower()

        if severity not in summary:
            severity = "info"

        summary[severity] += 1
        score += SEVERITY_WEIGHT.get(severity, 1)

    risk_level = calculate_risk_level(score)

    scan["risk"] = {
        "score": score,
        "level": risk_level,
        "summary": summary,
        "total_findings": len(findings),
    }

    state.set_threat("Critical", summary["critical"])
    state.set_threat("High", summary["high"])
    state.set_threat("Medium", summary["medium"])
    state.set_threat("Low", summary["low"])

    state.add_event(f"[+] Risk Score: {score}")
    state.add_event(f"[+] Overall Risk: {risk_level}")

    state.complete_stage("Risk Analysis")

    state.set_progress(95)

    return scan


def calculate_risk_level(score):

    if score >= 80:
        return "Critical"

    if score >= 50:
        return "High"

    if score >= 25:
        return "Medium"

    if score >= 10:
        return "Low"

    return "Informational"