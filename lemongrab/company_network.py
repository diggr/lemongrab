import networkx as nx
import yaml

from .combined_dataset import get_combined_dataset
from itertools import combinations
from pathlib import Path
from provit import Provenance
from .settings import (
    COMPANY_NETWORKS_DIR,
    LOG_FILE_EXT,
    NETWORK_PROV_ACTIVITY,
    NETWORK_PROV_DESC,
    PROV_AGENT,
)
from .utils import load_gamelist
from tqdm import tqdm


class CompanyNetworkBuilder:
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

    def __init__(
        self,
        gamelist=None,
        countries=None,
        platform=None,
        roles=False,
        publisher=False,
        log_file_ext=LOG_FILE_EXT,
    ):

        self.roles = roles
        self.countries = countries
        self.platform = platform
        self.publisher = publisher
        self.gamelist_file = gamelist

        self.log_file_extension = log_file_ext

    def build(self):

        g = nx.Graph()
        all_games = set()

        games = {}

        self.dataset = get_combined_dataset()
        if not self.gamelist_file:
            self.dataset.set_filter([self.platform], self.countries)
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
                    self.dataset.filtered_dataset[c1_id],
                    self.countries,
                    self.platform,
                    c1_role,
                )

            if c2 not in games:
                games[c2] = self._filter_games(
                    self.dataset.filtered_dataset[c2_id],
                    self.countries,
                    self.platform,
                    c2_role,
                )

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

        out_path = Path(COMPANY_NETWORKS_DIR)
        out_filename = "company_network_"

        if self.gamelist_file:
            project_name = self.gamelist_file.split("/")[-1].replace(".yml", "")
            out_filename += project_name
        else:
            out_filename += self.countries_str(self.countries)
            out_filename += "_" + self.platform_str(self.platform)
        if self.roles:
            out_filename += "_roles"
        if self.publisher:
            out_filename += "_pub"

        out_filename += ".graphml"
        out_file = out_path / out_filename
        nx.write_graphml(g, out_file)

        prov = Provenance(out_file)
        prov.add(
            agents=[PROV_AGENT],
            activity=NETWORK_PROV_ACTIVITY,
            description=NETWORK_PROV_DESC.format(
                platforms=self.platform_str(self.platform),
                countries=self.countries_str(self.countries),
            ),
        )
        prov.save()

        self._write_log(out_file, len(g.nodes), len(g.edges), len(all_games))

        return out_file, len(g.nodes), len(g.edges), len(all_games)

    def _write_log(self, out_file, n_nodes, n_edges, n_games):
        """
        Write the parameters and results into a logfile.
        """
        log = {
            "countries": list(self.countries),
            "platform": self.platform,
            "roles": self.roles,
            "publisher": self.publisher,
            "nodes": n_nodes,
            "edges": n_edges,
            "games": n_games,
        }

        with open(f"{out_file}_log.{self.log_file_ext}", "w") as outfile:
            yaml.dump(log, outfile)

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
        Returns a list of all games a company worked on based on filter criterias countries,
        platform and role
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


def build_company_network(
    gamelist=None, countries=None, platform=None, roles=False, publisher=False
):
    """
    CompanyNetworkBuilder factory which runs the build
    and returns stats about the result.
    """
    cn_builder = CompanyNetworkBuilder(gamelist, countries, platform, roles, publisher)
    return cn_builder.build()
