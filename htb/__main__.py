import click

from .commands import domain


@click.group()
def entry_point():
    pass


entry_point.add_command(domain.cli)

if __name__ == "__main__":
    entry_point()
