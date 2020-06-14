# Custom blocks

A [Python-Markdown] extension to define custom block types using
an uniform, parametrizable and nestable syntax.

[Python-Markdown]: https://python-markdown.github.io/

> **This extension is still in its first development stages.**
> It is a proposal open to debate.
> While the debate goes on, the marks and the extension API could not be stable.

This is a markdown extension to simplify the use and definition
of new types of blocks, by means of a common syntax.
It defines a common way of specify the type of the block,
the parameters and the content and deals with the parsing part.
Block types are defined by a function taking the parameters
and the content and generating the resulting html.

This way is very easy to define your own block types or even
redefine existing ones to suit your needs.

It also provides several useful examples of blocks types:

- Figures with caption, thumbnail and lightbox like visualization
- Admonitions (compatible with the standard extra extension)
- Embeded tweets
- Embeded videos from youtube, vimeo...
- External links cards (like Facebook and Twitter do, when you post a link)

## Common markdown syntax

All blocks can be used using a syntax similar to this:

```markdown
::: mytype param1 "param with many words" key1=value2 key2="value2 with words"
	Indented **content**

	The block ends whenever the indentation stops
This is out of the block
```
This will be interpreted as follows:

- first a block marker, by default `:::`
- the mandatory type, `mytype`,
- then positional and keyword parameters
- optionally, several lines of indented content
- unindented lines are not considered part of the block content

As a block type may interpret the content as markdown,
blocks can be nested by indentation:

```markdown
::: recipe
	# Sweet water
	::: ingredients "4 persons"
		- two spons of suggar
		- a glass of tap water
	Drop the suggar into the glass. Stir.
```

## Implementing a custom block type

### Python function

**This is still a draft**

```python
def mytype(_context, param1, param2, key1, key2='default2'):
	...
```

- You can either return an html string, a etree Element
  or manipulate context.parent and return None
- You have content dedented available at context.content
- You can use context.parser to reparse markdown, for example the content
- Any parameter 

## Usage examples of predefined block types

```markdown
::: youtube HUBNt18RFbo center
::: twitter marcmushu 1270395360163307530
::: twitter marcmushu 1270395360163307530 theme=dark lang=es track=true

::: figure ethernalbulb.jpg left thumb
	The century old bulb still bringing light.

	This make you think you have been mocked.

::: figure ethernalbulb.jpg right

::: figure ethernalbulb.jpg wide

::: figure ethernalbulb.jpg 
```

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


## Inspiration

This extension has been inspired by several existing software and other markdown extensions.

### LaTeX macros

I wanted to implement something i had in LaTeX.
The ability to create repeating content by defining a parametrized code.

LaTeX macros are hard to write and very hard to deal with error,
but they are still a quite cool tool.
So, with Python and Markdown should be cooler.

### Python

Using identation as syntactic element to generate structure
is a pythonic think. Sure.

It also influenced regarding the flexibility of using
keyword and positional parameters.

### Superfences

[Superfences] extension lets you extend and define your own type of fences
and then make them do things beyond what fences are suposed to do,
formating code.

I used the idea of having different types of blocks you can define the behaviour
within the same common syntax.

Despite that, that common syntax was not enough to have parameters
and it was hard to define sub blocks.
Also you are abusing a construct that is suposed to be used for code.

[Superfences]: https://facelessuser.github.io/pymdown-extensions/extensions/superfences/

### Admonitions

[Admonitions] extension lets you define divs with classes and nest them if you want.
This is quite useful to structure your html, despite the fact
you can only control html attributes.

I like the idea of using indent to nest admonitions and reparsing the content as markdown
again is a strategy i also took for this extension.

Sadly, this extension just renders the output in one way,
a div with a title div.
The only chance you have to change the output is 
by using css or js.

[Admonitions]: https://python-markdown.github.io/extensions/admonition/

### Container

[Containers] generates more direct html than admonitions (no title).
But instead using indentation, it uses closing tag.
This syntax is hard to follow when you have several nested items.

[Containers]: https://github.com/markdown-it/markdown-it-container



## Changes

### Unreleased

- First working version
- Support for function based generators
- Default block: container
- Example blocks: admonition, twitter, youtube, figure



