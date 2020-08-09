# Custom blocks for Markdown

[![image](https://img.shields.io/travis/vokimon/markdown-customblocks/master.svg?style=flat-square&label=TravisCI)](https://travis-ci.org/vokimon/markdown-customblocks)
[![image](https://img.shields.io/coveralls/vokimon/markdown-customblocks/master.svg?style=flat-square&label=Coverage)](https://coveralls.io/r/vokimon/markdown-customblocks)
[![image](https://img.shields.io/pypi/v/markdown-customblocks.svg?style=flat-square&label=PyPI)](https://pypi.org/project/markdown-customblocks/)
[![license: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![image](https://img.shields.io/pypi/dm/markdown-customblocks.svg?style=flat-square&label=PyPI%20Downloads)](https://pypi.org/project/markdown-customblocks/)
<!--
[![image](https://img.shields.io/pypi/pyversions/markdown-customblocks.svg?style=flat-square&label=Python%20Versions)](https://pypi.org/project/markdown-customblocks/)
[![image](https://img.shields.io/pypi/implementation/markdown-customblocks.svg?style=flat-square&label=Python%20Implementations)](https://pypi.org/project/markdown-customblocks/)
-->

This [Python-Markdown] extension defines
a common markup for parametrizable and nestable components that can be extended by defining a plain Python function.

Includes some sample components for div containers, admonitions, figures, link cards... and embeds from common sites (youtube, vimeo, twitter...)

[Python-Markdown]: https://python-markdown.github.io/

- [What is it?](#what-is-it)
- [Why this?](#why-this)
- [Installation and setup](#installation-and-setup)
- [General markup syntax](#general-markup-syntax)
- [Implementing a generator](#implementing-a-generator)
- [Predefined generators](#predefined-generators)
    - [Container (`customblocks.generators.container`)](#container-customblocksgeneratorscontainer)
    - [Admonition (`customblocks.generators.admonition`)](#admonition-customblocksgeneratorsdmonition)
    - [Link card (`customblocks.generators.linkcard`)](#link-card-customblocksgeneratorsinkcard)
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

## What is it?

This extension parses markup structures like this one:

```markdown
::: mytype "value 1" param2=value2
    Indented content
```

delegating the HTML generation to custom functions (generators)
you can define or redefine for the type (`mytype`, in the example) to suit your needs.
For example, we could bind `mytype` to this generator:

```python
def mygenerator(ctx, param1, param2):
    """Quick and dirty generator, needs escaping"""
    return f"""<div attrib1="{param1}" attrib2="{param2}">{ctx.content}</div>"""
```

and the previous markdown will generate:

```html
<div attrib1="value 1" attrib2="value2">Indented Content</div>
```

The extension also provides several useful generators:

- `container`: A classed div with arbitrary classes, attributes and content (This is the default when no type matches)
- `figure`: Figures with caption and more
- `admonition`: Admonitions (quite similar to the [standard extra extension][ExtraAdmonitions])
- `twitter`: Embeded tweets
- `youtube`: Embeded videos from youtube...
- `vimeo`: Embeded videos from vimeo...
- `linkcard`: External link cards (like Facebook and Twitter do, when you post a link)
- `verkami`: Fund raising project widget in [Verkami]
- `goteo`: Fund raising project widget in [Goteo]

[ExtraAdmonitions]: https://python-markdown.github.io/extensions/admonition/

They are examples, you can always rewrite them to suit your needs.

## Why this?

Markdown, has a quite limited set of structures,
and you often end up writing html by hand:
A figure, an embed...
If you use that structure multiple times,
whenever you find a better way,
you end up updating the structures in multiple places.
That's why you should use (or develop) a markdown extension to ease the proces.

There is a catch.
Each markdown extension has to identify its own markup.
For new extensions, is hard to find a handy markup no body is using yet.
Because of that, the trend is having a lot of different markups,
even for extensions sharing purpose.
When you find a better extension for your figures,
again, it is likely you have to edit all your figures, once more,
because the markup is different.

Also coding an extension is hard.
Markdown extension API is required to be complex to address many other scenarios.
But this extension responds to this usual scenario:

> I want to generate this **piece of html** which
> depends on those **parameters** and maybe it should
> include a given **content**.

**So, why not using a common markup for all those structures?**
: This way, we can define a common parser for all them.
To create a new block type, we have no need to find out an unused markup or developing new parsers.

**So, why not using a type name to identify the structure?**
: It provides a conceptual link to the block meaning.
Both when you read the markup and when you change the behaviour.
We can redefine how the block type behaves by hooking a different behaviour to the type name.

**So, why not defining a common attribute markup?**
: This way we can set a common way to map attributes to Python functions.
The extension can delegate HTML generation to the function by looking at the signature. No extra glue required.

**So, why not using indentation to define inner content?**
: It visually shows the scope of the block and allows nesting.
If the content is reparsed as Markdown,
it could still include other components with their inner content a level down.

We all stand on giants' shoulders so take a look at the [long list](doc/inspiration.md)
of markdown extensions and other software that inspired and influenced this extension.
Kudos for them.


## Installation and setup

To install:

```bash
$ pip install markdown-customblocks
```

In order to enable it in Markdown:

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
Such values can be either single worded or quoted.
Also some values may explicit a target parameter with a _key_.

After the _headline_, several lines of indented _content_ may follow,
and the block ends at the very first line back to the previous indentation.
Emtpy lines are included and there is no need of an empty line to end the block.

> By using indentation you don't need a closing tag,
> but if you miss it, you might place a closing `:::` at the same
> level of the headline.

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

This is the default generator when no other generator matches the block type.
It can be used to generate html div document structure with markdown.

It creates a `<div>` element with the type name as class.
Keyless values are added as additional classes and
key values are added as attributes for the `div` element.

`*args`
: added as additional classes for the outter div

`**kwds`
: added as attributes for the outter div


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

Generated code emulates the one generated by ReST admonitions
(which is also emulated by `markdown.extra.admonition`).
So, you can benefit from existing styles and themes.

`title`
: in the title box show that text instead of the 

`*args`
: added as additional classes for the outter div

`**kwds`
: added as attributes for the outter div

**Warning:**
If you are migrating from `extra.admonition`,
be careful as `extra` identifies title using the quotes,
while `customblocks` will take the first parameter as title and next values as additional classes.
If you like having the classes before, you should explicit the `title` key.

```markdown
::: danger blinking title="Super danger"
    Do **not** try to do this at home
```

### Figure (`customblocks.generators.figure`)

An image as captioned figure.
The content is taken as caption.

`url`
: the url to the image

`alt` (keyword only)
: image alt attribute

`title` (keyword only)
: image title attribute

`*args`
: additional classes for root `<figure>` tag

`**kwds`
: additional attributes for root `<figure>` tag




### Link card (`customblocks.generators.linkcard`)

A link card is a informative box about an external source.
It is similar to the card that popular apps like
Wordpress, Facebook, Twitter, Telegram, Slack...
generate when you embed/post a link.

The generator downloads the target url and extracts social [metadata][SocialMeta]:
Featured image, title, description...

[SocialMeta]: https://css-tricks.com/essential-meta-tags-social-media/

```markdown
::: linkcard https://css-tricks.com/essential-meta-tags-social-media/
```

`url`
: The url to embed as card

`wideimage` (Flag, default True)
: Whether the featured image will be shown wide, if not, a small thumb will be shown

Content, if provided will be used as excerpt instead of the summary in the page.

Additionally you can provide the following keyword parameters
to override information extracted from the url:

- `image`: the image heading the card
- `title`: the caption
- `description`: the text describing the link
- `siteurl`: a link to the main site
- `sitename`: the name of the main site
- `siteicon`: the site icon

### Youtube (`customblocks.generators.youtube`)

This generator generates an embeded youtube video.

```markdown
::: youtube HUBNt18RFbo nocontrols left-align
```

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

Recommended css:

```css
.videowrapper {
    position:relative;
    padding-bottom:56.25%;
    overflow:hidden;
    height:0;
    width:100%
}
.videowrapper iframe {
    position:absolute;
    left:0;
    top:0;
    width:100%;
    height:100%;
}
```

Or you could set `youtube_inlineFluidStyle` config to `True`
and the style will be added inline to every video.


### Vimeo (`customblocks.generators.vimeo`)

This generator generates an embeded vimeo video.

```markdown
::: vimeo 139579122  nocontrols left-align
```

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
as nested function calls that look like the the actual xml structure.
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

Properties are cached so you once you use them for one page,
later uses, have litle impact.

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

### markdown-customblocks 1.1.1 (2020-08-08)

- documentation fixes

### markdown-customblocks 1.1.0 (2020-08-08)

- `utils.Fetcher`: Helper for catched downloads
- `utils.PageInfo`: Page information retrieval helper
- `utils.E`: Helper to generate HTML using hyperscript idiom
- `utils.Markdown`: Helper to include markdown in hyperscript
- `linkcard`: Example style emulating Wordpress' embedded link
- `linkcard`: Explicit image, description, title...
- `linkcard`: Fix: relative links to images and icons
- `linkcard`: Removed half implemented embedimage flag
- `twitter`: Cache twitter info downloads

### markdown-customblocks 1.0.0 (2020-06-27)

- Register a generator with a string like `'module.submodule:function'`
- Support single quoted values

### markdown-customblocks 0.3.0 (2020-06-27)

- Provide `ctx.config` from `extension_configs.customblocks.config`
- New generators: vimeo, verkami, goteo
- admonition: title should be a `<p>` not a `<div>` for ReST styles to work
- youtube: responsive/fluid sizing
- documented all generators

### markdown-customblocks 0.2.0 (2020-06-25)

- Improve documentation (parameter passing, toc...)
- Provide `ctx.metadata` to access Markdown.Meta (from `extra.meta`, `full_yaml_metadata`... extensions)
- `figure`: link to the image

### markdown-customblocks 0.1.0 (2020-06-23)

- First public version
- Support for function based generators
- Default generator: container
- Example generators: admonition, twitter, youtube, figure, linkcard


## TODO

- Default css for generators
- Flags: coerce to bool?
- Annotations: coerce to any type
- Fetcher: configurable cache dir
- Linkcard:
	- Look for short description by class (ie wikipedia)
- Youtube:
    - Take aspect ratio and sizes from Youtube api
    - Use covers
    - Privacy safe mode
- Twitter
    - Privacy safe mode
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






