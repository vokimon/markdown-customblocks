import unittest
from markdown import markdown
from markdown import test_tools


class Examples_Test(test_tools.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.default_kwargs = dict(
            extensions = [
                'customblocks',
            ],
        )

    def setupConfig(self, **kwds):
        (
            self.default_kwargs
                .setdefault('extension_configs',{})
                .setdefault('customblocks', {})
                .setdefault('config', {})
                .update(kwds)
        )

    def assertMarkdown(self, markdown, html, **kwds):
        self.assertMarkdownRenders(
            self.dedent(markdown),
            self.dedent(html),
            **kwds)

    def test_admonition(self):
        self.assertMarkdown("""\
            ::: note title="A title"
                content
            """, """\
            <div class="admonition note">
            <p class="admonition-title">A title</p>
            <p>content</p>
            </div>
            """)

    def test_admonition_byPosition(self):
        self.assertMarkdown("""\
            ::: note "A title"
                content
            """, """\
            <div class="admonition note">
            <p class="admonition-title">A title</p>
            <p>content</p>
            </div>
            """)

    def test_admonition_extra(self):
        self.assertMarkdown("""\
            ::: note "A title" super style="float:left;width:30%"
                content
            """, """\
            <div class="admonition note super" style="float:left;width:30%">
            <p class="admonition-title">A title</p>
            <p>content</p>
            </div>
            """)

    def test_admonition_noTitle(self):
        self.assertMarkdown("""\
            ::: note style="float:left;width:30%"
                content
            """, """\
            <div class="admonition note" style="float:left;width:30%">
            <p class="admonition-title">Note</p>
            <p>content</p>
            </div>
            """)

    def test_youtube(self):
        self.assertMarkdown("""\
            ::: youtube 7SS24_CgwEM
            """, """\
            <div class="videowrapper youtube">
            <iframe src="https://www.youtube.com/embed/7SS24_CgwEM"></iframe>
            </div>
            """)

    def test_youtube_withAutoplay(self):
        self.assertMarkdown("""\
            ::: youtube 7SS24_CgwEM autoplay
            """, """\
            <div class="videowrapper youtube">
            <iframe src="https://www.youtube.com/embed/7SS24_CgwEM?autoplay=1"></iframe>
            </div>
            """)

    def test_youtube_withAutoplayAndLoop(self):
        self.assertMarkdown("""\
            ::: youtube 7SS24_CgwEM autoplay loop
            """, """\
            <div class="videowrapper youtube">
            <iframe src="https://www.youtube.com/embed/7SS24_CgwEM?autoplay=1&amp;loop=1"></iframe>
            </div>
            """)

    def test_youtube_nocontrols(self):
        self.assertMarkdown("""\
            ::: youtube 7SS24_CgwEM nocontrols
            """, """\
            <div class="videowrapper youtube">
            <iframe src="https://www.youtube.com/embed/7SS24_CgwEM?controls=0"></iframe>
            </div>
            """)

    def test_youtube_inlineStyles_byConfig(self):
        self.setupConfig(youtube_inlineFluidStyle=True)
        self.assertMarkdown("""\
            ::: youtube 7SS24_CgwEM nocontrols
            """, """\
            <div class="videowrapper youtube" style="position:relative; padding-bottom:56.25%; height:0; overflow:hidden; width:100%">
            <iframe src="https://www.youtube.com/embed/7SS24_CgwEM?controls=0" style="position:absolute; top:0; left:0; width:100%; height:100%;"></iframe>
            </div>
            """)

    def test_vimeo(self):
        self.assertMarkdown("""\
            ::: vimeo 55297514
            """, """\
            <iframe allow="autoplay; fullscreen" allowfullscreen="allowfullscreen" frameborder="0" height="300" src="https://player.vimeo.com/video/55297514?portrait=0" width="100%"></iframe>
            """)

    def test_vimeo_loop(self):
        self.assertMarkdown("""\
            ::: vimeo 55297514 loop
            """, """\
            <iframe allow="autoplay; fullscreen" allowfullscreen="allowfullscreen" frameborder="0" height="300" src="https://player.vimeo.com/video/55297514?portrait=0&amp;loop=1" width="100%"></iframe>
            """)

    def test_vimeo_autoplay(self):
        self.assertMarkdown("""\
            ::: vimeo 55297514 autoplay
            """, """\
            <iframe allow="autoplay; fullscreen" allowfullscreen="allowfullscreen" frameborder="0" height="300" src="https://player.vimeo.com/video/55297514?portrait=0&amp;autoplay=1" width="100%"></iframe>
            """)

    def test_vimeo_nobyline(self):
        self.assertMarkdown("""\
            ::: vimeo 55297514 nobyline
            """, """\
            <iframe allow="autoplay; fullscreen" allowfullscreen="allowfullscreen" frameborder="0" height="300" src="https://player.vimeo.com/video/55297514?byline=0&amp;portrait=0" width="100%"></iframe>
            """)

    def test_vimeo_portrait(self):
        self.assertMarkdown("""\
            ::: vimeo 55297514 portrait
            """, """\
            <iframe allow="autoplay; fullscreen" allowfullscreen="allowfullscreen" frameborder="0" height="300" src="https://player.vimeo.com/video/55297514?" width="100%"></iframe>
            """)

    def test_verkami(self):
        self.assertMarkdown("""\
            ::: verkami 7948
            """,
            '<iframe'
            ' allowtransparency="true"'
            ' class="js-widget-iframe"'
            ' frameborder="0"'
            ' id="verkamiPortrait"'
            ' scrolling="no"'
            ' src="https://www.verkami.com/projects/7948/widget_portrait"'
            ' style="width: 240px; height: 350px"'
            '></iframe>'
        )

    def test_verkami_landscape(self):
        self.assertMarkdown("""\
            ::: verkami 7948 landscape
            """,
            '<iframe'
            ' allowtransparency="true"'
            ' class="js-widget-iframe"'
            ' frameborder="0"'
            ' id="verkamiLandscape"' # this changes
            ' scrolling="no"'
            # and the end of this:
            ' src="https://www.verkami.com/projects/7948/widget_landscape"'
            # and this (dimensions):
            ' style="width: 480px; height: 210px"'
            '></iframe>'
        )

    def test_goteo(self):
        self.assertMarkdown("""\
            ::: goteo my-project
            """,
            '<iframe'
            ' frameborder="0"'
            ' height="492px"'
            ' scrolling="no"'
            ' src="//www.goteo.org/widget/project/my-project"'
            ' width="300px"'
            '></iframe>'
        )

    def test_tweet_allOptions(self):
        self.assertMarkdown("""\
            ::: twitter marcmushu 1270395360163307530 theme=dark hideimages align=right conversation
            """, """\
            <blockquote align="right" class="twitter-tweet" data-dnt="true" data-theme="dark">
            <p dir="ltr" lang="ca">Sóc l'únic que creu que els pares s'haurien de gastar tots els seus diners en el que vulguin (ja que s'ho han currat durant anys) abans de morir en comptes de deixar res d'herència?</p>— marc (@marcmushu) <a href="https://twitter.com/marcmushu/status/1270395360163307530?ref_src=twsrc%5Etfw">June 9, 2020</a></blockquote>
            """)

    def test_tweet(self):
        self.assertMarkdown("""\
            ::: twitter marcmushu 1270395360163307530
            """, """\
            <blockquote class="twitter-tweet" data-dnt="true">
            <p dir="ltr" lang="ca">Sóc l'únic que creu que els pares s'haurien de gastar tots els seus diners en el que vulguin (ja que s'ho han currat durant anys) abans de morir en comptes de deixar res d'herència?</p>— marc (@marcmushu) <a href="https://twitter.com/marcmushu/status/1270395360163307530?ref_src=twsrc%5Etfw">June 9, 2020</a></blockquote>
            """)

    def test_linkcard(self):
        self.assertMarkdown("""
            ::: linkcard https://www.eldiario.es/economia/Congreso-decreto-ingreso-minimo-vital_0_1036596743.html
            ""","""
            <div class="linkcard">
            <a href="https://www.eldiario.es/economia/Congreso-decreto-ingreso-minimo-vital_0_1036596743.html"><img src="https://www.eldiario.es/fotos/Gobierno-abajo-PSOE-Socialista-Transicion_EDIIMA20200429_0307_3.jpg" style="float:right; width=30%" /></a>
            <div class="link-sitename">ELDIARIO.ES</div>
            <h3><a href="https://www.eldiario.es/economia/Congreso-decreto-ingreso-minimo-vital_0_1036596743.html">El ingreso mínimo vital contra la pobreza sale adelante en el Congreso con el apoyo de todos los partidos excepto Vox</a></h3>
            <div class="linkcard-description">
            <p>La nueva renta mínima estatal se tramitará como proyecto de ley, para que los grupos parlamentarios puedan incluir y debatir enmiendas al textoMAPA | Los municipios y barrios más afectados por la pobreza en España que pretende combatir el ingreso mínimo vital</p>
            </div>
            <div class="readmore"><a href="https://www.eldiario.es/economia/Congreso-decreto-ingreso-minimo-vital_0_1036596743.html">Read More</a></div>
            </div>
            """)

    def test_figure(self):
        self.assertMarkdown("""
            ::: figure "https://via.placeholder.com/300.png"
                This figure is awsome
            """,
            "<figure>"
            """<a href="https://via.placeholder.com/300.png"><img src="https://via.placeholder.com/300.png" /></a>"""
            "<figcaption>\n"
            "<p>This figure is awsome</p>\n"
            "</figcaption>\n"
            "</figure>"
            )

    def test_figure_title(self):
        self.assertMarkdown("""
            ::: figure "https://via.placeholder.com/300.png" title="This is a title"
                This figure is awsome
            """,
            "<figure>"
            '<a href="https://via.placeholder.com/300.png">'
            '<img '
                'src="https://via.placeholder.com/300.png" '
                'title="This is a title" '
            '/></a>'
            "<figcaption>\n"
            "<p>This figure is awsome</p>\n"
            "</figcaption>\n"
            "</figure>"
            )

    def test_figure_alt(self):
        self.assertMarkdown("""
            ::: figure "https://via.placeholder.com/300.png" alt="This is a title"
                This figure is awsome
            """,
            "<figure>"
            '<a href="https://via.placeholder.com/300.png">'
            '<img '
                'alt="This is a title" '
                'src="https://via.placeholder.com/300.png" '
            '/></a>'
            "<figcaption>\n"
            "<p>This figure is awsome</p>\n"
            "</figcaption>\n"
            "</figure>"
            )

    def test_figure_classes(self):
        self.assertMarkdown("""
            ::: figure "https://via.placeholder.com/300.png" left-align
                This figure is awsome
            """,
            '<figure class="left-align">'
            '<a href="https://via.placeholder.com/300.png">'
            '<img '
                'src="https://via.placeholder.com/300.png" '
            '/></a>'
            "<figcaption>\n"
            "<p>This figure is awsome</p>\n"
            "</figcaption>\n"
            "</figure>"
            )


    def test_figure_attributes_toFigure(self):
        self.assertMarkdown("""
            ::: figure "https://via.placeholder.com/300.png" style="background: red"
                This figure is awsome
            """,
            '<figure style="background: red">'
            '<a href="https://via.placeholder.com/300.png">'
            '<img '
                'src="https://via.placeholder.com/300.png" '
            '/></a>'
            "<figcaption>\n"
            "<p>This figure is awsome</p>\n"
            "</figcaption>\n"
            "</figure>"
            )

# vim: et ts=4 sw=4
