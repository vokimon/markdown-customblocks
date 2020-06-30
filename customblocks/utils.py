from markdown.util import etree


def E(tag, **attribs):
	tag, *classes = tag.split('.')
	element = etree.Element(tag or 'div',
		{'class': ' '.join(classes)} if classes else {},
		**{k:format(v) for k,v in attribs.items()}
	)
	return element


# vim: et ts=4 sw=4
