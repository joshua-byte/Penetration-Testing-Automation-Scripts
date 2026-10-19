# Dictionary Hash Cracker

A simple Python tool that attempts to recover passwords from hashes

## Features

- Supports MD5, NTLM, and bcrypt hashes.
- Accepts a target hash and wordlist path.
- Displays the number of attempts and progress percentage.

## Requirements

- Python 3
- `bcrypt`
- `pycryptodome`

Install the dependencies:

```bash
python -m pip install bcrypt pycryptodome
```

## Usage

Run the script:

```bash
python main.py
```

Select the hash type, enter the target hash, and provide the path to your wordlist when prompted.


## Disclaimer

Use this tool only with hashes you own or are explicitly authorized to audit.

