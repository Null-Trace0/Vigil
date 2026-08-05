"""
VIGIL Knowledge Base

Provides:
- Description
- Security Impact
- Recommendation

for common vulnerability classes.

Matching is performed by checking whether
the vulnerability title contains one of the
keywords below.
"""

KNOWLEDGEBASE = {

# ==========================================================
# Remote Code Execution
# ==========================================================

"remote code execution": {
    "description":
        "A Remote Code Execution (RCE) vulnerability allows an attacker to execute arbitrary commands or code on the target system.",

    "impact":
        "Complete system compromise, malware deployment, privilege escalation and data theft.",

    "recommendation":
        "Immediately update the affected software, disable vulnerable functionality, restrict access and apply vendor security patches."
},

# ==========================================================
# Command Injection
# ==========================================================

"command execution": {
    "description":
        "The application improperly executes user supplied commands on the operating system.",

    "impact":
        "Attackers may gain complete control over the underlying operating system.",

    "recommendation":
        "Validate input, avoid shell execution and implement strict allow-listing."
},

# ==========================================================
# SQL Injection
# ==========================================================

"sql injection": {
    "description":
        "SQL Injection allows attackers to manipulate backend database queries.",

    "impact":
        "Database compromise, authentication bypass and sensitive data disclosure.",

    "recommendation":
        "Use prepared statements, parameterized queries and strict input validation."
},

# ==========================================================
# XSS
# ==========================================================

"cross site scripting": {
    "description":
        "Cross-Site Scripting executes malicious JavaScript inside another user's browser.",

    "impact":
        "Session hijacking, credential theft and phishing attacks.",

    "recommendation":
        "Escape output, sanitize input and deploy Content Security Policy."
},

# ==========================================================
# Default Credentials
# ==========================================================

"default login": {
    "description":
        "The service is using default credentials or publicly known passwords.",

    "impact":
        "Unauthorized administrative access.",

    "recommendation":
        "Immediately replace all default credentials with strong unique passwords."
},

"default password": {
    "description":
        "The application accepts default credentials.",

    "impact":
        "Administrative compromise.",

    "recommendation":
        "Disable default accounts and enforce strong passwords."
},

"default credentials": {
    "description":
        "Default credentials remain enabled.",

    "impact":
        "Privilege escalation and unauthorized access.",

    "recommendation":
        "Replace vendor default passwords before deployment."
},

# ==========================================================
# Anonymous Login
# ==========================================================

"anonymous login": {
    "description":
        "Anonymous authentication is enabled.",

    "impact":
        "Unauthenticated users may access system resources.",

    "recommendation":
        "Disable anonymous authentication unless absolutely required."
},

"anonymous ftp": {
    "description":
        "FTP allows anonymous users.",

    "impact":
        "Information disclosure or unauthorized uploads.",

    "recommendation":
        "Disable anonymous FTP access."
},

# ==========================================================
# Credential Disclosure
# ==========================================================

"credential": {
    "description":
        "The service exposes weak or recoverable credentials.",

    "impact":
        "Account compromise and lateral movement.",

    "recommendation":
        "Rotate passwords, enable MFA and remove exposed credentials."
},

# ==========================================================
# Enumeration
# ==========================================================

"enumeration": {
    "description":
        "The target leaks information useful for reconnaissance.",

    "impact":
        "Attackers gain valuable intelligence before exploitation.",

    "recommendation":
        "Limit information disclosure and disable unnecessary banners."
},

# ==========================================================
# Directory Listing
# ==========================================================

"directory listing": {
    "description":
        "Directory indexing is enabled.",

    "impact":
        "Sensitive files may become publicly accessible.",

    "recommendation":
        "Disable directory browsing."
},

# ==========================================================
# Information Disclosure
# ==========================================================

"information": {
    "description":
        "The service exposes unnecessary information.",

    "impact":
        "Assists attackers during reconnaissance.",

    "recommendation":
        "Reduce information leakage and remove unnecessary headers."
},

# ==========================================================
# Missing Security Headers
# ==========================================================

"security headers": {
    "description":
        "HTTP security headers are missing.",

    "impact":
        "Browsers lose built-in protections against common attacks.",

    "recommendation":
        "Implement CSP, HSTS, X-Frame-Options, X-Content-Type-Options and Referrer-Policy."
},

# ==========================================================
# TLS
# ==========================================================

"tls": {
    "description":
        "Weak TLS configuration detected.",

    "impact":
        "Encrypted communication may become vulnerable.",

    "recommendation":
        "Disable legacy TLS versions and weak cipher suites."
},

"ssl": {
    "description":
        "Weak SSL configuration detected.",

    "impact":
        "Sensitive communication may be intercepted.",

    "recommendation":
        "Upgrade to modern TLS configuration."
},

# ==========================================================
# SMB
# ==========================================================

"smb": {
    "description":
        "SMB service exposed.",

    "impact":
        "Information disclosure and lateral movement.",

    "recommendation":
        "Disable SMBv1, enforce signing and restrict network exposure."
},

# ==========================================================
# FTP
# ==========================================================

"ftp": {
    "description":
        "FTP service detected.",

    "impact":
        "Credentials may be transmitted in plaintext.",

    "recommendation":
        "Replace FTP with SFTP or FTPS."
},

# ==========================================================
# HTTP
# ==========================================================

"http": {
    "description":
        "HTTP service detected.",

    "impact":
        "Traffic may be intercepted without encryption.",

    "recommendation":
        "Redirect all traffic to HTTPS."
},

# ==========================================================
# Apache
# ==========================================================

"apache": {
    "description":
        "Apache HTTP Server identified.",

    "impact":
        "Outdated versions may contain known vulnerabilities.",

    "recommendation":
        "Upgrade Apache and disable unnecessary modules."
},

# ==========================================================
# nginx
# ==========================================================

"nginx": {
    "description":
        "Nginx server detected.",

    "impact":
        "Older versions may expose known vulnerabilities.",

    "recommendation":
        "Keep Nginx updated and remove unused modules."
},

# ==========================================================
# PHP
# ==========================================================

"php": {
    "description":
        "PHP technology detected.",

    "impact":
        "Older versions frequently contain critical vulnerabilities.",

    "recommendation":
        "Upgrade PHP to the latest supported release."
},

# ==========================================================
# WordPress
# ==========================================================

"wordpress": {
    "description":
        "WordPress installation detected.",

    "impact":
        "Plugins and themes may introduce vulnerabilities.",

    "recommendation":
        "Keep WordPress core, themes and plugins updated."
},

    "remote code execution": {
        "description":
            "A Remote Code Execution (RCE) vulnerability allows an attacker to execute arbitrary commands or code on the target system.",

        "impact":
            "Complete compromise of the affected host, malware deployment, privilege escalation and data theft.",

        "recommendation":
            "Immediately patch the affected software, restrict network exposure and apply the latest vendor security updates."
    },

    "postgresql": {
        "description":
            "PostgreSQL database service is exposed to the network.",

        "impact":
            "Misconfigurations or weak credentials may allow unauthorized database access or information disclosure.",

        "recommendation":
            "Restrict PostgreSQL access to trusted hosts, enforce strong authentication and keep the database updated."
    },

    "mysql": {
        "description":
            "MySQL database service is exposed.",

        "impact":
            "Attackers may attempt credential attacks or exploit known database vulnerabilities.",

        "recommendation":
            "Restrict remote access, use strong passwords and update MySQL to the latest supported version."
    },

    "vnc": {
        "description":
            "A VNC remote desktop service has been detected.",

        "impact":
            "If exposed publicly or protected by weak credentials, attackers may obtain remote graphical access to the system.",

        "recommendation":
            "Restrict VNC access using firewall rules or a VPN, require authentication and disable unused VNC services."
    },

    "ftp": {
        "description":
            "An FTP service is available on the target.",

        "impact":
            "Traditional FTP transmits credentials in plaintext and may expose sensitive data during transmission.",

        "recommendation":
            "Replace FTP with SFTP or FTPS whenever possible and disable anonymous access."
    },

    "http": {
        "description":
            "An HTTP service has been identified.",

        "impact":
            "Traffic transmitted over HTTP is not encrypted and may be intercepted or modified by attackers.",

        "recommendation":
            "Redirect users to HTTPS and disable unnecessary HTTP methods such as TRACE."
    },

    "security headers": {
        "description":
            "Important HTTP security headers are missing from server responses.",

        "impact":
            "Missing security headers reduce browser protections against clickjacking, XSS and MIME-type attacks.",

        "recommendation":
            "Implement Content-Security-Policy, Strict-Transport-Security, X-Frame-Options, X-Content-Type-Options and Referrer-Policy."
    },

    "information": {
        "description":
            "The application exposes unnecessary information about the underlying software or configuration.",

        "impact":
            "Information disclosure assists attackers during reconnaissance and exploitation.",

        "recommendation":
            "Remove unnecessary banners, hide version information and limit publicly exposed system details."
    },

    "enumeration": {
        "description":
            "The service allows attackers to enumerate users, resources or system information.",

        "impact":
            "Enumeration significantly improves an attacker's ability to identify valid targets and plan further attacks.",

        "recommendation":
            "Disable unnecessary enumeration features, restrict anonymous access and enforce authentication."
    },

    "php": {
        "description":
            "A PHP application or runtime has been detected.",

        "impact":
            "Outdated PHP versions may contain publicly known vulnerabilities that allow code execution or information disclosure.",

        "recommendation":
            "Upgrade PHP to the latest supported release and remove deprecated or unused extensions."
    },

    "samba": {
        "description":
            "A Samba file-sharing service has been detected.",

        "impact":
            "Outdated or misconfigured Samba installations may allow information disclosure, unauthorized access or remote code execution.",

        "recommendation":
            "Update Samba to the latest supported version, disable SMBv1 and restrict anonymous shares."
    },

    "rpc": {
        "description":
            "RPC services are exposed on the target system.",

        "impact":
            "Attackers may enumerate network services or exploit vulnerable RPC endpoints.",

        "recommendation":
            "Restrict RPC access using firewall rules and disable unnecessary RPC services."
    },

    "tomcat manager": {
        "description":
            "The Apache Tomcat Manager interface is accessible.",

        "impact":
            "If weak credentials are used, attackers may gain administrative access and deploy malicious applications.",

        "recommendation":
            "Restrict Manager access, enforce strong authentication and disable the interface if not required."
    }

}