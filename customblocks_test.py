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
			<div class="myblock">
			<p>Some content</p>
			</div>
			""")

	def test_content_unindentedNotIncluded(self):
		self.assertMarkdown("""\
			::: myblock
			Not content
			""", """\
			<div class="myblock"></div>
			<p>Not content</p>
			""")

	def test_content_reparsed(self):
		self.assertMarkdown("""\
			::: myblock
				- a list
			""", """\
			<div class="myblock">
			<ul>
			<li>a list</li>
			</ul>
			</div>
			""")

	def test_content_secondIndentKept(self):
		self.assertMarkdown("""\
			::: myblock
				- a list
					- subitem
			""", """\
			<div class="myblock">
			<ul>
			<li>a list<ul>
			<li>subitem</li>
			</ul>
			</li>
			</ul>
			</div>
			""")

	def test_content_extraIndent(self):
		self.assertMarkdown("""\
			::: myblock
					extra indented
			""", """\
			<div class="myblock">
			<pre><code>extra indented
			</code></pre>
			</div>
			""")

	def test_content_joinLaterIndentedBlocks(self):
		self.assertMarkdown("""\
			::: myblock
				Some content

				More content
			""", """\
			<div class="myblock">
			<p>Some content</p>
			<p>More content</p>
			</div>
			""")


	def test_content_nested(self):
		self.assertMarkdown("""\
			::: myblock
				::: inner
					Inner content
				Some content
			""", """\
			<div class="myblock">
			<div class="inner">
			<p>Inner content</p>
			</div>
			<p>Some content</p>
			</div>
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


	


