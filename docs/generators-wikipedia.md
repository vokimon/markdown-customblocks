# Wikipedia (`customblocks.generates.wikipedia`)

Generates a [linkcard](../generators-linkcard) from from a lemma for the Wikipedia.

The difference with a `linkcard` is that
instead of the full url to the article
you just must provide the lemma/title.

## Options

`lemma`
: The lemma for the article

`lang` (keyword only, default `en`)
: Language (or wikipedia instance)

`*args`
: extra positional arguments are appended as classes
for the top level element

`**kwds`
: any extra keyword argument is used like in a `linkcard`


## Examples

```markdown
::: wikipedia "Sant Joan Despí"
```

::: wikipedia "Sant Joan Despí"

```markdown
::: wikipedia "Sant Joan Despí" lang=ca
```

::: wikipedia "Sant Joan Despí" lang=ca

```markdown
::: wikipedia "Sant Joan Despí" wideimage
```

::: wikipedia "Sant Joan Despí" wideimage


## Styling

Generated Wikipedia cards are just linkcards with
an additional `wikipedia` class
to target them specifically, if you need to.
Refer to linkcard [styling section](/markdown-customblocks/generators-linkcard/#styling).
Examples above use the stylesheet referred there.

