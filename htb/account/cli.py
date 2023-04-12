import functools
import sys

import click

from . import handlers, prompt
from .persistence import provide_persistence, inject_persistence, Persistence


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
    return handlers.add(accounts)


@cli.command("delete", help="Delete account.")
@provide_persistence
@require_account
def delete(accounts: dict):
    return handlers.delete(accounts)


@cli.command("update", help="Update account password.")
@provide_persistence
@require_account
def update(accounts: dict):
    return handlers.update(accounts)


@cli.command(help="Refresh all accounts.")
@provide_persistence
@require_account
def refresh(accounts: dict):
    handlers.refresh(accounts)


@cli.command("prompt")
@provide_persistence
def _prompt(accounts: dict):
    return prompt.prompt(accounts)
