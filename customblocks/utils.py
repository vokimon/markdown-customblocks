from markdown.util import etree


def E(tag):
	return etree.Element(tag or 'div')


# vim: et ts=4 sw=4
