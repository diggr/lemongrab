import json
import yaml

from pathlib import Path
from .settings import (
    DATASETS_DIR,
    ID_2_SLUG_FILENAME,
    MOBYGAMES_COMPANIES_FILENAME,
    WIKIDATA_MAPPING_FILENAME
)


def write_json(data, outfilename):
    with open(outfilename, "w") as outfile:
        json.dump(data, outfile, indent=4)
    return filename


def read_json(infilename):
    with open(infilename) as infile:
        return json.load(infile)


def read_yaml(infilename):
    with open(infilename) as infile:
        return yaml.safe_load(infile)


def get_datasets():
    """
    Opens dataset files and returns their contents.
    """
    mobygames_companies = read_json(Path(DATASETS_DIR) / MOBYGAMES_COMPANIES_FILENAME)
    id_2_slug = read_json(Path(DATASETS_DIR) / ID_2_SLUG_FILENAME)
    wikidata_mapping = read_json(Path(DATASETS_DIR) / WIKIDATA_MAPPING_FILENAME)
    return mobygames_companies, id_2_slug, wikidata_mapping


def load_gamelist(gamelist_file):
    with open(gamelist_file) as f:
        games = yaml.safe_load(f)

    gamelist = []
    for title, links in games.items():
        for mg_slug in links["mobygames"]:
            gamelist.append(mg_slug)

    return gamelist
