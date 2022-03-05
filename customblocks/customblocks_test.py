import unittest
from markdown import markdown
from markdown import test_tools
from xml.etree import ElementTree as etree

try:
    import full_yaml_metadata
except ImportError:
    full_yaml_metadata = None


class CustomBlockExtension_Test(test_tools.TestCase):
    def setUp(self):
        self.default_kwargs = dict(
            extensions = [
                'customblocks',
            ],
        )

    def setupCustomBlocks(self, **kwds):
        (
            self.default_kwargs
                .setdefault('extension_configs',{})
                .setdefault('customblocks', {})
                .setdefault('generators', {})
                .update(kwds)
        )

    def setupConfig(self, **kwds):
        (
            self.default_kwargs
                .setdefault('extension_configs',{})
                .setdefault('customblocks', {})
                .setdefault('config', {})
                .update(kwds)
        )

    def addExtensions(self, *args):
        self.default_kwargs['extensions'] += args

    def assertMarkdown(self, markdown, html, **kwds):
        self.assertMarkdownRenders(
            self.dedent(markdown),
            self.dedent(html),
            **kwds)

    def test_simple(self):
        self.assertMarkdown("""\
            ::: myblock
            """, """\
            <div class="myblock"></div>
            """)

    def test_simple_noSpace(self):
        self.assertMarkdown("""\
            :::myblock
            """, """\
            <div class="myblock"></div>
            """)

    def test_simple_manySpaces(self):
        self.assertMarkdown("""\
            :::  myblock
            """, """\
            <div class="myblock"></div>
            """)

    def test_content_singleLine(self):
        self.assertMarkdown("""\
            ::: myblock
                Some content
            """, """\
            <div class="myblock">
            <p>Some content</p>
            </div>
            """)

    def test_content_unindentedNotIncluded(self):
        self.assertMarkdown("""\
            ::: myblock
            Not content
            """, """\
            <div class="myblock"></div>
            <p>Not content</p>
            """)

    def test_content_reparsed(self):
        self.assertMarkdown("""\
            ::: myblock
                - a list
            """, """\
            <div class="myblock">
            <ul>
            <li>a list</li>
            </ul>
            </div>
            """)

    def test_content_secondIndentKept(self):
        self.assertMarkdown("""\
            ::: myblock
                - a list
                    - subitem
            """, """\
            <div class="myblock">
            <ul>
            <li>a list<ul>
            <li>subitem</li>
            </ul>
            </li>
            </ul>
            </div>
            """)

    def test_content_extraIndent(self):
        self.assertMarkdown("""\
            ::: myblock
                    extra indented
            """, """\
            <div class="myblock">
            <pre><code>extra indented
            </code></pre>
            </div>
            """)

    def test_content_joinLaterIndentedBlocks(self):
        self.assertMarkdown("""\
            ::: myblock
                Some content

                More content
            """, """\
            <div class="myblock">
            <p>Some content</p>
            <p>More content</p>
            </div>
            """)


    def test_nested(self):
        self.assertMarkdown("""\
            ::: myblock
                ::: inner
                    Inner content
                Some content
            """, """\
            <div class="myblock">
            <div class="inner">
            <p>Inner content</p>
            </div>
            <p>Some content</p>
            </div>
            """)

    def test_inMiddleOfABlock(self):
        self.assertMarkdown("""\
            Not in block
            ::: myblock
                Some content
            """, """\
            <p>Not in block</p>
            <div class="myblock">
            <p>Some content</p>
            </div>
            """)

    def test_explicitEnd(self):
        self.assertMarkdown("""\
            ::: myblock
                Some content
            :::
            """, """\
            <div class="myblock">
            <p>Some content</p>
            </div>
            """)

    def test_explicitEnd_contentAfter(self):
        self.assertMarkdown("""\
            ::: myblock
                Some content
            :::
                Some code
            """, """\
            <div class="myblock">
            <p>Some content</p>
            </div>
            <pre><code>Some code
            </code></pre>
            """)

    def test_explicitEnd_afterOutContent_ignored(self):
        self.assertMarkdown("""\
            ::: myblock
                Some content
            Outer code
            :::
            """, """\
            <div class="myblock">
            <p>Some content</p>
            </div>
            <p>Outer code
            :::</p>
            """)

    def test_singleParam(self):
        self.assertMarkdown("""\
            ::: myblock param1
            """, """\
            <div class="myblock param1"></div>
            """)

    def test_manyParams(self):
        self.assertMarkdown("""\
            ::: myblock param1 param2
            """, """\
            <div class="myblock param1 param2"></div>
            """)

    def test_quotedParam(self):
        self.assertMarkdown("""\
            ::: myblock "quoted param"
            """, """\
            <div class="myblock quoted-param"></div>
            """)

    def test_manyParams_extraSeparation(self):
        self.assertMarkdown("""\
            ::: myblock   param1   param2
            """, """\
            <div class="myblock param1 param2"></div>
            """)

    def test_noParams_trailingSpaces(self):
        # There is a space after myblock
        self.assertMarkdown("""\
            ::: myblock 
            """, """\
            <div class="myblock"></div>
            """)

    def test_keyParam(self):
        self.assertMarkdown("""\
            ::: myblock key=value
            """, """\
            <div class="myblock" key="value"></div>
            """)

    def test_keyParam_quotedValue(self):
        self.assertMarkdown("""\
            ::: myblock key="value with spaces"
            """, """\
            <div class="myblock" key="value with spaces"></div>
            """)

    def test_quotedValues_escapedQuotes(self):
        self.assertMarkdown("""\
            ::: myblock key="value \\"with spaces"
            """, """\
            <div class="myblock" key="value &quot;with spaces"></div>
            """)

    def test_quotedValues_escapedEol(self):
        self.assertMarkdown("""\
            ::: myblock key="value \\nwith eols"
            """, """\
            <div class="myblock" key="value \nwith eols"></div>
            """)

    def test_singleQuotedValues(self):
        self.assertMarkdown("""\
            ::: myblock key='value with spaces'
            """, """\
            <div class="myblock" key="value with spaces"></div>
            """)

    def test_singleQuotedValues_escapeQuotes(self):
        self.assertMarkdown("""\
            ::: myblock key='value with\\' "quotes"'
            """, """\
            <div class="myblock" key="value with' &quot;quotes&quot;"></div>
            """)

    def test_spacesAtTheEnd(self):
        self.assertMarkdown("""\
            ::: myblock key="value \\nwith eols"\t \t
            """, """\
            <div class="myblock" key="value \nwith eols"></div>
            """)

    def test_param_nonalphanumeric(self):
        self.assertMarkdown("""\
            ::: myblock http://lala.com/~alice
            """, """\
            <div class="myblock http://lala.com/~alice"></div>
            """)

    def test_keyParam_nonalphanumeric(self):
        self.assertMarkdown("""\
            ::: myblock url=http://lala.com/~alice
            """, """\
            <div class="myblock" url="http://lala.com/~alice"></div>
            """)


    def test_customGenerator_returnsEtree(self):
        def custom():
            return etree.Element("custom")

        self.setupCustomBlocks(custom=custom)

        self.assertMarkdown("""\
            ::: custom
            """,
            """\
            <custom></custom>
            """)

    def test_customGenerator_returnsBytes(self):
        def custom():
            return "<custom></custom>".encode('utf8')

        self.setupCustomBlocks(custom=custom)

        self.assertMarkdown("""\
            ::: custom
            """,
            """\
            <custom></custom>
            """)

    def test_customGenerator_returnsString(self):
        def custom():
            return "<custom></custom>"

        self.setupCustomBlocks(custom=custom)

        self.assertMarkdown("""\
            ::: custom
            """,
            """\
            <custom></custom>
            """)


    def test_customGenerator_receivesParent(self):
        def custom(ctx):
            etree.SubElement(ctx.parent, 'custom')

        self.setupCustomBlocks(custom=custom)

        self.assertMarkdown("""\
            ::: custom
            """,
            """\
            <custom></custom>
            """)

    def test_customGenerator_keyword(self):
        def custom(ctx, key):
            div = etree.SubElement(ctx.parent, 'custom')
            div.set('key', key)

        self.setupCustomBlocks(custom=custom)

        self.assertMarkdown("""\
            ::: custom key=value
            """,
            """\
            <custom key="value"></custom>
            """)

    def test_customGenerator_positional(self):
        def custom(ctx, key):
            div = etree.SubElement(ctx.parent, 'custom')
            div.set('key', key)

        self.setupCustomBlocks(custom=custom)

        self.assertMarkdown("""\
            ::: custom value
            """,
            """\
            <custom key="value"></custom>
            """)

    def test_customGenerator_unexpectedKeyword(self):
        def custom():
            return "<custom></custom>"

        self.setupCustomBlocks(custom=custom)
        with self.assertWarns(UserWarning) as ctx:
            self.assertMarkdown("""\
                ::: custom unexpected=value
                """,
                """\
                <custom></custom>
                """)
        self.assertEqual(format(ctx.warning),
            "In block 'custom', ignoring unexpected parameter 'unexpected'")

    def test_customGenerator_keyOnlyParam(self):
        def custom(*, key):
            return "<custom key='{}'></custom>".format(key)

        self.setupCustomBlocks(custom=custom)
        self.assertMarkdown("""\
            ::: custom key=value
            """,
            """\
            <custom key="value"></custom>
            """)

    def test_customGenerator_varKeywordTakesAll(self):
        def custom(**kwds):
            return "<custom key='{key}'></custom>".format(**kwds)

        self.setupCustomBlocks(custom=custom)
        self.assertMarkdown("""\
            ::: custom key=value
            """,
            """\
            <custom key="value"></custom>
            """)

    def test_customGenerator_missingKey(self):
        def custom(key):
            return "<custom key='{}'></custom>".format(key)

        self.setupCustomBlocks(custom=custom)
        with self.assertWarns(UserWarning) as ctx:
            self.assertMarkdown("""\
                ::: custom
                """,
                """\
                <custom key=""></custom>
                """)
        self.assertEqual(format(ctx.warning),
            "In block 'custom', missing mandatory attribute 'key'")

    def test_customGenerator_missingKeyWithDefault(self):
        def custom(key='default'):
            return "<custom key='{}'></custom>".format(key)

        self.setupCustomBlocks(custom=custom)
        self.assertMarkdown("""\
            ::: custom
            """,
            """\
            <custom key="default"></custom>
            """)

    def test_customGenerator_tooManyPositionals(self):
        def custom():
            return "<custom></custom>"

        self.setupCustomBlocks(custom=custom)
        with self.assertWarns(UserWarning) as ctx:
            self.assertMarkdown("""\
                ::: custom extra
                """,
                """\
                <custom></custom>
                """)
        self.assertEqual(format(ctx.warning),
            "In block 'custom', ignored extra attribute 'extra'")

    def test_customGenerator_varPositional(self):
        def custom(*args):
            return "<custom>{}</custom>".format(", ".join(args))

        self.setupCustomBlocks(custom=custom)
        self.assertMarkdown("""\
            ::: custom extra "another extra"
            """,
            """\
            <custom>extra, another extra</custom>
            """)

    def test_customGenerator_onlyPositional(self):
        def custom(param, /):
            return "<custom>{}</custom>".format(param)

        self.setupCustomBlocks(custom=custom)
        self.assertMarkdown("""\
            ::: custom positional
            """,
            """\
            <custom>positional</custom>
            """)

    def test_customGenerator_onlyKeyword(self):
        def custom(*, key):
            return "<custom key='{}'></custom>".format(key)

        self.setupCustomBlocks(custom=custom)
        self.assertMarkdown("""\
            ::: custom key=value
            """,
            """\
            <custom key="value"></custom>
            """)

    def test_customGenerator_onlyKeyword_cannotBeSetByPos(self):
        def custom(*, key):
            return "<custom key='{}'></custom>".format(key)

        self.setupCustomBlocks(custom=custom)
        with self.assertWarns(UserWarning) as ctx:
            self.assertMarkdown("""\
                ::: custom extra
                """,
                """\
                <custom key=""></custom>
                """)
        self.assertEqual(format(ctx.warning),
            "In block 'custom', missing mandatory attribute 'key'")


    def test_customGenerator_onlyPositional_cannotBeSetByKey(self):
        def custom(param, /):
            return "<custom>{}</custom>".format(param)

        self.setupCustomBlocks(custom=custom)
        with self.assertWarns(UserWarning) as ctx:
            self.assertMarkdown("""\
                ::: custom param=value
                """,
                """\
                <custom></custom>
                """)
        self.assertEqual(format(ctx.warning),
            "In block 'custom', missing mandatory attribute 'param'")

    def test_customGenerator_varKeyword_cannotBeSetByKey(self):
        def custom(**kwd):
            result = etree.Element('custom')
            for key, value in kwd.items():
                result.set(key, value)
            return result

        self.setupCustomBlocks(custom=custom)
        self.assertMarkdown("""\
            ::: custom kwd=value
            """,
            """\
            <custom kwd="value"></custom>
            """)

    def test_customGenerator_varPositional_cannotBeSetByKey(self):
        def custom(*args):
            return "<custom>{}</custom>".format(", ".join(args))

        self.setupCustomBlocks(custom=custom)
        with self.assertWarns(UserWarning) as ctx:
            self.assertMarkdown("""\
                ::: custom args=value
                """,
                """\
                <custom></custom>
                """)
        self.assertEqual(format(ctx.warning),
            "In block 'custom', ignoring unexpected parameter 'args'")

    def test_customGenerator_onlyPositional_unsetWithDefaults(self):
        def custom(param='default', /):
            return "<custom param='{}'></custom>".format(param)

        self.setupCustomBlocks(custom=custom)
        self.assertMarkdown("""\
            ::: custom
            """,
            """\
            <custom param="default"></custom>
            """)

    def test_customGenerator_flag_withBoolDefault(self):
        def custom(*, flag=False):
            return "<custom flag='{}'></custom>".format(flag)

        self.setupCustomBlocks(custom=custom)
        self.assertMarkdown("""\
            ::: custom flag
            """,
            """\
            <custom flag="True"></custom>
            """)

    def test_customGenerator_flag_undetectedWithNoBoolDefault(self):
        def custom(*, flag='default'):
            return "<custom flag='{}'></custom>".format(flag)

        self.setupCustomBlocks(custom=custom)
        with self.assertWarns(UserWarning) as ctx:
            self.assertMarkdown("""\
                ::: custom flag
                """,
                """\
                <custom flag="default"></custom>
                """)
        self.assertEqual(format(ctx.warning),
            "In block 'custom', ignored extra attribute 'flag'")

    def test_customGenerator_flag_markedAsAnnotation(self):
        def custom(*, flag:bool):
            return "<custom flag='{}'></custom>".format(flag)

        self.setupCustomBlocks(custom=custom)
        self.assertMarkdown("""\
            ::: custom flag
            """,
            """\
            <custom flag="True"></custom>
            """)

    def test_customGenerator_noflag_markedAsBoolDefault(self):
        def custom(*, flag=True):
            return "<custom flag='{}'></custom>".format(flag)

        self.setupCustomBlocks(custom=custom)
        self.assertMarkdown("""\
            ::: custom noflag
            """,
            """\
            <custom flag="False"></custom>
            """)

    def test_customGenerator_noflag_markedAsAnotation(self):
        def custom(*, flag:bool):
            return "<custom flag='{}'></custom>".format(flag)

        self.setupCustomBlocks(custom=custom)
        self.assertMarkdown("""\
            ::: custom noflag
            """,
            """\
            <custom flag="False"></custom>
            """)

    def test_customGenerator_unparsedContentReceived(self):
        def custom(ctx):
            return "<custom>{}</custom>".format(ctx.content)

        self.setupCustomBlocks(custom=custom)
        self.assertMarkdown("""\
            ::: custom
                this is content

                this is too
            this is not
            """,
            """\
            <custom>this is content

            this is too</custom><p>this is not</p>
            """)

    def test_customGenerator_parserReceived(self):
        def custom(ctx):
            div = etree.Element('custom')
            ctx.parser.parseChunk(div, ctx.content)
            return div

        self.setupCustomBlocks(custom=custom)
        self.assertMarkdown("""\
            ::: custom
                this is content

                this is too
            this is not
            """,
            """\
            <custom><p>this is content</p><p>this is too</p></custom><p>this is not</p>
            """)

    def test_customGenerator_typeReceived(self):
        def custom(ctx):
            return etree.Element(ctx.type)

        self.setupCustomBlocks(custom=custom)
        self.assertMarkdown("""\
            ::: custom
            """,
            """\
            <custom></custom>
            """)

    def test_customGenerator_positionalWithExcess(self):
        def custom(ctx, positional=None, *args):
            return (
                "<custom>\n"
                f"positional={positional}\n"
                f"args={args}\n"
                "</custom>\n"
            )

        self.setupCustomBlocks(custom=custom)
        self.assertMarkdown("""\
            ::: custom "A title" super
                content
            """, """\
            <custom>
            positional=A title
            args=('super',)
            </custom>
            """)

    def test_metadata_withNoMetadataExtension(self):
        def custom(ctx):
            return "<custom>{}</custom>".format(ctx.metadata)

        self.setupCustomBlocks(custom=custom)
        self.assertMarkdown("""\
            ::: custom
            """, """\
            <custom>None</custom>""")

    def test_metadata_extraMeta(self):
        def custom(ctx):
            return "<custom>{}</custom>".format(ctx.metadata)

        self.addExtensions('meta')
        self.setupCustomBlocks(custom=custom)
        self.assertMarkdown("""\
            ---
            mymeta: metavalue
            ---
            ::: custom
            """, """\
            <custom>{'mymeta': ['metavalue']}</custom>""")

    def test_metadata_extraMeta_none(self):
        def custom(ctx):
            return "<custom>{}</custom>".format(ctx.metadata)

        self.addExtensions('meta')
        self.setupCustomBlocks(custom=custom)
        self.assertMarkdown("""\
            ::: custom
            """, """\
            <custom>{}</custom>""")

    def test_metadata_extraMeta_empty(self):
        def custom(ctx):
            return "<custom>{}</custom>".format(ctx.metadata)

        self.addExtensions('meta')
        self.setupCustomBlocks(custom=custom)
        self.assertMarkdown("""\
            ---
            ...
            ::: custom
            """, """\
            <custom>{}</custom>""")

    @unittest.skipIf(not full_yaml_metadata, "Requires full-yaml-metadata")
    def test_metadata_fullYamlMetadataExtension(self):
        def custom(ctx):
            return "<custom>{}</custom>".format(ctx.metadata)

        self.addExtensions('full_yaml_metadata')
        self.setupCustomBlocks(custom=custom)
        self.assertMarkdown("""\
            ---
            mymeta: metavalue
            ---
            ::: custom
            """, """\
            <custom>{'mymeta': 'metavalue'}</custom>""")

    @unittest.skipIf(not full_yaml_metadata, "Requires full-yaml-metadata")
    def test_metadata_fullYamlMetadataExtension_none(self):
        def custom(ctx):
            return "<custom>{}</custom>".format(ctx.metadata)

        self.addExtensions('full_yaml_metadata')
        self.setupCustomBlocks(custom=custom)
        self.assertMarkdown("""\
            ::: custom
            """, """\
            <custom>None</custom>""")

    @unittest.skipIf(not full_yaml_metadata, "Requires full-yaml-metadata")
    def test_metadata_fullYamlMetadataExtension_empty(self):
        def custom(ctx):
            return "<custom>{}</custom>".format(ctx.metadata)

        self.addExtensions('full_yaml_metadata')
        self.setupCustomBlocks(custom=custom)
        self.assertMarkdown("""\
            ---
            ...
            ::: custom
            """, """\
            <custom>None</custom>""")

    def test_config(self):
        def custom(ctx):
            return "<custom>{}</custom>".format(ctx.config.parameter)

        self.setupConfig(parameter='value')
        self.setupCustomBlocks(custom=custom)
        self.assertMarkdown("""\
            ::: custom
            """, """\
            <custom>value</custom>""")


    def test_customGenerator_byName(self):
        self.setupConfig(parameter='value')
        self.setupCustomBlocks(custom='customblocks.customblocks_test:mycustom')
        self.assertMarkdown("""\
            ::: custom
            """, """\
            <custom></custom>""")

    def test_customGenerator_byName_wrongName(self):
        self.setupConfig(parameter='value')
        self.setupCustomBlocks(custom='customblocks.customblocks_test:wrongName')
        with self.assertRaises(AttributeError) as ctx:
            self.assertMarkdown("""\
                ::: custom
                """, """\
                Should raise an exception""")
        self.assertEqual(format(ctx.exception),
            "module 'customblocks.customblocks_test' has no attribute 'wrongName'")

    def test_customGenerator_byName_wrongModule(self):
        self.setupConfig(parameter='value')
        self.setupCustomBlocks(custom='bad_module:mycustom')
        with self.assertRaises(ModuleNotFoundError) as ctx:
            self.assertMarkdown("""\
                ::: custom
                """, """\
                Should raise an exception""")
        self.assertEqual(format(ctx.exception),
            "No module named 'bad_module'")

    def test_customGenerator_byName_noColon(self):
        self.setupConfig(parameter='value')
        self.setupCustomBlocks(custom='customblocks.customblocks_test')
        with self.assertRaises(ValueError) as ctx:
            self.assertMarkdown("""\
                ::: custom
                """, """\
                Should raise an exception""")
        self.assertEqual(format(ctx.exception),
            "not enough values to unpack (expected 2, got 1)")

    def test_customGenerator_byName_notCallable(self):
        self.setupConfig(parameter='value')
        self.setupCustomBlocks(custom='customblocks.customblocks_test:notcallable')
        with self.assertRaises(ValueError) as ctx:
            self.assertMarkdown("""\
                ::: custom
                """, """\
                Should raise an exception""")
        self.assertEqual(format(ctx.exception),
            "customblocks.customblocks_test:notcallable is not callable")


def mycustom():
    return "<custom></custom>"
notcallable="can not be called"

"""
- what to do with dashed keys
- Flags given values are turned into bool
- complementary flags are assigned by order
- other type annotations and conversions
- test ctx in any place other than the first one. should it fail??
- More than one warning
"""


# vim: et ts=4 sw=4
