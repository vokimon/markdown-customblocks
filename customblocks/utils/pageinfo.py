from yamlns import namespace as ns
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urlunsplit
from decorator import decorator

@decorator
def cached(f, self):
    """After the property decorator, makes the property cached"""
    propname = f.__name__
    if propname not in self._cache:
        self._cache[propname] = f(self)
    return self._cache.get(propname)

class PageInfo:
    """Retrieves metadata information from a webpage: title, description,
    featured image, site icon, site name...
    """

    def __init__(self, html, url=None, **overrides):
        self._fullurl = url
        self._url = urlparse(url)
        self._html = html
        self._cache = overrides

    @property
    @cached
    def _soup(self):
        return BeautifulSoup(self._html, 'html.parser')

    def _tag(self, name):
        tag = self._soup.find(name)
        if tag: return tag.get_text()

    def _meta(self, name):
        meta = self._soup.find('meta', property=name)
        if meta: return meta.get('content')
        meta = self._soup.find('meta', dict(name=name))
        if meta: return meta.get('content')

    def _rel(self, name):
        rel = self._soup.find('link', rel=name)
        if not rel: return
        return rel.get('href')

    def absolute(self, relative):
        if relative is None: return None
        if not self._fullurl: return relative
        return urljoin(self._fullurl, relative)

    @property
    @cached
    def sitename(self):
        return (
            self._meta('og:site_name') or
            self._url.hostname
        )

    @property
    def siteurl(self):
        return urlunsplit((self._url.scheme, self._url.netloc,'','','')) or None

    @property
    @cached
    def siteicon(self):
        return (
            self.absolute(
                self._rel('icon') or
                '/favicon.ico'
            )
        )

    @property
    @cached
    def title(self):
        return (
            self._meta('og:title') or
            self._tag('title') or
            self.sitename
        )

    def _mediawikiDescription(self):
        if 'MediaWiki' not in (self._meta('generator') or ''):
            return
        # Not all pages have shortdescription and it is too short
        #description = self._soup.find(class_='shortdescription')
        #if description: return description

        baseurl, lemma = self._rel('canonical').split('/wiki/')
        excerpt_url = baseurl+ '/w/api.php?' + (
            f'format=json&action=query&prop=extracts&exsentences=2&exintro&titles={lemma}'
        )
        from . import Fetcher
        fetcher = Fetcher('fetchercache/wikipedia') # TODO: Configurable
        content = ns.deep(fetcher.get(excerpt_url).json())
        for page in content.query.pages.values():
            if 'extract' in page:
                return page.extract

    @property
    @cached
    def description(self):
        return (
            self._meta('og:description') or
            self._meta('twitter:description') or
            self._meta('description') or
            self._mediawikiDescription() or
            ''
        )

    @property
    @cached
    def image(self):
        return self.absolute(
            self._meta('og:image') or
            self._meta('twitter:image') or
            None
        )


# vim: et ts=4 sw=4
