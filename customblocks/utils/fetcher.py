import requests
from yamlns import namespace as ns

class Fetcher:

    def __init__(self, cache):
        ''

    def get(self, url):
        response = requests.get(url)
        return response



# vim: et ts=4 sw=4
