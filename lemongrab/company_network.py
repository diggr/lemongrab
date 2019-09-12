import networkx as nx
import json
from tqdm import tqdm
from itertools import combinations

COMPANY_DATASET = "datasets/mobygames_companies.json"
WIKIDATA_MAPPING = "datasets/wikidata_mapping.json"
ID_2_SLUG = "datasets/mobygames_companies_id_to_slug.json"




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
    
    def _filter_dataset(self, dataset, countries, platform):
        filtered_ids = []
        for company_id, games in dataset.items():


            if not platform and not countries:
                filtered_ids.append(company_id)
                continue

            r_countries = set()
            platforms = set()
            for game in games:
                r_countries.update(game["release_countries"])
                platforms.update([ game["platform"]])
        
            c_overlap = len(set(countries).intersection(r_countries))

            if platform and not countries:
                if platform in platforms:
                    filtered_ids.append(company_id)
            elif countries and not platform:
                if c_overlap > 0:
                    filtered_ids.append(company_id)
            else:
                if c_overlap > 0 and platform in platforms:
                    filtered_ids.append(company_id)

        print(len(filtered_ids))
        return filtered_ids


    def _filter_games(self, ds, countries, platform):
        if countries:
            ds = [ x for x in ds if len(set(x["release_countries"]).intersection(set(countries))) > 0 ]
        if platform:
            ds = [ x for x in ds if platform == x["platform"]]

        return set([ x["game_slug"] for x in ds ])

    def __init__(self, countries=None, platform=None):
        companies = load_company_dataset()
        slug_map = companies["slug_map"]

        g = nx.Graph()
        
        all_games = set()
        print("generating network graph ...")
        for c1, c2 in tqdm(combinations(self._filter_dataset(companies["production_details"], countries, platform), 2)):

            c1_games = self._filter_games(companies["production_details"][c1], countries, platform)
            c2_games = self._filter_games(companies["production_details"][c2], countries, platform)

            overlap = c1_games.intersection(c2_games)
            all_games = all_games.union(overlap)

            if len(overlap) > 0:
                g.add_edge(c1, c2, weight=len(overlap))
        
        for node in g.nodes():
            slug = slug_map[node]
            country = None
            if node in companies["wiki_map"]:
                country = companies["wiki_map"][node]["country"]
            if not country:
                country = "undefined"
            g.nodes[node]["country"] = country
            g.nodes[node]["label"] = companies["production_details"][node][0]["company_name"]

        out_file = "company_networks/company_network_"
        if countries:
            out_file += "_".join(countries).replace(" ", "_")
        if platform:
            out_file += "_{}".format(platform.replace(" ","_"))
        out_file += ".graphml"

        print("\nNetwork file saved as: {}\n".format(out_file))
        nx.write_graphml(g, out_file)
        print("Nodes in network: {}".format(len(g.nodes)))
        print("Edges in network: {}".format(len(g.edges)))
        print("Games: {}".format(len(all_games)))

