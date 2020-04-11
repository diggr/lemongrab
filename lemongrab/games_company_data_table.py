import json
import yaml
import os

from collections import defaultdict
from .combined_dataset import get_combined_dataset
from itertools import combinations
from provit import Provenance
from tqdm import tqdm
from .utils import read_yaml, get_datasets

class GamesDataTableBuilder:

    def __init__(self, gamelist_filename):
        self.gamelist = read_yaml(gamelist_filename)
        self._load_company_dataset()

    def _load_company_dataset(self):
        dataset, id_2_slug, wiki = get_datasets()

        id_2_slug_map = {x["company_id"]: x["slug"] for x in id_2_slug}
        wiki_map = {x["mobygames_slug"]: x for x in wiki}

        self.datasets = {
            "production_details": dataset,
            "slug_map": id_2_slug_map,
            "wiki_map": wiki_map,
        }

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

        return {"platforms": list(platforms), "companies": companies_dataset}


