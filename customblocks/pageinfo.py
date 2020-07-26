from yamlns import namespace as ns
from bs4 import BeautifulSoup

class PageInfo:

    def __init__(self, html):
        self._html = html
        self._soup = BeautifulSoup(html, 'html.parser')

    def _tag(self, name):
        tag = self._soup.find(name)
        if tag: return tag.text

    @property
    def title(self):
        ogtitle = self._soup.find('meta', property='og:title')
        if ogtitle: return ogtitle.get('content')
        return self._tag('title')


# vim: et ts=4 sw=4
