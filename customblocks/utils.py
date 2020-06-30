from markdown.util import etree


def E(tag):
	tag, *classes = tag.split('.',1)
	return etree.Element(tag or 'div',
		{'class': classes[0]} if classes else {}
	)


# vim: et ts=4 sw=4
