import hashlib
import os
from Crypto.Hash import MD4
import bcrypt

def crack_md5(target_hash, wordlist_path):
    target_hash = target_hash.strip().lower()

    return crack_hash(
        target_hash,
        wordlist_path,
        lambda word: hashlib.md5(
            word.encode("utf-8")
        ).hexdigest()
    )

def crack_ntlm(target_hash, wordlist_path):
    target_hash = target_hash.strip().lower()

    def hash_word(word):
        md4 = MD4.new()
        md4.update(word.encode("utf-16le"))
        return md4.hexdigest()

    return crack_hash(target_hash, wordlist_path, hash_word)

def crack_bcrypt(target_hash, wordlist_path):
    if not os.path.isfile(wordlist_path):
        return "Wordlist not found."

    try:
        target_hash_bytes = target_hash.strip().encode("utf-8")
        if not target_hash.startswith(("$2a$", "$2b$", "$2y$")):
            return "Invalid bcrypt hash format."
        with open(wordlist_path, "r", encoding="latin-1") as file:
            words = [line.strip() for line in file if line.strip()]

        if not words:
            return "Wordlist is empty."
        total = len(words)
        for tried, word in enumerate(words, start=1):
            percent = tried / total * 100

            print(
                f"\r[*] Attempts: {tried}/{total} "
                f"| Progress: {percent:.1f}%",
                end="",
                flush=True
            )

            try:
                if bcrypt.checkpw(
                    word.encode("utf-8"),
                    target_hash_bytes
                ):
                    print()
                    return f"FOUND:{word}"

            except (ValueError, TypeError):
                return "Invalid bcrypt hash structure."

        print()
        return "Password not found in wordlist."

    except OSError as error:
        return f"File error: {error}"
def crack_hash(target_hash, wordlist_path, hash_function):
    if not os.path.isfile(wordlist_path):
        return "Wordlist not found."

    try:
        with open(wordlist_path, "r", encoding="latin-1") as file:
            words = [line.strip() for line in file if line.strip()]

        if not words:
            return "Wordlist is empty."

        total = len(words)

        for tried, word in enumerate(words, start=1):
            percent = tried / total * 100

            print(
                f"\r[*] Attempts: {tried}/{total} "
                f"| Progress: {percent:.1f}%",
                end="",
                flush=True
            )

            if hash_function(word).lower() == target_hash:
                print()
                return f"FOUND:{word}"

        print()
        return "Password not found in wordlist."

    except OSError as error:
        return f"File error: {error}"


def main():
    print("=" * 45)
    print("          DICTIONARY HASH CRACKER")
    print("=" * 45)
    print("1. MD5")
    print("2. NTLM")
    print("3. bcrypt")

    choice = input("\nSelect hash type (1-3): ").strip()

    functions = {
        "1": ("MD5", crack_md5),
        "2": ("NTLM", crack_ntlm),
        "3": ("bcrypt", crack_bcrypt)
    }

    if choice not in functions:
        print("[!] Invalid selection.")
        return

    hash_type, crack_function = functions[choice]

    target_hash = input(f"Enter the {hash_type} hash: ").strip()
    wordlist_path = input("Enter the wordlist path: ").strip()

    print(f"\n[*] Starting {hash_type} dictionary test...")

    result = crack_function(target_hash, wordlist_path)

    print("\n" + "=" * 45)

    if result.startswith("FOUND:"):
        password = result[len("FOUND:"):]
        print("[+] Password found!")
        print(f"[+] Candidate: {password}")
    else:
        print(f"[-] {result}")

    print("=" * 45)


if __name__ == "__main__":
    main()
