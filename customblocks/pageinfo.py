from yamlns import namespace as ns
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urlunsplit

class PageInfo:
    """Retrieves metadata information from a webpage: title, description,
    featured image, site icon, site name...
    """

    def __init__(self, html, url=None, **overrides):
        self._fullurl = url
        self._url = urlparse(url)
        self._html = html
        self._soup = BeautifulSoup(html, 'html.parser')
        self._overrides = overrides

    def _tag(self, name):
        tag = self._soup.find(name)
        if tag: return tag.text

    def _meta(self, name):
        meta = self._soup.find('meta', property=name)
        if meta: return meta.get('content')

    def _rel(self, name):
        rel = self._soup.find('link', rel=name)
        if not rel: return
        return rel.get('href')

    def absolute(self, relative):
        if not self._fullurl: return relative
        return urljoin(self._fullurl, relative)

    @property
    def sitename(self):
        return (
            self._overrides.get('sitename') or
            self._meta('og:site_name') or
            self._url.hostname
        )

    @property
    def siteurl(self):
        return urlunsplit((self._url.scheme, self._url.netloc,'','','')) or None

    @property
    def siteicon(self):
        return (
            self._overrides.get('siteicon') or
            self.absolute(
                self._rel('icon') or
                '/favicon.ico'
            )
        )

    @property
    def title(self):
        return (
            self._overrides.get('title') or
            self._meta('og:title') or
            self._tag('title') or
            self.sitename
        )

    @property
    def description(self):
        return (
            self._overrides.get('description') or
            self._meta('og:description') or
            self._meta('twitter:description') or
            self._meta('description') or
            ''
        )

    @property
    def image(self):
        if 'image' in self._overrides:
            return self._overrides.get('image')
        return self.absolute(
            self._meta('og:image') or
            self._meta('twitter:image') or
            self.siteicon
        )


# vim: et ts=4 sw=4
