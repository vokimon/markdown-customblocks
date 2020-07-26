from yamlns import namespace as ns
from bs4 import BeautifulSoup

class PageInfo:

    def __init__(self, html):
        self._html = html
        self._soup = BeautifulSoup(html, 'html.parser')

    @property
    def title(self):
        title = self._soup.find('title')
        if title: return title.text
        ogtitle = self._soup.find('meta', property='og:title')
        if ogtitle: return ogtitle.get('content')


# vim: et ts=4 sw=4
