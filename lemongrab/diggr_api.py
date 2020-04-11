"""
Simple wrapper for diggr api for easier data access
"""

import requests

MA_IDS = "/mediaartdb"
MG_IDS = "/mobygames"

MG_BY_SLUG = "/mobygames/slug/{slug}"

LINKS = "/{dataset}/{id}/links"

ENTRY = "/{dataset}/{id}"


class DiggrApi:
    """
    Wrapper around the unifiedAPI by diggr.
    """

    def __init__(self, base_url):
        self.session = requests.Session()
        self.base_url = base_url

    def _call(self, url):
        try:
            rsp = self.session.get(url)
            data = rsp.json()
            return data
        except:
            print("invalid api call: {}".format(url))
            return None

    def mobygames_ids(self):
        data = self._call(self.base_url + MG_IDS)
        return data["ids"]

    def mediaartdb_ids(self):
        data = self._call(self.base_url + MA_IDS)
        return data["ids"]

    def links(self, dataset, id_):
        data = self._call(self.base_url + LINKS.format(dataset=dataset, id=id_))
        return data["links"]

    def entry(self, dataset, id_):
        data = self._call(self.base_url + ENTRY.format(dataset=dataset, id=id_))
        try:
            return data["entry"]
        except:
            print("no data available for {}/{}".format(dataset, id_))
            return None

    def mobygames_slug_to_id(self, slug):
        data = self._call(self.base_url + MG_BY_SLUG.format(slug=slug))
        try:
            return data["entry"]["id"]
        except:
            print("couldn't retrieve mobygames id for slug {}".format(slug))
            return None


