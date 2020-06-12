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


def default(blockType, parser, parent, content):
	div = etree.SubElement(parent, 'div')
	div.set('class', '%s' % (blockType))
	if content:
		parser.parseChunk(div, content)

class CustomBlocksProcessor(BlockProcessor):
	RE = re.compile(r'(?:^|\n)::: *([\w\-]+)(?:\n|$)')
	RE_END= r'^:::(?:$|\n)' # Not required but sometimes useful

	def test(self, parent, block):
		return self.RE.search(block)

	def run(self, parent, blocks):
		block = blocks[0]
		match = self.RE.search(block)
		mainClass = match.group(1)
		previous = block[:match.start()]
		if previous:
			self.parser.parseChunk(parent, previous)
		blocks[0] = block[match.end():]
		content = []
		while True:
			remainder = blocks.pop(0)
			indented, unindented = self.detab(remainder)
			if indented:
				content.append(indented)
			if unindented:
				unindented = re.sub(self.RE_END, '', unindented)
				if unindented:
					blocks.insert(0,unindented)
				break
			if not blocks: break
		default(
			blockType=mainClass,
			parent=parent,
			content='\n\n'.join(content),
			parser=self.parser,
		)
		return True

"""
# TODO
+ Takes content
+ Content is reprocessed
+ Inter custom blocks
+ In the middle of a paragraph
+ Indentation over within the block
- key parameters
- parameters with commas
- calling custom functions
"""




def makeExtension(**kwargs):  # pragma: no cover
    return CustomBlocksExtension(**kwargs)
