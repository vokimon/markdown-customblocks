# Custom blocks for Markdown

[![image](https://img.shields.io/travis/vokimon/markdown-customblocks/master.svg?style=flat-square&label=TravisCI)](https://travis-ci.org/vokimon/markdown-customblocks)
[![image](https://img.shields.io/coveralls/vokimon/markdown-customblocks/master.svg?style=flat-square&label=Coverage)](https://coveralls.io/r/vokimon/markdown-customblocks)
[![image](https://img.shields.io/pypi/v/markdown-customblocks.svg?style=flat-square&label=PyPI)](https://pypi.org/project/markdown-customblocks/)
[![license: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
<!--
[![image](https://img.shields.io/pypi/dm/markdown-customblocks.svg?style=flat-square&label=PyPI%20Downloads)](https://pypi.org/project/markdown-customblocks/)
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
	- [Container (`customblocks.generators.container`)](#container-customblocks.generators.container)
	- [Admonition (`customblocks.generators.admonition`)](#admonition-customblocks.generators.admonition)
	- [Link card (`customblocks.generators.linkcard`)](#link-card-customblocks.generators.linkcard)
	- [Figure (`customblocks.generators.figure`)](#figure-customblocks.generators.figure)
	- [Youtube (`customblocks.generators.youtube`)](#youtube-customblocks.generators.youtube)
	- [Twitter (`customblocks.generators.twitter`)](#twitter-customblocks.generators.twitter)
- [Motivation](#motivation)
- [Release history](#release-history)
	

## What is it?

> **Warning: This extension is still in its early development stages.**\
> It is a proposal still open to discussion and
> generators API could be subject of change.

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
- `linkcard`: External link cards (like Facebook and Twitter do, when you post a link)

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

> **Warning:** This is still a draft. Conventions are likely to change until first stable version.

A block type can be defined just by defining a generator function:

```python
def mytype(ctx, param1, myflag:bool, param2, param3, yourflag=True, param4='default2'):
	...
```

You have to register it to a type

```python
MARKDOWN = {
	...
    'extensions_configs': {
        'customblocks': {
			'generators': {
				'mytype': mytype,
			}
        },
    },
}
```

The generator can use several strategies to generate content:

- Return an html string,
- Return `etree` `Element`, or
- Manipulate `ctx.parent` and return `None`

The first parameter, `ctx`, is the context.
If you don't use it, you can skip it but it is useful if you want to receive some context parameters:

- `ctx.parent`: the parent node
- `ctx.content`: the indented part of the block, with the indentation removed
- `ctx.parser`: the markdown parser, can be used to parse the content or any other markdown code
- `ctx.type`: the type of the block
	- If you reuse the same function for different types, this is how you diferentiate them
- `ctx.metadata`: A dictionary with metadata from your metadata plugin.

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
	Milk and chicken has been the responsibles the demoratization
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
<div class="admonition-title">Danger</div>
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


### Figure (`customblocks.generators.figure`)

Not documented yet.


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

Content is ignored.

### Twitter (`customblocks.generators.twitter`)

Not documented yet.

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

### markdown-customblocks 0.2.0 (2020-06-25)

- Improve documentation (parameter passing, toc...)
- Provide `ctx.metadata` to access Markdown.Meta (from `extra.meta`, `full_yaml_metadata`... extensions)
- `figure`: link to the image

### markdown-customblocks 0.1.0 (2020-06-23)

- First working version
- Support for function based generators
- Default block: container
- Example blocks: admonition, twitter, youtube, figure, linkcard


## TODO

- Make configuration available to generators
- Generator specific configuration
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






