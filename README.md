<h1 align="center">Vigil</h1>

<p align="center">
  <strong>Automated Vulnerability Assessment Framework</strong>
</p>

<p align="center">
  Reconnaissance · Enumeration · Fingerprinting · Vulnerability Detection · CVE Mapping · Risk Analysis
</p>

---

**Vigil** is a CLI-based vulnerability assessment framework designed to automate the early stages of a security assessment.

It combines established security tools with structured processing, CVE mapping, risk analysis, remediation guidance, and HTML reporting while providing a live terminal dashboard throughout the assessment.

```text
                    TARGET
                      │
                      ▼
               RECONNAISSANCE
        Subfinder · HTTPX · DNSX
              Katana · WHOIS
                      │
                      ▼
                 ENUMERATION
                    Nmap
                      │
                      ▼
                FINGERPRINTING
                WhatWeb · curl
                      │
                      ▼
           VULNERABILITY DETECTION
                Nuclei · Nikto
                      │
                      ▼
                 CVE MAPPING
                      │
                      ▼
                 RISK ANALYSIS
                      │
                      ▼
                 HTML REPORT
```

> **Vigil performs vulnerability assessment and analysis only. It does not automatically exploit identified vulnerabilities.**

---

## Features

- Automated reconnaissance and target discovery
- Subdomain and DNS enumeration
- Live HTTP service discovery
- Web crawling and endpoint discovery
- WHOIS information collection
- Port, service, and version enumeration
- Technology and web stack fingerprinting
- HTTP header inspection
- Automated vulnerability detection
- CVE mapping and enrichment
- CVSS-based severity information
- Risk scoring and severity classification
- Remediation recommendations
- Interactive terminal dashboard
- Structured assessment output
- HTML vulnerability assessment reports
- Modular assessment pipeline

---

## Dashboard

Vigil provides a live terminal interface for monitoring the assessment as the pipeline executes.

<p align="center">
  <img src="screenshots/dashboard.png" width="95%" alt="Vigil interactive dashboard">
</p>

The dashboard provides visibility into the current pipeline stage, assessment progress, discovered services, findings, risk information, and runtime events.

---

## Installation

### Automated Setup

Clone the repository:

```bash
git clone https://github.com/Null-Trace0/Vigil.git
cd Vigil
```

Give the installer execute permission and run it using Bash:

```bash
chmod +x install.sh
bash install.sh
```

The installer supports Linux distributions using `pacman`, `apt`, or `dnf` and installs or verifies the dependencies required by Vigil.

After installation:

```bash
vigil --help
```

### Manual Setup

If the automated installer fails or your distribution is not supported, Vigil can be installed manually.

Ensure Python 3.10+, `pipx`, Git, Go, and the required external security tools are installed.

Install Vigil:

```bash
pipx install .
```

The following external tools must be available through your `PATH`:

```text
nmap
subfinder
httpx
dnsx
katana
nuclei
whatweb
nikto
curl
whois
```

Verify the installation:

```bash
vigil --help
```

---

## Usage

Run an assessment against a target:

```bash
vigil -d example.com
```

View available options:

```bash
vigil --help
```

Individual vulnerability scanners can be skipped when required:

```bash
vigil -d example.com --skip-nuclei
```

```bash
vigil -d example.com --skip-nikto
```

---

## Assessment Workflow

Vigil processes collected information through a sequential assessment pipeline.

### 1. Reconnaissance

```text
Subfinder  → Subdomain Discovery
HTTPX      → Live HTTP Service Discovery
DNSX       → DNS Enumeration
Katana     → Web Crawling and Endpoint Discovery
WHOIS      → Domain Registration Information
```

### 2. Enumeration

```text
Nmap       → Port, Service and Version Enumeration
```

### 3. Fingerprinting

```text
WhatWeb    → Web Technology Fingerprinting
curl       → HTTP Header Inspection
```

### 4. Vulnerability Detection

```text
Nuclei     → Template-Based Vulnerability Detection
Nikto      → Web Server Security Assessment
```

### 5. Analysis

Collected results are processed for:

```text
CVE Mapping
    ↓
CVSS Severity
    ↓
Risk Analysis
    ↓
Remediation Guidance
```

### 6. Reporting

Assessment data is consolidated into a structured HTML report.

---

## Assessment Report

Vigil generates an HTML report after completing the assessment.

<p align="center">
  <img src="screenshots/report-home.png" width="95%" alt="Vigil HTML vulnerability assessment report">
</p>

### Vulnerability Findings

Individual findings contain vulnerability details, severity information, impact, references, and remediation guidance where available.

<p align="center">
  <img src="screenshots/report-findings.png" width="95%" alt="Vigil vulnerability findings">
</p>

### Risk Overview

The report provides a summarized view of identified findings and their severity distribution.

<p align="center">
  <img src="screenshots/risk-overview.png" width="95%" alt="Vigil risk overview">
</p>

---

## Requirements

### Platform

Vigil is designed for Linux.

The automated installer supports distributions using:

| Package Manager | Distribution Family |
| --- | --- |
| `pacman` | Arch Linux, CachyOS and derivatives |
| `apt` | Debian, Ubuntu, Kali, Linux Mint and derivatives |
| `dnf` | Fedora and derivatives |

Some external tools may require additional installation methods depending on the distribution.

### Python

Vigil requires:

```text
Python 3.10+
```

Python package dependencies are handled automatically during installation.

### External Tools

| Tool | Purpose |
| --- | --- |
| Nmap | Port, service, and version enumeration |
| Subfinder | Subdomain discovery |
| HTTPX | Live HTTP service probing |
| DNSX | DNS enumeration |
| Katana | Web crawling and endpoint discovery |
| WHOIS | Domain registration information |
| WhatWeb | Web technology fingerprinting |
| curl | HTTP header inspection |
| Nuclei | Template-based vulnerability detection |
| Nikto | Web server security assessment |

---

## Generated Output

Vigil separates generated assessment data from the application itself.

```text
output/
├── recon/
├── enumeration/
├── fingerprint/
├── scanner/
└── vulnerability/

reports/
logs/
```

`output/` contains intermediate and structured assessment data produced by individual modules.

`reports/` contains generated HTML vulnerability assessment reports.

`logs/` contains runtime and assessment logs.

Generated assessment data is excluded from the repository by default.

---

## Limitations

Vigil automates parts of a vulnerability assessment, but automated results should not be treated as a replacement for manual validation.

Results may contain false positives, false negatives, incomplete CVE mappings, or findings requiring additional investigation.

Assessment coverage depends on the target, network accessibility, external tool capabilities, and vulnerability templates available at scan time.

Vigil does not automatically exploit detected vulnerabilities.

---

## Responsible Use

Vigil is intended for authorized security testing, security research, lab environments, and educational use.

Only scan systems that you own or have explicit permission to assess.

Users are responsible for ensuring their use of Vigil complies with applicable laws, regulations, scope restrictions, and authorization requirements.

The developers assume no responsibility for unauthorized or unlawful use of this software.

---

## License

Copyright © 2026 NullTrace.

Vigil is licensed under the **Apache License 2.0**. See the [LICENSE](LICENSE) file for the full license terms.