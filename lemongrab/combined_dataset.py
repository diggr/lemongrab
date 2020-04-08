import json

from tqdm import tqdm
from collections import Counter, defaultdict
from .settings import (
    DATASETS_DIR,
    MOBYGAMES_COMPANIES_FILENAME,
    ID_2_SLUG_FILENAME,
    WIKIDATA_MAPPING
)
from .utils import read_json

class CombinedDataset:
    """
    Prepares a company dataset for the lemongrab browser

    Use the factory get_combined_dataset to inistanciate!
    dataset = get_combined_dataset()
    dataset.set_filter(platforms, countries)
    overview = dataset.get_overview()
    """
    def __init__(self, mobygames_companies, id_2_slug, wikidata_mapping)
        self.base_dataset = mobygames_companies
        self.slug_map = {x["company_id"]: x["slug"] for x in id_2_slug}
        self.country_map = {
            x["mobygames_slug"]: x["country"] for x in wikidata_mapping if x["country"]
        }
        self.setup_data()

    def get_company_data(self, company_name):
        pass

    def get_company_country_data(self, company):
        pass

    def get_production_role_data(self, production_role):
        pass

    def get_overview(self):
        production_roles = Counter()
        companies = Counter()
        companies_games = defaultdict(set)
        companies_with_country = 0
        countries_accumulated = Counter()
        games_dataset = defaultdict(list)

        for company_id, games in self.filtered_dataset.items():

            company_country = ""
            company_slug = self.slug_map[company_id]
            if company_slug in self.country_map:
                company_country = self.country_map[company_slug]

            for game in games:
                companies_games[company_id].update([game["game_slug"]])
                production_roles.update([game["production_role"]])

                games_dataset[game["game_slug"]].append(
                    {
                        "game_title": game["game_title"],
                        "company_name": game["company_name"],
                        "company_country": company_country,
                        "production_role": game["production_role"],
                    }
                )

        companies = Counter(
            {
                self.base_dataset[x][0]["company_name"]: len(y)
                for x, y in companies_games.items()
            }
        )
        companies_games = companies_games

        countries_acc = defaultdict(set)
        companies_with_country = 0
        for company_id in companies_games.keys():
            if company_id in self.slug_map:
                slug = self.slug_map[company_id]
                if slug in self.country_map:
                    companies_with_country += 1
                    countries_acc[self.country_map[slug]].add(
                        self.base_dataset[company_id][0]["company_name"]
                    )

        countries_accumulated = Counter({x: len(y) for x, y in countries_acc.items()})

        return {
            "companies": companies,
            "companies_most_common": list(companies.most_common(30)),
            "company_games": dict(companies_games),
            "company_countries": list(countries_accumulated.most_common(200)),
            "companies_with_country": companies_with_country,
            "production_roles": list(production_roles.most_common(50)),
            "games_table": dict(games_dataset),
        }

    def set_gamelist_filter(self, gamelist):
        self.filtered_dataset = {}

        for company_id, games in self.base_dataset.items():
            filtered_games = []
            for game in games:
                if game["game_slug"] in gamelist:
                    filtered_games.append(game)

            if len(filtered_games) > 0:
                self.filtered_dataset[company_id] = filtered_games

    def set_filter(self, platforms, countries):
        self.filtered_dataset = {}
        countries = set(countries)
        for company_id, games in self.base_dataset.items():

            filtered_games = []
            for game in games:
                add = False
                if game["platform"] in platforms or len(platforms) == 0:
                    # companies.update([ game["company_name"] ])
                    if len(countries) > 0:
                        if len(countries.intersection(game["release_countries"])) > 0:
                            add = True
                    else:
                        add = True

                if add:
                    filtered_games.append(game)
            if len(filtered_games) > 0:
                self.filtered_dataset[company_id] = filtered_games

    def setup_data(self):
        self.platforms = set()
        self.countries = set()
        self.roles = set()
        for games in self.base_dataset.values():
            for game in games:
                if game["platform"]:
                    self.platforms.add(game["platform"])
                self.countries.update(
                    [country for country in game["release_countries"] if country]
                )

        self.platforms = sorted(list(self.platforms))
        self.countries = sorted(list(self.countries))


def get_combined_dataset():
    """
    Factory which returns an instance of CombinedDataset.
    """
    mobygames_companies = read_json(Path(DATASETS_DIR) / MOBYGAMES_COMPANIES_FILENAME)
    id_2_slug = read_json(Path(DATASETS_DIR) / ID_2_SLUG_FILENAME)
    wikidata_mapping = read_json(Path(DATASETS_DIR) / WIKIDATA_MAPPING_FILENAME)
    return CombinedDataset(mobygames_companies, id_2_slug, wikidata_mapping)
