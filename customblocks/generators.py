from bs4 import BeautifulSoup
from yamlns import namespace as ns
import uuid

from .utils import E, Markdown
from .utils import PageInfo
from .utils import Fetcher

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

def figure(ctx, url, *args, lightbox:bool=None, **kwds):
    title = kwds.pop('title', None)
    alt = kwds.pop('alt', None)
    id = kwds.pop('id',None) or (str(uuid.uuid4()) if lightbox else None)
    classes = list(args)
    if lightbox: classes.append('lightbox')
    return E('figure',
        dict(
            _class = ' '.join(classes) or None,
            id = id,
        ),
        E('a.lightbox-background', href="javascript:history.back()") if lightbox else '',
        E('a',
            dict(
                href = f'#{id}' if lightbox else url,
                target = None if lightbox else '_blank'
            ),
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

def linkcard(ctx, url, *args, wideimage=True, **overrides):
    fetcher = Fetcher('fetchercache/linkcard') # TODO: Configurable
    response = fetcher.get(url)

    info = PageInfo(response.text, url, **overrides)

    nl='\n'
    return E('.linkcard',
        dict(_class=' '.join(args)),
        info.image and E('.linkcard-featured-image' + ('.side' if not wideimage else ''), nl,
            E('a', dict(href=url, target='_blank'), nl,
                E('img', src=info.image), nl,
            ), nl,
        ), nl,
        E('p.linkcard-heading',
            E('a', info.title, href=url, target="_blank"),
        ), nl,
        E('.linkcard-excerpt', nl,
            Markdown(ctx.content) if ctx.content.strip()
            else E('p', nl, info.description, nl), nl,
            E('span.linkcard-more', E('a', 'Read more', href=url, target="_blank")), nl,
        ), nl,
        E('.linkcard-footer', nl,
            E('.linkcard-site-title', nl,
                E('a',
                    dict(href=info.siteurl, target="_blank"), nl,
                    E('img.linkcard-site-icon',
                        height='32',
                        src=info.siteicon,
                        width='32',
                    ), nl,
                    E('span', info.sitename.upper()), nl,
                ), nl,
            ), nl,
            E('.linkcard-meta', nl)
        ),
    )


def youtube(ctx, id, *args, autoplay=False, controls=True, loop=False, style=None, **kwds):
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
    if style:
        if wrapperStyle: wrapperStyle = "; ".join((wrapperStyle, style))
        else: wrapperStyle = style

    url = f"https://www.youtube-nocookie.com/embed/{id}{options}"
    return E(
        ''.join(f'.{cls}' for cls in ('videowrapper', 'youtube', *args)),
        E('iframe',
            src=url,
            frameborder=0,
            style=iframeStyle,
        ),
        style=wrapperStyle,
        **kwds,
    )

def vimeo(ctx, id, *args, autoplay=False, loop=False, byline=True, portrait=False, **kwds):
    options=[o for o in [
        'dnt=1', # cookieless (GDPR compliant)
        'byline=0' if not byline else '',
        'portrait=0' if not portrait else '',
        'loop=1' if loop else '',
        'autoplay=1' if autoplay else '',
    ] if o]

    return E(
        ''.join(f'.{cls}' for cls in ('videowrapper', 'vimeo', *args)),
        kwds,
        E('iframe',
            src = "https://player.vimeo.com/video/{}?{}"
                .format(id, '&'.join(options)),
            width="100%",
            height="300",
            frameborder="0",
            allow="autoplay; fullscreen",
            allowfullscreen="allowfullscreen",
        )
    )

def peertube(ctx, instance, uuid, *args,
        start=None, stop=None, loop=False, autoplay=False,
        muted=False, title=True, controls=True, p2p=True,
        **kwds
):
    # TODO:
    # warningTitle=0 To hide the privacy warning subtitle
    # peertubeLink=0 To hide the link to the video in peertube instance
    options = []
    if start is not None:
        options.append("start={}".format(start))
    if stop is not None:
        options.append("stop={}".format(stop))
    if loop: options.append("loop=1")
    if autoplay: options.append("autoplay=1")
    if muted: options.append("muted=1")
    if not title: options.append("title=0")
    if not controls: options.append("controlBar=0")
    if not p2p: options.append("p2p=0")

    options = '&amp;'.join(options)
    if options: options = "?"+options

    return E(
        ''.join(f'.{cls}' for cls in ('videowrapper', 'peertube', *args)),
        kwds,
        E('iframe',
            src=f"https://{instance}/videos/embed/{uuid}{options}",
            allowfullscreen="allowfullscreen",
            sandbox="allow-same-origin allow-scripts allow-popups",
            frameborder="0",
        ),
    )


def verkami(ctx, id, *, landscape=False):
    orientation = 'landscape' if landscape else 'portrait'
    style = (
        "width: 480px; height: 210px"
        if landscape else
        "width: 240px; height: 490px"
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
        scrolling="no",
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

    fetcher = Fetcher('fetchercache/twitter')
    oembedurl = (
        f'https://publish.twitter.com/oembed?'
        f'url=https://twitter.com/{user}/status/{tweet}&dnt=True{options}'
    )
    response = fetcher.get(oembedurl)
    result = ns(response.json())
    soup = BeautifulSoup(result.html, 'html.parser')
    return type(u'')(soup.find('blockquote'))

def mastodon(ctx, instance, user, post):
    # TODO: For future prove using oembed https://{instance}/api/oembed
    return E('.postembed.mastodon',
        E('iframe.mastodon-embed',
            src=f"https://{instance}/{user}/{post}/embed",
            style="max-width: 100%; border: 0",
            width="400",
            #allow="autoplay; clipboard-write; encrypted-media; picture-in-picture; web-share",
            allowfullscreen="allowfullscreen",
        ),
        # Adjusts iframe height to the content
        E('script',
            {'async': "async"},
            src=f"https://{instance}/embed.js",
        ),
    )

def facebook(ctx, page, post, *args, text=True, width='auto', height=452., **kwds):
    text = 'true' if text and text!='false' else 'false'
    return E('iframe',
        dict(_class=' '.join(args)),
        src="https://www.facebook.com/plugins/post.php?"
            f"href=https%3A%2F%2Fwww.facebook.com%2F{page}%2Fposts%2F{post}&amp;show_text={text}&amp;lazy=false&amp;width=auto",
        height=f"{height}",
        scrolling="no",
        frameborder="0",
        allowfullscreen="true",
        allow="autoplay; clipboard-write; encrypted-media; picture-in-picture; web-share",
        **kwds
    )

def instagram(ctx, post, *args, caption=True, **kwds):
    permalink = f"https://www.instagram.com/p/{post}"
    return E('blockquote.instagram-media',
        {
            'data-instgrm-permalink': permalink,
            'data-instgrm-version': "14",
        },
        { 'data-instgrm-captioned': True } if caption else {},
        E('script', {'async': True, 'src': "//www.instagram.com/embed.js"}),
        E('', 'Instagram post embedding not available. '),
        E('a', "Watch it on Instagram", href=permalink),
        dict(_class=' '.join(args)),
        **kwds
    )

def map(ctx, location=None, marker=True, *args, **kwds):
    import geocoder
    geocoding = geocoder.osm(location).json
    bbox = '%2C'.join(str(x) for x in (
        geocoding['bbox']['northeast'][::-1] +
        geocoding['bbox']['southwest'][::-1]
    ))
    boundary = f"/relation/{geocoding['osm_id']}"
    markerparam = f'&amp;marker={geocoding["lat"]}%2C{geocoding["lng"]}' if marker else ''
    return E('iframe.map',
        dict(_class=' '.join(args)),
        frameborder="0",
        marginwidth="0",
        marginheight="0",
        scrolling="no",
        style="display: block; width: 100%; width: 1fr; aspect-ratio: 16 / 9",
        src=f"https://www.openstreetmap.org/export/embed.html?relation=345893&amp;layer=mapnik&amp;bbox={bbox}{markerparam}&amp;query=lanteira",
        **kwds
    )

def wikipedia(ctx, lemma, *args, lang=None, wideimage=False, **kwds):
    lang = lang or 'en'
    wiki_url = f'https://{lang}.wikipedia.org/wiki/{lemma}'
    return linkcard(ctx, wiki_url, 'wikipedia', wideimage=wideimage, *args, **kwds)

# vim: et ts=4 sw=4
