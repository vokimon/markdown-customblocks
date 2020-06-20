import unittest
from markdown import markdown
from markdown import test_tools
from markdown.util import etree

class CustomBlockExtension_Test(test_tools.TestCase):

	def setUp(self):
		self.default_kwargs = dict(
			extensions = [
				'customblocks',
			],
		)

	def setupCustomBlocks(self, **kwds):
		(
			self.default_kwargs
				.setdefault('extension_configs',{})
				.setdefault('customblocks', {})
				.setdefault('renderers', {})
				.update(kwds)
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

	def test_quotedValues_escapedEol(self):
		self.assertMarkdown("""\
			::: myblock key="value \\nwith eols"
			""", """\
			<div class="myblock" key="value \nwith eols"></div>
			""")

	def test_fenceSymbol(self):
		self.assertMarkdown("""\
			::: myblock key="value \\nwith eols"
			""", """\
			<div class="myblock" key="value \nwith eols"></div>
			""")

	def test_admonition(self):
		self.assertMarkdown("""\
			::: notice title="A title"
				content
			""", """\
			<div class="admonition notice">
			<div class="admonition-title">A title</div>
			<p>content</p>
			</div>
			""")

	def test_admonition_byPosition(self):
		self.assertMarkdown("""\
			::: notice "A title"
				content
			""", """\
			<div class="admonition notice">
			<div class="admonition-title">A title</div>
			<p>content</p>
			</div>
			""")

	def test_admonition_extra(self):
		self.assertMarkdown("""\
			::: notice "A title" super style="float:left;width:30%"
				content
			""", """\
			<div class="admonition notice super" style="float:left;width:30%">
			<div class="admonition-title">A title</div>
			<p>content</p>
			</div>
			""")

	def test_customGenerator_returnsEtree(self):
		def custom():
			return etree.Element("custom")

		self.setupCustomBlocks(custom=custom)

		self.assertMarkdown("""\
			::: custom
			""",
			"""\
			<custom></custom>
			""")

	def test_customGenerator_returnsBytes(self):
		def custom():
			return "<custom></custom>".encode('utf8')

		self.setupCustomBlocks(custom=custom)

		self.assertMarkdown("""\
			::: custom
			""",
			"""\
			<custom></custom>
			""")

	def test_customGenerator_returnsString(self):
		def custom():
			return "<custom></custom>"

		self.setupCustomBlocks(custom=custom)

		self.assertMarkdown("""\
			::: custom
			""",
			"""\
			<custom></custom>
			""")


	def test_customGenerator_receivesParent(self):
		def custom(ctx):
			etree.SubElement(ctx.parent, 'custom')

		self.setupCustomBlocks(custom=custom)

		self.assertMarkdown("""\
			::: custom
			""",
			"""\
			<custom></custom>
			""")

	def test_customGenerator_keyword(self):
		def custom(ctx, key):
			div = etree.SubElement(ctx.parent, 'custom')
			div.set('key', key)

		self.setupCustomBlocks(custom=custom)

		self.assertMarkdown("""\
			::: custom key=value
			""",
			"""\
			<custom key="value"></custom>
			""")

	def test_customGenerator_positional(self):
		def custom(ctx, key):
			div = etree.SubElement(ctx.parent, 'custom')
			div.set('key', key)

		self.setupCustomBlocks(custom=custom)

		self.assertMarkdown("""\
			::: custom value
			""",
			"""\
			<custom key="value"></custom>
			""")

	def test_customGenerator_unexpectedKeyword(self):
		def custom():
			return "<custom></custom>"

		self.setupCustomBlocks(custom=custom)
		with self.assertWarns(UserWarning) as ctx:
			self.assertMarkdown("""\
				::: custom unexpected=value
				""",
				"""\
				<custom></custom>
				""")
		self.assertEqual(format(ctx.warning),
			"In block 'custom', ignoring unexpected parameter 'unexpected'")

	def test_customGenerator_keyOnlyParam(self):
		def custom(*, key):
			return "<custom key='{}'></custom>".format(key)

		self.setupCustomBlocks(custom=custom)
		self.assertMarkdown("""\
			::: custom key=value
			""",
			"""\
			<custom key="value"></custom>
			""")

	def test_customGenerator_varKeywordTakesAll(self):
		def custom(**kwds):
			return "<custom key='{key}'></custom>".format(**kwds)

		self.setupCustomBlocks(custom=custom)
		self.assertMarkdown("""\
			::: custom key=value
			""",
			"""\
			<custom key="value"></custom>
			""")

	def test_customGenerator_missingKey(self):
		def custom(key):
			return "<custom key='{}'></custom>".format(key)

		self.setupCustomBlocks(custom=custom)
		with self.assertWarns(UserWarning) as ctx:
			self.assertMarkdown("""\
				::: custom
				""",
				"""\
				<custom key=""></custom>
				""")
		self.assertEqual(format(ctx.warning),
			"In block 'custom', missing mandatory attribute 'key'")

	def test_customGenerator_missingKeyWithDefault(self):
		def custom(key='default'):
			return "<custom key='{}'></custom>".format(key)

		self.setupCustomBlocks(custom=custom)
		self.assertMarkdown("""\
			::: custom
			""",
			"""\
			<custom key="default"></custom>
			""")

	def test_customGenerator_tooManyPositionals(self):
		def custom():
			return "<custom></custom>"

		self.setupCustomBlocks(custom=custom)
		with self.assertWarns(UserWarning) as ctx:
			self.assertMarkdown("""\
				::: custom value
				""",
				"""\
				<custom></custom>
				""")
		self.assertEqual(format(ctx.warning),
			"In block 'custom', ignored extra attribute 'value'")

	def test_customGenerator_varPositional(self):
		def custom(*args):
			return "<custom>{}</custom>".format(", ".join(args))

		self.setupCustomBlocks(custom=custom)
		self.assertMarkdown("""\
			::: custom extra "another extra"
			""",
			"""\
			<custom>extra, another extra</custom>
			""")



# + VAR_KEYWORD
# + Unfilled
# + Unfilled with default
# + too many pos
# - VAR_POSITIONAL
# - Only positional
# - key presence in args means = True if type(defaut) is bool
# - key presence in args means = True if annotation is bool
# - ctx in any place other than the first should fail??
# - More than one warning






