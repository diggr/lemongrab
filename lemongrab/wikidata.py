import json

from SPARQLWrapper import SPARQLWrapper, JSON
from pathlib import Path
from provit import Provenance
from .settings import (
    DATASETS_DIR,
    SPARQL_ENDPOINT,
    SPARQL_QUERY,
    SPARQL_AGENT,
    PROV_AGENT,
    WIKIDATA_MAPPING_FILENAME,
    WIKIDATA_PROV_ACTIVITY,
    WIKIDATA_PROV_DESC,
)

def build_wikidata_mapping():
    """
    Fetches all wikidata items with a mobygames company ID.
    Result is saved as JSON to DATASETS_DIR / WIKIDATA_MAPPING_FILENAME.
    """
    sparql = SPARQLWrapper(
        SPARQL_ENDPOINT,
        agent=SPARQL_AGENT,
    )

    sparql.setQuery(SPARQL_QUERY)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    dataset = []
    for binding in results["results"]["bindings"]:
        country = None
        if "countryLabel" in binding:
            country = binding["countryLabel"]["value"]

        dataset.append(
            {
                "mobygames_slug": binding["companyId"]["value"],
                "country": country,
                "wkp": binding["item"]["value"].split("/")[-1],
            }
        )

    mapping_filename = Path(DATASETS_DIR) / WIKIDATA_MAPPING_FILENAME
    with open(mapping_filename, "w") as f:
        json.dump(dataset, f, indent=4)

    prov = Provenance(mapping_filename, overwrite=True)
    prov.add(
        agents=[PROV_AGENT],
        activity=WIKIDATA_PROV_ACTIVITY,
        description=WIKIDATA_PROV_DESC
    )
    prov.add_primary_source("wikidata")
    prov.save()


    return len(dataset), mapping_filename
