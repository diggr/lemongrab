#!/usr/bin/env python3
import click
from lemongrab.wikidata import build_wikidata_mapping
from lemongrab.company_dataset import build_company_dataset
from lemongrab.company_network import CompanyNetworkBuilder

try:
    from lemongrab.browser import start_browser
    BROWSER_AVAILABLE = True
except Exception:
    BROWSER_AVAILABLE = False

cli = click.Group()

@cli.command()
def wikidata_mapping():
    build_wikidata_mapping()

@cli.command()
def company_dataset():
    build_company_dataset()

if BROWSER_AVAILABLE:
    @cli.command()
    def browser():
        start_browser()


@cli.command()
@click.option("--country", "-c", multiple=True, default=None)
@click.option("--platform", "-p", default=None)
@click.option("--roles/--no-roles", default=False)
@click.option("--publisher/--no-publisher", default=False)
def company_network(country, platform, roles, publisher):
    cn = CompanyNetworkBuilder(country, platform, roles, publisher)

if __name__ == "__main__":
    cli()
