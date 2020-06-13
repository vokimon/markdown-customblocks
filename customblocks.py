from __future__ import absolute_import
from __future__ import unicode_literals
from markdown.extensions import Extension
from markdown.blockprocessors import BlockProcessor
from markdown.util import etree
import re

def container(*args, _type, _parser, _parent, _content, **kwds):
	div = etree.SubElement(_parent, 'div')
	div.set('class', '%s' % (' '.join(
		'-'.join(cl.split())
		for cl in [_type]+list(args)
	)))
	for k,v in kwds.items():
		div.set(k,v)
	_parser.parseChunk(div, _content)

def admonition(title=None, *args, _type, _parser, _parent, _content, **kwds):
	div = etree.SubElement(_parent, 'div')
	div.set('class', 'admonition %s' % (' '.join(
		'-'.join(cl.split())
		for cl in [_type]+list(args)
	)))
	if title: 
		titlediv = etree.SubElement(div, 'div')
		titlediv.set('class', 'admonition-title')
		titlediv.text = title
	for k,v in kwds.items():
		div.set(k,v)
	_parser.parseChunk(div, _content)

typeGenerators = dict(
	notice=admonition,
	danger=admonition,
	info=admonition,
)

class CustomBlocksExtension(Extension):
    """ CustomBlocks extension for Python-Markdown. """

    def __init__(self, **kwargs):
        self.config = dict(
            fallback = [container,
                "Renderer used when the type is not defined. "
                "By default, is a div container."],
            renderers = [{},
                "Type-renderer bind as a dict, it will update the default map. "
                "Set a type to None to use the fallback."],
            )
        super(CustomBlocksExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        """ Add CustomBlocks to Markdown instance. """
        md.registerExtension(self)
        processor = CustomBlocksProcessor(md.parser)
        processor.config = self.getConfigs()
        md.parser.blockprocessors.register(processor, 'customblocks', 105)


class CustomBlocksProcessor(BlockProcessor):
	RE = re.compile(r'(?:^|\n)::: *([\w\-]+)(?: +(?:[\w]+=)?("(?:\\.|[^"])*"|[\w\-]+))*(?:\n|$)')
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
				blocks.insert(0,unindented)
				break
		return '\n\n'.join(content)

	def _processParams(self, params):
		RE_PARAM = re.compile(r' (?:([\w\-]+)=)?("(?:\\.|[^"])*"|[\w\-]+)')
		args =[]
		kwd = {}
		for key, param in RE_PARAM.findall(params):
			if param[0]==param[-1]=='"':
				param = eval(param)
			if key:
				kwd[key]=param
			else:
				args.append(param)
		return args, kwd

	def run(self, parent, blocks):
		block = blocks[0]
		match = self.RE.search(block)
		previous = block[:match.start()]
		if previous:
			self.parser.parseChunk(parent, previous)
		_type = match.group(1)
		args, kwds = self._processParams(block[match.end(1): match.end()])
		blocks[0] = block[match.end():]
		content = self._indentedContent(blocks)
		# Remove optional closing if present
		if blocks:
			blocks[0] = re.sub(self.RE_END, '', blocks[0])

		print(self.config)
		typeGenerators.update(self.config['renderers'])

		generator = typeGenerators.get(_type, container)
		result = generator(
			_type=_type,
			_parent=parent,
			_content=content,
			_parser=self.parser,
			*args,
			**kwds,
		)
		if result is None:
			return True
		if type(result) == type(u''):
			result = result.encode('utf8')
		if type(result) == type(b''):
			result = etree.XML(result)
		parent.append(result)
		return True

"""
# TODO
- calling custom functions
- generalize interface
"""




def makeExtension(**kwargs):  # pragma: no cover
    return CustomBlocksExtension(**kwargs)
