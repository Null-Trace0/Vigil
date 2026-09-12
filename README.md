# Vigil

Vigil is a CLI-based vulnerability assessment framework built to automate the early stages of a security assessment.

It combines reconnaissance, web crawling, service enumeration, technology fingerprinting, vulnerability detection, CVE mapping, risk analysis, and HTML reporting into a single workflow while providing a live terminal dashboard throughout the assessment.

---

## Features

- Automated reconnaissance and target discovery
- Subdomain and DNS enumeration
- Live host discovery
- Web crawling and endpoint discovery
- Domain registration and WHOIS collection
- Port, service, and version enumeration
- Technology and web stack fingerprinting
- HTTP header inspection
- Automated vulnerability detection
- CVE mapping and enrichment
- CVSS-based severity information
- Risk scoring and severity classification
- Remediation recommendations
- Interactive terminal dashboard
- Structured scan output
- HTML vulnerability assessment reports
- Modular assessment pipeline

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

After installation, verify Vigil:

```bash
vigil --help
```

### Manual Setup

If the automated installer fails or your distribution is not supported, Vigil can be installed manually.

Ensure Python 3.10+, `pipx`, Git, Go, and the required external security tools are installed.

Install Vigil from the repository:

```bash
pipx install .
```

Ensure the following tools are installed and available in your `PATH`:

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

View all available options:

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

Vigil is designed for vulnerability assessment and does not perform automated exploitation.

---

## Workflow

Vigil processes collected information through a sequential assessment pipeline.

```text
Target
  │
  ▼
Reconnaissance
  │
  ├── Subfinder
  ├── HTTPX
  ├── DNSX
  ├── Katana
  └── WHOIS
  │
  ▼
Enumeration
  │
  └── Nmap
  │
  ▼
Fingerprinting
  │
  ├── WhatWeb
  └── curl
  │
  ▼
Vulnerability Detection
  │
  ├── Nuclei
  └── Nikto
  │
  ▼
CVE Mapping
  │
  ▼
Risk Analysis
  │
  ▼
HTML Report
```

Information collected during one stage is passed to later stages, allowing Vigil to build a more complete assessment instead of running each tool independently.

---

## Interactive Dashboard

Vigil provides a live terminal dashboard while an assessment is running.

The dashboard displays assessment information such as:

- Current pipeline stage
- Assessment progress
- Live events
- Discovered services
- Vulnerability findings
- Risk information
- Scan statistics

This allows the assessment to be monitored without waiting for the final report to be generated.

---

## Requirements

### Platform

Vigil is designed for Linux.

The automated installer includes support for distributions using:

- `pacman` — Arch Linux and derivatives such as CachyOS
- `apt` — Debian, Ubuntu, Kali, Linux Mint, and derivatives
- `dnf` — Fedora and derivatives

Some tools may require additional installation methods depending on the distribution.

### Python

Vigil requires:

```text
Python 3.10+
```

Python package dependencies are handled automatically during installation.

### External Tools

| Tool | Purpose |
| --- | --- |
| Nmap | Port scanning, service and version enumeration |
| Subfinder | Subdomain discovery |
| HTTPX | Live HTTP service probing |
| DNSX | DNS enumeration |
| Katana | Web crawling and endpoint discovery |
| WHOIS | Domain registration and ownership information |
| WhatWeb | Web technology fingerprinting |
| curl | HTTP header and response inspection |
| Nuclei | Template-based vulnerability detection |
| Nikto | Web server security assessment |

All required tools should be available through the user's `PATH`.

---

## Generated Output

Generated data is stored under the appropriate output, report, and log directories.

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

The `output/` directory contains intermediate and structured assessment data produced by the different modules, including reconnaissance, discovered endpoints, enumeration results, fingerprinting data, and scanner output.

The `reports/` directory contains generated HTML vulnerability assessment reports.

The `logs/` directory contains runtime and assessment logs.

---

## Screenshots

### Interactive Dashboard

The terminal dashboard provides live visibility into the assessment while the pipeline is running.

<p align="center">
  <img src="screenshots/dashboard.png" width="95%" alt="Vigil interactive dashboard">
</p>

### HTML Report

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

The report provides a summarized view of the identified findings and their severity distribution.

<p align="center">
  <img src="screenshots/risk-overview.png" width="95%" alt="Vigil risk overview">
</p>

---

## Limitations

Vigil automates parts of a vulnerability assessment, but automated scanner results should not be treated as a replacement for manual validation.

Results may include false positives, false negatives, incomplete CVE mappings, or findings that require additional investigation.

Assessment coverage depends on the target, network accessibility, external tool capabilities, and vulnerability templates available at scan time.

Vigil does not automatically exploit detected vulnerabilities.

---

## Responsible Use

Vigil is intended for authorized security testing, security research, lab environments, and educational use.

Only scan systems that you own or have explicit permission to assess.

Users are responsible for ensuring that their use of Vigil complies with applicable laws, regulations, scope restrictions, and authorization requirements.

The developers assume no responsibility for unauthorized or unlawful use of this software.

---

## License

Copyright © 2026 NullTrace.

Vigil is licensed under the **Apache License 2.0**. See the [LICENSE](LICENSE) file for the full license terms.