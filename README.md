# 🛡️ VIGIL

> Open Source Vulnerability Assessment Framework

[Badges]

---

## Overview

Short description of VIGIL.

---

## Features

- Reconnaissance
- Enumeration
- Fingerprinting
- Vulnerability Detection
- CVE Mapping
- Risk Analysis
- HTML Reports
- Interactive Dashboard

---

## Screenshots

Dashboard

![Dashboard](screenshots/dashboard.png)

HTML Report

![Report](screenshots/report.png)

---

## Architecture

(Image)

---

## Workflow

Target
   ↓
Recon
   ↓
Enumeration
   ↓
Fingerprinting
   ↓
Scanning
   ↓
Vulnerability Detection
   ↓
CVE Mapping
   ↓
Risk Analysis
   ↓
HTML Report

---

## Installation

```bash
git clone https://github.com/Null-Trace0/Vigil.git

cd Vigil

chmod +x tools/install.sh

./tools/install.sh
```

---

## Usage

```bash
python main.py -d example.com
```

Skip Nuclei

```bash
python main.py -d example.com --skip-nuclei
```

Skip Nikto

```bash
python main.py -d example.com --skip-nikto
```

---

## Output

```
output/
reports/
logs/
```

---

## Project Structure

```
core/
ui/
tools/
reports/
output/
```

---

## Tools Used

| Tool | Purpose |
|------|---------|
| Nmap | Port Scanning |
| Nuclei | Vulnerability Detection |
| Subfinder | Recon |
| HTTPX | HTTP Probing |
| DNSX | DNS Enumeration |
| Katana | Crawling |
| WhatWeb | Fingerprinting |
| FFUF | Directory Discovery |
| Nikto | Web Server Scanning |

---

## Requirements

### Python

- rich
- requests
- jinja2
- beautifulsoup4
- pyyaml
- psutil
- lxml

### External Tools

- Nmap
- Nuclei
- FFUF
- WhatWeb
- Nikto
- Subfinder
- HTTPX
- DNSX
- Katana

---

## Roadmap

- PDF Reports
- Docker Support
- Multi-target Scanning
- API Scanning
- Plugin Support

---

## Contributing

Contributions are welcome.

---

## Reporting Issues

Open a GitHub Issue.

---

## Disclaimer

Use only on systems you own or are authorized to test.

---

## License

MIT License

---

## Acknowledgements

- Nmap
- ProjectDiscovery
- FFUF
- WhatWeb
- Nikto
- Python
- Rich
