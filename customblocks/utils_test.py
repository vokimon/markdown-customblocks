import unittest
from markdown.util import etree
from .utils import E
from textwrap import dedent

class ETest(unittest.TestCase):

	def assertXml(self, e, expected):
		self.assertMultiLineEqual(
			etree.tostring(e,'unicode'),
			dedent(expected.strip()))
		

	def test_tag_named(self):
		e = E('div')
		self.assertXml(e, """\
			<div />
		""")

	def test_tag_noName(self):
		e = E('')
		self.assertXml(e, """\
			<div />
		""")

	def test_tag_class(self):
		e = E('.myclass')
		self.assertXml(e, """\
			<div class="myclass" />
		""")


# vim: et ts=4 sw=4
