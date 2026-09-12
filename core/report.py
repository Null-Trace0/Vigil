"""Standalone HTML reporting for VIGIL assessments."""

from datetime import datetime
from html import escape
from pathlib import Path
import re
from core.knowledgebase import KNOWLEDGEBASE

import config
from core import utils

REPORT_DIR = Path(config.REPORT_DIR)
SEVERITIES = ("critical", "high", "medium", "low", "info")
SEVERITY_LABELS = {
    "critical": "Critical", "high": "High", "medium": "Medium",
    "low": "Low", "info": "Info",
}


def run(scan, state):
    """Generate and register the final standalone assessment report."""
    state.add_event("[*] Generating Report")
    state.set_stage_running("Report")
    utils.create_directory(REPORT_DIR)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = REPORT_DIR / f"report_{timestamp}.html"
    utils.save_text(report_file, generate_html(scan))
    scan["report"] = str(report_file.resolve())
    state.set_report(str(report_file.resolve()))
    state.complete_stage("Report")
    return scan

# ==========================================================
# KNOWLEDGE LOOKUP
# ==========================================================

def get_vulnerability_details(title):
    """
    Returns description, impact and recommendation
    using keyword matching.
    """

    title_lower = title.lower()

    # Longest keywords first
    keywords = sorted(
        KNOWLEDGEBASE.keys(),
        key=len,
        reverse=True,
    )

    for keyword in keywords:

        if keyword in title_lower:
            return KNOWLEDGEBASE[keyword]

    return {
        "description":
            "No detailed description is currently available for this vulnerability.",

        "impact":
            "Potential security impact depends on the affected service and deployment.",

        "recommendation":
            "Review the finding manually, verify exploitability and apply the latest vendor security updates."
    }


# ==========================================================
# SEVERITY COLORS
# ==========================================================

def severity_color(severity):

    severity = severity.lower()

    colors = {
        "critical": "#ef4444",
        "high": "#f97316",
        "medium": "#facc15",
        "low": "#22c55e",
        "info": "#3b82f6",
    }

    return colors.get(
        severity,
        "#64748b",
    )

def generate_html(scan):
    """Assemble a complete, self-contained report document."""
    generated_at = datetime.now()
    return "\n".join((
        "<!doctype html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>VIGIL Assessment — {text(scan.get('target', 'Unknown target'))}</title>",
        f"<style>{build_css()}</style>",
        "</head><body>",
        build_header(scan, generated_at),
        '<main class="report-shell">',
        build_dashboard(scan),
        build_severity(scan),
        build_attack_surface(scan),
        build_host_information(scan),
        build_ports(scan),
        build_technologies(scan),
        build_vulnerabilities(scan),
        build_recommendations(scan),
        "</main>",
        build_footer(generated_at),
        "</body></html>",
    ))


def build_css():
    """Return all report styling; no external resources are required."""
    return r'''
:root{--bg:#0d1117;--surface:#161b22;--surface-2:#1f2630;--line:#30363d;--text:#e6edf3;--muted:#8b949e;--accent:#58a6ff;--critical:#ff4d5e;--high:#ff9b4a;--medium:#f2cc60;--low:#3fb950;--info:#58a6ff;--shadow:0 12px 32px rgba(0,0,0,.22)}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--text);font:15px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif}.report-shell,.hero-inner,.footer-inner{width:min(1180px,calc(100% - 40px));margin:auto}.hero{border-bottom:1px solid var(--line);background:radial-gradient(circle at 82% 0,#17335a 0,transparent 35%),linear-gradient(135deg,#0d1117,#161b22);padding:52px 0 38px}.eyebrow{margin:0 0 7px;color:#79c0ff;font-size:11px;font-weight:800;letter-spacing:.18em;text-transform:uppercase}.brand{font-size:clamp(42px,7vw,72px);line-height:1;letter-spacing:.15em;margin:0;font-weight:850}.subtitle{margin:13px 0 28px;color:var(--muted);font-size:17px}.meta-grid{display:flex;flex-wrap:wrap;gap:10px}.meta{background:rgba(22,27,34,.85);border:1px solid var(--line);border-radius:10px;padding:8px 12px;color:var(--muted);font-size:12px}.meta b{color:var(--text);font-weight:650}.risk-pill,.badge{display:inline-flex;align-items:center;border-radius:999px;font-size:11px;font-weight:800;letter-spacing:.05em;text-transform:uppercase;padding:5px 10px}.risk-pill{margin-left:5px}.section{padding:42px 0 4px}.section-head{display:flex;justify-content:space-between;gap:18px;align-items:end;margin-bottom:18px}.section-kicker{margin:0;color:var(--accent);font-weight:800;text-transform:uppercase;letter-spacing:.12em;font-size:11px}.section h2{font-size:25px;margin:2px 0 0;letter-spacing:-.03em}.section-intro{margin:0;color:var(--muted);max-width:600px}.grid{display:grid;gap:15px}.dashboard{grid-template-columns:repeat(4,1fr)}.surface-grid{grid-template-columns:repeat(5,1fr)}.stat-card,.severity-card,.panel,.finding,.recommendation{background:linear-gradient(145deg,var(--surface),#141a21);border:1px solid var(--line);border-radius:14px;box-shadow:var(--shadow)}.stat-card{padding:20px;transition:transform .2s ease,border-color .2s ease,box-shadow .2s ease}.stat-card:hover,.finding:hover,.recommendation:hover{transform:translateY(-4px);border-color:#57606a;box-shadow:0 16px 36px rgba(0,0,0,.3)}.stat-label{color:var(--muted);font-size:12px;text-transform:uppercase;font-weight:750;letter-spacing:.08em}.stat-value{display:block;font-size:31px;font-weight:800;letter-spacing:-.05em;margin-top:5px}.stat-note{display:block;color:var(--muted);font-size:12px;margin-top:4px}.severity-grid{grid-template-columns:repeat(5,1fr)}.severity-card{padding:16px;border-top:3px solid var(--tone)}.severity-card .count{font-size:26px;font-weight:800}.severity-card .name{color:var(--muted);font-size:12px;text-transform:uppercase;font-weight:700}.distribution{height:10px;border-radius:20px;background:#21262d;overflow:hidden;display:flex;margin-top:18px}.distribution span{height:100%;min-width:0}.panel{padding:20px;overflow:hidden}.table-wrap{overflow-x:auto}.data-table{border-collapse:collapse;width:100%;min-width:670px}.data-table th{font-size:11px;color:var(--muted);text-align:left;text-transform:uppercase;letter-spacing:.08em;padding:0 12px 11px;border-bottom:1px solid var(--line)}.data-table td{padding:13px 12px;border-bottom:1px solid rgba(48,54,61,.7);vertical-align:top}.data-table tr:last-child td{border:0}.data-table tr:hover td{background:rgba(88,166,255,.04)}.code{font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-size:13px}.badges{display:flex;gap:8px;flex-wrap:wrap}.tech-badge{padding:7px 11px;border:1px solid #2f81f7;border-radius:999px;background:rgba(56,139,253,.12);color:#b6e3ff;font-weight:650;font-size:13px}.finding-list{display:grid;gap:16px}.finding{padding:23px;border-left:4px solid var(--tone);transition:transform .2s ease,border-color .2s ease,box-shadow .2s ease}.finding-top{display:flex;align-items:flex-start;justify-content:space-between;gap:16px}.finding h3{margin:9px 0 2px;font-size:20px;line-height:1.3}.finding-meta{color:var(--muted);font-size:13px}.finding-meta strong{color:var(--text)}.finding-body{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:19px}.finding-copy{margin:5px 0 0;color:#c9d1d9}.finding-copy.empty{color:var(--muted);font-style:italic}.detail-label{margin:0;color:var(--muted);font-size:10px;font-weight:800;letter-spacing:.1em;text-transform:uppercase}.links{display:flex;flex-wrap:wrap;gap:7px;margin-top:6px}.links a{color:#79c0ff;text-decoration:none;border-bottom:1px solid rgba(121,192,255,.35)}.links a:hover{color:#fff}.recommendations{grid-template-columns:repeat(2,1fr)}.recommendation{display:flex;gap:16px;padding:18px;transition:transform .2s ease,border-color .2s ease}.priority{flex:0 0 38px;height:38px;display:grid;place-items:center;background:rgba(88,166,255,.15);border:1px solid rgba(88,166,255,.38);border-radius:10px;color:#79c0ff;font-weight:850}.recommendation h3{font-size:15px;margin:0 0 3px}.recommendation p{color:var(--muted);margin:0;font-size:13px}.empty-state{padding:28px;text-align:center;color:var(--muted);border:1px dashed #484f58;border-radius:14px}.footer{margin-top:52px;border-top:1px solid var(--line);background:#010409;padding:24px 0}.footer-inner{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;color:var(--muted);font-size:12px}.footer-brand{color:var(--text);font-weight:800;letter-spacing:.12em}.critical{background:rgba(255,77,94,.16);color:#ff9aa5}.high{background:rgba(255,155,74,.16);color:#ffc18e}.medium{background:rgba(242,204,96,.16);color:#f8e3a3}.low{background:rgba(63,185,80,.16);color:#7ee787}.info{background:rgba(88,166,255,.16);color:#a5d6ff}
@media(max-width:850px){.dashboard{grid-template-columns:repeat(2,1fr)}.surface-grid{grid-template-columns:repeat(3,1fr)}.severity-grid{grid-template-columns:repeat(3,1fr)}.finding-body{grid-template-columns:1fr}.section-head{display:block}.section-intro{margin-top:7px}}@media(max-width:520px){.report-shell,.hero-inner,.footer-inner{width:min(100% - 28px,1180px)}.hero{padding:36px 0 28px}.dashboard,.surface-grid,.severity-grid,.recommendations{grid-template-columns:1fr}.finding-top{display:block}.finding-top .badge{margin-top:12px}.section{padding-top:32px}}@media print{body{background:#fff;color:#111;font-size:11px}.hero,.footer{background:#fff;color:#111}.hero,.footer,.stat-card,.severity-card,.panel,.finding,.recommendation{box-shadow:none;border-color:#bbb}.subtitle,.meta,.stat-note,.section-intro,.finding-meta,.finding-copy.empty,.recommendation p,.footer-inner{color:#444}.meta{background:#fff}.section{padding-top:22px}.finding,.panel{break-inside:avoid}.stat-card:hover,.finding:hover{transform:none}.tech-badge{color:#14599c;border-color:#14599c;background:#fff}}
'''


def build_header(scan, generated_at):
    risk = scan.get("risk") or {}
    level = normalise_severity(risk.get("level", "Info"))
    duration = scan.get("duration", "Not recorded")
    return f'''<header class="hero"><div class="hero-inner">
<p class="eyebrow">Security Assessment Report</p><h1 class="brand">VIGIL</h1>
<p class="subtitle">Open Source Vulnerability Assessment Framework</p><div class="meta-grid">
<span class="meta">Target <b>{text(scan.get("target", "Unknown"))}</b></span>
<span class="meta">Generated <b>{generated_at.strftime("%d %b %Y, %H:%M:%S")}</b></span>
<span class="meta">Scan Duration <b>{text(duration)}</b></span>
<span class="meta">Overall Risk <span class="risk-pill {level}">{text(risk.get("level", "Informational"))}</span></span>
</div></div></header>'''


def build_dashboard(scan):
    risk = scan.get("risk") or {}
    findings = as_list(scan.get("vulnerabilities"))
    technologies = technology_list(scan)
    cards = (
        ("Risk Score", number(risk.get("score", 0)), "Weighted exposure score"),
        ("Overall Risk", risk.get("level", "Informational"), "Assessment posture"),
        ("Total Findings", risk.get("total_findings", len(findings)), "Validated scanner observations"),
        ("Technologies", len(technologies), "Detected platform components"),
    )
    content = "".join(f'<article class="stat-card"><span class="stat-label">{text(label)}</span><strong class="stat-value">{text(value)}</strong><span class="stat-note">{text(note)}</span></article>' for label, value, note in cards)
    return section("Executive Dashboard", "A concise view of the target's current security exposure.", f'<div class="grid dashboard">{content}</div>')


def build_severity(scan):
    summary = severity_summary(scan)
    total = sum(summary.values())
    cards = "".join(f'<article class="severity-card" style="--tone:var(--{severity})"><div class="count">{summary[severity]}</div><div class="name">{SEVERITY_LABELS[severity]}</div></article>' for severity in SEVERITIES)
    bar = "".join(f'<span style="background:var(--{severity});width:{(summary[severity] / total * 100) if total else 0:.2f}%"></span>' for severity in SEVERITIES)
    description = "Finding distribution by severity. " + (f"{total} finding{'s' if total != 1 else ''} identified." if total else "No findings were identified.")
    return section("Severity Overview", description, f'<div class="grid severity-grid">{cards}</div><div class="distribution" aria-label="Severity distribution">{bar}</div>')


def build_attack_surface(scan):
    recon = scan.get("recon") or {}
    enumeration = scan.get("enumeration") or {}
    items = (
        ("Subdomains", len(as_list(recon.get("subdomains")))), ("Alive Hosts", len(as_list(recon.get("alive_hosts")))),
        ("Open Ports", len(open_ports(scan))), ("Technologies", len(technology_list(scan))),
        ("DNS Records", len(as_list(recon.get("dns")))),
    )
    cards = "".join(f'<article class="stat-card"><span class="stat-label">{label}</span><strong class="stat-value">{value}</strong><span class="stat-note">{("Nmap target: " + text(enumeration.get("host"))) if label == "Open Ports" and enumeration.get("host") else "Discovered during assessment"}</span></article>' for label, value in items)
    return section("Attack Surface", "Externally visible assets and services discovered during reconnaissance.", f'<div class="grid surface-grid">{cards}</div>')


def build_host_information(scan):
    enumeration = scan.get("enumeration") or {}
    recon = scan.get("recon") or {}
    host = enumeration.get("hostname") or scan.get("target") or "Unavailable"
    rows = (
        ("Host", host), ("IP Address", enumeration.get("host")),
        ("Operating System", enumeration.get("os")), ("Status", enumeration.get("state") or "Unknown"),
        ("Alive Endpoints", len(as_list(recon.get("alive_hosts")))), ("WHOIS Data", "Collected" if recon.get("whois") else "Unavailable"),
    )
    table = "".join(f"<tr><th>{text(label)}</th><td>{text(value)}</td></tr>" for label, value in rows)
    return section("Host Information", "Primary host attributes identified during service enumeration.", f'<div class="panel table-wrap"><table class="data-table"><tbody>{table}</tbody></table></div>')


def build_ports(scan):
    ports = open_ports(scan)
    if not ports:
        content = '<div class="empty-state">No open ports were recorded during enumeration.</div>'
    else:
        rows = "".join(f"<tr><td class=\"code\">{text(port.get('port', '—'))}</td><td>{text(port.get('protocol', '—'))}</td><td>{text(port.get('service', 'Unknown'))}</td><td>{text(port.get('product', '—'))}</td><td>{text(port.get('version', '—'))}</td><td><span class=\"badge low\">{text(port.get('state', 'Unknown'))}</span></td></tr>" for port in ports)
        content = f'<div class="panel table-wrap"><table class="data-table"><thead><tr><th>Port</th><th>Protocol</th><th>Service</th><th>Product</th><th>Version</th><th>State</th></tr></thead><tbody>{rows}</tbody></table></div>'
    return section("Open Ports", "Services exposed by the enumerated target.", content)


def build_technologies(scan):
    technologies = technology_list(scan)
    content = '<div class="empty-state">No technologies were confidently identified.</div>' if not technologies else '<div class="panel"><div class="badges">' + "".join(f'<span class="tech-badge">{text(item)}</span>' for item in technologies) + "</div></div>"
    return section("Technologies", "Application and infrastructure technologies detected through fingerprinting.", content)


def build_vulnerabilities(scan):
    findings = as_list(scan.get("vulnerabilities"))
    if not findings:
        content = '<div class="empty-state">No vulnerabilities were identified by the configured scanners.</div>'
    else:
        content = '<div class="finding-list">' + "".join(build_finding(finding) for finding in findings if isinstance(finding, dict)) + "</div>"
    return section("Vulnerabilities", "Detailed findings, business impact, and remediation guidance.", content)


def build_finding(finding):

    severity = normalise_severity(
        finding.get("severity", "info")
    )

    # --------------------------------------------------
    # Knowledgebase lookup
    # --------------------------------------------------

    enrichment = knowledgebase_entry(finding)

    description = (
        finding.get("description")
        or enrichment.get("description")
    )

    impact = (
        finding.get("impact")
        or enrichment.get("impact")
    )

    recommendation = (
        finding.get("recommendation")
        or enrichment.get("recommendation")
    )

    cves = as_list(
        finding.get("cve")
    )

    references = references_for(
        finding
    )

    cve_text = (
        ", ".join(
            str(cve).upper()
            for cve in cves
            if cve
        )
        or "No CVE Assigned"
    )

    references_html = (
        '<span class="finding-copy empty">'
        'No public references available.'
        '</span>'
    )

    if references:

        references_html = (
            '<div class="links">'
            + "".join(
                f'<a href="{attribute(url)}" '
                f'target="_blank" '
                f'rel="noopener noreferrer">'
                f'{text(link_label(url))}'
                f'</a>'
                for url in references
            )
            + "</div>"
        )

    return f"""
<article class="finding" style="--tone:var(--{severity})">

<div class="finding-top">

<div>

<span class="badge {severity}">
{SEVERITY_LABELS[severity]}
</span>

<h3>{text(finding.get("title","Untitled Finding"))}</h3>

<div class="finding-meta">

<strong>Source:</strong>
{text(finding.get("source","Unknown"))}

&nbsp;&nbsp;|&nbsp;&nbsp;

<strong>CVSS:</strong>
{text(finding.get("cvss") or "N/A")}

&nbsp;&nbsp;|&nbsp;&nbsp;

<strong>CVE:</strong>
{text(cve_text)}

</div>

</div>

</div>

<div class="finding-body">

<div>

<p class="detail-label">
Description
</p>

{copy_block(
    description,
    "No description available."
)}

<p class="detail-label">
Security Impact
</p>

{copy_block(
    impact,
    "Impact not available."
)}

</div>

<div>

<p class="detail-label">
Recommendation
</p>

{copy_block(
    recommendation,
    "Review the affected service and apply the latest vendor security updates."
)}

<p class="detail-label">
References
</p>

{references_html}

</div>

</div>

</article>
"""

def build_recommendations(scan):
    recommendations = executive_recommendations(scan)
    cards = "".join(f'<article class="recommendation"><span class="priority">{index}</span><div><h3>{text(title)}</h3><p>{text(detail)}</p></div></article>' for index, (title, detail) in enumerate(recommendations, 1))
    return section("Executive Recommendations", "Prioritized actions derived from the observed attack surface and findings.", f'<div class="grid recommendations">{cards}</div>')


def build_footer(generated_at):
    return f'''<footer class="footer"><div class="footer-inner"><div><span class="footer-brand">VIGIL</span> &nbsp; Open Source Vulnerability Assessment Framework</div><div>Generated {generated_at.strftime("%d %b %Y, %H:%M:%S")} · Version {text(getattr(config, "VERSION", "Unknown"))} · Vigil by NullTrace</div></div></footer>'''

def section(title, intro, content):
    return f'<section class="section"><div class="section-head"><div><p class="section-kicker">VIGIL Assessment</p><h2>{text(title)}</h2></div><p class="section-intro">{text(intro)}</p></div>{content}</section>'


def severity_summary(scan):
    summary = {severity: 0 for severity in SEVERITIES}
    risk_summary = (scan.get("risk") or {}).get("summary") or {}
    if isinstance(risk_summary, dict):
        for key, value in risk_summary.items():
            severity = normalise_severity(key)
            summary[severity] += safe_int(value)
    if not any(summary.values()):
        for finding in as_list(scan.get("vulnerabilities")):
            if isinstance(finding, dict):
                summary[normalise_severity(finding.get("severity"))] += 1
    return summary


def technology_list(scan):
    technologies = (scan.get("fingerprint") or {}).get("technologies") or []
    if isinstance(technologies, str):
        technologies = [technologies]
    return sorted({str(item).strip() for item in technologies if str(item).strip()}, key=str.lower)


def open_ports(scan):
    ports = (scan.get("enumeration") or {}).get("ports") or []
    if not isinstance(ports, list):
        return []
    return [port for port in ports if isinstance(port, dict) and port.get("state", "open").lower() == "open"]


def knowledgebase_entry(finding):
    """
    Performs fuzzy keyword matching against the
    VIGIL knowledgebase.
    """

    ALIASES = {

        # FTP
        "ftp anonymous login": "anonymous ftp",
        "anonymous login": "anonymous ftp",
        "anonymous ftp": "anonymous ftp",

        # Default Credentials
        "default login": "default credentials",
        "default password": "default credentials",
        "weak password": "default credentials",
        "empty password": "default credentials",
        "default credentials": "default credentials",

        # RCE
        "remote code execution": "remote code execution",
        "command execution": "remote code execution",
        "code execution": "remote code execution",
        "rce": "remote code execution",

        # Directory Listing
        "directory browsing": "directory listing",
        "directory listing": "directory listing",
        "directory index": "directory listing",
        "index of": "directory listing",

        # HTTP
        "http trace": "http",
        "trace method": "http",
        "http service": "http",

        # Headers
        "missing security headers": "security headers",
        "security headers": "security headers",

        # SSL/TLS
        "tls": "ssl",
        "ssl": "ssl",

        # Servers
        "apache http server": "apache",
        "apache": "apache",
        "nginx": "nginx",
        "openssh": "openssh",
        "tomcat": "tomcat",
        "wordpress": "wordpress",
        "php": "php",

        # Services
        "ftp": "ftp",
        "smb": "smb",
        "rdp": "rdp",
        "postgresql": "postgresql",
        "postgres": "postgresql",
        "mysql": "mysql",
        "mariadb": "mysql",
        "vnc": "vnc",

        # Generic
        "information disclosure": "information",
        "information": "information",
        "enumeration": "enumeration",

    }

    searchable = " ".join(
        str(finding.get(key, ""))
        for key in (
            "title",
            "description",
            "service",
            "product",
        )
    ).lower()

    # ---------------------------------------
    # Alias matching
    # ---------------------------------------

    for alias, target in ALIASES.items():

        if alias in searchable:

            if target in KNOWLEDGEBASE:

                return KNOWLEDGEBASE[target]

    # ---------------------------------------
    # Generic keyword matching
    # ---------------------------------------

    keywords = sorted(
        KNOWLEDGEBASE.keys(),
        key=len,
        reverse=True,
    )

    for keyword in keywords:

        words = keyword.lower().split()

        if all(word in searchable for word in words):

            return KNOWLEDGEBASE[keyword]

    # ---------------------------------------
    # Default
    # ---------------------------------------

    return {

        "description":
            "No detailed description is currently available for this finding.",

        "impact":
            "Successful exploitation could negatively affect the confidentiality, integrity or availability of the affected system.",

        "recommendation":
            "Review this finding manually, verify exploitability and apply the latest vendor security updates."

    }


def references_for(finding):
    values = finding.get("references") or finding.get("reference") or finding.get("refs") or []
    if isinstance(values, str):
        values = re.split(r"[\s,]+", values)
    if not isinstance(values, (list, tuple, set)):
        return []
    return [str(value) for value in values if str(value).startswith(("http://", "https://"))]


def executive_recommendations(scan):
    summary = severity_summary(scan)
    findings_text = " ".join(str(finding.get("title", "")) + " " + str(finding.get("description", "")) for finding in as_list(scan.get("vulnerabilities")) if isinstance(finding, dict)).lower()
    recommendations = []
    if summary["critical"] or summary["high"]:
        recommendations.append(("Patch critical vulnerabilities", "Prioritize remediation and validation of all critical and high-severity findings."))
    if any(word in findings_text for word in ("outdated", "version", "apache", "nginx", "openssh", "wordpress")):
        recommendations.append(("Update outdated software", "Apply supported versions and security updates to identified services and application components."))
    if open_ports(scan):
        recommendations.append(("Reduce exposed services", "Review open ports, disable unnecessary services, and restrict administration interfaces to trusted networks."))
    fingerprint = scan.get("fingerprint") or {}
    headers = fingerprint.get("headers") or {}
    header_text = " ".join(str(key).lower() for key in headers) if isinstance(headers, dict) else ""
    if "https" not in findings_text:
        recommendations.append(("Enforce HTTPS", "Use modern TLS across the application and redirect all plaintext HTTP traffic to HTTPS."))
    if not any(header in header_text for header in ("content-security-policy", "strict-transport-security", "x-frame-options")):
        recommendations.append(("Implement security headers", "Deploy HSTS, Content-Security-Policy, clickjacking protection, and other appropriate browser security headers."))
    recommendations.append(("Establish continuous assessment", "Repeat scanning after remediation and incorporate authenticated testing and monitoring into the security program."))
    return recommendations[:5]


def normalise_severity(value):
    severity = str(value or "info").strip().lower()
    return "info" if severity in ("informational", "information", "unknown", "") or severity not in SEVERITIES else severity


def as_list(value):
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def safe_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def number(value):
    return value if value not in (None, "") else 0


def text(value):
    return escape(str(value if value not in (None, "") else "Unavailable"))


def attribute(value):
    return escape(str(value), quote=True)


def copy_block(value, fallback):
    if not value:
        return f'<p class="finding-copy empty">{text(fallback)}</p>'
    return f'<p class="finding-copy">{text(value)}</p>'


def link_label(url):
    return re.sub(r"^https?://", "", url).rstrip("/") or url
