from markdown.util import etree


def E(tag):
	tag, *classes = tag.split('.')
	return etree.Element(tag or 'div',
		{'class': ' '.join(classes)} if classes else {}
	)


# vim: et ts=4 sw=4
