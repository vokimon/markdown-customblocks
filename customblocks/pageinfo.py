from yamlns import namespace as ns
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urlunsplit

class PageInfo:

    def __init__(self, html, url=None):
        self._html = html
        self._soup = BeautifulSoup(html, 'html.parser')
        self._url = urlparse(url)

    def _tag(self, name):
        tag = self._soup.find(name)
        if tag: return tag.text

    def _meta(self, name):
        meta = self._soup.find('meta', property=name)
        if meta: return meta.get('content')


    @property
    def site(self):
        return self._meta('og:site') or self._url.hostname

    @property
    def siteurl(self):
        return urlunsplit((self._url.scheme, self._url.netloc,'','','')) or None

    @property
    def title(self):
        ogtitle = self._meta('og:title')
        if ogtitle: return ogtitle
        return self._tag('title') or self.site



# vim: et ts=4 sw=4
