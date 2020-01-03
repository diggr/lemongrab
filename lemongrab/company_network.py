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
from tqdm import tqdm
from itertools import combinations
from provit import Provenance

COMPANY_DATASET = "datasets/mobygames_companies.json"
WIKIDATA_MAPPING = "datasets/wikidata_mapping.json"
ID_2_SLUG = "datasets/mobygames_companies_id_to_slug.json"

#provenance infomration
PROV_AGENT = "lemongrab.py"
PROV_ACTIVITY = "build_company_network"
PROV_DESC = "Company graph containing all companies for platforms {platforms} and release countries {countries}"

def load_company_dataset():
    with open(COMPANY_DATASET) as f:
        ds = json.load(f)
    with open(WIKIDATA_MAPPING) as f:
        wiki = json.load(f)
    with open(ID_2_SLUG) as f:
        id_2_slug = json.load(f)

    id_2_slug_map = { x["company_id"]: x["slug"] for x in id_2_slug }
    wiki_map = { x["mobygames_slug"]: x for x in wiki }

    return {
        "production_details": ds,
        "slug_map": id_2_slug_map,
        "wiki_map": wiki_map
    }


class CompanyNetworkBuilder():
    

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
            roles = set([ x["production_role"] for x in games ])
            for role in roles:
                if not self.publisher and role == "Published by":
                    continue

                ids.append("{}__{}".format(company_id, role))
            return ids
        else:
            return [ company_id ]


    def _filter_dataset(self, dataset, countries, platform):
        """
        Returns a list of company_ids who worked on games released in :countries:
        and on :platform:
        """
        filtered_ids = []
        for company_id, games in dataset.items():


            if not platform and not countries:
                filtered_ids.append(company_id)
                continue

            r_countries = set()
            platforms = set()
            for game in games:
                r_countries.update(game["release_countries"])
                platforms.update([game["platform"]])
        
            c_overlap = len(set(countries).intersection(r_countries))

            if platform and not countries:
                if platform in platforms:
                    filtered_ids += self.company_ids(company_id, games)

            elif countries and not platform:
                if c_overlap > 0:
                    filtered_ids += self.company_ids(company_id, games)
            else:
                if c_overlap > 0 and platform in platforms:
                    filtered_ids += self.company_ids(company_id, games)

        print(len(filtered_ids))
        return filtered_ids


    def _filter_games(self, ds, countries, platform, role):
        """
        Returns a list of all games a company worked on based on filter criterias countries, platform and role
        """
        if countries:
            ds = [ x for x in ds if len(set(x["release_countries"]).intersection(set(countries))) > 0 ]
        if platform:
            ds = [ x for x in ds if platform == x["platform"]]
        if role:
            ds = [ x for x in ds if x["production_role"] == role]

        return set([ x["game_slug"] for x in ds ])



    def _get_wiki_country(self, company_id):
        """
        Returns country information from wikidata for a mobygames compnay id :company_id:
        Returns "undefined" if no country information is available
        """        
        slug = self.companies["slug_map"][company_id]
        country = ""
        if slug in self.companies["wiki_map"]:
            country = self.companies["wiki_map"][slug]["country"]
        if country:
            return country
        else:
            return "undefined"


    def countries_str(self, countries):
        if countries:
            return "_".join(countries).replace(" ", "_")
        else:
            return ""


    def platform_str(self, platform):
        if platform:
            return platform.replace(" ","_")
        else:
            return ""


    def __init__(self, countries=None, platform=None, roles=False, publisher=False):

        self.roles = roles
        self.publisher = publisher

        self.companies = load_company_dataset()
        #slug_map = companies["slug_map"]

        g = nx.Graph()
        
        all_games = set()

        print("generating network graph ...")
        games = {}
        for c1, c2 in tqdm(combinations(self._filter_dataset(self.companies["production_details"], countries, platform), 2)):

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
                games[c1] = self._filter_games(self.companies["production_details"][c1_id], countries, platform, c1_role)
            else:
                c1_games = games[c1]

            if c2 not in games:
                games[c2] = self._filter_games(self.companies["production_details"][c2_id], countries, platform, c2_role)
            else:
                c2_games = games[c2]

            overlap = games[c1].intersection(games[c2])
            all_games = all_games.union(overlap)

            if len(overlap) > 0:
                g.add_edge(c1, c2, weight=len(overlap))
        
        #add node information
        for node in g.nodes():
            id_ = node.split("__")[0]
            if self.roles:
                role = node.split("__")[1]

            g.nodes[node]["country"] = self._get_wiki_country(id_)
            if self.roles:
                g.nodes[node]["label"] = self.companies["production_details"][id_][0]["company_name"] + "(" + role + ")"
            else:
                g.nodes[node]["label"] = self.companies["production_details"][id_][0]["company_name"]
            g.nodes[node]["no_of_games"] = len(games[node])

        out_file = "company_networks/company_network_"
        out_file += self.countries_str(countries)
        out_file += "_"+self.platform_str(platform)
        if self.roles:
            out_file += "_roles"
        if self.publisher:
            out_file += "_pub"
        out_file += ".graphml"

        print("\nNetwork file saved as: {}\n".format(out_file))
        nx.write_graphml(g, out_file)
        print("Nodes in network: {}".format(len(g.nodes)))
        print("Edges in network: {}".format(len(g.edges)))
        print("Games: {}".format(len(all_games)))

        prov = Provenance(out_file)
        prov.add(
            agents = [PROV_AGENT],
            activity = PROV_ACTIVITY,
            description = PROV_DESC.format(
                platforms=self.platform_str(platform), 
                countries=self.countries_str(countries)) 
        )
        prov.save()
