from __future__ import absolute_import
from __future__ import unicode_literals
from markdown.extensions import Extension
from markdown.blockprocessors import BlockProcessor
from markdown.util import etree
import re


class CustomBlocksExtension(Extension):
    """ Admonition extension for Python-Markdown. """

    def extendMarkdown(self, md):
        """ Add Admonition to Markdown instance. """
        md.registerExtension(self)

        md.parser.blockprocessors.register(CustomBlocksProcessor(md.parser), 'admonition', 105)


class CustomBlocksProcessor(BlockProcessor):
	RE = re.compile(r'(?:^|\n)::: *([\w\-]+)(?:\n|$)')

	def test(self, parent, block):
		return self.RE.search(block)

	def run(self, parent, blocks):
		block = blocks.pop(0)
		match = self.RE.search(block)
		mainClass = match.group(1)
		remainder = block[match.end():]
		div = etree.SubElement(parent, 'div')
		div.set('class', '%s' % (mainClass))
		indented, unindented = self.detab(remainder)
		if indented:
			self.parser.parseChunk(div, indented)
		blocks.insert(0,unindented)
		return True

"""
# TODO
+ Takes content
- Content is reprocessed
- Subblocs are reprocessed
- In the middle of a paragraph
+ Indentation over within the block
- key parameters
- parameters with commas
"""




def makeExtension(**kwargs):  # pragma: no cover
    return CustomBlocksExtension(**kwargs)
