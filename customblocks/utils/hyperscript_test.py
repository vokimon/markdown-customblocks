import unittest
from xml.etree import ElementTree as etree
from .hyperscript import E, Markdown
from textwrap import dedent

class ETest(unittest.TestCase):

    def assertXml(self, e, expected):
        self.assertMultiLineEqual(
            etree.tostring(e,'unicode'),
            dedent(expected.strip()))
        

    def test_tag_named(self):
        e = E('div')
        self.assertXml(e, """\
            <div />
        """)

    def test_tag_noName(self):
        e = E('')
        self.assertXml(e, """\
            <div />
        """)

    def test_tag_class(self):
        e = E('.myclass')
        self.assertXml(e, """\
            <div class="myclass" />
        """)

    def test_tag_manyClasses(self):
        e = E('.myclass.otherclass')
        self.assertXml(e, """\
            <div class="myclass otherclass" />
        """)

    def test_attribute(self):
        e = E('', attr1='value')
        self.assertXml(e, """\
            <div attr1="value" />
        """)

    def test_attribute_integer(self):
        e = E('', attr1=200)
        self.assertXml(e, """\
            <div attr1="200" />
        """)

    def test_attribute_attributeEncode(self):
        e = E('', attr1="""a&<>"'z""")
        self.assertXml(e, """\
            <div attr1="a&amp;&lt;&gt;&quot;'z" />
        """)

    def test_child(self):
        e = E('', E('child'))
        self.assertXml(e, """\
            <div><child /></div>
        """)

    def test_text(self):
        e = E('', "content")
        self.assertXml(e, """\
            <div>content</div>
        """)

    def test_text_afterChild(self):
        e = E('', E('child'), "content")
        self.assertXml(e, """\
            <div><child />content</div>
        """)

    def test_text_twice(self):
        e = E('', "first", "later")
        self.assertXml(e, """\
            <div>firstlater</div>
        """)

    def test_text_twice_afterChild(self):
        e = E('', E('child'), "first", "later")
        self.assertXml(e, """\
            <div><child />firstlater</div>
        """)

    def test_text_afterSecondChild(self):
        e = E('', E('child'), E('sibbling'), "content")
        self.assertXml(e, """\
            <div><child /><sibbling />content</div>
        """)

    def test_text_interChildren(self):
        e = E('', E('child'), "content", E('sibbling'))
        self.assertXml(e, """\
            <div><child />content<sibbling /></div>
        """)

    def test_attrib_asChildren(self):
        e = E('', dict(attrib="value"))
        self.assertXml(e, """\
            <div attrib="value" />
        """)

    def test_attrib_keywordWins(self):
        e = E('', dict(attrib="value1"), attrib="value2")
        self.assertXml(e, """\
            <div attrib="value2" />
        """)

    def test_attrib_settwice_laterWins(self):
        e = E('', dict(attrib="value1"), dict(attrib="value2"))
        self.assertXml(e, """\
            <div attrib="value2" />
        """)

    def test_attrib_none_unsets(self):
        e = E('', attrib=None)
        self.assertXml(e, """\
            <div />
        """)

    def test_classkey_specialUnderline(self):
        e = E('', _class='myclass')
        self.assertXml(e, """\
            <div class="myclass" />
        """)

    def test_classkey_additive(self):
        e = E('.myclass', _class='other')
        self.assertXml(e, """\
            <div class="myclass other" />
        """)

    def test_classchild(self):
        e = E('', dict(_class='myclass'))
        self.assertXml(e, """\
            <div class="myclass" />
        """)

    def test_classchild_additive(self):
        e = E('.aclass', dict(_class='myclass'))
        self.assertXml(e, """\
            <div class="aclass myclass" />
        """)

    def test_classNone(self):
        e = E('.aclass', dict(_class=None))
        self.assertXml(e, """\
            <div class="aclass" />
        """)

    def test_child_list_processedRecursively(self):
        e = E('', [E("first"), E("second")])
        self.assertXml(e, """\
            <div><first /><second /></div>
        """)

    def test_child_areKeptGrandchild(self):
        e = E('grandpa', E("dad", E("child")))
        self.assertXml(e, """\
            <grandpa><dad><child /></dad></grandpa>
        """)

    def test_child_iterators(self):
        e = E('ul', (
                E('li', item)
                for item in 'ABC'
            ))
        self.assertXml(e, """\
            <ul><li>A</li><li>B</li><li>C</li></ul>
        """)

    def test_child_none(self):
        e = E('', None, 'hola', None)
        self.assertXml(e, """\
            <div>hola</div>
        """)


    def test_markdown_defaultParser(self):
        e = E('.container',
            Markdown(
                """!!! danger "Caution"\nshit happens""",
            )
        )
        self.assertXml(e, """\
            <div class="container"><p>!!! danger "Caution"\nshit happens</p></div>
        """)

    def test_markdown_customParser(self):
        import markdown
        md = markdown.Markdown(extensions=['admonition'])
        e = E('',
            Markdown(
                """!!! danger "Caution"\nshit happens""",
                parser=md.parser
            )
        )
        self.assertXml(e, """\
            <div><div class="admonition danger"><p class="admonition-title">Caution</p></div><p>shit happens</p></div>
        """)



# vim: et ts=4 sw=4
