from __future__ import absolute_import
from __future__ import unicode_literals
from markdown.extensions import Extension
from markdown.blockprocessors import BlockProcessor
from markdown.util import etree
import re
from yamlns import namespace as ns
import inspect
import warnings
from .generators import container

class CustomBlocksExtension(Extension):
    """ CustomBlocks extension for Python-Markdown. """

    def __init__(self, **kwargs):
        self.config = dict(
            fallback = [container,
                "Renderer used when the type is not defined. "
                "By default, is a div container."],
            generators = [{},
                "Type-renderer bind as a dict, it will update the default map. "
                "Set a type to None to use the fallback."],
            )
        super(CustomBlocksExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        """ Add CustomBlocks to Markdown instance. """
        md.registerExtension(self)
        processor = CustomBlocksProcessor(md.parser)
        processor.config = self.getConfigs()
        processor.md = md
        md.parser.blockprocessors.register(processor, 'customblocks', 105)


class CustomBlocksProcessor(BlockProcessor):
	RE = re.compile(r'(?:^|\n)::: *([\w\-]+)(?: +(?:[\w]+=)?("(?:\\.|[^"])*"|[\S]+))*(?:\n|$)')
	RE_END= r'^:::(?:$|\n)' # Explicit end marker, not required but sometimes useful

	def test(self, parent, block):
		return self.RE.search(block)

	def _indentedContent(self, blocks):
		"""
		Extracts all the indented content from blocks
		until the first line that is not indented.
		Returns the indented lines removing the indentations.
		"""
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
		"""Parses the block head line to extract parameters,
		Parameters are values consisting on single word o
		double quoted multiple words, that may be preceded
		by a single word key and an equality sign without
		no spaces in between.
		The method returns a tuple of a list with all keyless
		parameters and a dict with all keyword parameters.
		"""
		print(params)
		RE_PARAM = re.compile(r' (?:([\w\-]+)=)?("(?:\\.|[^"])*"|[\S]+)')
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

	def _adaptParams(self, callback, ctx, args, kwds):
		"""
		Takes args and kwds extracted from custom block head line
		and adapts them to the signature of the callback.
		"""
		def warn(message):
			warnings.warn(f"In block '{ctx.type}', " + message)

		signature = inspect.signature(callback)

		# Turn flags into boolean keywords
		for name, param in signature.parameters.items():
			if (
				type(param.default) != bool and
				param.annotation != bool
			): continue

			if name in args:
				args.remove(name)
				kwds[name]=True

			if 'no'+name in args:
				args.remove('no'+name)
				kwds[name]=False

		outargs = []
		outkwds = {}
		acceptAnyKey = False
		acceptAnyPos = False
		for name, param in signature.parameters.items():
			if name == 'ctx':
				outargs.append(ctx)
				continue
			if param.kind == param.VAR_KEYWORD:
				acceptAnyKey = True
				continue
			if param.kind == param.VAR_POSITIONAL:
				acceptAnyPos = True
				continue

			value = (
				kwds.pop(name) if name in kwds and param.kind != param.POSITIONAL_ONLY
				else args.pop(0) if args and param.kind != param.KEYWORD_ONLY
				else param.default if param.default is not param.empty
				else warn(f"missing mandatory attribute '{name}'") or ""
			)
			if param.kind == param.KEYWORD_ONLY:
				outkwds[name] = value
			else:
				outargs.append(value)

		# Extend var pos
		if acceptAnyPos:
			outargs.extend(args)
		else:
			for arg in args:
				warn(f"ignored extra attribute '{arg}'")
		# Extend var key
		if acceptAnyKey:
			outkwds.update(kwds)
		else:
			for key in kwds:
				warn(f"ignoring unexpected parameter '{key}'")

		return outargs, outkwds

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

		typeGenerators.update(self.config['generators'])

		generator = typeGenerators.get(_type, container)

		ctx = ns()
		ctx.type = _type
		ctx.parent = parent
		ctx.content = content
		ctx.parser = self.parser
		ctx.metadata = self.parser.md.Meta if hasattr(self.parser.md, "Meta") else None

		outargs, kwds = self._adaptParams(generator, ctx, args, kwds)

		result = generator(*outargs, **kwds)

		if result is None:
			return True
		if type(result) == type(u''):
			result = result.encode('utf8')
		if type(result) == type(b''):
			result = etree.XML(result)
		parent.append(result)
		return True


from . import generators


typeGenerators = dict(
	attention = generators.admonition,
	caution = generators.admonition,
	danger = generators.admonition,
	error = generators.admonition,
	hint = generators.admonition,
	important = generators.admonition,
	note = generators.admonition,
	tip = generators.admonition,
	warning = generators.admonition,
	youtube = generators.youtube,
	twitter = generators.twitter,
	linkcard = generators.linkcard,
	figure = generators.figure,
)



def makeExtension(**kwargs):  # pragma: no cover
    return CustomBlocksExtension(**kwargs)
