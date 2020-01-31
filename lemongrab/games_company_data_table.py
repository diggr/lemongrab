

import json
import yaml
import os
from tqdm import tqdm
from collections import defaultdict
from itertools import combinations
from provit import Provenance

COMPANY_DATASET = "datasets/mobygames_companies.json"
WIKIDATA_MAPPING = "datasets/wikidata_mapping.json"
ID_2_SLUG = "datasets/mobygames_companies_id_to_slug.json"




class GamesDataTableBuilder():



    def _load_gamelist(self, gamelist_file):
        with open(gamelist_file) as f:
            games = yaml.safe_load(f)
        return games

    def _load_company_dataset(self):
        with open(COMPANY_DATASET) as f:
            dataset = json.load(f)
        with open(WIKIDATA_MAPPING) as f:
            wiki = json.load(f)
        with open(ID_2_SLUG) as f:
            id_2_slug = json.load(f)

        id_2_slug_map = { x["company_id"]: x["slug"] for x in id_2_slug }
        wiki_map = { x["mobygames_slug"]: x for x in wiki }

        self.datasets = {
            "production_details": dataset,
            "slug_map": id_2_slug_map,
            "wiki_map": wiki_map }

    def _get_data(self, mg_slugs):
        platforms = set()
        companies = self.datasets["production_details"]

        companies_dataset = defaultdict(set)

        for company_id, details in companies.items():
            for entry in details:
                if entry["game_slug"] in mg_slugs:
                    slug = self.datasets["slug_map"][company_id]
                    if slug in self.datasets["wiki_map"]:
                        country = self.datasets["wiki_map"][slug]["country"] 
                    else:
                        country = "unknown"
                    companies_dataset[country].add(company_id)
                    platforms.add(entry["platform"])
        
        return {
            "platforms": list(platforms),
            "companies": companies_dataset
        }



    def __init__(self, gamelist):
        self.gamelist = self._load_gamelist(gamelist)    
        self._load_company_dataset()

        for title, links in self.gamelist.items():
            data = self._get_data(links["mobygames"])

            print(data)
            break