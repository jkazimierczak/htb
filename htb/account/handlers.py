import sys

import questionary

from .refresh import CT8


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
    return accounts


def delete(accounts: dict):
    selected = questionary.checkbox(
        "Select account(s) to delete:",
        choices=[account for account in accounts],
    ).ask()
    if not selected:
        sys.exit(0)

    conf = questionary.confirm(
        "Are you sure you want to remove selected accounts?"
    ).ask()
    if not conf:
        sys.exit(0)

    for account in selected:
        accounts.pop(account)

    return accounts


def update(accounts: dict):
    selected = questionary.select(
        "Select account to modify:",
        choices=[account for account in accounts],
    ).ask()
    if not selected:
        sys.exit(0)

    new_password = questionary.password("New password: ").ask()

    accounts.update({selected: new_password})
    return accounts


def refresh(accounts: dict):
    ct8 = CT8()

    for username, password in accounts.items():
        ct8.login(username, password)


def list(accounts: dict):
    for name in accounts:
        print(name)