import unittest
from . import utils_htmlmeta
from .utils import E
from xml.etree import ElementTree as etree

class HtmlMeta_Test(unittest.TestCase):

    def html(self, e):
        return etree.tostring(e, 'unicode')

    from yamlns.testutils import assertNsEqual

    def test_extractInfo(self):
        snippet = self.html(
            E('html',
                E('head',
                    E('title','My title')
                )
            )
        )
        info = utils_htmlmeta.extractInfo(snippet)
        self.assertNsEqual(info, """\
            title: My title
            """)

# vim et ts=4 sw=4
