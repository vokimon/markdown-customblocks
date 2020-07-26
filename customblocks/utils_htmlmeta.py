from yamlns import namespace as ns
from bs4 import BeautifulSoup

def extractInfo(html):
    soup = BeautifulSoup(html, 'html.parser')
    titleElement = soup.find('title')
    return ns(
        title = titleElement.text,
    )


# vim: et ts=4 sw=4
