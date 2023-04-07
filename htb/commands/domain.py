import shutil
from typing import Generator

import click

from pathlib import Path

from dataclasses import dataclass

import questionary

DOMAIN_DIR = Path().home().joinpath("domains")
PUBLIC_HTML = "public_html"


@dataclass()
class Domain:
    path: Path

    def __post_init__(self):
        self.enabled = self.path.joinpath(PUBLIC_HTML).exists()
        self.disabled = self.path.joinpath(f".{PUBLIC_HTML}").exists()

    def __str__(self):
        return str(self.path.name)

    def state_str(self):
        """Returns a string signaling domain's state."""
        if self.enabled:
            return f"+ {self}"
        else:
            return f"- {self}"


def get_domains() -> Generator[Domain, None, None]:
    paths = sorted(DOMAIN_DIR.iterdir())

    for path in paths:
        domain = Domain(path)

        if not (domain.enabled or domain.disabled):
            continue

        yield domain


@click.group("domain")
def cli():
    pass


@cli.command("list")
def _list():
    for domain in get_domains():
        print(domain.state_str())


@cli.command("toggle")
def _list():
    selection = questionary.checkbox(
        "Select domain/s to toggle visibility of public_html:",
        choices=[questionary.Choice(domain.state_str()) for domain in get_domains()],
    ).ask()

    domains = []
    for ans in selection:
        domain = Domain(Path(ans.lstrip("+- ")))
        domains.append(domain)

    for domain in domains:
        if domain.enabled:
            shutil.move(domain.path / PUBLIC_HTML, domain.path / f".{PUBLIC_HTML}")
        else:
            shutil.move(domain.path / f".{PUBLIC_HTML}", domain.path / PUBLIC_HTML)
