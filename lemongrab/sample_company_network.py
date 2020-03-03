"""
Builds a network of companies based on a tulpa generated
company sample.
"""

import networkx as nx

from .company_network import PROV_AGENT, PROV_ACTIVITY
from dataclasses import dataclass
from itertools import combinations
from pprint import pprint
from provit import Provenance
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


class SampleCompanyNetwork:

    def __init__(self, game_company_sample):
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
            self.graph.add_node(c.company_id)
            self.graph.nodes[c.company_id]["label"] = c.company_name
            self.graph.nodes[c.company_id]["role"] = c.role
            self.graph.nodes[c.company_id]["platform"] = c.platform


        for c1, c2 in tqdm(combinations(self.companies, 2)):
            c1_games = set(self._filter_games(c1))
            c2_games = set(self._filter_games(c2))

            overlap = c1_games.intersection(c2_games)
            all_games = set().union(overlap)

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
            activity = PROV_ACTIVITY,
            description = "Build company network based on tulpa exported sample"
        )
        prov.save()
