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

STEP_PAUSE=0.8

pause_step() {
    sleep "$STEP_PAUSE"
}

echo -e "${BLUE}"
echo "========================================"
echo "           VIGIL Installer"
echo "========================================"
echo -e "${NC}"

pause_step

# ==========================================================
# Detect Linux Distribution
# ==========================================================

if command -v pacman >/dev/null 2>&1; then
    DISTRO="arch"

elif command -v apt >/dev/null 2>&1; then
    DISTRO="debian"

elif command -v dnf >/dev/null 2>&1; then
    DISTRO="fedora"

else
    echo -e "${RED}Unsupported Linux distribution.${NC}"
    exit 1
fi

echo -e "${GREEN}Detected:${NC} $DISTRO"

pause_step

# ==========================================================
# Install Base Dependencies
# ==========================================================

echo
echo -e "${GREEN}Installing system dependencies...${NC}"

pause_step

case "$DISTRO" in

arch)

    sudo pacman -S --needed --noconfirm \
        python \
        python-pip \
        python-pipx \
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
        pipx \
        git \
        golang \
        nmap \
        ffuf
    ;;

fedora)

    sudo dnf install -y \
        python3 \
        python3-pip \
        pipx \
        git \
        golang \
        nmap \
        ffuf
    ;;

esac

pause_step

# ==========================================================
# Local Binary Directory
# ==========================================================

mkdir -p "$HOME/.local/bin"

export PATH="$HOME/.local/bin:$PATH"
export GOBIN="$HOME/.local/bin"

# ==========================================================
# Install Vigil
# ==========================================================

echo
echo -e "${BLUE}[→]${NC} Installing Vigil..."

pause_step

if pipx list 2>/dev/null | grep -q "package vigil"; then

    echo -e "${YELLOW}Vigil is already installed. Updating...${NC}"

    pipx install . --force

else

    pipx install .

fi

echo -e "${GREEN}[✔] Vigil installed${NC}"

pause_step

# ==========================================================
# ProjectDiscovery Tools
# ==========================================================

echo
echo -e "${GREEN}Installing ProjectDiscovery tools...${NC}"

pause_step

install_go_tool() {

    local name="$1"
    local package="$2"

    echo
    echo -e "${BLUE}[→]${NC} Installing $name..."

    sleep 0.4

    GOBIN="$HOME/.local/bin" go install "$package"

    echo -e "${GREEN}[✔]${NC} $name installed"

    sleep 0.4
}

install_go_tool \
    "Subfinder" \
    "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"

install_go_tool \
    "HTTPX" \
    "github.com/projectdiscovery/httpx/cmd/httpx@latest"

install_go_tool \
    "DNSX" \
    "github.com/projectdiscovery/dnsx/cmd/dnsx@latest"

install_go_tool \
    "Katana" \
    "github.com/projectdiscovery/katana/cmd/katana@latest"

install_go_tool \
    "Nuclei" \
    "github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest"

pause_step

# ==========================================================
# FFUF
# ==========================================================

if ! command -v ffuf >/dev/null 2>&1; then

    echo
    echo -e "${BLUE}[→]${NC} Installing FFUF..."

    pause_step

    if command -v yay >/dev/null 2>&1; then

        yay -S --noconfirm ffuf

    elif command -v paru >/dev/null 2>&1; then

        paru -S --noconfirm ffuf

    else

        GOBIN="$HOME/.local/bin" \
            go install github.com/ffuf/ffuf/v2@latest

    fi

    echo -e "${GREEN}[✔] FFUF installed${NC}"

    pause_step

fi

# ==========================================================
# WhatWeb
# ==========================================================

if ! command -v whatweb >/dev/null 2>&1; then

    echo
    echo -e "${BLUE}[→]${NC} Installing WhatWeb..."

    pause_step

    case "$DISTRO" in

        arch)

            if command -v yay >/dev/null 2>&1; then

                yay -S --noconfirm whatweb

            elif command -v paru >/dev/null 2>&1; then

                paru -S --noconfirm whatweb

            else

                echo -e "${YELLOW}WhatWeb could not be installed automatically.${NC}"
                echo "Install it manually before running Vigil."

            fi
            ;;

        debian)

            sudo apt install -y whatweb || true
            ;;

        fedora)

            sudo dnf install -y whatweb || true
            ;;

    esac

    pause_step

fi

# ==========================================================
# Nikto
# ==========================================================

if ! command -v nikto >/dev/null 2>&1; then

    echo
    echo -e "${BLUE}[→]${NC} Installing Nikto..."

    pause_step

    case "$DISTRO" in

        arch)

            if command -v yay >/dev/null 2>&1; then

                yay -S --noconfirm nikto

            elif command -v paru >/dev/null 2>&1; then

                paru -S --noconfirm nikto

            else

                echo -e "${YELLOW}Nikto could not be installed automatically.${NC}"
                echo "Install it manually before running Vigil."

            fi
            ;;

        debian)

            sudo apt install -y nikto || true
            ;;

        fedora)

            sudo dnf install -y nikto || true
            ;;

    esac

    pause_step

fi

# ==========================================================
# Verify Installation
# ==========================================================

echo
echo -e "${BLUE}========================================"
echo "              Verification"
echo -e "========================================${NC}"

sleep 1

verify() {

    if command -v "$1" >/dev/null 2>&1; then

        echo -e "[${GREEN}✔${NC}] $1"

    else

        echo -e "[${RED}✘${NC}] $1"

    fi

    sleep 0.15
}

verify vigil
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

sleep 1

# ==========================================================
# Finish
# ==========================================================

echo
echo -e "${GREEN}Installation complete.${NC}"
echo

if command -v vigil >/dev/null 2>&1; then

    echo "Run:"
    echo
    echo "  vigil --help"
    echo "  vigil <target>"

else

    echo -e "${YELLOW}Vigil was installed, but ~/.local/bin is not currently in your PATH.${NC}"
    echo
    echo "Add this to your shell configuration:"
    echo
    echo '  export PATH="$HOME/.local/bin:$PATH"'
    echo

fi
