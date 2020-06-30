from markdown.util import etree


def E(tag, **attribs):
	tag, *classes = tag.split('.')
	return etree.Element(tag or 'div',
		{'class': ' '.join(classes)} if classes else {},
		**{k:format(v) for k,v in attribs.items()}
	)


# vim: et ts=4 sw=4
