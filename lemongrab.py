import click
from lemongrab.wikidata import build_wikidata_mapping
from lemongrab.company_dataset import build_company_dataset
from lemongrab.company_network import CompanyNetworkBuilder

@click.group()
def cli():
    pass

@cli.command()
def wikidata_mapping():
    build_wikidata_mapping()

@cli.command()
def company_dataset():
    build_company_dataset()

@cli.command()
@click.option("--country", "-c", multiple=True, default=None)
@click.option("--platform", "-p", default=None)
def company_network(country, platform):
    cn = CompanyNetworkBuilder(country, platform)

if __name__ == "__main__":
    cli()