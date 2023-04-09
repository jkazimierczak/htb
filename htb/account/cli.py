import sys

import click
import questionary

from htb.account.persistence import provide_persistence


@click.group("account", help="CT8 account management.")
def cli():
    pass


@cli.command(help="Refresh accounts.")
def refresh():
    pass


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
