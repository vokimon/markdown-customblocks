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

Customblocks is an extension for [Python-Markdown]
that settles a **common markup** for **parametrizable and nestable components**
whose output can be **redefined** by means of a simple Python function.

Many off-the-shelf components are provided such as
div-containers, admonitions, figures, link cards, maps...
and some embeded widgets from common sites (youtube, vimeo, twitter, facebook, instagram, goteo, verkami...)

It also includes convenience tools to ease component definition:
hyperscript html generation, cached page fetching and metadata page extraction.

[Python-Markdown]: https://python-markdown.github.io/


## Installation and setup

To install:

```bash
$ pip install markdown-customblocks
```

And then activate it as any other Markdown extension.

From command line:

```bash
$ markdown -x customblocks ...
```

In Python code:

```python
import markdown
md = markdown.Markdown(extensions=["customblocks"])
md.convert(markdowncontent)
```

In [Pelican](https://blog.getpelican.com/) config:

```python
MARKDOWN = {
    'extensions': [
        'customblocks',
    ],
}
```

For [MkDocs](https://www.mkdocs.org), add this to `mkdocs.yml`:

```yaml
markdown_extensions:
  - customblocks
```

If you need to specify additional parameters for the extension,
refer to the documentation of your generator.


## Basic usage

Customblocks extension parses markup structures like this one:

```markdown
::: mytype "value 1" param2=value2
    Indented content
```
Then, the extension delegates HTML generation to a Python function (_generator_)
which is bound to the type name, `mytype` in the example.

The extension provides many predefined generators
and you might define your own for new types or
redefine existing ones to suit your needs.

If no generator is bound to the type name,
the div-container generator is used as fallback,
generating this:

```html
<div class="mytype value-1" param2="value2">
   <p>Indented code</p>
</div>
```


But we could bind `mytype` to the following generator:

```python
def mygenerator(ctx, param1, param2):
    return f"""<div attrib1="{param1}" attrib2="{param2}">{ctx.content}</div>"""
```

That would generate this HTML:

```html
<div attrib1="value 1" attrib2="value2">Indented Content</div>
```

::: warning
    Notice that this is a silly example.
    It will work for simple params and text content,
    but it does not escape them properly.
    The [hyperscript tool](#hyperscript-generation) can be used to make this painless.

## Built-in generators

The extension provides the following predefined generators:

- `container`: A div element with arbitrary classes, attributes and content. This is the default when no type matches.
- `admonition`: Admonitions, boxes for notes, warnings... (quite similar to the [standard extra extension][ExtraAdmonitions]).
  It is bound to types `note`,  `info`, `error`, `warning`....
- `figure`: Full featured figures with captions, lightbox...
- `map`: Maps from OpenStreetMaps.org
- `linkcard`: External link cards (like Facebook and Twitter do, when you post a link)
- `youtube`: Embeded videos from youtube...
- `vimeo`: Embeded videos from vimeo...
- `twitter`: Embeded tweets
- `facebook`: Embeded post from facebook...
- `instagram`: Embeded post from instagram...
- `verkami`: Fund raising project widget in [Verkami]
- `goteo`: Fund raising project widget in [Goteo]

[ExtraAdmonitions]: https://python-markdown.github.io/extensions/admonition/

If you wonder why this extension exists and
why the design choices were taken like this,
read the [motivation](motivation.md).
We all stand on giants' shoulders so take a look at the [long list](inspiration.md)
of markdown extensions and other software that inspired and influenced ideas for this extension.
Kudos for all of them.


## General markup syntax

This is a more complete example of markup:

```markdown
::: mytype param1 key1=value1 "other param" key2='value2 with words' flag1 noflag2
    Indented **content**

    The block ends whenever the indentation stops
This unindented line is not considered part of the block
```

**The headline:**
The line starting with `:::` is the _headline_.
It specifies, first, the block type (`mytype`) followed by a set of _values_
that will be passed to the generator as parameters.


**Block type:**
The type is used to select the generator function.
If there is no generator bound to the type, the div-container generator, will be used by default.

**Quotes:**
Muti-word values can be passed by using either single or double quotes.
You can skip quotes if your value is single worded.

**Explicit keywords:**
Also some values may target an explicit parameter with a _key_.
This works as follows:
from the available block parameters, values with a key are set first,
then the remaining unset parameters are filled by position.

**Flags (bools):**
Boolean parameters (flags) can be set by just adding a value with the name of the flag, like `flag1` in the example.
And they can be unset by adding the name with a `no` prefix, like `noflag2` in the example.

**Content:**
After the _headline_, several lines of indented _content_ may follow.
The content ends with the very first non-emtpy line back on the previous indentation.

Indentation is removed from the content for the generator to process it.
A block type may choose to interpret this content as markdown as well.
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
	A closing `:::` tag is optional.
	For most cases, indentation should be enough, visually, and functionally.
	Seldomly, it is necessary like in the following markdown to
	split the mealphoto content from a code block which is also indented.

	    ::: mealphoto sweetwater.jpg
		    Looks gorgeus!
	    :::
		    This is a code block by indentation


## Further reading

- [Full documentation](https://vokimon.github.io/markdown-customblocks)
- [Code](https://github.com/vokimon/markdown-customblocks)
- [Release History](CHANGES.md)
- [Road map](TODO.md)

