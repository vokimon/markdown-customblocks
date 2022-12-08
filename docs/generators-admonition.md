# Admonition (`customblocks.generators.admonition`)

An admonition is a specially formatted text out of the main flow
which remarks a piece of text.
Often the text is placed in a box and with a side
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

With the style of this documentation, it looks like this:

::: danger
    Do not try to do this at home

## Options

`title`
: in the title box show that text instead of the 

`*args`
: added as additional classes for the outter div

`**kwds`
: added as attributes for the outter div

content:
: reparsed as markdown

::: warning
	If you are migrating from `extra.admonition`,
	be careful since `extra` identifies title because the quotes,
	while `customblocks` will take the first parameter as title and next values as additional classes.
	If you like having the classes before, you should explicit especify `title` key.

		::: danger blinking title="Super danger"
		    Do **not** try to do this at home

## Styling

You can use the [recommended style](css/admonition.css).

Since most themes in generation environments (Pelican, mkdocs...)
have already styles for admonitions, it might work without that css
(just like this documentation) which is using mkdocs defaults.

## Examples

```markdown
::: note
	This is a note

::: note "Custom note title" style="border-width: 3pt; border-radius: 10pt"
	This is a note with customized style and title, and rich **markdown**

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

::: note "Custom note title" style="border-width: 3pt; border-radius: 10pt"
	This is a note with customized style and title, and rich **markdown**

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


