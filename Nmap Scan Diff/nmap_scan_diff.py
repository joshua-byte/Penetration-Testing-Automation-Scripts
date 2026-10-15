
import xml.etree.ElementTree as ET


def read_scan(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    hosts = set()
    open_ports = {}

    for host in root.findall("host"):
        addresses = {
            address.get("addr")
            for address in host.findall("address")
            if address.get("addr")
        }

        hosts.update(addresses)

        for port in host.findall("./ports/port"):
            state_element = port.find("state")

            if state_element is None:
                continue

            state = state_element.get("state")

            if state != "open":
                continue

            protocol = port.get("protocol", "unknown")
            port_id = port.get("portid", "unknown")

            service_element = port.find("service")

            if service_element is not None:
                service = service_element.get("name", "unknown")
                product = service_element.get("product", "")
                version = service_element.get("version", "")
            else:
                service = "unknown"
                product = ""
                version = ""

            details = " ".join(
                value
                for value in (service, product, version)
                if value
            )

            for address in addresses:
                key = (address, protocol, port_id)
                open_ports[key] = details

    return hosts, open_ports


if __name__ == "__main__":
    old_file = input("Enter the previous scan XML filename: ")
    new_file = input("Enter the current scan XML filename: ")

    old_hosts, old_ports = read_scan(old_file)
    new_hosts, new_ports = read_scan(new_file)

    newly_open = new_ports.keys() - old_ports.keys()
    no_longer_open = old_ports.keys() - new_ports.keys()
    common_ports = old_ports.keys() & new_ports.keys()
    changed_services = {
        key: (old_ports[key], new_ports[key])
        for key in common_ports
        if old_ports[key] != new_ports[key]
    }

    print("Newly open ports:")
    for key in sorted(newly_open):
        print(key, "-", new_ports[key])

    print("\nPorts no longer reported open:")
    for key in sorted(no_longer_open):
        print(key, "-", old_ports[key])

    print("\nService/version changes:")
    for key, (old_service, new_service) in sorted(
        changed_services.items()
    ):
        print(key)
        print("  Before:", old_service)
        print("  After: ", new_service)
