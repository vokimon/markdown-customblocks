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

A [Python-Markdown] extension to define custom block types
using an uniform, parametrizable and nestable syntax.

[Python-Markdown]: https://python-markdown.github.io/

- [What is it?](#what-is-it)
- [Installation and setup](#installation-and-setup)
- [General markdown syntax](#general-markdown-syntax)
- [Implementing a custom block type](#implementing-a-custom-block-type)
- [Predefined block types](#predefined-block-types)
    - [Container (`customblocks.generators.container`)](#container-customblocksgeneratorscontainer)
    - [Admonition (`customblocks.generators.admonition`)](#admonition-customblocksgeneratorsdmonition)
    - [Link card (`customblocks.generators.linkcard`)](#link-card-customblocksgeneratorsinkcard)
    - [Figure (`customblocks.generators.figure`)](#figure-customblocksgeneratorsfigure)
    - [Youtube (`customblocks.generators.youtube`)](#youtube-customblocksgeneratorsyoutube)
    - [Vimeo (`customblocks.generators.vimeo`)](#vimeo-customblocksgeneratorsvimeo)
    - [Twitter (`customblocks.generators.twitter`)](#twitter-customblocksgeneratorstwitter)
    - [Verkami (`customblocks.generators.verkami`)](#verkami-customblocksgeneratorsverkami)
    - [Goteo (`customblocks.generators.goteo`)](#goteo-customblocksgeneratorsgoteo)
- [Motivation](#motivation)
- [Release history](#release-history)
- [TODO](#todo)


## What is it?

This markdown extension simplifies the definition and use
of new types of block, by defining a common syntax for them.
That is, a common way to specify the type of the block,
its attributes and content.

Custom block types are defined by a simple generator function.
The extension deals with markdown parsing and
it passes attributes and inner content as parameters to the generator.
The generator uses them to generate the desired HTML code.

The extension also provides several useful examples of generators:

- `container`: The default one, a classed div with arbitrary classes, attributes and content.
- `figure`: Figures with caption and more
- `admonition`: Admonitions (quite similar to the [standard extra extension][ExtraAdmonitions])
- `twitter`: Embeded tweets
- `youtube`: Embeded videos from youtube...
- `vimeo`: Embeded videos from vimeo...
- `linkcard`: External link cards (like Facebook and Twitter do, when you post a link)
- `verkami`: Fund raising project widget in [Verkami]
- `goteo`: Fund raising project widget in [Goteo]

[ExtraAdmonitions]: https://python-markdown.github.io/extensions/admonition/

While they are quite convenient you can overwrite them all by defining your own function...
Or your could contribute to enhance them. :-)


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

## General markdown syntax

This is an example of custom block usage:

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
    Drop the suggar into the glass. Stir.
```

## Implementing a custom block type

A block type can be defined just by defining a **generator** function.
The signature of the generator will determine the attributes that accept from the headline.

```python
def mytype(ctx, param1, myflag:bool, param2, param3, yourflag=True, param4='default2'):
    ...
```

You have to register it to a type:

```python
MARKDOWN = {
    ...
    'extensions_configs': {
        'customblocks': {
            'generators': {
                # direct symbol reference
                'mytype': mytype,
                # using import strings
                'akamytype': 'myparentmodule.mymodule:mytype',
            }
        },
    },
}
```

A generator can use several strategies to generate content:

- Return an html string
- Return `etree` `Element`
- Manipulate `ctx.parent` and return `None`

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

## Predefined block types

This is a quick reference for the use of the included generators.
Detailed explanation follows.

```markdown
::: linkcard http://othersite.com/post/2020-06-01-john-s-work

::: youtube HUBNt18RFbo center

::: twitter marcmushu 1270395360163307530

::: twitter marcmushu 1270395360163307530 theme=dark lang=es track=true

::: figure ethernalbulb.jpg left thumb
    The century old bulb still bringing light.

    This make you think you have been mocked.

::: figure ethernalbulb.jpg right

::: figure ethernalbulb.jpg wide

::: figure ethernalbulb.jpg 

::: important "Remember the milk"
    Milk and chicken has been the responsibles the democratization
    of the protein sources.
```

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

A link cards is a informative box about an external source.
It is similar to the card that popular apps like Facebook, Twitter, Telegram, Slack... generate when you post a link.

The generator downloads the target url and extracts social [metadata][SocialMeta]:
Featured image, title, description...

[SocialMeta]: https://css-tricks.com/essential-meta-tags-social-media/

```markdown
::: linkcard https://css-tricks.com/essential-meta-tags-social-media/
```

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


## Motivation

Each markdown extension has to detect its own markers
without messing with other extensions.
Because of that, the trend has been each extension
using its different unique marking syntax.

Often several extensions implement the same concept
(say twitter links, figures, thumbnails, admonitions...)
providing more or less features and using different syntax.
If you find a better extension for the same feature,
you end up rewritting your markdown sources.

Also writting an extension is quite hard.
The extension architecture is complex by need.
It has to support a wide range of scenarios.
But a common scenario here is the macro scenario:

> I want to generate this **piece of html** which
> depends on those **parameters** and maybe it should
> include a given **content**.

So, it would be nice to:

- Have a common syntax and differentiate block by a semantic name
- Have a common way to specify parameters
- Define the content in a way that you could nest blocks
- Plugins just specify the expected parameters in the signature and generate the output with them
- Get the block type you like and add the feature you miss

We all stand on giants' shoulders so take a look at the [long list](doc/inspiration.md)
of markdown extensions and other software that inspired and influenced this extension.


## Release history

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
- Figure
    - Thumbnail generation
    - lightbox
    - Deexternalizer
- Youtube:
    - Take aspect ratio and sizes from Youtube api
    - Use covers
    - Privacy safe mode
- Twitter
    - Privacy safe mode






