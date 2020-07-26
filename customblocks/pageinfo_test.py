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
                    E('title','My title')
                )
            )
        ))
        self.assertEqual(info.title, "My title")

# vim: et ts=4 sw=4
