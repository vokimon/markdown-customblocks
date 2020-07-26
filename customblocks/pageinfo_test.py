import unittest
from .pageinfo import PageInfo
from .utils import E
from xml.etree import ElementTree as etree

class PageInfo_Test(unittest.TestCase):

    def html(self, e):
        return etree.tostring(e, 'unicode')

    from yamlns.testutils import assertNsEqual

    def test_title_fromTitleTag(self):
        info = PageInfo(self.html(
            E('html',
                E('head',
                    E('title','My title'),
                )
            )
        ))
        self.assertEqual(info.title, "My title")


    def test_title_withNoTitle(self):
        info = PageInfo(self.html(
            E('html',
            )
        ))
        self.assertEqual(info.title, None)

    def test_title_openGraphTitle(self):
        info = PageInfo(self.html(
            E('html',
                E('head',
                    E('meta',
                        property='og:title',
                        content='OG Title',
                    )
                )
            )
        ))
        self.assertEqual(info.title, "OG Title")

    def test_title_openGraphPrioritized(self):
        info = PageInfo(self.html(
            E('html',
                E('head',
                    E('title','My title'),
                    E('meta',
                        property='og:title',
                        content='OG Title',
                    )
                )
            )
        ))
        self.assertEqual(info.title, "OG Title")

    def test_sitename_fromMeta(self):
        info = PageInfo(self.html(
            E('html',
                E('head',
                    E('meta',
                        property='og:site_name',
                        content='OG Site',
                    )
                )
            )
        ), url='http://www.mydomain.com/page/subpage')

        self.assertEqual(info.sitename, "OG Site")

    def test_sitename_fromDomain(self):
        info = PageInfo(self.html(
            E('html',
            )
        ), url='http://www.mydomain.com/page/subpage')

        self.assertEqual(info.sitename, "www.mydomain.com")

    def test_sitename_noSource(self):
        info = PageInfo(self.html(
            E('html',
            )
        ))

        self.assertEqual(info.sitename, None)

    def test_title_whenNoSource_takeSiteName(self):
        info = PageInfo(self.html(
            E('html',
            )
        ), url='http://www.mydomain.com/page/subpage')
        self.assertEqual(info.title, 'www.mydomain.com')

    def test_siteurl(self):
        info = PageInfo(self.html(
            E('html',
            )
        ), url='http://www.mydomain.com/page/subpage')
        self.assertEqual(info.siteurl, 'http://www.mydomain.com')

    def test_siteurl_noUrlProvided(self):
        info = PageInfo(self.html(
            E('html',
            )
        ))
        self.assertEqual(info.siteurl, None)

    def test_description_noDescription(self):
        info = PageInfo(self.html(
            E('html',
            )
        ))
        self.assertEqual(info.description, "")

    def test_description_fromMeta(self):
        info = PageInfo(self.html(
            E('html',
                E('head',
                    E('meta',
                        property='description',
                        content='HTML Description',
                    ),
                )
            )
        ))
        self.assertEqual(info.description, "HTML Description")

    def test_description_fromTwitter(self):
        info = PageInfo(self.html(
            E('html',
                E('head',
                    E('meta',
                        property='description',
                        content='HTML Description',
                    ),
                    E('meta',
                        property='twitter:description',
                        content='Twitter Description',
                    ),
                )
            )
        ))
        self.assertEqual(info.description, "Twitter Description")

    def test_description_fromOpenGraph(self):
        info = PageInfo(self.html(
            E('html',
                E('head',
                    E('meta',
                        property='description',
                        content='HTML Description',
                    ),
                    E('meta',
                        property='twitter:description',
                        content='Twitter Description',
                    ),
                    E('meta',
                        property='og:description',
                        content='OG Description',
                    ),
                )
            )
        ))
        self.assertEqual(info.description, "OG Description")

    def test_siteicon_takesFirst(self):
        info = PageInfo(self.html(
            E('html',
                E('head',
                    E('link',
                        rel='icon',
                        href='siteicon.png',
                    ),
                    E('link',
                        rel='icon',
                        href='secondicon.png',
                    ),
                ),
            )
        ))
        self.assertEqual(info.siteicon, "siteicon.png")

    def test_siteicon_shortcuticon(self):
        info = PageInfo(self.html(
            E('html',
                E('head',
                    E('link',
                        rel='shortcut icon',
                        href='shortcuticon.png',
                    ),
                ),
            )
        ))
        self.assertEqual(info.siteicon, "shortcuticon.png")

    def test_siteicon_noIcon(self):
        info = PageInfo(self.html(
            E('html',
            )
        ))
        self.assertEqual(info.siteicon, "/favicon.ico")

    def test_absolute_nourl_unmodified(self):
        info = PageInfo("<html />", url=None)
        self.assertEqual(
            info.absolute("next.html"),
            "next.html"
            )

    def test_absolute_relativeToPage(self):
        info = PageInfo("<html />", url='http://site.com/path/page.html')
        self.assertEqual(
            info.absolute("next.html"),
            "http://site.com/path/next.html"
            )

    def test_absolute_relativeToRoot(self):
        info = PageInfo("<html />", url='http://site.com/path/page.html')
        self.assertEqual(
            info.absolute("/next.html"),
            "http://site.com/next.html"
            )

    def test_absolute_alreadyAbsolute(self):
        info = PageInfo("<html />", url='http://site.com/path/page.html')
        self.assertEqual(
            info.absolute("https://othersite.org/next.html"),
            "https://othersite.org/next.html"
            )

    def test_siteicon_withUrl(self):
        info = PageInfo(self.html(
            E('html',
                E('head',
                    E('link',
                        rel='icon',
                        href='icon.png',
                    ),
                ),
            )
        ), url='http://site.com/path/page.html')

        self.assertEqual(info.siteicon,
            "http://site.com/path/icon.png")


    def test_image_fromOpenGraph(self):
        info = PageInfo(self.html(
            E('html',
                E('head',
                    E('meta',
                        property='twitter:image',
                        content='twitter.jpg',
                    ),
                    E('meta',
                        property='og:image',
                        content='og.jpg',
                    ),
                )
            )
        ))
        self.assertEqual(info.image, "og.jpg")

    def test_image_fromTwitter(self):
        info = PageInfo(self.html(
            E('html',
                E('head',
                    E('meta',
                        property='twitter:image',
                        content='twitter.jpg',
                    ),
                )
            )
        ))
        self.assertEqual(info.image, "twitter.jpg")

    def test_image_noImage_takesSiteImage(self):
        info = PageInfo(self.html(
            E('html',
            )
        ))
        self.assertEqual(info.image, "/favicon.ico")

    def test_image_withUrl(self):
        info = PageInfo(self.html(
            E('html',
                E('head',
                    E('meta',
                        property='og:image',
                        content='og.jpg',
                    ),
                )
            )
        ), url='http://site.com/path/page.html')

        self.assertEqual(info.image, "http://site.com/path/og.jpg")




# vim: et ts=4 sw=4
