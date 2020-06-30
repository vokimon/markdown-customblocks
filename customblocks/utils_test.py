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

	def test_tag_manyClasses(self):
		e = E('.myclass.otherclass')
		self.assertXml(e, """\
			<div class="myclass otherclass" />
		""")

	def test_attribute(self):
		e = E('', attr1='value')
		self.assertXml(e, """\
			<div attr1="value" />
		""")
		




# vim: et ts=4 sw=4
