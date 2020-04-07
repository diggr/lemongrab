"""
Builds a game company network based on the company dataset.

Nodes:  game companies (or game companies and their specific production roles (
        e.g. "Nintendo_Developed By", and "Nintendo_Published By"))
Edges:  Number of games both companies worked on (based on their co-appearence in the
        release information)

Additional node information:
* label
* country information based on wikidata dataset
* num_of_games: number of games the company worked on, within the filtered dataset


Filter options:

* countries: resease country (can be multiple)
* platform (can be multiple)

"""

import networkx as nx
import json
import yaml
import os
from tqdm import tqdm
from collections import defaultdict
from itertools import combinations
from pathlib import Path
from provit import Provenance

from .combined_dataset import CompanyDataset
from .utils import load_gamelist

OUT_DIR = "company_networks"

COMPANY_DATASET = "datasets/mobygames_companies.json"
WIKIDATA_MAPPING = "datasets/wikidata_mapping.json"
ID_2_SLUG = "datasets/mobygames_companies_id_to_slug.json"

# provenance infomration
PROV_AGENT = "lemongrab.py"
PROV_ACTIVITY = "build_company_network"
PROV_DESC = "Company graph containing all companies for platforms {platforms} and release countries {countries}"


class CompanyNetworkBuilder:

    def company_ids(self, company_id, games):
        """
        Returns a list of unique ids for a game company when roles should be
        considered:
        ["<COMPANY_ID>__<ROLE1>", "<COMPANY_ID>__<ROLE2>", ... ]
        otherwise just returns company id:
        ["COMPANY_ID"]
        """
        ids = []
        if self.roles:
            roles = set([x["production_role"] for x in games])
            for role in roles:
                if not self.publisher and role == "Published by":
                    continue

                ids.append("{}__{}".format(company_id, role))
            return ids
        else:
            return [company_id]

    def _filter_games(self, ds, countries, platform, role):
        """
        Returns a list of all games a company worked on based on filter criterias countries, platform and role
        """
        if countries:
            ds = [
                x
                for x in ds
                if len(set(x["release_countries"]).intersection(set(countries))) > 0
            ]
        if platform:
            ds = [x for x in ds if platform == x["platform"]]
        if role:
            ds = [x for x in ds if x["production_role"] == role]

        return set([x["game_slug"] for x in ds])

    def _get_wiki_country(self, company_id):
        """
        Returns country information from wikidata for a mobygames compnay id :company_id:
        Returns "undefined" if no country information is available
        """
        slug = self.dataset.slug_map[company_id]
        country = ""
        if slug in self.dataset.country_map:
            country = self.dataset.country_map[slug]
        if country:
            return country
        else:
            return "undefined"

    def countries_str(self, countries):
        """
        Returns a somewhat normalized country string.
        """
        if countries:
            return "_".join(countries).replace(" ", "_")
        else:
            return ""

    def platform_str(self, platform):
        """
        Returns a somewhat normalized platform string.
        """
        if platform:
            return platform.replace(" ", "_")
        else:
            return ""

    def __init__(
        self, gamelist=None, countries=None, platform=None, roles=False, publisher=False
    ):

        self.roles = roles
        self.publisher = publisher
        self.gamelist_file = gamelist

        g = nx.Graph()
        all_games = set()

        print("generating network graph ...")
        games = {}

        self.dataset = CompanyDataset()
        if not self.gamelist_file:
            self.dataset.set_filter([platform], countries)
        else:
            gamelist = load_gamelist(self.gamelist_file)
            self.dataset.set_gamelist_filter(gamelist)

        company_list = []
        for company_id, production_roles in self.dataset.filtered_dataset.items():
            company_list += self.company_ids(company_id, production_roles)

        for c in company_list:
            g.add_node(c)

        for c1, c2 in tqdm(combinations(company_list, 2)):
            if self.roles:
                c1_id = c1.split("__")[0]
                c1_role = c1.split("__")[1]
                c2_id = c2.split("__")[0]
                c2_role = c2.split("__")[1]
            else:
                c1_id = c1
                c1_role = None
                c2_id = c2
                c2_role = None

            if c1 not in games:
                games[c1] = self._filter_games(
                    self.dataset.filtered_dataset[c1_id], countries, platform, c1_role
                )
            else:
                c1_games = games[c1]

            if c2 not in games:
                games[c2] = self._filter_games(
                    self.dataset.filtered_dataset[c2_id], countries, platform, c2_role
                )
            else:
                c2_games = games[c2]

            overlap = games[c1].intersection(games[c2])
            all_games = all_games.union(overlap)

            if len(overlap) > 0:
                g.add_edge(c1, c2, weight=len(overlap))

        # add node information
        for node in g.nodes():
            id_ = node.split("__")[0]
            if self.roles:
                role = node.split("__")[1]

            g.nodes[node]["country"] = self._get_wiki_country(id_)
            if self.roles:
                g.nodes[node]["company_name"] = self.dataset.filtered_dataset[id_][0][
                    "company_name"
                ]
                g.nodes[node]["role"] = role
                g.nodes[node]["label"] = (
                    self.dataset.filtered_dataset[id_][0]["company_name"]
                    + "("
                    + role
                    + ")"
                )
            else:
                g.nodes[node]["label"] = self.dataset.filtered_dataset[id_][0][
                    "company_name"
                ]
            g.nodes[node]["no_of_games"] = len(games[node])

        out_path = Path(OUT_DIR)
        if not out_path.is_dir():
            out_path.mkdir()
        out_filename = "company_network_"

        if self.gamelist_file:
            project_name = self.gamelist_file.split("/")[-1].replace(".yml", "")
            out_filename += project_name
        else:
            out_filename += self.countries_str(countries)
            out_filename += "_" + self.platform_str(platform)
        if self.roles:
            out_filename += "_roles"
        if self.publisher:
            out_filename += "_pub"
        out_filename += ".graphml"

        out_file = out_path / out_filename

        print("\nNetwork file saved as: {}n".format(out_file))
        nx.write_graphml(g, out_file)
        print("Nodes in network: {}".format(len(g.nodes)))
        print("Edges in network: {}".format(len(g.edges)))
        print("Games: {}".format(len(all_games)))

        prov = Provenance(out_file)
        prov.add(
            agents=[PROV_AGENT],
            activity=PROV_ACTIVITY,
            description=PROV_DESC.format(
                platforms=self.platform_str(platform),
                countries=self.countries_str(countries),
            ),
        )
        prov.save()
