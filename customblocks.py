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


def default(blockType, parser, parent, content, args):
	div = etree.SubElement(parent, 'div')
	div.set('class', '%s' % (' '.join([blockType]+list(args))))
	if content:
		parser.parseChunk(div, content)

class CustomBlocksProcessor(BlockProcessor):
	RE = re.compile(r'(?:^|\n)::: *([\w\-]+)(?: ([\w\-]+))*(?:\n|$)')
	RE_END= r'^:::(?:$|\n)' # Explicit end marker, not required but sometimes useful

	def test(self, parent, block):
		return self.RE.search(block)

	def _indentedContent(self, blocks):
		content = []
		while blocks:
			block = blocks.pop(0)
			indented, unindented = self.detab(block)
			if indented:
				content.append(indented)
			if unindented:
				unindented = re.sub(self.RE_END, '', unindented)
				if unindented:
					blocks.insert(0,unindented)
				break
		return '\n\n'.join(content)

	def run(self, parent, blocks):
		block = blocks[0]
		match = self.RE.search(block)
		mainClass = match.group(1)
		params = block[match.end(1): match.end()].split()
		previous = block[:match.start()]
		if previous:
			self.parser.parseChunk(parent, previous)
		blocks[0] = block[match.end():]
		content = self._indentedContent(blocks)
		default(
			blockType=mainClass,
			parent=parent,
			content=content,
			parser=self.parser,
			args=params,
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
