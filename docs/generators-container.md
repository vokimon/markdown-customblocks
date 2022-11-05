# Container (`customblocks.generators.container`)

This generator is the default one used when a type has no generator associated.

It generates a `<div>` element
with the typename as class.
It also appends any positional parameter as additional classes
and keyword arguments as attributes.
The content is reinterpreted as markdown.

This is quite useful to create a 'div' structure
in the html document.

### Options

`*args`
: added as additional classes for the outter div

`**kwds`
: added as attributes for the outter div

content:
: reparsed as markdown

### Example

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

