import shutil
import sys
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

        if self.enabled and self.disabled:
            raise ValueError(f"Domain {self.path.name} is both enabled and disabled")

    def __hash__(self):
        return hash(self.path)

    def __str__(self):
        return str(self.path.name)

    def state_str(self):
        """Returns a string signaling domain's state."""
        if self.enabled:
            return f"● {self}"
        else:
            return f"○ {self}"


def discover_domains() -> Generator[Domain, None, None]:
    paths = sorted(DOMAIN_DIR.iterdir())

    for path in paths:
        domain = Domain(path)

        if not (domain.enabled or domain.disabled):
            continue

        yield domain


def get_domains() -> Generator[Domain, None, None]:
    domains = discover_domains()

    disabled_domains = []
    for domain in domains:
        if domain.enabled:
            yield domain
        else:
            disabled_domains.append(domain)

    disabled_domains.reverse()
    while disabled_domains:
        yield disabled_domains.pop()


@click.group("domain", help="Domain management tools.")
def cli():
    pass


@cli.command("list", help="List available domains.")
def _list():
    domains = get_domains()

    for domain in domains:
        if domain.enabled:
            click.secho(domain.state_str(), fg="green")
        else:
            click.echo(domain.state_str())


@cli.command("toggle", help="Toggle domain(s) by renaming public_html.")
def toggle():
    domains = list(get_domains())

    selection = questionary.checkbox(
        "Select domain/s which should remain enabled:",
        choices=[
            questionary.Choice(str(domain), value=domain, checked=domain.enabled)
            for domain in domains
        ],
    ).ask()

    if not selection:
        sys.exit(0)

    def _disable(domain: Domain):
        if domain.enabled:
            shutil.move(domain.path / PUBLIC_HTML, domain.path / f".{PUBLIC_HTML}")

    def _enable(domain: Domain):
        if domain.disabled:
            shutil.move(domain.path / f".{PUBLIC_HTML}", domain.path / PUBLIC_HTML)

    for domain in selection:
        _enable(domain)

    to_disable = set(domains).difference(set(selection))
    for domain in to_disable:
        _disable(domain)
