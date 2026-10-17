
import os
import requests

target = input("Enter the target URL: ").strip().rstrip("/")
wordlist = input("Enter the path to your wordlist file: ").strip()

# Check if the wordlist file exists
if not os.path.isfile(wordlist):
    print(f"[!] Error: The file '{wordlist}' does not exist.")
    raise SystemExit(1)

if not target.startswith(("http://", "https://")):
    target = "https://" + target

print(f"\nChecking paths on {target} using {wordlist}...")
print("-" * 50)

# Status codes to be reported
interesting_codes = (200, 301, 302, 401, 403)

try:
    with open(wordlist, "r", encoding="utf-8", errors="ignore") as file:
        
        for line in file:
            path = line.strip().lstrip("/")

            if not path:
                continue

            url = f"{target}/{path}"

            print(f"[*] Testing: {url}")

            try:
                response = requests.get(url,timeout=3,allow_redirects=False)

                print(f"    Status: {response.status_code}")

                if response.status_code in (200, 301, 302, 401, 403):
                    print(f"    [+] Interesting response: {url}")

            except requests.RequestException as error:
                print(f"    [!] Request failed: {error}")


except OSError as error:
    print(f"[!] Could not read wordlist: {error}")
