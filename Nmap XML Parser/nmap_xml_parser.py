
import xml.etree.ElementTree as ET
import argparse
import html
from datetime import datetime
from pathlib import Path


def parse_nmap_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    hosts = []

    for host in root.findall("host"):
        # Host status
        status_ele = host.find("status")
        status = (
            status_ele.get("state", "unknown")
            if status_ele is not None
            else "unknown"
        )

        # IPv4 address
        address_ele = host.find("./address[@addrtype='ipv4']")
        ip = (
            address_ele.get("addr", "Unknown")
            if address_ele is not None
            else "Unknown"
        )

        # Hostname
        hostname_ele = host.find("./hostnames/hostname")
        hostname = (
            hostname_ele.get("name", "")
            if hostname_ele is not None
            else ""
        )

        ports = []

        for port in host.findall("./ports/port"):
            state_ele = port.find("state")

            if state_ele is None:
                continue

            state = state_ele.get("state", "unknown")

            # Only include ports that are open
            if state != "open":
                continue

            service_ele = port.find("service")

            service_name = (
                service_ele.get("name", "unknown")
                if service_ele is not None
                else "unknown"
            )

            product = (
                service_ele.get("product", "")
                if service_ele is not None
                else ""
            )

            version = (
                service_ele.get("version", "")
                if service_ele is not None
                else ""
            )

            ports.append({
                "port": port.get("portid", "unknown"),
                "protocol": port.get("protocol", "unknown"),
                "service": service_name,
                "product": product,
                "version": version,
            })

        hosts.append({
            "ip": ip,
            "hostname": hostname,
            "status": status,
            "ports": ports,
        })

    return hosts


def generate_html_report(hosts, output_file):

    total_hosts = len(hosts)
    total_open_ports = sum(len(host["ports"]) for host in hosts)
    hosts_up = sum(1 for host in hosts if host["status"] == "up")

    def safe(value):
        return html.escape(str(value), quote=True)

    host_rows = []
    port_rows = []

    for host in hosts:
        host_rows.append(f"""
            <tr>
                <td>{safe(host['ip'])}</td>
                <td>{safe(host['hostname'] or 'N/A')}</td>
                <td>{safe(host['status'])}</td>
                <td>{len(host['ports'])}</td>
            </tr>
        """)

        for port in host["ports"]:
            version_details = " ".join(
                part for part in (
                    port["product"],
                    port["version"]
                ) if part
            ) or "Not detected"

            port_rows.append(f"""
                <tr>
                    <td>{safe(host['ip'])}</td>
                    <td>{safe(port['port'])}/{safe(port['protocol'])}</td>
                    <td>{safe(port['service'])}</td>
                    <td>{safe(version_details)}</td>
                </tr>
            """)

    if not host_rows:
        host_rows.append(
            '<tr><td colspan="4">No hosts found in the XML.</td></tr>'
        )

    if not port_rows:
        port_rows.append(
            '<tr><td colspan="4">No open ports reported.</td></tr>'
        )

    generated_at = datetime.now().astimezone().strftime(
        "%Y-%m-%d %H:%M:%S %Z"
    )

    report = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nmap Scan Report</title>
    <style>
        body {{
            margin: 0;
            padding: 32px;
            background: #f3f5f8;
            color: #202938;
            font-family: Arial, sans-serif;
        }}
        main {{
            max-width: 1100px;
            margin: auto;
        }}
        h1 {{ margin-bottom: 8px; }}
        .subtitle {{ color: #64748b; margin-bottom: 28px; }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 16px;
            margin-bottom: 28px;
        }}
        .card, section {{
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 20px;
        }}
        .metric {{
            font-size: 30px;
            font-weight: bold;
            margin-top: 8px;
        }}
        section {{ margin-bottom: 24px; overflow-x: auto; }}
        h2 {{ margin-top: 0; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
        }}
        th, td {{
            padding: 12px;
            border-bottom: 1px solid #e2e8f0;
        }}
        th {{ background: #f8fafc; }}
        footer {{
            color: #64748b;
            font-size: 13px;
            margin-top: 24px;
        }}
        @media (max-width: 600px) {{
            body {{ padding: 16px; }}
        }}
    </style>
</head>
<body>
<main>
    <h1>Nmap Scan Report</h1>
    <p class="subtitle">
        Generated: {safe(generated_at)}
    </p>

    <div class="summary">
        <div class="card">
            Hosts in XML
            <div class="metric">{total_hosts}</div>
        </div>
        <div class="card">
            Hosts reported up
            <div class="metric">{hosts_up}</div>
        </div>
        <div class="card">
            Open ports
            <div class="metric">{total_open_ports}</div>
        </div>
    </div>

    <section>
        <h2>Host Inventory</h2>
        <table>
            <thead>
                <tr>
                    <th>IP Address</th>
                    <th>Hostname</th>
                    <th>Status</th>
                    <th>Open Ports</th>
                </tr>
            </thead>
            <tbody>
                {''.join(host_rows)}
            </tbody>
        </table>
    </section>

    <section>
        <h2>Open Port and Service Inventory</h2>
        <table>
            <thead>
                <tr>
                    <th>Host</th>
                    <th>Port</th>
                    <th>Service</th>
                    <th>Detected Product / Version</th>
                </tr>
            </thead>
            <tbody>
                {''.join(port_rows)}
            </tbody>
        </table>
    </section>

    <footer>
        This report summarizes information recorded in the supplied Nmap XML.
        Detected services and versions do not, by themselves, establish that
        a vulnerability exists. Results depend on scan scope and options.
    </footer>
</main>
</body>
</html>
"""

    Path(output_file).write_text(report, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(
        description="Parse Nmap XML and generate an HTML report."
    )
    parser.add_argument("xml_file", help="Path to Nmap XML input")
    parser.add_argument(
        "-o", "--output",
        default="scan_report.html",
        help="HTML output path (default: scan_report.html)"
    )

    args = parser.parse_args()

    try:
        hosts = parse_nmap_xml(args.xml_file)
        generate_html_report(hosts, args.output)

    except (ET.ParseError, OSError) as exc:
        parser.error(f"Could not process input or output file: {exc}")

    print(f"Parsed {len(hosts)} host(s).")
    print(f"HTML report generated: {args.output}")


if __name__ == "__main__":
    main()

