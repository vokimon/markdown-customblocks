![Logo](img/logo-customblocks.svg)

# Customblocks for Markdown

[![CI](https://github.com/vokimon/markdown-customblocks/actions/workflows/main.yml/badge.svg)](https://github.com/vokimon/markdown-customblocks/actions/workflows/main.yml)
[![Coverage](https://img.shields.io/coveralls/vokimon/markdown-customblocks/master.svg?style=flat-square&label=Coverage)](https://coveralls.io/r/vokimon/markdown-customblocks)
[![PyPi](https://img.shields.io/pypi/v/markdown-customblocks.svg?style=flat-square&label=PyPI)](https://pypi.org/project/markdown-customblocks/)
[![license: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![downloads](https://img.shields.io/pypi/dm/markdown-customblocks.svg?style=flat-square&label=PyPI%20Downloads)](https://pypi.org/project/markdown-customblocks/)
<!--
[![image](https://img.shields.io/pypi/pyversions/markdown-customblocks.svg?style=flat-square&label=Python%20Versions)](https://pypi.org/project/markdown-customblocks/)
[![image](https://img.shields.io/pypi/implementation/markdown-customblocks.svg?style=flat-square&label=Python%20Implementations)](https://pypi.org/project/markdown-customblocks/)
-->

Customblocks is an extension for [Python-Markdown] that defines
a **common markup** for **parametrizable and nestable components**
that can be **user defined** with a simple Python function.

The extension also provides sample components that can be used off-the-shelf:
div containers, admonitions, figures, link cards... and embeds from common sites (youtube, vimeo, twitter...)

[Python-Markdown]: https://python-markdown.github.io/

- [Introduction](#introduction)
- [Motivation](#motivation)
- [Installation and setup](#installation-and-setup)
- [General markup syntax](#general-markup-syntax)
- [Implementing a generator](#implementing-a-generator)
- [Predefined generators](#predefined-generators)
    - [Container (`customblocks.generators.container`)](#container-customblocksgeneratorscontainer)
    - [Admonition (`customblocks.generators.admonition`)](#admonition-customblocksgeneratorsadmonition)
    - [Link card (`customblocks.generators.linkcard`)](#link-card-customblocksgeneratorslinkcard)
    - [Figure (`customblocks.generators.figure`)](#figure-customblocksgeneratorsfigure)
    - [Youtube (`customblocks.generators.youtube`)](#youtube-customblocksgeneratorsyoutube)
    - [Vimeo (`customblocks.generators.vimeo`)](#vimeo-customblocksgeneratorsvimeo)
    - [Twitter (`customblocks.generators.twitter`)](#twitter-customblocksgeneratorstwitter)
    - [Verkami (`customblocks.generators.verkami`)](#verkami-customblocksgeneratorsverkami)
    - [Goteo (`customblocks.generators.goteo`)](#goteo-customblocksgeneratorsgoteo)
- [Generator tools](#generator-tools)
	- [Hyperscript generation](#hyperscript-generation)
	- [PageInfo](#pageinfo)
	- [Fetcher](#fetcher)
- [Release history](#release-history)
- [TODO](#todo)

## Introduction

The extension parses markup structures like this one:

```markdown
::: mytype "value 1" param2=value2
    Indented content
```

and then delegates HTML generation to custom python functions (_generators_)
you can write and bind to the type (`mytype`, in the example).

For instance, we could bind `mytype` to the following generator:

```python
def mygenerator(ctx, param1, param2):
    return f"""<div attrib1="{param1}" attrib2="{param2}">{ctx.content}</div>"""
```

So that, the previous markdown would generate:

```html
<div attrib1="value 1" attrib2="value2">Indented Content</div>
```

Generating html with f-strings like this,
without the proper escaping,
is not a good idea.
Don't hesitate.
The extension provides utilities you can use in you generators to make all that painless.


The extension also provides several useful generators you can use out of the box:

- `container`: A div element with arbitrary classes, attributes and content (This is the default when no type matches)
- `admonition`: Admonitions, boxes for notes, warnings... (quite similar to the [standard extra extension][ExtraAdmonitions])
- `figure`: Full featured figures with captions, lightbox...
- `linkcard`: External link cards (like Facebook and Twitter do, when you post a link)
- `twitter`: Embeded tweets
- `youtube`: Embeded videos from youtube...
- `vimeo`: Embeded videos from vimeo...
- `verkami`: Fund raising project widget in [Verkami]
- `goteo`: Fund raising project widget in [Goteo]

[ExtraAdmonitions]: https://python-markdown.github.io/extensions/admonition/

They are examples, you can always rewrite them to suit your needs.

We all stand on giants' shoulders so take a look at the [long list](docs/inspiration.md)
of markdown extensions and other software that inspired and influenced ideas for this extension.
Kudos for all of them.


## Installation and setup

To install:

```bash
$ pip install markdown-customblocks
```

From command line:

```bash
markdown -x customblocks ...
```

From Python:

```python
import markdown
md = markdown.Markdown(
    extensions=["customblocks"],
    extension_configs=dict(
        customblocks={
           ...
	}
    ),
md.convert(markdowncontent)
```

In order to enable it in Pelican:

```python
MARKDOWN = {
    'extensions': [
        'customblocks',
    ],
}
```

## General markup syntax

This is a more complete example of custom block usage:

```markdown
::: mytype param1 key1=value1 "param with many words" key2="value2 with words"
    Indented **content**

    The block ends whenever the indentation stops
This unindented line is not considered part of the block
```

The line starting with `:::` is the _headline_.
It specifies, first, the block type (`mytype`) followed by a set of _values_.
Such values can be either single worded or multi word by quoting them.

Also some values may explicit a target parameter with a _key_.
From the available block parameters, key values are set first,
and then the remaining unset parameters are filled by position.

After the _headline_, several lines of indented _content_ may follow.
The content ends with the very first non-emtpy line back on the previous indentation.

A block type may interpret the content as markdown as well.
So you can have nested blocks by adding extra indentation.
For example:

```markdown
::: recipe
    # Sweet water
    ::: ingredients "4 persons"
        - two spons of suggar
        - a glass of tap water
    ::: mealphoto sweetwater.jpg
        Looks gorgeus!
    Drop the suggar into the glass. Stir.
```

::: note
	By using indentation, you don't need a closing tag in most cases.
	You can use, a closing `:::` at the same level of the headline.

```markdown
::: mealphoto sweetwater.jpg
	Looks gorgeus!
:::
	This is an indented code
```

## Parameter matching

Besides `ctx`, the rest of function parameters are filled using values parsed from _head line_.
Unlike Python, you can interleave in the headline values with and without keys.
They are resolved as follows:

- **Explicit key:** When a key in the headline matches a keyable parameter name in the generator, the value is assigned to it
- **Flag:** Generator arguments annotated as `bool` (like example's `myflag`), or defaulting to `True` or `False`, (like example's `yourflag`) are considered flags
    - When a keyless value matches a flag name in the generator (`myflag`), `True` is passed
    - When it matches the flag name prefixed with `no` (`nomyflag`), `False` is passed
- **Positional:** Remaining headline values and function parameters are assigned one-to-one by position
- **Restricted:** Restrictions on how to receive the values ([keyword-only] and [positional-only]) are respected and they will receive only values from either key or keyless values
- **Varidics:** If the signature contains key (`**kwds`) or positional (`*args`) varidic variables, any remaining key and keyless values from the headline are assigned to them

Following Markdown phylosophy, errors are warned but do not stop the processing, so:

- Unmatched function parameters without a default value will be warned and assigned an empty string.
- Unused headline values will be warned and ignored.

[keyword-only]: https://www.python.org/dev/peps/pep-3102/
[positional-only]: https://www.python.org/dev/peps/pep-0570/

A generator can use several strategies to generate content:

- Return an html string (single root node)
- Return a `markdown.etree` `Element` object
- Manipulate `ctx.parent` to add the content and return `None`


## Implementing a generator

A block type can be defined just by hooking the **generator** function to the type.

```python
MARKDOWN = {
    ...
    'extensions_configs': {
        'customblocks': {
            'generators': {
                # by direct symbol reference
                'mytype': myparentmodule.mymodule.mytype,
                # or using import strings (notice the colon)
                'aka_mytype': 'myparentmodule.mymodule:mytype',
            }
        },
    },
}
```


The signature of the generator will determine the attributes taken from the headline.

```python
def mytype(ctx, param1, myflag:bool, param2, param3, yourflag=True, param4='default2'):
    ...
```

The first parameter, `ctx`, is the context.
If you don't use it, you can skip it.
But it is useful if you want to receive some context parameters like:

- `ctx.parent`: the parent node
- `ctx.content`: the indented part of the block, with the indentation removed
- `ctx.parser`: the markdown parser, can be used to parse the inner content or any other markdown code
- `ctx.type`: the type of the block
    - If you reuse the same function for different types, this is how you diferentiate them
- `ctx.metadata`: A dictionary with metadata from your metadata plugin.
- `ctx.config`: A dictionary passed from `extension_configs.customblocks.config`

Besides `ctx`, the rest of function parameters are filled using values parsed from _head line_.
Unlike Python, you can interleave in the headline values with and without keys.
They are resolved as follows:

- **Explicit key:** When a key in the headline matches a keyable parameter name in the generator, the value is assigned to it
- **Flag:** Generator arguments annotated as `bool` (like example's `myflag`), or defaulting to `True` or `False`, (like example's `yourflag`) are considered flags
    - When a keyless value matches a flag name in the generator (`myflag`), `True` is passed
    - When it matches the flag name prefixed with `no` (`nomyflag`), `False` is passed
- **Positional:** Remaining headline values and function parameters are assigned one-to-one by position
- **Restricted:** Restrictions on how to receive the values ([keyword-only] and [positional-only]) are respected and they will receive only values from either key or keyless values
- **Varidics:** If the signature contains key (`**kwds`) or positional (`*args`) varidic variables, any remaining key and keyless values from the headline are assigned to them

Following Markdown phylosophy, errors are warned but do not stop the processing, so:

- Unmatched function parameters without a default value will be warned and assigned an empty string.
- Unused headline values will be warned and ignored.

[keyword-only]: https://www.python.org/dev/peps/pep-3102/
[positional-only]: https://www.python.org/dev/peps/pep-0570/

A generator can use several strategies to generate content:

- Return an html string (single root node)
- Return a `markdown.etree` `Element` object
- Manipulate `ctx.parent` to add the content and return `None`

In order to construct an ElementTree,
we recommend using the [Hyperscript utility](#hyperscript-generation).
Resulting code will be more compact and readable and
makes proper escaping when injecting values.

## Predefined generators

### Container (`customblocks.generators.container`)

This is the default generator if no generator
is associated to the type.

It generates a `<div>` element
with the typename as class.
It also appends any positional parameter as additional classes
and keyword arguments as attributes.
The content is reinterpreted as markdown.

This is quite useful to create a 'div' structure
in the html document.

#### Options

`*args`
: added as additional classes for the outter div

`**kwds`
: added as attributes for the outter div

content:
: reparsed as markdown

#### Example

The following example:

```markdown
::: sidebar left style="width: 30em"
    ::: widget
        # Social
        ...
    ::: widget
        # Related
        ...
```

Renders as:

```html
<div class='sidebar left' style="width: 30em">
    <div class='widget'>
        <h1>Social</h1>
        <p>...</p>
    </div>
    <div class='widget'>
        <h1>Related</h1>
        <p>...</p>
    </div>
</div>
```

### Admonition (`customblocks.generators.admonition`)

An admonition is a specially formatted text out of the main flow
which remarks a piece of text, often in a box or with a side
icon to identify it as that special type of text.

Admonition generator is, by default, assigned to the following types:
`attention`, `caution`, `danger`, `error`, `hint`, `important`, `note`, `tip`, `warning`.

So you can write:

```markdown
::: danger
    Do not try to do this at home
```

In order to generate:

```html
<div class="admonition danger">
<p class="admonition-title">Danger</p>
<p>Do not try to do this at home</p>
</div>
```

::: danger
    Do not try to do this at home

Generated code emulates the one generated by ReST admonitions
(which is also emulated by `markdown.extra.admonition`).
So, you can benefit from existing styles and themes.

#### Options

`title`
: in the title box show that text instead of the 

`*args`
: added as additional classes for the outter div

`**kwds`
: added as attributes for the outter div

content:
: reparsed as markdown

**Warning:**
If you are migrating from `extra.admonition`,
be careful as `extra` identifies title using the quotes,
while `customblocks` will take the first parameter as title and next values as additional classes.
If you like having the classes before, you should explicit the `title` key.

```markdown
::: danger blinking title="Super danger"
    Do **not** try to do this at home
```

#### Examples

By using this [recommended style](css/admonition.css)
from .

```markdown
::: note
	This is a note

::: note "Custom note title" style="border-radius:6px"
	This is a note with customized style

	- item
	- item

::: important
	This is important

::: warning
	This is a warning

::: caution
	This is a caution

::: attention
	Something to be attended

::: danger
	This is a danger

::: error
	This is a error

::: hint
	This is a hint

::: tip
	This is a tip
```

::: note
	This is a note

::: note "Custom note title" style="border-radius:6px"
	This is a note with customized style

	- item
	- item

::: important
	This is important

::: warning
	This is a warning

::: caution
	This is a caution

::: attention
	Something to be attended

::: danger
	This is a danger

::: error
	This is a error

::: hint
	This is a hint

::: tip
	This is a tip


### Figure (`customblocks.generators.figure`)

An image as captioned figure.
The content is taken as caption.
```markdown
::: figure images/myimage.jpg alt='an image' nice
    This is a **nice** image.
```

Renders into:

```html
<figure class="nice">
  <a href="images/myimage.jpg target="_blank">
    <img src="images/myimage.jpg" alt="an image" />
  </a>
  <figcaption>
    <p>This is a <b>nice</b> image</p>
  </figcaption>
</figure>
```

`url`
: the url to the image

`alt` (keyword only)
: image alt attribute

`title` (keyword only)
: image title attribute

`lightbox` (bool)
: whether to open a lightbox on click or not

`*args`
: additional classes for root `<figure>` tag

`**kwds`
: additional attributes for root `<figure>` tag

The `lightbox` option generates a slighty different markup:

```markdown
:::figure lightbox https://www.w3schools.com/howto/img_lights.jpg pull-right style="width:40%"
    what a gorgeus image
```

```html
<figure class="lightbox pull-right" id="fafb8273-ef7c-47b4-a31f-57d9e0387fc1" style="width:40%">
  <a class="lightbox-background" href="javascript:history.back()"></a>
  <a href="#fafb8273-ef7c-47b4-a31f-57d9e0387fc1">
    <img src="https://www.w3schools.com/howto/img_snow.jpg" />
  </a>
  <figcaption>
    <p>what a gorgeus image</p>
  </figcaption>
</figure>

```

:::figure https://www.w3schools.com/howto/img_lights.jpg lightbox pull-right style="width:40%"
    what a gorgeus image

The `lightbox` relies heavily on css in order to work.
So, in this case, you are encoraged to use the recommended [figure css](css/figure.css).


TODO (you can help!):

- global configuration
- figure enumeration ("Figure N:")
- thumbnails
- fetch external images to make them local
- css for placement classes (left, centered, right...)
- improve css

### Link card (`customblocks.generators.linkcard`)

A link card is a informative box about an external source.
It is similar to the card that popular apps like
Wordpress, Facebook, Twitter, Telegram, Slack...
generate when you embed/post a link.

In order to build the box,
the generator downloads the target url and extracts social [metadata][SocialMeta]:
Featured image, title, description...
The download page is cached so that first non-failing download will avoid further downloads.

[SocialMeta]: https://css-tricks.com/essential-meta-tags-social-media/

```markdown
::: linkcard https://css-tricks.com/essential-meta-tags-social-media/
```

::: linkcard https://css-tricks.com/essential-meta-tags-social-media/

The above example uses [this css](css/linkcard.css).


`url`
: The url to embed as card

`wideimage` (Flag, default True)
: Whether the featured image will be shown wide, if not, a small thumb will be shown

Content, if provided will be used as excerpt instead of the summary in the page.

Additionally you can provide the following keyword parameters
to override information extracted from the url:

- `image`: the image heading the card
- `title`: the caption
- `description`: the text describing the link (though using content is recommended)
- `siteurl`: a link to the main site
- `sitename`: the name of the main site
- `siteicon`: the site icon

This generator uses the `fetcher` helper.
So, that the first fetch will cached for later generations.

### Youtube (`customblocks.generators.youtube`)

This generator generates an embeded youtube video.

#### Example

```markdown
::: youtube HUBNt18RFbo
```

```html
<div class="videowrapper youtube">
  <iframe src="https://www.youtube-nocookie.com/embed/HUBNt18RFbo"></iframe>
</div>
```

::: youtube HUBNt18RFbo

::: warning
	Even though, youtube-nocookie.com is suposed to avoid tracing cookies,
	google sets some tracing cookies from one of the included javascript files.

#### Options

`autoplay` (flag, default False)
: starts the video as soon as it is loaded

`loop` (flag, default False)
: restart again the video once finished

`controls` (flag, default True)
: show the controls

`*args`
: added as additional class for the outter div

`**kwds`
: added as attributes for the outter div

Indented content is ignored.

[Recommended css](css/videowrapper.css)

Or you could set `youtube_inlineFluidStyle` config to `True`
and the style will be added inline to every video.


### Vimeo (`customblocks.generators.vimeo`)

This generator generates an embeded vimeo video.

```markdown
::: vimeo 139579122 
```

::: vimeo 139579122

#### Options

`autoplay` (flag, default False)
: starts the video as soon as it is loaded

`loop` (flag, default False)
: restart again the video once finished

`bylabel` (flag, default True)
: Shows the video author's name

`portrait` (flag, default False)
: Shows the video author's avatar

`*args`
: added as additional class for the outter div

`**kwds`
: added as attributes for the outter div

Content is ignored.


### Twitter (`customblocks.generators.twitter`)

Embeds a tweet.

```markdown
::: twitter marcmushu 1270395360163307530 theme=dark lang=es track=true
```

#### Options

`user`:
: the user that wrote the tweet

`tweet`
: the tweet id (a long number)

`theme` (optional, default `light`)
: It can be either `dark` or `light`

`hideimages`
: Do not show attached images in the embedded

`align`
: `left`, `center` or `right`

`conversation`
: whether to add or not the full thread


### Verkami (`customblocks.generators.verkami`)

Embeds a [Verkami] fund raising campaign widget.

[Verkami]: https://www.verkami.com/

```markdown
::: verkami 26588 landscape
```

`id`
: The id of the project (can be the number or the full id)

`landscape` (Flag, default False)
: instead of a portrait widget generate a landscape one


### Goteo (`customblocks.generators.goteo`)

Embeds a [Goteo] fund raising campaign widget.

[Goteo]: https://goteo.org

```markdown
::: goteo my-cool-project
```

`id`
: The id of the project


## Generator tools

Common code has been extracted from predefined generators.
If you need this functionality you are encouraged to use them.

- Hyperscript: to generate html
- PageInfo: to extract metadata from a webpage
- Fetcher: to download resources with file based cache


### Hyperscript generation

You can generate html with strings or using `etree`; but there is a more elegant option.

[Hyperscript] is the idea of writing code that generates html/xml
as nested function calls that look like the actual xml structure.
This can be done by using the `customblocks.utils.E` function which has this signature:

```
def E(tag, *children, **attributes): ...
```

`tag` is the name of the tag (`pre`, `div`, `strong`...).
An empty string is equivalent to `div`.
It can have appended several `.classname` that will be added as element class.

Any keyword parameter will be taken as element attributes.
You can use the special `_class` attribute to append more classes.
Notice the underline, as `class` is a reserved word in Python.

`children` takes the keyless parameters and they can be:

- `None`: then it will be ignored
- `dict`: it will be merged with the attributes
- `str`: it will be added as text
- `etree.Element`: it will be added as child node
- `customblocks.utils.Markdown`: will append parsed markdown (see below)
- Any `tuple`, `list` or iterable: will add each item following previous rules

```python
from customblocks.utils import E, Markdown

def mygenerator(ctx, image):
	return (
		E('.mytype',
			dict(style="width: 30%; align: left"),
			E('a', dict(href=image),
				E('img', src=image),
			),
			Markdown(ctx.content, ctx.parser),
		)
	)
```

[Hyperscript]: http://hyperhype.github.io/hyperscript/

### PageInfo

`utils.pageinfo.PageInfo` is a class that retrieves
meta information from html pages by means of its properties.

Properties are computed lazily and use cache.
Once you get one property for a given page, later uses will have little impact.

Any attribute you explicit on the constructor will override
the ones derived from actual content.

```python
info = PageInfo(html, url='http://site.com/path/page.html')
info.sitename # the name of the site (meta og:site_name or the domain
info.siteicon # the favicon or similar
info.siteurl  # the base url of the site (not the page)
info.title    # page title (from og:title meta or `<title>` content)
info.description # short description (from og:description or twitter:description)
info.image    # featured image (from og:image or twitter:image, or site image)
```

### Fetcher

A fetcher object is a wrapper around the `requests` library
that uses caching to avoid downloading once and again remote resource
each time you compile the markdown file.

The first time a resource is succesfully downloaded by a fetcher
the request response is stored in the provided folder in a yaml file
which has the mangled url as name.
Successive tries to download it just take the content of that file
to construct a query.

```python
from customblocks.utils import Fetcher

fetcher = Fetcher('mycachedir')
response = fetcher.get('https://canvoki.net/codder')
# to force next call
fetcher.remove('https://canvoki.net/codder')
```

## Release history

See [CHANGES.md](CHANGES.md)


## TODO

- Default css for generators
- Flags: coerce to bool?
- Annotations: coerce to any type
- Fetcher:
	- configurable cache dir
	- file name too long
	- handle connection errors
- Linkcard:
	- Mediawiki: Short description and main image: https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts|pageimages&exintro=&explaintext=&titles=Sant%20Joan%20Desp%C3%AD
- Youtube:
    - Take aspect ratio and sizes from Youtube api
    - Use covers https://i.ytimg.com/vi/{code}/hqdefault.jpg
- Twitter
    - Privacy safe mode
- Instagram
- peertube
```html
<iframe title="Onion Rice from 1977: The Instruction the Recipe Submitter gives is Priceless!" src="https://tilvids.com/videos/embed/bb6057d2-427b-4c31-9b8c-0a8c7d0a29c9?start=4m51s&amp;stop=5m1s&amp;loop=1&amp;autoplay=1&amp;muted=1" allowfullscreen="" sandbox="allow-same-origin allow-scripts allow-popups" width="560" height="315" frameborder="0"></iframe>
```
- Figure flags:
	- no flag
		- Un modified url
	- local (when remote url)
		- download
		- place it on a given dir
		- set url to local path
	- inline
		- download
		- detect mime type
		- compute base 64
		- set url to data url
	- thumb
		- download
		- generate a thumb
		- place the thumb on thumb dir
		- when combined with 'inline'
			- url to the local path
		- when combined with 'local'
			- link to the image
	- lightbox
	- sized






