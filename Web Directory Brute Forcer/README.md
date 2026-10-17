# Web Directory Brute Forcer

A simple Python tool that checks a web server for common directories and paths using a wordlist. It sends HTTP requests and displays the response status codes to help identify responses.

## Features

- Tests paths from a wordlist.
- Displays each URL being tested.
- Shows HTTP status codes.
- Highlights interesting responses such as `200`, `301`, `302`, `401`, and `403`.
- Handles request errors and timeouts.

Install dependencies:

```bash
python -m pip install requests flask
```

## Usage

Start the local test server:

```bash
python test_server.py
```

In another terminal, run the brute forcer:

```bash
python main.py
```
<img width="652" height="527" alt="Screenshot 2026-10-18 004010" src="https://github.com/user-attachments/assets/f80b15e2-f05c-4d96-8561-6e48d4bb97b8" />

## Disclaimer

This tool is intended for learning and authorized security testing. Only test systems you own or have explicit permission to assess.
