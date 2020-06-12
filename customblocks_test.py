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


	def test_nested(self):
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

	def test_inMiddleOfABlock(self):
		self.assertMarkdown("""\
			Not in block
			::: myblock
				Some content
			""", """\
			<p>Not in block</p>
			<div class="myblock">
			<p>Some content</p>
			</div>
			""")

	def test_explicitEnd(self):
		self.assertMarkdown("""\
			::: myblock
				Some content
			:::
			""", """\
			<div class="myblock">
			<p>Some content</p>
			</div>
			""")

	def test_explicitEnd_contentAfter(self):
		self.assertMarkdown("""\
			::: myblock
				Some content
			:::
				Some code
			""", """\
			<div class="myblock">
			<p>Some content</p>
			</div>
			<pre><code>Some code
			</code></pre>
			""")

	def test_explicitEnd_afterOutContent_ignored(self):
		self.assertMarkdown("""\
			::: myblock
				Some content
			Outer code
			:::
			""", """\
			<div class="myblock">
			<p>Some content</p>
			</div>
			<p>Outer code
			:::</p>
			""")

	def test_singleParam(self):
		self.assertMarkdown("""\
			::: myblock param1
			""", """\
			<div class="myblock param1"></div>
			""")

	def test_manyParams(self):
		self.assertMarkdown("""\
			::: myblock param1 param2
			""", """\
			<div class="myblock param1 param2"></div>
			""")

	def test_quotedParam(self):
		self.assertMarkdown("""\
			::: myblock "quoted param"
			""", """\
			<div class="myblock quoted-param"></div>
			""")

	def test_manyParams_extraSeparation(self):
		self.assertMarkdown("""\
			::: myblock   param1   param2
			""", """\
			<div class="myblock param1 param2"></div>
			""")

	def test_keyParam(self):
		self.assertMarkdown("""\
			::: myblock key=value
			""", """\
			<div class="myblock" key="value"></div>
			""")

	def test_keyParam_quotedValue(self):
		self.assertMarkdown("""\
			::: myblock key="value with spaces"
			""", """\
			<div class="myblock" key="value with spaces"></div>
			""")

	def test_quotedValues_escapedQuotes(self):
		self.assertMarkdown("""\
			::: myblock key="value \\"with spaces"
			""", """\
			<div class="myblock" key="value &quot;with spaces"></div>
			""")



