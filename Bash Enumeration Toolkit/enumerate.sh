
#!/usr/bin/env bash

set -u

if [[ $# -ne 1 ]]; then
    echo "Usage: ./enumerate.sh <domain>"
    exit 1
fi

domain="${1#http://}"
domain="${domain#https://}"
domain="${domain%%/*}"

if [[ ! "$domain" =~ ^[a-zA-Z0-9.-]+$ ]]; then
    echo "Invalid domain format."
    exit 1
fi

timestamp=$(date +"%Y%m%d_%H%M%S")
output_dir="results_${domain}_${timestamp}"

mkdir -p "$output_dir"

echo "[+] Target: $domain"
echo "[+] Output: $output_dir"

check_tool() {
    if command -v "$1" >/dev/null 2>&1; then
        echo "[+] $1 is installed"
        return 0
    else
        echo "[-] $1 is not installed"
        return 1
    fi
}

run_recon() {
    echo "[+] Running basic reconnaissance..."

    if check_tool dig; then
        dig +short "$domain" > "$output_dir/dns.txt"
    fi

    if check_tool curl; then
        if curl -sS -I --max-time 10 "https://$domain" \
            -o "$output_dir/https_headers.txt"; then
            echo "[+] HTTPS headers saved"
        else
            echo "[-] HTTPS request failed"
        fi
    fi
}

run_subdomain_enum() {
    echo "[+] Running passive subdomain enumeration..."

    if check_tool subfinder; then
        if subfinder -d "$domain" -silent \
            -o "$output_dir/subdomains.txt"; then
            echo "[+] Subdomain results saved"

            if check_tool dnsx; then
                if dnsx -l "$output_dir/subdomains.txt" -silent \
                    -o "$output_dir/resolved_subdomains.txt"; then
                    echo "[+] Resolved subdomains saved"
                else
                    echo "[-] DNS resolution failed"
                fi
            fi
        else
            echo "[-] Subfinder encountered an error"
        fi
    fi
}

run_service_enum() {
    echo
    read -r -p "Run Nmap service enumeration? Only proceed with authorization. (y/n): " confirm

    if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
        echo "[-] Skipping Nmap"
        return 0
    fi

    if check_tool nmap; then
        if nmap -sV "$domain" -oN "$output_dir/nmap_services.txt"; then
            echo "[+] Nmap results saved"
        else
            echo "[-] Nmap encountered an error"
        fi
    fi
}

echo "[+] Checking available tools..."
check_tool dig || true
check_tool curl || true
check_tool subfinder || true
check_tool dnsx || true
check_tool nmap || true

run_recon
run_subdomain_enum
run_service_enum

echo
echo "[+] Enumeration finished."
echo "[+] Results saved in: $output_dir"

