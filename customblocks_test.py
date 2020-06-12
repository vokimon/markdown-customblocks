import unittest
from markdown import markdown
from markdown import test_tools

class CustomBlockExtension_Test(test_tools.TestCase):

	def setUp(self):
		self.default_kwargs = dict(
			extensions = [
				'customblocks',
			],
		)

	def assertMarkdown(self, markdown, html, **kwds):
		self.assertMarkdownRenders(
			self.dedent(markdown),
			self.dedent(html),
			**kwds)

	def test_simple(self):
		self.assertMarkdown("""\
			::: myblock
			""", """\
			<div class="myblock"></div>
			""")

	def test_simple_noSpace(self):
		self.assertMarkdown("""\
			:::myblock
			""", """\
			<div class="myblock"></div>
			""")

	def test_simple_manySpaces(self):
		self.assertMarkdown("""\
			:::  myblock
			""", """\
			<div class="myblock"></div>
			""")

	def test_content_singleLine(self):
		self.assertMarkdown("""\
			::: myblock
				Some content
			""", """\
			<div class="myblock">Some content</div>
			""")



	def _test_innerAndOuter(self):

		self.assertMarkdownRenders(self.dedent("""\
			::: block
				inner
			outer
			"""),self.dedent("""\
			<div class='block'>
			<p>inner</p>
			</div>
			<p>outer</p>
			"""))


	


