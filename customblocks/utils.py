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
		if type(child) == etree.Element:
			element.append(child)
		if isinstance(child, dict):
			for k,v in child.items():
				element.set(k,v)
	return element


# vim: et ts=4 sw=4
