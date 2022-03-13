# Inspiration

This extension has been inspired by several existing software and other markdown extensions.

## LaTeX macros

I wanted to implement something i had in LaTeX.
The ability to create repeating content by defining a parametrized code.

LaTeX macros are hard to write and very hard to deal with errors,
but they are still a quite cool tool once you have them working.
So, having that with Python and Markdown should be simpler and cooler.

## Python

Using identation as syntactic element to generate structure
is a pythonic think. Sure.
Having both keyword and positional parameters is also a Pythonic thing,
although this extension is more flexible in the order of providing them.


## Superfences

[Superfences] extension lets you extend and define your own type of fences
and then make them do things beyond what fences are suposed to do,
formating code.

I used the idea of having different types of blocks you can define the behaviour
within the same common syntax.

Despite that, that common syntax was not enough to have parameters
and it was hard to define sub blocks.
Also you are abusing a construct that is suposed to be used for code.

[Superfences]: https://facelessuser.github.io/pymdown-extensions/extensions/superfences/

## Admonitions

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

## Container

[Containers] generates more direct html than admonitions (no title).
But instead using indentation, it uses closing tag.
This syntax is hard to follow when you have several nested items.

[Containers]: https://github.com/markdown-it/markdown-it-container

## Other extensions

- [Structured Markdown](https://pypi.org/project/structured-markdown/)

## Youtube extensions

- [Video-to-Markdown](https://github.com/marcomontalbano/video-to-markdown)



