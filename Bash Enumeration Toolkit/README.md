# Bash Enumeration Toolkit

## Purpose

A Bash script that automates basic reconnaissance, passive subdomain enumeration, and service enumeration for authorized penetration testing assessments.

## Features

- **DNS Recon:** Retrieves DNS records using `dig`.
- **HTTP Headers:** Checks HTTPS response headers using `curl`.
- **Subdomain Enumeration:** Discovers subdomains using `subfinder`.
- **DNS Resolution:** Resolves discovered subdomains using `dnsx`.
- **Service Enumeration:** Uses Nmap to identify open ports and detected services.
- **Output Management:** Saves results in a timestamped directory.

## Language and Tools

- **Language:** Bash
- **Tools:** `dig`, `curl`, `subfinder`, `dnsx`, `nmap`

## Usage

Make the script executable:

```bash
chmod +x enumerate.sh
```

Run the script with a target domain:

```bash
./enumerate.sh example.com
```

Replace `example.com` with a domain you own or are explicitly authorized to assess.

The script prompts for confirmation before running Nmap service enumeration.

## Disclaimer

Use this script only on systems and domains you own or have explicit authorization to assess.
