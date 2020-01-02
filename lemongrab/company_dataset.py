import json
import diggrtoolbox as dt
from collections import defaultdict
from tqdm import tqdm
from provit import Provenance
from .diggr_api import DiggrApi

OUT_FILE = "datasets/mobygames_companies.json"

PROV_AGENT = "lemongrab.py"
PROV_ACTIVITY = "build_companies_dataset"
PROV_DESC = "Dataset containing all companies in mobygames and their corresponding game/release information"

def build_company_dataset():

    api = DiggrApi("http://172.18.85.170:6660")
    pm = dt.PlatformMapper("mobygames")

    dataset = defaultdict(list)

    for id_ in tqdm(api.mobygames_ids()):
        data = api.entry("mobygames", id_)
        slug = data["raw"]["moby_url"].split("/")[-1]

        for platform in data["raw"]["platforms"]:
            for release in platform["releases"]:
                for company in release["companies"]:
                    dataset[company["company_id"]].append({
                        "company_name": company["company_name"],
                        "game_id": id_,
                        "game_slug": slug,
                        "game_title": data["title"],
                        "game_years": data["years"],
                        "production_role": company["role"],
                        "release_countries": release["countries"],
                        "platform": pm[platform["platform_name"]]
                    })
        
    print("Save company dataset as: {}".format(OUT_FILE))
    with open(OUT_FILE,"w") as f:
        json.dump(dict(dataset), f, indent=4)

    prov = Provenance(OUT_FILE, overwrite=True)
    prov.add(
        agents = [PROV_AGENT],
        activity = PROV_ACTIVITY,
        description = PROV_DESC
    )
    prov.add_primary_source("mobygames")
    prov.add_primary_source("diggr_platform_mapping")
    prov.save()
