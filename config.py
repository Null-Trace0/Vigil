"""
Vigil Configuration File

This file contains all configurable values used throughout the application.
Changing values here updates them across the entire project.
"""

# ========================
# Application Information
# ========================

APP_NAME = "Vigil"
VERSION = "0.1.0"

# ========================
# Project Directories
# ========================

OUTPUT_DIR = "output"
REPORT_DIR = "reports"
LOG_DIR = "logs"
TEMPLATE_DIR = "templates"

# ========================
# External Tools
# ========================

REQUIRED_TOOLS = [
    "subfinder",
    "dnsx",
    "httpx",
    "katana",
    "nmap",
    "whatweb",
    "nikto",
    "nuclei",
    "curl",
    "whois",
]