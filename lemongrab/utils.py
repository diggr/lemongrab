import yaml


def load_gamelist(gamelist_file):
    with open(gamelist_file) as f:
        games = yaml.safe_load(f)

    gamelist = []
    for title, links in games.items():
        for mg_slug in links["mobygames"]:
            gamelist.append(mg_slug)

    return gamelist
