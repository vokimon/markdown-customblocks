# Instagram (`customblocks.generators.instagram`)

Embeds an [Instagram] post.

You can find the post url by clicking on the three dots
and `Go to post`.
The url usually has the form:

`https://www.instagram.com/p/{post}/`

::: warning
    Generated code will include user tracking from Facebook.
    User browser might, wisely, block the embed.

    A privacy safe version of this plugin is planned for the future.


[Instagram]: https://instagram.com

## Options

`post`
: post id you can retrieve from the url when showing the 

`caption/nocaption`
: (flag, keyword only, default true) if true show the caption and the comments

`*args`
: any keyless argument will turn into additional classes for the outer element

`**kwds`
: any keyword argument will turn into additional attributes for the outer element


## Styling

For styling purposes, upper element can be selected with `blockquote.instagram-media`.


## Examples

```markdown
::: instagram CkYZbEhIgjS nocaption
```

::: instagram CkYZbEhIgjS nocaption

```markdown
::: instagram CkYZbEhIgjS
```

::: instagram CkYZbEhIgjS

```markdown
::: instagram CkYZbEhIgjS nocaption style="width: 100%"
```

::: instagram CkYZbEhIgjS nocaption style="width: 100%"

## TODOs

- Privacy friendly version


