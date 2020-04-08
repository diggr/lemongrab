"""
Builds a reduced local company dataset from the unified api mobygames dataset.

The dataset is dictionary with the (mobygames) company id as its key, and a list of
the production roles for all the games the company was involved in.

<company_id>: [ <game_1_prod_info_1>, <game_1_prod_info_2>, <game_3_prod_info_1> , ... ]


The production information contain the data points:

Company-specific information:
* company_name
* production role

Game-specific information:
* game_id
* game_slug
* game_title
* game_years
* release_countries
* platform

"""
import json

from collections import defaultdict
from .diggr_api import DiggrApi
import diggrtoolbox as dt
from provit import Provenance
from .settings import (
    DATASETS_DIR,
    DIGGR_API,
    MOBYGAMES_COMPANIES_FILENAME,
    COMPANIES_PROV_ACTIVITY,
    COMPANIES_PROV_DESC,
    PROV_AGENT,
)
from tqdm import tqdm


def build_mobygames_companies(unified_api_url=DIGGR_API):

    api = DiggrApi(unified_api_url)
    pm = dt.PlatformMapper("mobygames")

    dataset = defaultdict(list)

    for id_ in tqdm(api.mobygames_ids()):
        data = api.entry("mobygames", id_)
        slug = data["raw"]["moby_url"].split("/")[-1]

        for platform in data["raw"]["platforms"]:
            for release in platform["releases"]:
                for company in release["companies"]:
                    dataset[company["company_id"]].append(
                        {
                            "company_name": company["company_name"],
                            "game_id": id_,
                            "game_slug": slug,
                            "game_title": data["title"],
                            "game_years": data["years"],
                            "production_role": company["role"],
                            "release_countries": release["countries"],
                            "platform": pm[platform["platform_name"]],
                        }
                    )

    mobygames_companies_filename = Path(DATASETS_DIR) / MOBYGAMES_COMPANIES_FILENAME
    with open(OUT_FILE, "w") as f:
        json.dump(dict(dataset), f, indent=4)

    prov = Provenance(OUT_FILE, overwrite=True)
    prov.add(agents=[PROV_AGENT], activity=PROV_ACTIVITY, description=PROV_DESC)
    prov.add_primary_source("mobygames")
    prov.add_primary_source("diggr_platform_mapping")
    prov.save()

    return mobygames_companies_filename
