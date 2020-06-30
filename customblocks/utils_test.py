import unittest
from markdown.util import etree
from .utils import E
from textwrap import dedent

class ETest(unittest.TestCase):

	def assertXml(self, e, expected):
		self.assertMultiLineEqual(
			etree.tostring(e,'unicode'),
			dedent(expected.strip()))
		

	def test_simpleNode(self):
		e = E('div')
		self.assertXml(e, """\
			<div />
		""")


# vim: et ts=4 sw=4
