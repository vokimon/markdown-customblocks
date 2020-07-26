from yamlns import namespace as ns
from bs4 import BeautifulSoup

class PageInfo:

    def __init__(self, html, url=None):
        self._html = html
        self._soup = BeautifulSoup(html, 'html.parser')

    def _tag(self, name):
        tag = self._soup.find(name)
        if tag: return tag.text

    def _meta(self, name):
        meta = self._soup.find('meta', property=name)
        if meta: return meta.get('content')


    @property
    def site(self):
        return self._meta('og:site')

    @property
    def title(self):
        ogtitle = self._meta('og:title')
        if ogtitle: return ogtitle
        return self._tag('title')



# vim: et ts=4 sw=4
