import functools
import sys

import click
import questionary

from .persistence import provide_persistence, inject_persistence, Persistence
from .refresh import CT8


def require_account(f):
    """Decorator, that ensures that at least one account exists."""

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        accounts = kwargs.get("accounts", None)

        if len(accounts) == 0:
            print("No accounts found. Add an account first.")
            sys.exit(0)

        return f(*args, **kwargs)

    return wrapper


@click.group("account", help="CT8 account management.")
def cli():
    pass


@cli.command(help="Reinitialize storage file.")
@inject_persistence
def reinitialize(persistence: Persistence):
    persistence.reinitialize()


@cli.command(help="Add account.")
@provide_persistence
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


@cli.command("delete", help="Delete account.")
@provide_persistence
@require_account
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


@cli.command("update", help="Update account password.")
@provide_persistence
@require_account
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


@cli.command(help="Refresh all accounts.")
@provide_persistence
@require_account
def refresh(accounts: dict):
    ct8 = CT8()

    for username, password in accounts.items():
        ct8.login(username, password)
