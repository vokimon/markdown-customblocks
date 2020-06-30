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

	def test_attribute_integer(self):
		e = E('', attr1=200)
		self.assertXml(e, """\
			<div attr1="200" />
		""")

	def test_attribute_attributeEncode(self):
		e = E('', attr1="""a&<>"'z""")
		self.assertXml(e, """\
			<div attr1="a&amp;&lt;&gt;&quot;'z" />
		""")

	def test_child(self):
		e = E('', E('child'))
		self.assertXml(e, """\
			<div><child /></div>
		""")

	def test_text(self):
		e = E('', "content")
		self.assertXml(e, """\
			<div>content</div>
		""")

	def test_text_afterElement(self):
		e = E('', E('child'), "content")
		self.assertXml(e, """\
			<div><child />content</div>
		""")

	def test_text_twice(self):
		e = E('', "first", "later")
		self.assertXml(e, """\
			<div>firstlater</div>
		""")




# vim: et ts=4 sw=4
