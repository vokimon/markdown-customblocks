# Custom blocks for Markdown

**Test Status:**
[![image](https://img.shields.io/travis/vokimon/markdown-customblocks/master.svg?style=flat-square&label=TravisCI)](https://travis-ci.org/vokimon/markdown-customblocks)
[![image](https://img.shields.io/coveralls/vokimon/markdown-customblocks/master.svg?style=flat-square&label=Coverage)](https://coveralls.io/r/vokimon/markdown-customblocks)

**Version Info:**
[![image](https://img.shields.io/pypi/v/markdown-customblocks.svg?style=flat-square&label=PyPI)](https://pypi.org/project/markdown-customblocks/)
[![image](https://img.shields.io/pypi/dm/markdown-customblocks.svg?style=flat-square&label=PyPI%20Downloads)](https://pypi.org/project/markdown-customblocks/)

**Compatibility:**
[![image](https://img.shields.io/pypi/pyversions/markdown-customblocks.svg?style=flat-square&label=Python%20Versions)](https://pypi.org/project/markdown-customblocks/)
[![image](https://img.shields.io/pypi/implementation/markdown-customblocks.svg?style=flat-square&label=Python%20Implementations)](https://pypi.org/project/markdown-customblocks/)


A [Python-Markdown] extension to define custom block types
using an uniform, parametrizable and nestable syntax.

[Python-Markdown]: https://python-markdown.github.io/

> **This extension is still in its early development stages.**
> It is a proposal still open to debate.
> While the debate goes on, the markup syntax and the extension API could not be stable.

[TOC]

## What is it?

This markdown extension simplifies the definition and use
of new types of block, by defining a common syntax for them.
That is, a common way to specify the type of the block,
the parameters and the content.

The extension deals with markdown parsing.
You just need to define a generator function for your block type.
That function will receive, as function arguments, the attributes and the inner content
and it should generate the proper html.

The plugin also provides several useful examples of block type functions:

- `container`: The default one, a classed div with specifiable attributes and content.
- `figure`: Figures with caption, thumbnail and lightbox like visualization
- `admonition`: Admonitions (quite similar to the [standard extra extension][ExtraAdmonitions])
- `twitter`: Embeded tweets
- `youtube`: Embeded videos from youtube...
- `linkcard`: External link cards (like Facebook and Twitter do, when you post a link)

[ExtraAdmonitions]: https://python-markdown.github.io/extensions/admonition/


While they are quite convenient you can overwrite them all by defining your own function...
Or your could contribute to enhance them. :-)

## General markdown syntax

```markdown
::: mytype param1 key1=value1 "param with many words" key2="value2 with words"
	Indented **content**

	The block ends whenever the indentation stops
This unindented line is not considered part of the block
```

The line starting with `:::` is the _headline_.
It specifies, first, the block type and, then, a set of _values_.
Values can be either single worded or quoted.
Also some values may specify a target parameter with the _key_.

After the _headline_, several lines of indented _content_ may follow.
It stops at the very first line back to the previous indentation.

> By using indentation you don't need a clossing tag,
> but if you miss it, you might place a clossing `:::` at the same
> level of the headline.

A block type may interpret the content as markdown as well.
In such cases, indentation enables nesting.
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

> This is still a draft. Conventions are likely to change until first stable version.

A new block type can be defined just by defining a function:

```python
def mytype(ctx, param1, myflag:bool, param2, param3, param4='default2'):
	...
```

The first parameter, `ctx`, is the context.
You might not define it, but it is useful if you want to receive some context parameters:

- `ctx.parent`: the parent node
- `ctx.content`: the indented part of the block, with the indentation removed
- `ctx.parser`: the markdown parser, can be used to parse the content or any other markdown code
- `ctx.type`: the type of the block
	- If you reuse the same function for different types, this is how you diferentiate them

The rest of the parameters are filled using values from the _head line_.

- First, key values are assigned to function arguments directly by name with the key
- Also flags (explained below) are assigned by name
- Values without key and matching no flag are assigned in order to the unassigned function arguments
- Any keyword-only and positional-only parameters will receive only values from either key or keyless values
- Remaining key and keyless values are assigned to the key (`**kwds`) and positional (`*args`) varidic arguments, if they are specified in the signature

You can use several strategies to generate content:

- Return html string,
- Return `etree` `Element`
- Manipulate `ctx.parent` and return `None`

Function arguments annotated as `bool` (or having True or False as defaults) are considered flags

- Flags are set to True if there is a keyless value matching its name. In the example `myflag`
- Flags are set to False if there is a keyless value matching its name prefixed with `no`. In the example, `nomyflag`


## Usage examples of predefined block types

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

### Container (`customblocks.container`)

If the specified type does not match with any generator, this is the default generator.

Creates `<div>` elements with the type name as class. 
It can be used to structure html with markdown content inside.


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

Will generate:

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

### Admonition (`customblocks.admonition`)

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
</div
```

`title`
: in the title box show that text instead of the 

`*args`
: added as additional classes for the outter div

`**kwds`
: added as attributes for the outter div



### Link cards (`customblocks.example.linkcard`)

Link cards are informative blocks to an external source.
It is similar to the card that popular apps like Facebook, Twitter, Telegram, Slack... do when you post a link.

The generator downloads the target url and extracts social [metadata][SocialMeta]:
Featured image, title, description...

[SocialMeta]: https://css-tricks.com/essential-meta-tags-social-media/

```markdown
::: linkcard http://othersite.com/post/2020-06-01-john-s-work
```

### Youtube (`customblocks.example.youtube`)

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
- Plugins just specify the expected parameters and generate the content
- Get the extension you like and add the feature you miss
- Nest them

We all stand on giants' shoulders so take a look at the [long list](doc/inspiration.md)
of markdown extensions and other software that inspired and influenced this extension.


## Changes

### markdown-customblocks 0.1.0 (2020-06-22)

- First working version
- Support for function based generators
- Default block: container
- Example blocks: admonition, twitter, youtube, figure, linkcard



