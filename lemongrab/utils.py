import json
import yaml


def write_json(data, outfilename):
    with open(outfilename, "w") as outfile:
        json.dump(data, outfile, indent=4)
    return filename


def read_json(infilename):
    with open(infilename, "w") as infile:
        return json.load(infile)


def load_gamelist(gamelist_file):
    with open(gamelist_file) as f:
        games = yaml.safe_load(f)

    gamelist = []
    for title, links in games.items():
        for mg_slug in links["mobygames"]:
            gamelist.append(mg_slug)

    return gamelist
