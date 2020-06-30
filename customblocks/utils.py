from markdown.util import etree


def E(tag, *children, **attribs):
    tag, *classes = tag.split('.')
    attributes = dict()

    def blend(adict):
        if '_class' in adict:
            aclass = adict.pop('_class')
            if aclass:
                classes.append(aclass)
        attributes.update(adict)

    for child in children:
        if isinstance(child, dict):
            blend(child)
    blend(attribs)

    element = etree.Element(tag or 'div',
        {'class': ' '.join(classes)} if classes else {},
        **{
            k:format(v)
            for k,v in attributes.items()
            if v is not None
        }
    )
    def appendChild(child):
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
        for item in child:
            appendChild(item)
 
    for child in children:
        appendChild(child)

    return element


# vim: et ts=4 sw=4
