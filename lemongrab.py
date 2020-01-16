#!/usr/bin/env python3
import click
from lemongrab.wikidata import build_wikidata_mapping
from lemongrab.company_dataset import build_company_dataset
from lemongrab.company_network import CompanyNetworkBuilder
from lemongrab.browser import start_browser
from config import DIGGR_API

cli = click.Group()

@cli.command()
def wikidata_mapping():
    """
    Fetch new Wikidata company dataset
    """
    build_wikidata_mapping()

@cli.command()
def company_dataset():
    """
    Build new company dataset from the Mobygames dataset
    """
    build_company_dataset(DIGGR_API)


@cli.command()
def browser():
    """
    Start data exploration and visualization browser
    """
    start_browser()


@cli.command()
@click.option("--gamelist", "-g", default=None)
@click.option("--country", "-c", multiple=True, default=None)
@click.option("--platform", "-p", default=None)
@click.option("--roles/--no-roles", default=False)
@click.option("--publisher/--no-publisher", default=False)
def company_network(gamelist, country, platform, roles, publisher):
    """
    Build company network for Gephi import
    """
    cn = CompanyNetworkBuilder(gamelist, country, platform, roles, publisher)

if __name__ == "__main__":
    cli()
