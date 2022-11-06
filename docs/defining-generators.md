# Implementing a generator

## Binding to a typename

A block type can be defined just by hooking the **generator** function to the type.

In Python:

```python
import markdown
md = markdown.Markdown(
    extensions=["customblocks"],
    extension_configs=dict(
        customblocks={
            # by direct symbol reference
            'mytype': myparentmodule.mymodule.mytype,
            # or using import strings (notice the colon)
            'aka_mytype': 'myparentmodule.mymodule:mytype',
            ...
        }
    ),
)
md.convert(markdowncontent)
```

In Pelican config:

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

## Parameter mapping

The signature of the generator will determine the attributes taken from the headline.
Say you have a generator with the following signature:

```python
def mytype(ctx, param1, myflag:bool, param2, param3, yourflag=True, param4='default2'):
    ...
```

Function parameters are filled using values parsed from _head line_.
Unlike Python, you can interleave in the headline values with and without keys.
They are resolved as follows:

1. **Context:** The `ctx` parameter is ignored for parameter matching. See bellow on how to use it.
1. **Explicit keys:** Explicit keys in the headline matching function parameters not defined as '[positional only](positional-only)' are matched first.
1. **Flag:** Generator arguments annotated as `bool` (like example's `myflag`), or defaulting to `True` or `False`, (like example's `yourflag`) are considered flags, so:
    - When a keyless value matches a flag name in the generator (`myflag`), `True` is passed
    - When it matches the flag name prefixed with `no` (`nomyflag`), `False` is passed
1. **Positional:** Keyless values in the headline are assigned one-to-one by position order to the unassigned parameters, (excluding those defined as '[keyword-only]').
1. **Varidics:** If the signature contains key (`**kwds`) or positional (`*args`) varidic variables, any remaining key and keyless values from the headline are assigned to them
1. **Unmatched function parameters:** If they have no default value, will be warned and assigned an empty string.
1. **Unmatched headline parameters:** They will be warned and ignored.

[keyword-only]: https://www.python.org/dev/peps/pep-3102/
[positional-only]: https://www.python.org/dev/peps/pep-0570/

## The context object

Regarding the `ctx` parameter, it is the context.
If you don't use it, you can skip it.
But it is useful if you want to receive some context parameters like:

- `ctx.parent`: the parent node
- `ctx.content`: the indented part of the block, with the indentation removed
- `ctx.parser`: the markdown parser, can be used to parse the inner content or any other markdown code
- `ctx.type`: the type of the block
    - If you reuse the same function for different types, this is how you diferentiate them
- `ctx.metadata`: A dictionary with metadata from your metadata plugin.
- `ctx.config`: A dictionary passed from `extension_configs.customblocks.config`

## Producing HTML

A generator can use several strategies to generate content:

- Return an html string (single root node)
- Return a `markdown.etree` `Element` object
- Manipulate `ctx.parent` to add the content and return `None`

In order to construct an ElementTree,
we recommend using the [Hyperscript utility](#hyperscript).
Resulting code will be more compact and readable and
makes proper escaping when injecting values.


## Generator helpers

Common code has been extracted from predefined generators.
If you need this functionality you are encouraged to use them.

- Hyperscript: to generate html
- PageInfo: to extract metadata from a webpage
- Fetcher: to download resources with file based cache


### Hyperscript

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



