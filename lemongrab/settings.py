import os

DIGGR_API = os.environ.get("DIGGR_API", "http://127.0.0.1:6660")
DATASETS_DIR = "lemongrab_datasets"
COMPANY_NETWORKS_DIR = "company_networks"
WIKIDATA_MAPPING_FILENAME = "wikidata_mapping.json"
MOBYGAMES_COMPANIES_FILENAME = "mobygames_companies.json"

SPARQL_ENDPOINT = "https://query.wikidata.org/sparql"
SPARQL_AGENT = "lemongrab of diggr.link"
SPARQL_QUERY = """
SELECT ?item ?itemLabel ?countryLabel ?companyId
{
  ?item wdt:P4773 ?companyId.
  OPTIONAL { ?item wdt:P17 ?country. }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
"""

PROV_AGENT = "lemongrab"

WIKIDATA_PROV_ACTIVITY = "build_wikidata_mapping"
WIKIDATA_PROV_DESC = "Contains all items in Wikidata with a Mobygames Company ID (P4773) an their country information"

COMPANIES_PROV_ACTIVITY = "build_companies_dataset"
COMPANIES_PROV_DESC = "Dataset containing all companies in mobygames and their corresponding game/release information"


