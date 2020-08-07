import requests
from yamlns import namespace as ns

class Fetcher:

    def __init__(self, cache):
        self.cachedir = cache

    def _url2path(self, url):
        return self.cachedir / (
            url
                .replace('://','_')
                .replace('//','_')
                .replace('/','_')
            )

    def _response2namespace(self, response):
        result = ns(
            url=response.url,
            headers=ns(response.headers),
            status_code=response.status_code,
        )
        if 'text' in response.headers['Content-Type']:
            result.update(text=response.text)
        else:
            result.update(content=response.content)

        return result

    def get(self, url):
        response = requests.get(url)
        return response

# vim: et ts=4 sw=4
