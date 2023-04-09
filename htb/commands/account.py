import base64
import functools
import json
import sys
import uuid
from pathlib import Path

import click
import cryptography.fernet
import questionary
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

KDF_ITERS = 2_000_000
ACCOUNTS_DB = Path(__file__).parent / "accounts.bin"


PASSWORD_PROMPT = questionary.password("File password: ")


def key_prompt() -> bytes:
    """Return a fernet-compatible key from password provided by the user."""
    password: str = PASSWORD_PROMPT.ask()
    if not password:
        print("Password cannot be empty.")
        sys.exit(-1)

    salt = uuid.UUID(int=uuid.getnode()).bytes

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt, iterations=KDF_ITERS
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def setup_database() -> bytes:
    print(
        "Operating on accounts requires additional setup.\n"
        "Account details will be stored in an encrypted file."
        "Make sure to use strong password."
    )
    key = key_prompt()
    fernet = Fernet(key)
    data = fernet.encrypt(json.dumps({}).encode())

    with open(ACCOUNTS_DB, "wb") as f:
        f.write(data)

    print("Encrypted file setup completed.")
    return key


def supply_database(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        key = None
        if not ACCOUNTS_DB.exists():
            key = setup_database()

        if not key:
            key = key_prompt()

        fernet = Fernet(key)
        with open(ACCOUNTS_DB, "rb") as fr:
            try:
                decrypted = fernet.decrypt(fr.read())
                accounts = json.loads(decrypted)
            except cryptography.fernet.InvalidToken:
                print("Invalid password provided.")
                sys.exit(-1)

        return f(*args, accounts=accounts, **kwargs)

    return wrapper


def save_to_file(accounts: dict):
    """Save accounts to an encrypted file."""
    key = key_prompt()

    fernet = Fernet(key)
    data = fernet.encrypt(json.dumps(accounts).encode())

    with open(ACCOUNTS_DB, "wb") as f:
        f.write(data)


@click.group("account", help="CT8 account management.")
def cli():
    pass


@cli.command(help="Refresh accounts.")
def refresh():
    pass


@cli.command(help="Add account.")
@supply_database
def add(accounts: dict):
    username = questionary.text("CT8 login:").ask()
    if username in accounts:
        confirm = questionary.confirm("User already exists. Change password?").ask()
        if not confirm:
            sys.exit(0)

    password = None
    try:
        while not password:
            password = questionary.password("Password:").ask()
            if not password:
                print("Password cannot be empty.")
    except KeyboardInterrupt:
        sys.exit(0)

    accounts.update({username: password})
    save_to_file(accounts)
