import click

from .commands import domain, account


@click.group()
def entry_point():
    pass


entry_point.add_command(domain.cli)
entry_point.add_command(account.cli)

if __name__ == "__main__":
    entry_point()
