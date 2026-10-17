# HTTP Security Headers Checker

A simple Python tool that checks a website's HTTP response for common security headers. 

## Features

- Checks 6 common HTTP security headers.
- Displays the HTTP status code.
- Shows which headers are present or missing.
- Generates a `security_headers_report.txt` report.

## Security Headers Checked

- **Strict-Transport-Security** — Enforces HTTPS in supporting browsers.
- **Content-Security-Policy** — Helps restrict permitted content sources.
- **X-Content-Type-Options** — Helps prevent MIME-type sniffing.
- **X-Frame-Options** — Helps control framing and clickjacking.
- **Referrer-Policy** — Controls referrer information sent by browsers.
- **Permissions-Policy** — Controls access to selected browser features.

## Usage

Run the script:

```bash
python main.py
```

Enter the target URL when prompted:

```text
Enter the target URL: https://example.com
```
<img width="641" height="523" alt="Screenshot 2026-10-18 000739" src="https://github.com/user-attachments/assets/cf3a62db-fa85-420d-8691-8707fbff1d74" />


## Limitations

- Checks headers from the HTTP response it receives.
- A missing header does not automatically mean the website is vulnerable.
- Results may differ depending on the URL, redirects, and response type.
