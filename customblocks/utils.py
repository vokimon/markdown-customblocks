from markdown.util import etree


def E(tag, *children, **attribs):
	tag, *classes = tag.split('.')
	element = etree.Element(tag or 'div',
		{'class': ' '.join(classes)} if classes else {},
		**{k:format(v) for k,v in attribs.items()}
	)
	for child in children:
		if type(child) == str:
			if len(element):
				element[-1].tail = (element[-1].tail or '') + child
			else:
				element.text = (element.text or '') + child
			continue
		element.append(child)
	return element


# vim: et ts=4 sw=4
