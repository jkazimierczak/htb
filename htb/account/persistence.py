import base64
import functools
import json
import os
import sys
import uuid

import cryptography.fernet
import questionary
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from htb import STORAGE_DIR

KDF_ITERS = 4_000_000
ACCOUNTS_FILE = STORAGE_DIR / "accounts.storage"


def provide_persistence(f):
    """Decorator that provides persistence. It injects account data
    into decorated functions. Value returned from decorated function
    will be stored back to persistent storage."""

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        persistence = Persistence()

        if not ACCOUNTS_FILE.exists():
            persistence.setup()

        accounts = persistence.load()

        new_accounts = f(*args, accounts=accounts, **kwargs)
        if not new_accounts:
            return

        persistence.save(new_accounts)

    return wrapper


class Persistence:
    def __init__(self, key: bytes = None):
        self._key = key

    @property
    def key(self):
        """Return a fernet-compatible key from password provided by the user."""
        if self._key:
            return self._key

        try:
            while True:
                password: str = questionary.password("File password:").unsafe_ask()
                if not password:
                    print("Password cannot be empty.")
                    continue

                password_conf: str = questionary.password(
                    "Confirm password:"
                ).unsafe_ask()

                if password == password_conf:
                    break

                print("Passwords are not the same.")
        except KeyboardInterrupt:
            raise KeyboardInterrupt()

        salt = uuid.UUID(int=uuid.getnode()).bytes

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(), length=32, salt=salt, iterations=KDF_ITERS
        )
        self._key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return self._key

    def setup(self):
        """Setup persistent storage for credentials."""
        print(
            "This operation requires an encrypted file to be set-up.",
            "Make sure to use strong password, as it protects login credentials.",
            sep=os.linesep,
        )
        fernet = Fernet(self.key)
        data = fernet.encrypt(json.dumps({}).encode())

        with open(ACCOUNTS_FILE, "wb") as f:
            f.write(data)

        print("Encrypted file setup completed.")

    def load(self) -> dict:
        """Load credentials from persistent encrypted storage."""
        with open(ACCOUNTS_FILE, "rb") as fr:
            try:
                decrypted = Fernet(self.key).decrypt(fr.read())
                return json.loads(decrypted)
            except cryptography.fernet.InvalidToken:
                print("Invalid password provided.")
                sys.exit(-1)

    def save(self, data: dict) -> None:
        """Save credentials to persistent encrypted storage."""
        serialized = json.dumps(data).encode()
        data = Fernet(self.key).encrypt(serialized)

        with open(ACCOUNTS_FILE, "wb") as f:
            f.write(data)
