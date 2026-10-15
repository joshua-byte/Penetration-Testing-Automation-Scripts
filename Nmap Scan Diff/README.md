# Nmap Scan Diff

## Purpose

A Python script that compares two Nmap XML scan results to identify changes in open ports and detected service information.

## Features

- Identifies newly open ports.
- Identifies ports no longer reported open.
- Detects changes in service and version information.
- Accepts scan filenames through user input.

## Language and Tools

- **Language:** Python
- **Tool:** Nmap
- **Library:** `xml.etree.ElementTree`

## Usage

Generate two XML scans of the same authorized target using consistent scan options:

```bash
nmap -sV -oX scan_before.xml <target>
nmap -sV -oX scan_after.xml <target>
```

Run the script:

```bash
python nmap_scan_diff.py
```

Enter the filenames when prompted:

```text
Enter the previous scan XML filename: scan_before.xml
Enter the current scan XML filename: scan_after.xml
```

The script displays detected port differences and service/version changes. A port missing from the second scan is not necessarily closed or remediated, so results depend on scan scope, options, and target reachability.
