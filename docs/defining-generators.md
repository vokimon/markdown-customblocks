# Creating new block types

## Binding to a typename

A block type can be defined just by hooking the **generator** function to the type.

### Python Code

```python
import markdown
md = markdown.Markdown(
    extensions=["customblocks"],
    extension_configs=dict(
        generators=dict(
            customblocks={
                # by direct symbol reference
                'mytype': mypackage.mymodule.mytype,
                # or using import strings (notice the colon)
                'aka_mytype': 'mypackage.mymodule:mytype',
                ...
            }
        )
    ),
)
md.convert(markdowncontent)
```

### Command line config

If you are using `markdown_py` command line,
you can use the `-c config.yaml` option,
and, in `config.yaml`, add:

```yaml
customblocks:
  generators:
    mytype: mypackage.mymodule:mytype
    aka_mytype: mypackage.mymodule:mytype
```

### Pelican

In `pelican.conf`:

```python
MARKDOWN = {
    ...
    'extensions_configs': {
        'customblocks': {
            'generators': {
                # by direct symbol reference
                'mytype': mypackage.mymodule.mytype,
                # or using import strings (notice the colon)
                'aka_mytype': 'mypackage.mymodule:mytype',
            }
        },
    },
}
```

### MkDocs

In `mkdocs.yaml`:

```yaml
markdown_extensions:
  - customblocks:
      generators:
        mytype: mypackage.mymodule:mytype,
        aka_mytype: mypackage.mymodule:mytype
```


### Packaging

If you are distributing the generator as a package,
and want it to be bound to a typename on install,
register an entry point in the `markdown.customblocks.generators` group.

In `setup.py`:

```python
setup(
    ...
    entry_points={
        ...
        markdown.customblocks.generators': [
            'mytype = mypackage.mymodule:mytype',
            'aka_mytype = mypackage.mymodule:mytype',
        ],
    },
    ...
}
```

::: warning
    Conflicting entrypoints from different packages
    are resolved randomly.
    Because of that, be carefull not to register names
    other developers have already used.

    It is ok to redefine an existing block type,
    but let the user to pick it explicitly on config.

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
1. **Explicit keys:** First, `customblocks` binds keyworded values on the headline whose key matches a parameter name in the generator
    (Excluding parameters defined as '[positional-only]')
1. **Flag:** Flags are parameters either annotated as `bool` (like example's `myflag`), or defaulting to `True` or `False`, (like example's `yourflag`).
    They are filled as follows:
    - When a keyless value matches a flag name in the generator (`myflag`), `True` is passed
    - When it matches the flag name prefixed with `no` (`nomyflag`), `False` is passed
1. **Positional:** Keyless values in the headline are assigned one-to-one by position order to the unassigned parameters, (excluding those defined as '[keyword-only]').
1. **Varidics:** If the signature contains key (`**kwds`) or positional (`*args`) varidic variables, any remaining key and keyless values from the headline are assigned to them
1. **Unmatched function parameters:** If they have no default value, will be warned and assigned an empty string.
1. **Unmatched headline parameters:** They will be warned and ignored.

[keyword-only]: https://www.python.org/dev/peps/pep-3102/
[positional-only]: https://www.python.org/dev/peps/pep-0570/

For example, by fedding the followin headline to the signature above:

```markdown
::: mytype noyourflag myflag value1 param1=value3 value4 bad=value5
```

Will set:
```python
param1 = "value3" # This will be matched first since uses a explicit key
yourFlag = False # Flags are set later, from noyourflag
myflag = True  # From myflag value
param2 = "value1" # param1 already filled, next in signature is param2
param3 = "" # No value given, will be warned, and set to ''
param4 = "default2" # this one will get its default value, no warning given
# Also warn about unexpected `bad` key, and ignored
```

## The context object

Regarding the `ctx` parameter, it is the context.
If you don't use it, you can skip it.
But it is useful if you want to receive some context parameters like:

- `ctx.parent`: the parent node
- `ctx.content`: the indented part of the block, with the indentation removed
- `ctx.parser`: the markdown parser, can be used to parse the inner content or any other markdown code
- `ctx.type`: the type of the block
    - If you reuse the same function for different types, this is how you discriminate them
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

def mytype(ctx, image):
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



