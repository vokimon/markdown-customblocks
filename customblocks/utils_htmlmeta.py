from yamlns import namespace as ns
from bs4 import BeautifulSoup

class PageInfo:

    def __init__(self, html):
        self._html = html
        self._soup = BeautifulSoup(html, 'html.parser')

    @property
    def title(self):
        return self._soup.find('title').text


# vim: et ts=4 sw=4
