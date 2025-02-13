#!/usr/bin/env python3
import click
import json
import sys

from .wikidata import build_wikidata_mapping
from .company_dataset import build_mobygames_companies
from .company_network import build_company_network
from pathlib import Path
from .sample_company_network import SampleCompanyNetwork
from .settings import (
    DIGGR_API,
    DATASETS_DIR,
    COMPANY_NETWORKS_DIR,
    ID_2_SLUG_FILENAME,
    ID_2_SLUG_PATH,
)
from shutil import copyfile
from .utils import build_aggregated_logs

company_dataset_present = True
try:
    from lemongrab.browser import start_browser
except FileNotFoundError:
    company_dataset_present = False


@click.group()
def cli():
    """
    Gather company data from mobygames and wikidata and build awesome research
    datasets and visualizations.This tool provides various commands to fetch data
    (via cli) and visualize it (via browser).
    """
    pass


@cli.command()
def init():
    """
    Setup lemongrab in the current directory
    """
    print(f"Initialize lemongrab project...")
    Path(DATASETS_DIR).mkdir()
    Path(COMPANY_NETWORKS_DIR).mkdir()
    copyfile(ID_2_SLUG_PATH, Path(DATASETS_DIR) / ID_2_SLUG_FILENAME)
    print(f"Finished.")


@cli.group()
def build():
    """
    Build the datasets required for analysis.
    """


@build.command()
def wikidata_mapping():
    """
    Fetch new Wikidata company dataset
    """
    print("Building wikidata mapping ...")

    try:
        n_entries, mapping_filename = build_wikidata_mapping()
    except RuntimeError as e:
        sys.exit(e)

    print(f"Mapped {n_entries} wikidata items with Mobygames Company ID.")
    print(f"Mapping file saved as: {mapping_filename}")


@build.command()
@click.option(
    "--unified-api-url", default=DIGGR_API, help="URL of any UnifiedAPI instance"
)
def mobygames_companies(unified_api_url):
    """
    Build new company dataset from the Mobygames dataset
    """
    print("Building company dataset...")
    mobygames_companies_filename = build_mobygames_companies(unified_api_url)
    print(f"Mobygames companies file saved as: {mobygames_companies_filename}")


@build.command()
@click.option(
    "--unified-api-url", default=DIGGR_API, help="URL of any UnifiedAPI instance"
)
@click.pass_context
def all(ctx, unified_api_url):
    """
    Build both, the Wikidata mapping and the company dataset.
    """
    ctx.invoke(wikidata_mapping)
    ctx.forward(mobygames_companies)


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
    print("Building company network...")
    out_file, n_nodes, n_edges, n_games = build_company_network(
        gamelist, country, platform, roles, publisher
    )
    print(f"Network file saved as: {out_file}")
    print(f"Nodes in network: {n_nodes}")
    print(f"Edges in network: {n_edges}")
    print(f"Games: {n_games}")


@cli.command()
@click.option("--out", default="company_networks/game_company_network_sample.graphml")
@click.argument("game_company_sample", type=click.File())
def game_company_sample_network(out, game_company_sample):
    """
    Builds a company network from a sample.
    """
    out_folder = Path(out).resolve().parent
    if not out_folder.is_dir():
        out_folder.mkdir(parents=True)
    scn = SampleCompanyNetwork(json.load(game_company_sample))
    scn.build_network().save_network(out)


@cli.command()
@click.option("--out", default="lemongrab_logs.csv")
def aggregate_logs(out):
    """
    Aggregates all logs of the current project into a CSV file.
    """
    outfilename, used_logs = build_aggregated_logs(out)
    print(f"Aggregates logs saved as: {outfilename}")
    print(f"Used log files:")
    for logfilename in used_logs:
        print(f"\t{logfilename}")
