"""
Builds a network of companies based on a tulpa generated
company sample.
"""

import networkx as nx

from .combined_dataset import get_combined_dataset
from dataclasses import dataclass
from itertools import combinations
from pprint import pprint
from provit import Provenance
from .settings import (
    PROV_AGENT,
    SAMPLE_PROV_ACTIVITY,
    SAMPLE_PROV_DESC
)
from tqdm import tqdm
from typing import List


@dataclass
class Company:

    company_id: int
    company_name: str
    role: str
    release_countries: List[str]
    platform : str
    game_slug : str


def get_wiki_country(c_id, company_dataset, none_return="undefined"):
    """
    Returns country information from wikidata for a mobygames company id.
    If no country is available "undefined" is returned. If None or something
    else is desired to be returned in case no country is available, this
    value can be set with the none_return parameter.
    """
    slug = company_dataset.slug_map.get(str(c_id), None)
    if slug:
        return company_dataset.country_map.get(slug, none_return)
    else:
        return none_return


class SampleCompanyNetwork:

    def __init__(self, game_company_sample):
        self.company_dataset = get_combined_dataset()
        self.games = list(game_company_sample.keys())
        self.companies = [Company(**c) for g in game_company_sample.values() for c in g]
        self.graph = nx.Graph()
        self.graph_done = False

    def _filter_games(self, company):
        games = []
        for c in self.companies:
            if c.company_id == company.company_id:
                games.append(c.game_slug)
        return games

    def build_network(self):

        for c in self.companies:
            c_id = c.company_id
            self.graph.add_node(c_id)
            self.graph.nodes[c_id]["role"] = c.role
            self.graph.nodes[c_id]["platform"] = c.platform
            self.graph.nodes[c_id]["country"] = get_wiki_country(c_id, self.company_dataset)
            self.graph.nodes[c_id]["name"] = c.company_name


        for c1, c2 in tqdm(combinations(self.companies, 2)):
            c1_games = set(self._filter_games(c1))
            c2_games = set(self._filter_games(c2))

            overlap = c1_games.intersection(c2_games)

            if len(overlap):
                self.graph.add_edge(c1.company_id, c2.company_id, weight=len(overlap))

        self.graph_done = True

        return self

    def save_network(self, outfilename):
        if self.graph_done:
            nx.write_graphml(self.graph, outfilename)
        else:
            raise RuntimeError("Graph must be created before it can be saved.")
        self._write_prov(outfilename)
        return self

    def _write_prov(self, outfilename):
        prov = Provenance(outfilename)
        prov.add(
            agents = [PROV_AGENT],
            activity = SAMPLE_PROV_ACTIVITY,
            description = SAMPLE_PROV_DESC
        )
        prov.save()
