import unittest
from markdown import markdown
from markdown import test_tools
import responses
from pathlib import Path

class Generators_Test(test_tools.TestCase):

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

    def test_admonition_sluggify(self):
        self.assertMarkdown("""\
            ::: note "A title" "super monition" style="float:left;width:30%"
                content
            """, """\
            <div class="admonition note super-monition" style="float:left;width:30%">
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
            <iframe frameborder="0" src="https://www.youtube-nocookie.com/embed/7SS24_CgwEM"></iframe>
            </div>
            """)

    def test_youtube_withAutoplay(self):
        self.assertMarkdown("""\
            ::: youtube 7SS24_CgwEM autoplay
            """, """\
            <div class="videowrapper youtube">
            <iframe frameborder="0" src="https://www.youtube-nocookie.com/embed/7SS24_CgwEM?autoplay=1"></iframe>
            </div>
            """)

    def test_youtube_withAutoplayAndLoop(self):
        self.assertMarkdown("""\
            ::: youtube 7SS24_CgwEM autoplay loop
            """, """\
            <div class="videowrapper youtube">
            <iframe frameborder="0" src="https://www.youtube-nocookie.com/embed/7SS24_CgwEM?autoplay=1&amp;loop=1"></iframe>
            </div>
            """)

    def test_youtube_nocontrols(self):
        self.assertMarkdown("""\
            ::: youtube 7SS24_CgwEM nocontrols
            """, """\
            <div class="videowrapper youtube">
            <iframe frameborder="0" src="https://www.youtube-nocookie.com/embed/7SS24_CgwEM?controls=0"></iframe>
            </div>
            """)

    def test_youtube_inlineStyles_byConfig(self):
        self.setupConfig(youtube_inlineFluidStyle=True)
        self.assertMarkdown("""\
            ::: youtube 7SS24_CgwEM nocontrols
            """, """\
            <div class="videowrapper youtube" style="position:relative; padding-bottom:56.25%; height:0; overflow:hidden; width:100%">
            <iframe frameborder="0" src="https://www.youtube-nocookie.com/embed/7SS24_CgwEM?controls=0" style="position:absolute; top:0; left:0; width:100%; height:100%;"></iframe>
            </div>
            """)

    def test_youtube_customClasses(self):
        self.assertMarkdown("""\
            ::: youtube 7SS24_CgwEM custom-class
            """, """\
            <div class="videowrapper youtube custom-class">
            <iframe frameborder="0" src="https://www.youtube-nocookie.com/embed/7SS24_CgwEM"></iframe>
            </div>
            """)

    def test_youtube_customAttribs(self):
        self.assertMarkdown("""\
            ::: youtube 7SS24_CgwEM attrib=value
            """, """\
            <div attrib="value" class="videowrapper youtube">
            <iframe frameborder="0" src="https://www.youtube-nocookie.com/embed/7SS24_CgwEM"></iframe>
            </div>
            """)

    def test_youtube_customStyle(self):
        self.assertMarkdown("""\
            ::: youtube 7SS24_CgwEM style="width:80%"
            """, """\
            <div class="videowrapper youtube" style="width:80%">
            <iframe frameborder="0" src="https://www.youtube-nocookie.com/embed/7SS24_CgwEM"></iframe>
            </div>
            """)

    def test_youtube_inlineStyles_byConfig_mergeCustomStyles(self):
        self.setupConfig(youtube_inlineFluidStyle=True)
        self.assertMarkdown("""\
            ::: youtube 7SS24_CgwEM nocontrols style="background: red"
            """, """\
            <div class="videowrapper youtube" style="position:relative; padding-bottom:56.25%; height:0; overflow:hidden; width:100%; background: red">
            <iframe frameborder="0" src="https://www.youtube-nocookie.com/embed/7SS24_CgwEM?controls=0" style="position:absolute; top:0; left:0; width:100%; height:100%;"></iframe>
            </div>
            """)

    def test_vimeo(self):
        self.assertMarkdown("""\
            ::: vimeo 55297514
            """, """\
            <div class="videowrapper vimeo">
            <iframe allow="autoplay; fullscreen" allowfullscreen="allowfullscreen" frameborder="0" height="300" src="https://player.vimeo.com/video/55297514?dnt=1&amp;portrait=0" width="100%"></iframe>
            </div>
            """)

    def test_vimeo_loop(self):
        self.assertMarkdown("""\
            ::: vimeo 55297514 loop
            """, """\
            <div class="videowrapper vimeo">
            <iframe allow="autoplay; fullscreen" allowfullscreen="allowfullscreen" frameborder="0" height="300" src="https://player.vimeo.com/video/55297514?dnt=1&amp;portrait=0&amp;loop=1" width="100%"></iframe>
            </div>
            """)

    def test_vimeo_autoplay(self):
        self.assertMarkdown("""\
            ::: vimeo 55297514 autoplay
            """, """\
            <div class="videowrapper vimeo">
            <iframe allow="autoplay; fullscreen" allowfullscreen="allowfullscreen" frameborder="0" height="300" src="https://player.vimeo.com/video/55297514?dnt=1&amp;portrait=0&amp;autoplay=1" width="100%"></iframe>
            </div>
            """)

    def test_vimeo_nobyline(self):
        self.assertMarkdown("""\
            ::: vimeo 55297514 nobyline
            """, """\
            <div class="videowrapper vimeo">
            <iframe allow="autoplay; fullscreen" allowfullscreen="allowfullscreen" frameborder="0" height="300" src="https://player.vimeo.com/video/55297514?dnt=1&amp;byline=0&amp;portrait=0" width="100%"></iframe>
            </div>
            """)

    def test_vimeo_portrait(self):
        self.assertMarkdown("""\
            ::: vimeo 55297514 portrait
            """, """\
            <div class="videowrapper vimeo">
            <iframe allow="autoplay; fullscreen" allowfullscreen="allowfullscreen" frameborder="0" height="300" src="https://player.vimeo.com/video/55297514?dnt=1" width="100%"></iframe>
            </div>
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
            ' style="width: 240px; height: 490px"'
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
            ::: twitter votomitico 1193240526373507072 theme=dark hideimages align=right conversation
            """, """\
            <blockquote align="right" class="twitter-tweet" data-dnt="true" data-theme="dark">
            <p dir="ltr" lang="es">Para que no te encuentres sorpresas y evitar malos entendidos, estas son todas las papeletas al congreso que te encontraras en la mesa.<a href="https://t.co/CteAknu7AW">https://t.co/CteAknu7AW</a></p>— Mitos electorales (@votomitico) <a href="https://twitter.com/votomitico/status/1193240526373507072?ref_src=twsrc%5Etfw">November 9, 2019</a></blockquote>
            """)

    def test_tweet(self):
        self.assertMarkdown("""\
            ::: twitter votomitico 1193240526373507072
            """, """\
            <blockquote class="twitter-tweet" data-dnt="true">
            <p dir="ltr" lang="es">Para que no te encuentres sorpresas y evitar malos entendidos, estas son todas las papeletas al congreso que te encontraras en la mesa.<a href="https://t.co/CteAknu7AW">https://t.co/CteAknu7AW</a></p>— Mitos electorales (@votomitico) <a href="https://twitter.com/votomitico/status/1193240526373507072?ref_src=twsrc%5Etfw">November 9, 2019</a></blockquote>
            """)

    def setupResponse(self):
        responses.add(
            method='GET',
            url='https://www.eldiario.es/economia/Congreso-decreto-ingreso-minimo-vital_0_1036596743.html',
            status=200,
            body=Path('testdata/ingresominimo.html').read_text(encoding='utf8'),
        )

    @responses.activate
    def test_linkcard(self):
        self.setupResponse()
        self.assertMarkdown("""
            ::: linkcard https://www.eldiario.es/economia/Congreso-decreto-ingreso-minimo-vital_0_1036596743.html
            ""","""\
<div class="linkcard">
<div class="linkcard-featured-image">
<a href="https://www.eldiario.es/economia/Congreso-decreto-ingreso-minimo-vital_0_1036596743.html" target="_blank">
<img src="https://static.eldiario.es/clip/79066be9-947d-4b83-bab9-a0d092bb391f_facebook-watermarked-aspect-ratio_default_0.jpg" />
</a>
</div>
<p class="linkcard-heading"><a href="https://www.eldiario.es/economia/Congreso-decreto-ingreso-minimo-vital_0_1036596743.html" target="_blank">El ingreso mínimo vital contra la pobreza sale adelante en el Congreso con el apoyo de todos los partidos excepto Vox</a></p>
<div class="linkcard-excerpt">
<p>
La nueva renta mínima estatal se tramitará como proyecto de ley, para que los grupos parlamentarios puedan incluir y debatir enmiendas al texto
</p>
<span class="linkcard-more"><a href="https://www.eldiario.es/economia/Congreso-decreto-ingreso-minimo-vital_0_1036596743.html" target="_blank">Read more</a></span>
</div>
<div class="linkcard-footer">
<div class="linkcard-site-title">
<a href="https://www.eldiario.es" target="_blank">
<img class="linkcard-site-icon" height="32" src="https://www.eldiario.es/favicon.png" width="32" />
<span>ELDIARIO</span>
</a>
</div>
<div class="linkcard-meta">
</div>
</div>
</div>
""")

    @responses.activate
    def test_linkcard_noImage(self):
        self.setupResponse()
        self.assertMarkdown("""
            ::: linkcard image='' https://www.eldiario.es/economia/Congreso-decreto-ingreso-minimo-vital_0_1036596743.html
            ""","""\
<div class="linkcard">
""" # No image here
"""\
<p class="linkcard-heading"><a href="https://www.eldiario.es/economia/Congreso-decreto-ingreso-minimo-vital_0_1036596743.html" target="_blank">El ingreso mínimo vital contra la pobreza sale adelante en el Congreso con el apoyo de todos los partidos excepto Vox</a></p>
<div class="linkcard-excerpt">
<p>
La nueva renta mínima estatal se tramitará como proyecto de ley, para que los grupos parlamentarios puedan incluir y debatir enmiendas al texto
</p>
<span class="linkcard-more"><a href="https://www.eldiario.es/economia/Congreso-decreto-ingreso-minimo-vital_0_1036596743.html" target="_blank">Read more</a></span>
</div>
<div class="linkcard-footer">
<div class="linkcard-site-title">
<a href="https://www.eldiario.es" target="_blank">
<img class="linkcard-site-icon" height="32" src="https://www.eldiario.es/favicon.png" width="32" />
<span>ELDIARIO</span>
</a>
</div>
<div class="linkcard-meta">
</div>
</div>
</div>
""")

    @responses.activate
    def test_linkcard_nowideimage(self):
        self.setupResponse()
        self.assertMarkdown("""
            ::: linkcard nowideimage https://www.eldiario.es/economia/Congreso-decreto-ingreso-minimo-vital_0_1036596743.html
            ""","""\
<div class="linkcard">
<div class="linkcard-featured-image side">""" # difference here
"""
<a href="https://www.eldiario.es/economia/Congreso-decreto-ingreso-minimo-vital_0_1036596743.html" target="_blank">
<img src="https://static.eldiario.es/clip/79066be9-947d-4b83-bab9-a0d092bb391f_facebook-watermarked-aspect-ratio_default_0.jpg" />
</a>
</div>
<p class="linkcard-heading"><a href="https://www.eldiario.es/economia/Congreso-decreto-ingreso-minimo-vital_0_1036596743.html" target="_blank">El ingreso mínimo vital contra la pobreza sale adelante en el Congreso con el apoyo de todos los partidos excepto Vox</a></p>
<div class="linkcard-excerpt">
<p>
La nueva renta mínima estatal se tramitará como proyecto de ley, para que los grupos parlamentarios puedan incluir y debatir enmiendas al texto
</p>
<span class="linkcard-more"><a href="https://www.eldiario.es/economia/Congreso-decreto-ingreso-minimo-vital_0_1036596743.html" target="_blank">Read more</a></span>
</div>
<div class="linkcard-footer">
<div class="linkcard-site-title">
<a href="https://www.eldiario.es" target="_blank">
<img class="linkcard-site-icon" height="32" src="https://www.eldiario.es/favicon.png" width="32" />
<span>ELDIARIO</span>
</a>
</div>
<div class="linkcard-meta">
</div>
</div>
</div>
""")

    @responses.activate
    def test_linkcard_image(self):
        self.setupResponse()
        self.assertMarkdown("""
            ::: linkcard image=cached.jpg https://www.eldiario.es/economia/Congreso-decreto-ingreso-minimo-vital_0_1036596743.html
            ""","""\
<div class="linkcard">
<div class="linkcard-featured-image">
<a href="https://www.eldiario.es/economia/Congreso-decreto-ingreso-minimo-vital_0_1036596743.html" target="_blank">
<img src="cached.jpg" />""" # the difference is here
"""
</a>
</div>
<p class="linkcard-heading"><a href="https://www.eldiario.es/economia/Congreso-decreto-ingreso-minimo-vital_0_1036596743.html" target="_blank">El ingreso mínimo vital contra la pobreza sale adelante en el Congreso con el apoyo de todos los partidos excepto Vox</a></p>
<div class="linkcard-excerpt">
<p>
La nueva renta mínima estatal se tramitará como proyecto de ley, para que los grupos parlamentarios puedan incluir y debatir enmiendas al texto
</p>
<span class="linkcard-more"><a href="https://www.eldiario.es/economia/Congreso-decreto-ingreso-minimo-vital_0_1036596743.html" target="_blank">Read more</a></span>
</div>
<div class="linkcard-footer">
<div class="linkcard-site-title">
<a href="https://www.eldiario.es" target="_blank">
<img class="linkcard-site-icon" height="32" src="https://www.eldiario.es/favicon.png" width="32" />
<span>ELDIARIO</span>
</a>
</div>
<div class="linkcard-meta">
</div>
</div>
</div>
""")

    @responses.activate
    def test_linkcard_content_asExcerpt(self):
        self.setupResponse()
        self.assertMarkdown("""
            ::: linkcard https://www.eldiario.es/economia/Congreso-decreto-ingreso-minimo-vital_0_1036596743.html
                This is my description
            ""","""\
<div class="linkcard">
<div class="linkcard-featured-image">
<a href="https://www.eldiario.es/economia/Congreso-decreto-ingreso-minimo-vital_0_1036596743.html" target="_blank">
<img src="https://static.eldiario.es/clip/79066be9-947d-4b83-bab9-a0d092bb391f_facebook-watermarked-aspect-ratio_default_0.jpg" />
</a>
</div>
<p class="linkcard-heading"><a href="https://www.eldiario.es/economia/Congreso-decreto-ingreso-minimo-vital_0_1036596743.html" target="_blank">El ingreso mínimo vital contra la pobreza sale adelante en el Congreso con el apoyo de todos los partidos excepto Vox</a></p>
<div class="linkcard-excerpt">"""
# difference is the following lines
"""
<p>This is my description</p>
<span class="linkcard-more"><a href="https://www.eldiario.es/economia/Congreso-decreto-ingreso-minimo-vital_0_1036596743.html" target="_blank">Read more</a></span>
</div>
<div class="linkcard-footer">
<div class="linkcard-site-title">
<a href="https://www.eldiario.es" target="_blank">
<img class="linkcard-site-icon" height="32" src="https://www.eldiario.es/favicon.png" width="32" />
<span>ELDIARIO</span>
</a>
</div>
<div class="linkcard-meta">
</div>
</div>
</div>
""")

    @responses.activate
    def test_linkcard_content_withMarkdown(self):
        self.setupResponse()
        self.assertMarkdown("""
            ::: linkcard https://www.eldiario.es/economia/Congreso-decreto-ingreso-minimo-vital_0_1036596743.html
                This is my **description**

                And has two lines
            ""","""\
<div class="linkcard">
<div class="linkcard-featured-image">
<a href="https://www.eldiario.es/economia/Congreso-decreto-ingreso-minimo-vital_0_1036596743.html" target="_blank">
<img src="https://static.eldiario.es/clip/79066be9-947d-4b83-bab9-a0d092bb391f_facebook-watermarked-aspect-ratio_default_0.jpg" />
</a>
</div>
<p class="linkcard-heading"><a href="https://www.eldiario.es/economia/Congreso-decreto-ingreso-minimo-vital_0_1036596743.html" target="_blank">El ingreso mínimo vital contra la pobreza sale adelante en el Congreso con el apoyo de todos los partidos excepto Vox</a></p>
<div class="linkcard-excerpt">"""
# difference is the following lines
"""
<p>This is my <strong>description</strong></p>
<p>And has two lines</p>
<span class="linkcard-more"><a href="https://www.eldiario.es/economia/Congreso-decreto-ingreso-minimo-vital_0_1036596743.html" target="_blank">Read more</a></span>
</div>
<div class="linkcard-footer">
<div class="linkcard-site-title">
<a href="https://www.eldiario.es" target="_blank">
<img class="linkcard-site-icon" height="32" src="https://www.eldiario.es/favicon.png" width="32" />
<span>ELDIARIO</span>
</a>
</div>
<div class="linkcard-meta">
</div>
</div>
</div>
""")


    def test_figure(self):
        self.assertMarkdown("""
            ::: figure "https://via.placeholder.com/300.png"
                This figure is awsome
            """,
            "<figure>"
            """<a href="https://via.placeholder.com/300.png" target="_blank"><img src="https://via.placeholder.com/300.png" /></a>"""
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
            '<a href="https://via.placeholder.com/300.png" target="_blank">'
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
            '<a href="https://via.placeholder.com/300.png" target="_blank">'
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
            '<a href="https://via.placeholder.com/300.png" target="_blank">'
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
            '<a href="https://via.placeholder.com/300.png" target="_blank">'
            '<img '
                'src="https://via.placeholder.com/300.png" '
            '/></a>'
            "<figcaption>\n"
            "<p>This figure is awsome</p>\n"
            "</figcaption>\n"
            "</figure>"
            )

    def test_figure_lightbox(self):
        self.assertMarkdown("""
            ::: figure "https://via.placeholder.com/300.png" lightbox id=myimage
                This figure is awsome
            """,
            '<figure class="lightbox" id="myimage">' # added id
            '<a class="lightbox-background" href="javascript:history.back()"></a>' # this is new
            '<a href="#myimage">' # No target, href is the id
            '<img '
                'src="https://via.placeholder.com/300.png" '
            '/></a>'
            "<figcaption>\n"
            "<p>This figure is awsome</p>\n"
            "</figcaption>\n"
            "</figure>"
            )

    def test_wikipedia(self):
        self.assertMarkdown("""
            ::: wikipedia "Sant Joan Despí"
            ""","""\
<div class="linkcard wikipedia">
<div class="linkcard-featured-image side">
<a href="https://en.wikipedia.org/wiki/Sant Joan Despí" target="_blank">
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Torre_de_la_Creu.JPG/1200px-Torre_de_la_Creu.JPG" />
</a>
</div>
<p class="linkcard-heading"><a href="https://en.wikipedia.org/wiki/Sant Joan Despí" target="_blank">Sant Joan Despí - Wikipedia</a></p>
<div class="linkcard-excerpt">
<p>
<p><b>Sant Joan Despí</b> (<small>Catalan pronunciation:&#160;</small><span title="Representation in the International Phonetic Alphabet (IPA)" lang="ca-Latn-fonipa">[ˈsaɲ ʒuˈan dəsˈpi]</span>; Old Catalan for '"Saint John of the Pine"') is a city and municipality located in the Baix Llobregat area (Barcelona province in Catalonia, Spain). It is situated on the left bank of the Llobregat river.</p>
</p>
<span class="linkcard-more"><a href="https://en.wikipedia.org/wiki/Sant Joan Despí" target="_blank">Read more</a></span>
</div>
<div class="linkcard-footer">
<div class="linkcard-site-title">
<a href="https://en.wikipedia.org" target="_blank">
<img class="linkcard-site-icon" height="32" src="https://en.wikipedia.org/static/favicon/wikipedia.ico" width="32" />
<span>EN.WIKIPEDIA.ORG</span>
</a>
</div>
<div class="linkcard-meta">
</div>
</div>
</div>
""")

    def test_wikipedia_lang(self):
        self.assertMarkdown("""
            ::: wikipedia "Sant Joan Despí" lang=ca
            ""","""\
<div class="linkcard wikipedia">
<div class="linkcard-featured-image side">
<a href="https://ca.wikipedia.org/wiki/Sant Joan Despí" target="_blank">
<img src="https://upload.wikimedia.org/wikipedia/commons/e/e5/MasMorell-SantJoanDespi-CasesAuriga-5573.jpg" />
</a>
</div>
<p class="linkcard-heading"><a href="https://ca.wikipedia.org/wiki/Sant Joan Despí" target="_blank">Sant Joan Despí - Viquipèdia, l'enciclopèdia lliure</a></p>
<div class="linkcard-excerpt">
<p>
<p><b>Sant Joan Despí</b> és un municipi dins de la comarca del Baix Llobregat, situat al pla del Llobregat, a l'esquerra del riu. El municipi confronta amb els de Sant Feliu de Llobregat, Sant Just Desvern, Esplugues de Llobregat, Cornellà de Llobregat, Sant Boi i Santa Coloma de Cervelló.</p>
</p>
<span class="linkcard-more"><a href="https://ca.wikipedia.org/wiki/Sant Joan Despí" target="_blank">Read more</a></span>
</div>
<div class="linkcard-footer">
<div class="linkcard-site-title">
<a href="https://ca.wikipedia.org" target="_blank">
<img class="linkcard-site-icon" height="32" src="https://ca.wikipedia.org/static/favicon/wikipedia.ico" width="32" />
<span>CA.WIKIPEDIA.ORG</span>
</a>
</div>
<div class="linkcard-meta">
</div>
</div>
</div>
""")

    def test_peertube(self):
        self.assertMarkdown("""
            ::: peertube tilvids.com bb6057d2-427b-4c31-9b8c-0a8c7d0a29c9
        """, """\
<div class="videowrapper peertube">
<iframe allowfullscreen="allowfullscreen" frameborder="0" sandbox="allow-same-origin allow-scripts allow-popups" src="https://tilvids.com/videos/embed/bb6057d2-427b-4c31-9b8c-0a8c7d0a29c9"></iframe>
</div>
""")

    def test_peertube_fullOptions(self):
        self.assertMarkdown("""
            ::: peertube tilvids.com bb6057d2-427b-4c31-9b8c-0a8c7d0a29c9 start=10s stop=1m loop autoplay muted notitle nocontrols nop2p
        """, """\
<div class="videowrapper peertube">
<iframe allowfullscreen="allowfullscreen" frameborder="0" sandbox="allow-same-origin allow-scripts allow-popups" src="https://tilvids.com/videos/embed/bb6057d2-427b-4c31-9b8c-0a8c7d0a29c9?start=10s&amp;stop=1m&amp;loop=1&amp;autoplay=1&amp;muted=1&amp;title=0&amp;controlBar=0&amp;p2p=0"></iframe>
</div>
""")

    def test_mastodon(self):
        self.assertMarkdown("""
            ::: mastodon mastodon.social @votomitico 101631141406914275
        """, """\
<div class="postembed mastodon">
<iframe allowfullscreen="allowfullscreen" class="mastodon-embed" src="https://mastodon.social/@votomitico/101631141406914275/embed" style="max-width: 100%; border: 0" width="400"></iframe>
<script async="async" src="https://mastodon.social/embed.js"></script>
</div>
""")

# vim: et ts=4 sw=4
