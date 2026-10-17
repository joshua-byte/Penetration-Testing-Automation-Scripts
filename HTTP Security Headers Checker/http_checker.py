
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

#boring report formatting stuff
def write_report(url, status, security_headers, headers, present, missing):
    filename = "security_headers_report.txt"

    with open(filename, "w", encoding="utf-8") as report:
        report.write("HTTP Security Headers Report\n")
        report.write("=" * 30 + "\n")
        report.write(f"Target: {url}\n")
        report.write(f"HTTP Status: {status}\n\n")

        report.write("Security Header Check\n")
        report.write("-" * 30 + "\n")

        for name, purpose in security_headers.items():
            value = headers.get(name)

            if value:
                report.write(f"[+] {name}: Present\n")
                report.write(f"    Value: {value}\n")
            else:
                report.write(f"[-] {name}: Missing\n")

            report.write(f"    Purpose: {purpose}\n\n")

        report.write("Summary\n")
        report.write("-" * 30 + "\n")
        report.write(f"Headers checked: {len(security_headers)}\n")
        report.write(f"Present: {present}\n")
        report.write(f"Missing: {missing}\n")

    print(f"\n[+] Report saved to {filename}")


url = input("Enter the target URL: ").strip()

if not url.startswith(("http://", "https://")): #handling user input by adding https:// if not entered
    url = "https://" + url

# security headers chosen
security_headers = {
    "Strict-Transport-Security":
        "Enforces HTTPS in supporting browsers.",
    "Content-Security-Policy":
        "Helps restrict permitted content sources.",
    "X-Content-Type-Options":
        "Helps prevent MIME-type sniffing.",
    "X-Frame-Options":
        "Helps control framing and clickjacking.",
    "Referrer-Policy":
        "Controls referrer information sent by browsers.",
    "Permissions-Policy":
        "Controls access to selected browser features."
}

try:
    request = Request(
        url,
        headers={"User-Agent": "VAPT-Headers-Checker/1.0"},
        method="GET"
    )

    with urlopen(request, timeout=10) as response:
        headers = response.headers
        status = response.status

        print("\nHTTP Status:", status)
        print("\nSecurity Header Check:")

        present = 0 #counters to track missing and present 
        missing = 0

        for name, purpose in security_headers.items():
            value = headers.get(name)

            if value:
                print(f"[+] {name}: Present")
                print(f"    Value: {value}")
                present += 1 
            else:
                print(f"[-] {name}: Missing")
                missing += 1

            print(f"    Purpose: {purpose}")

        print("\nSummary")
        print(f"Headers checked: {len(security_headers)}")
        print(f"Present: {present}")
        print(f"Missing: {missing}")

        write_report(
            url,
            status,
            security_headers,
            headers,
            present,
            missing
        )
#error handling
except HTTPError as error:
    print("HTTP Status:", error.code)
    print("The server returned an HTTP error.")

except URLError as error:
    print("Request failed:", error.reason)

except TimeoutError:
    print("Request timed out.")

except OSError as error:
    print("An error occurred:", error)
