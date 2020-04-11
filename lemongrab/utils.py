import csv
import json
import yaml

from pathlib import Path
from .settings import (
    COMPANY_NETWORKS_DIR,
    DATASETS_DIR,
    LOG_FILE_EXT,
    ID_2_SLUG_FILENAME,
    MOBYGAMES_COMPANIES_FILENAME,
    WIKIDATA_MAPPING_FILENAME,
)


def write_json(data, outfilename):
    with open(outfilename, "w") as outfile:
        json.dump(data, outfile, indent=4)
    return outfilename


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


with open("eggs.csv", "w", newline="") as csvfile:
    spamwriter = csv.writer(
        csvfile, delimiter=" ", quotechar="|", quoting=csv.QUOTE_MINIMAL
    )


def build_aggregated_logs(
    outfilename, company_networks_dir=COMPANY_NETWORKS_DIR, log_file_ext=LOG_FILE_EXT
):
    """
    Aggregates all logs from the company_networks directory into a single csv.
    """
    cn_path = Path(company_networks_dir)
    used_logs = []
    with open(outfilename, "w", newline="") as csvfile:
        logwriter_csv = csv.writer(
            csvfile, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        header_written = False
        for logfilename in cn_path.glob(f"*.{log_file_ext}"):
            log = read_yaml(logfilename)
            if not header_written:
                logwriter_csv.writerow(list(log.keys()))
                header_written = True
            log["countries"] = ", ".join(log["countries"])
            logwriter_csv.writerow(list(log.values()))
            used_logs.append(logfilename)
    return outfilename, used_logs
