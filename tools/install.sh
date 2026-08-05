#!/usr/bin/env bash

# ==========================================================
# VIGIL Installer
# Open Source Vulnerability Assessment Framework
# ==========================================================

set -e

GREEN="\033[1;32m"
RED="\033[1;31m"
YELLOW="\033[1;33m"
BLUE="\033[1;34m"
NC="\033[0m"

echo -e "${BLUE}"
echo "========================================"
echo "      VIGIL Dependency Installer"
echo "========================================"
echo -e "${NC}"

# ==========================================================
# Detect Package Manager
# ==========================================================

if command -v pacman >/dev/null 2>&1; then
    DISTRO="arch"

elif command -v apt >/dev/null 2>&1; then
    DISTRO="debian"

elif command -v dnf >/dev/null 2>&1; then
    DISTRO="fedora"

else
    echo -e "${RED}Unsupported Linux Distribution${NC}"
    exit 1
fi

echo -e "${GREEN}Detected:${NC} $DISTRO"

# ==========================================================
# Install System Packages
# ==========================================================

case "$DISTRO" in

arch)

sudo pacman -Sy --needed \
python \
python-pip \
python-virtualenv \
git \
go \
nmap \
base-devel

;;

debian)

sudo apt update

sudo apt install -y \
python3 \
python3-pip \
python3-venv \
git \
golang \
nmap \
ffuf

;;

fedora)

sudo dnf install -y \
python3 \
python3-pip \
git \
golang \
nmap \
ffuf

;;

esac

# ==========================================================
# Virtual Environment
# ==========================================================

if [ ! -d ".venv" ]; then

    echo -e "${GREEN}Creating Virtual Environment...${NC}"

    python -m venv .venv

fi

source .venv/bin/activate

# ==========================================================
# Python Packages
# ==========================================================

echo -e "${GREEN}Installing Python Packages...${NC}"

pip install --upgrade pip

pip install -r requirements.txt

# ==========================================================
# ProjectDiscovery Tools
# ==========================================================

echo -e "${GREEN}Installing ProjectDiscovery Tools...${NC}"

go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/projectdiscovery/httpx/cmd/httpx@latest
go install github.com/projectdiscovery/dnsx/cmd/dnsx@latest
go install github.com/projectdiscovery/katana/cmd/katana@latest
go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest

export PATH="$PATH:$HOME/go/bin"

# ==========================================================
# FFUF
# ==========================================================

if ! command -v ffuf >/dev/null 2>&1; then

    echo
    echo -e "${YELLOW}FFUF is not installed.${NC}"

    if command -v yay >/dev/null 2>&1; then

        yay -S --noconfirm ffuf

    elif command -v paru >/dev/null 2>&1; then

        paru -S --noconfirm ffuf

    else

        echo
        echo "Please install FFUF manually:"
        echo "https://github.com/ffuf/ffuf"
        echo

    fi

fi

# ==========================================================
# WhatWeb
# ==========================================================

if ! command -v whatweb >/dev/null 2>&1; then

    echo
    echo -e "${YELLOW}WhatWeb is not installed.${NC}"

    if command -v yay >/dev/null 2>&1; then

        yay -S --noconfirm whatweb

    elif command -v paru >/dev/null 2>&1; then

        paru -S --noconfirm whatweb

    else

        echo "Please install WhatWeb manually."

    fi

fi

# ==========================================================
# Nikto
# ==========================================================

if ! command -v nikto >/dev/null 2>&1; then

    echo
    echo -e "${YELLOW}Nikto is not installed.${NC}"

    if command -v yay >/dev/null 2>&1; then

        yay -S --noconfirm nikto

    elif command -v paru >/dev/null 2>&1; then

        paru -S --noconfirm nikto

    else

        echo "Please install Nikto manually."

    fi

fi

# ==========================================================
# Verify
# ==========================================================

echo
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}Verification${NC}"
echo -e "${BLUE}========================================${NC}"

verify() {

    if command -v "$1" >/dev/null 2>&1; then

        echo -e "[${GREEN}✔${NC}] $1"

    else

        echo -e "[${RED}✘${NC}] $1"

    fi

}

verify python
verify git
verify go
verify nmap
verify nuclei
verify subfinder
verify httpx
verify dnsx
verify katana
verify ffuf
verify whatweb
verify nikto

echo
echo -e "${GREEN}Installation Complete!${NC}"
echo
echo "Activate the virtual environment:"
echo
echo "source .venv/bin/activate"
echo
echo "Run VIGIL:"
echo
echo "python main.py -d example.com"
