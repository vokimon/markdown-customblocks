import base64
import html
import requests
from bs4 import BeautifulSoup
from xml.etree import ElementTree as etree
from yamlns import namespace as ns

from .utils import E, Markdown
from .pageinfo import PageInfo

def container(ctx, *args, **kwds):
    args = [ '-'.join(arg.split()) for arg in args ]
    return E('.'+ctx.type,
        dict(_class=' '.join(args)),
        Markdown(ctx.content, ctx.parser),
        **kwds
    )

def admonition(ctx, title=None, *args, **kwds):
    args = [ '-'.join(arg.split()) for arg in args ] # Untested case
    return E('.admonition.'+ctx.type,
        dict(_class=' '.join(list(args))),
        E('p.admonition-title', title or ctx.type.title()),
        Markdown(ctx.content, ctx.parser),
        **kwds
    )

def figure(ctx, url, *args, **kwds):
    title = kwds.pop('title', None)
    alt = kwds.pop('alt', None)
    return E('figure',
        dict(
            _class = ' '.join(args) or None,
        ),
        E('a', dict(href = url),
            E('img',
                src=url,
                title=title,
                alt=alt,
            )
        ),
        E('figcaption',
            Markdown(ctx.content, parser=ctx.parser)
        ),
        **kwds
    )

def linkcard(ctx, url, *, wideimage=True, embedimage=False, **overrides):
    response = requests.get(url)

    info = PageInfo(response.text, url, **overrides)

    siteName = info.sitename
    siteurl = info.siteurl
    title = info.title
    excerpt = info.description

    websiteicon = info.siteicon
    image = info.image

    if embedimage:
        imageresponse = requests.get(image, stream=True)
        if imageresponse.ok:
            imageBytes = imageresponse.raw.read()
            b64image = base64.b64encode(imageBytes).decode('ascii')
            # TODO: thumb it
            image = 'data:image/jpg;base64,' + b64image
    else:
        image = html.escape(image)

    nl='\n'
    return E('.linkcard',
        E('.linkcard-featured-image' + ('.square' if not wideimage else ''), nl,
            E('a', dict(href=url), nl,
                E('img', src=image), nl,
            ), nl,
        ), nl,
        E('p.linkcard-heading',
            E('a', title, href=url),
        ), nl,
        E('.linkcard-excerpt', nl,
            Markdown(ctx.content) if ctx.content.strip()
            else E('p', nl, info.description, nl), nl,
            E('span.linkcard-more', E('a', 'Read more', href=url)), nl,
        ), nl,
        E('.linkcard-footer', nl,
            E('.linkcard-site-title', nl,
                E('a.linkcard-site-icon',
                    dict(href=siteurl), nl,
                    E('img.linkcard-site-icon',
                        height='32',
                        src=websiteicon,
                        width='32',
                    ), nl,
                    E('span', siteName.upper()), nl,
                ), nl,
            ), nl,
            E('.linkcard-meta', nl)
        ),
    )


def youtube(ctx, id, *, autoplay=False, controls=True, loop=False):
    options = []
    inlineStyle = ctx.config.get('youtube_inlineFluidStyle', False)
    if autoplay:
        options.append('autoplay=1')
    if not controls:
        options.append('controls=0')
    if loop:
        options.append('loop=1')
    options = ('?' + '&'.join(options)) if options else ''
    wrapperStyle = (
            'position:relative; padding-bottom:56.25%; '
            'height:0; overflow:hidden; width:100%'
        ) if inlineStyle else None
    iframeStyle = (
            'position:absolute; '
            'top:0; left:0; '
            'width:100%; height:100%;'
        ) if inlineStyle else None

    url = f"https://www.youtube.com/embed/{id}{options}"
    return E('.videowrapper.youtube',
        E('iframe',
            src=url,
            style=iframeStyle,
        ),
        style=wrapperStyle,
    )

def vimeo(ctx, id, *, autoplay=False, loop=False, byline=True, portrait=False):
    options=[]
    if not byline: options.append("byline=0")
    if not portrait: options.append('portrait=0')
    if loop: options.append('loop=1')
    if autoplay: options.append('autoplay=1')

    return E('iframe',
        src = "https://player.vimeo.com/video/{}?{}"
            .format(id, '&'.join(options)),
        width="100%",
        height="300",
        frameborder="0",
        allow="autoplay; fullscreen",
        allowfullscreen="allowfullscreen",
    )

def verkami(ctx, id, *, landscape=False):
    orientation = 'landscape' if landscape else 'portrait'
    style = (
        "width: 480px; height: 210px"
        if landscape else
        "width: 240px; height: 350px"
    )
    return E('iframe.js-widget-iframe',
        id='verkami{}'.format(orientation.title()),
        allowtransparency="true",
        style=style,
        frameborder="0",
        scrolling="no",
        src="https://www.verkami.com/projects/{}/widget_{}".format(id,orientation),
    )

def goteo(ctx, id):
    return E('iframe',
        frameborder="0",
        height="492px",
        src="//www.goteo.org/widget/project/{}".format(id),
        width="300px",
        scrolling="no"
    )


def twitter(user,
    tweet=None,
    theme=None,
    hideimages=False,
    align=None,
    conversation=False,
):
    options = ''
    options += f'&theme={theme}' if theme in ('dark', 'light') else ''
    options += '&cards=hidden' if hideimages else ''
    options += f'&align={align}' if align in ('right', 'center', 'left') else ''
    options += f'&conversation=none' if not conversation else ''

    response = requests.get(
        f'https://publish.twitter.com/oembed?url=https://twitter.com/{user}/status/{tweet}&dnt=True{options}'
    )
    result = ns(response.json())
    #print("oembed result:", result.dump())
    soup = BeautifulSoup(result.html, 'html.parser')
    return type(u'')(soup.find('blockquote'))



# vim: et ts=4 sw=4
