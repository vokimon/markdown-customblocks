import json
from pathlib import Path
import requests
from yamlns import namespace as ns

class Fetcher:

    def __init__(self, cache):
        self.cachedir = Path(cache)
        if not self.cachedir.exists():
            self.cachedir.mkdir(parents=True)

    def _url2path(self, url):
        return self.cachedir / (
            url
                .replace('://','_')
                .replace('//','_')
                .replace('/','_')
            )

    def clear(self):
        for item in self.cachedir.glob('*'):
            item.unlink()
        if self.cachedir.exists():
            self.cachedir.rmdir()


    @staticmethod
    def _response2namespace(response):
        result = ns(
            url=response.url,
            headers=ns(response.headers),
            status_code=response.status_code,
        )
        try:
            result.update(json=response.json())
        except Exception:
            if 'text' in response.headers['Content-Type']:
                result.update(
                    text=response.text,
                    encoding=response.encoding,
                )
            else:
                result.update(content=response.content)

        return result

    @staticmethod
    def _namespace2response(namespace):
        result = requests.Response()
        for key in namespace:
            if key in ('content', 'text', 'json'): continue
            setattr(result, key, namespace[key])
        if 'text' in namespace:
            result._content = namespace.text.encode(namespace.encoding)
        elif 'json' in namespace:
            result._content = json.dumps(namespace.json).encode('utf8')
        else:
            result._content = namespace.content
        return result

    def get(self, url):
        cachefile = self._url2path(url)
        if cachefile.exists():
            info = ns.load(str(cachefile))
            return self._namespace2response(info)
        response = requests.get(url)
        if response.ok:
            self._response2namespace(response).dump(self._url2path(url))
        return response

    def remove(self, url):
        cachefile = self._url2path(url)
        cachefile.unlink()

# vim: et ts=4 sw=4
