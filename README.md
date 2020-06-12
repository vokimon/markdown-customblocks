# 

This plugin offers a uniform syntax of extending markdown with custom blocks.

This way you can easily define your own blocks and how do you want them
to be turn into html code.

It also provides several useful examples of blocks types:

- Figures with caption, thumbnail and lightbox like visualization
- Admonitions
- Embeded tweets
- Embeded videos from youtube, vimeo
- External links cards (like Facebook and Twitter does)

## Common syntax

```
::: type param1 "param with many words" key1=value2 key2="value2 with words"
	Indented content

	The block ends whenever the indentation stops

This is out of the block
```

So you have, first a block marker, by default `:::`,
then a mandatory type, and then positional and keyword parameters.
On the following lines, optionally you can place several indented
lines which are the content.

The block type might interpret the indented content as markdown,
in such case, it could contain an inner block itself, whose
content will be indented an additional level.

## Implementing a block type

### Python function

```python
def mytype(param1, param2, key1, key2='default2'):
	return 
```

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

I want to define what i want (inserting, a tweet a video or whatever)
and then improving how that is made without having to change my documents.

Many plugins addressing the same functionality,
ie. embed tweets, used different syntax.
Changing from one to another to improve the functionality is quite anoying.

And usually the solution seems to define a parametrized
html snippet, that i could improve and have impact
in all my documents.

## Inspiration

This plugin has been inspired by several existing plugins.

### Superfences

[Superfences] plugin is cool because you can extend and define your own type of fences
and then make them do things beyond what fences are suposed to do,
formating code.

I used the idea of having different types of blocks you can define the behaviour
within the same common syntax.

Despite that, that common syntax was not enough to have parameters
and it was imposible to define sub blocks.
Also you are abusing a construct that is suposed to be used for code.

[Superfences]: https://facelessuser.github.io/pymdown-extensions/extensions/superfences/

### Admonitions

[Admonitions] let you divs with classes and nest them if you want.
This is quite useful to structure your html, despite the fact
you can only control html attributes.

I like the idea of using indent to nest admonitions and reparsing the content as markdown
again is a strategy i also took for this plugin.

Sadly, this plugins just renders the output in one way,
a div with a title div.
The only chance you have to change the output is 
by using css and js.

[Admonitions]: https://python-markdown.github.io/extensions/admonition/

### Container

Containers generates more direct html than admonitions (no title).
But instead using indentation, it uses closing tag.
This syntax is hard to follow when you have several nested items.








