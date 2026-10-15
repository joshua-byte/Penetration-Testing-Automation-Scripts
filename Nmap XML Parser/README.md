# Nmap XML Parser

## Purpose

A Python script that parses Nmap XML scan results and generates an HTML report for easier review and documentation.

## Features

- Extracts host IP addresses and status.
- Lists open ports and detected services.
- Displays detected product and version information when available.
- Generates a structured HTML report.

## Language and Tools

- **Language:** Python
- **Tool:** Nmap
- **Libraries:** `xml.etree.ElementTree`, `argparse`, `html`, and other Python standard-library modules used by the script.

## Usage

First, generate an Nmap XML scan:

```bash
nmap -sV -oX scan_before.xml <target>
```

Run the parser:

```bash
python nmap_xml_parser.py scan_before.xml -o scan_report.html
```

Open `scan_report.html` in a web browser to view the report.
