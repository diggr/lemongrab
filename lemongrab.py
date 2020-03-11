#!/usr/bin/env python3
import click
import json

from lemongrab.wikidata import build_wikidata_mapping
from lemongrab.company_dataset import build_company_dataset
from lemongrab.company_network import CompanyNetworkBuilder
from lemongrab.sample_company_network import SampleCompanyNetwork
from config import DIGGR_API

company_dataset_present = True
try:
    from lemongrab.browser import start_browser
except FileNotFoundError:
    company_dataset_present = False

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


if company_dataset_present:

    @cli.command()
    def browser():
        """
        Start data exploration and visualization browser
        """
        start_browser()


@cli.command()
@click.option(
    "--gamelist",
    "-g",
    default=None,
    help="Filename of a tulpa generated gamelist to be used",
)
@click.option("--country", "-c", multiple=True, default=None, help="Include countries")
@click.option(
    "--platform", "-p", default=None, help="Include the platforms of the games"
)
@click.option(
    "--roles/--no-roles", default=False, help="Include/Exclude roles of a company"
)
@click.option("--publisher/--no-publisher", default=False)
def company_network(gamelist, country, platform, roles, publisher):
    """
    Build company network for Gephi import
    """
    cn = CompanyNetworkBuilder(gamelist, country, platform, roles, publisher)

@cli.command()
@click.option("--out", default="company_networks/game_company_network_sample.graphml")
@click.argument("game_company_sample", type=click.File())
def game_company_sample_network(out, game_company_sample):
    scn = SampleCompanyNetwork(json.load(game_company_sample))
    scn.build_network().save_network(out)

if __name__ == "__main__":
    cli()
