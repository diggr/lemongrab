from SPARQLWrapper import SPARQLWrapper, JSON
from provit import Provenance
import json

SPARQL_ENDPOINT = "https://query.wikidata.org/sparql"
QUERY = """
SELECT ?item ?itemLabel ?countryLabel ?companyId
{
  ?item wdt:P4773 ?companyId. 
  OPTIONAL { ?item wdt:P17 ?country. }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
"""

MAPPING_FILE = "datasets/wikidata_mapping.json"

PROV_AGENT = "lemongrab.py"
PROV_ACTIVITY = "build_wikidata_mapping"
PROV_DESC = "Contains all items in Wikidata with a Mobygames Company ID (P4773) an their country information"


def build_wikidata_mapping():
    sparql = SPARQLWrapper(SPARQL_ENDPOINT)

    sparql.setQuery(QUERY)
    sparql.setReturnFormat(JSON)    
    results = sparql.query().convert()

    dataset = []
    for binding in results["results"]["bindings"]:
        country = None
        if "countryLabel" in binding:
            country = binding["countryLabel"]["value"]

        dataset.append({
            "mobygames_slug": binding["companyId"]["value"],
            "country": country,
            "wkp": binding["item"]["value"].split("/")[-1]
        })

    print("Wikidata items with Mobygames Company ID: {}".format(len(dataset)))

    with open(MAPPING_FILE, "w") as f:
        json.dump(dataset, f, indent=4)
    
    prov = Provenance(MAPPING_FILE, overwrite=True)
    prov.add(
        agents = [PROV_AGENT],
        activity = PROV_ACTIVITY,
        description = PROV_DESC
    )
    prov.add_primary_source("wikidata")
    prov.save()

    print("\nMapping file saved as: {}".format(MAPPING_FILE))