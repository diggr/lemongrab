import json
import pandas as pd
from tqdm import tqdm
from collections import Counter,defaultdict

BASE_DATASET = "datasets/mobygames_companies.json"
SLUG_MAPPING = "datasets/mobygames_companies_id_to_slug.json"
WIKI_MAPPING = "datasets/wikidata_mapping.json"

class CompanyDataset():

    def set_filter(self, platforms, countries):
        companies_games = defaultdict(set)
        countries = set(countries)
        for company_id, games in self.base_dataset.items():
            
            platforms_ = set()
            countries_ = set()

            for game in games:
                add = False
                if game["platform"] in platforms or len(platforms) == 0:
                    #companies.update([ game["company_name"] ])
                    if len(countries) > 0:
                        if len(countries.intersection(game["release_countries"])) > 0:
                            add = True
                    else:
                        add = True
                        
                if add:
                    companies_games[ company_id ].update([ game["game_slug"] ])

        self.companies = Counter({ self.base_dataset[x][0]["company_name"]: len(y) for x, y in companies_games.items() })
        self.companies_games = companies_games

        self.countries_acc = defaultdict(set)
        self.companies_with_country = 0
        for company_id in self.companies_games.keys():
            if company_id in self.slug_map:
                slug = self.slug_map[company_id]
                if slug in self.country_map:
                    self.companies_with_country += 1
                    self.countries_acc[self.country_map[slug]].add(self.base_dataset[company_id][0]["company_name"])
        
        self.countries_accumulated = Counter({x: len(y) for x, y in self.countries_acc.items() })


    def get_data(self):
        self.platforms = set()
        self.countries = set()
        for games in self.base_dataset.values():
            for game in games:
                if game["platform"]:
                    self.platforms.add(game["platform"])
                self.countries.update([ country for country in game["release_countries"] if country ])

        self.platforms = sorted(list(self.platforms))
        self.countries = sorted(list(self.countries))


    def __init__(self):
        with open(BASE_DATASET) as f:
            self.base_dataset = json.load(f)

        with open(SLUG_MAPPING) as f:
            data = json.load(f) 
        self.slug_map = { x["company_id"]: x["slug"] for x in data }

        with open(WIKI_MAPPING) as f:
            data = json.load(f)
        self.country_map = { x["mobygames_slug"]: x["country"] for x in data if x["country"] }

        self.get_data()