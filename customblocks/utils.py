from xml.etree import ElementTree as etree
import markdown


def E(tag, *children, **attribs):
    """
    Functional builder of an etree.
    If the tag is empty, a div is considered.
    Tag can be appended with dot separated class names.
    Keywords and dict children are turned into attributes.
    Later children which are dict attributes overwrite previous values.
    Keyword attributes overwrite any value set by children dict
    Class attributes are exception to the former being added instead of replaced.
    Text children are turn into text nodes.
    Items of children being lists and generators are inlined as childs of the element.
    """
    tag, *classes = tag.split('.')
    attributes = dict()

    def blendAttrs(adict):
        if '_class' in adict:
            aclass = adict.pop('_class')
            if aclass:
                classes.append(aclass)
        attributes.update(adict)

    for child in children:
        if isinstance(child, dict):
            blendAttrs(child)
    blendAttrs(attribs)

    element = etree.Element(tag or 'div', {
        'class': ' '.join(classes)} if classes else {},
        **{
            k: format(v)
            for k,v in attributes.items()
            if v is not None
        }
    )
    def appendChild(child):
        if child is None:
            return
        if isinstance(child, dict):
            return
        if type(child) == str:
            if len(element):
                element[-1].tail = (element[-1].tail or '') + child
            else:
                element.text = (element.text or '') + child
            return
        if type(child) == etree.Element:
            element.append(child)
            return
        if type(child) == Markdown:
            child.parse(element)
            return
        for item in child:
            appendChild(item)
 
    for child in children:
        appendChild(child)

    return element

class Markdown:
    """
    Functional Buidler to insert text reparsed as Markdown into an etree
    """

    def __init__(self, text, parser=None):
        self.parser = parser or markdown.Markdown().parser
        self.text = text

    def parse(self, parent):
        self.parser.parseChunk(parent, self.text)




# vim: et ts=4 sw=4
