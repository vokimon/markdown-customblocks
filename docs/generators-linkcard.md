# Link card (`customblocks.generators.linkcard`)

A link card is a informative box about an external source.
It is similar to the card that popular apps like
Wordpress, Facebook, Twitter, Telegram, Slack...
generate when you embed/post a link.

In order to build the box,
the generator downloads the target url and extracts social [metadata][SocialMeta]:
Featured image, title, description...
The download page is cached so that first non-failing download will avoid further downloads.

[SocialMeta]: https://css-tricks.com/essential-meta-tags-social-media/

```markdown
::: linkcard https://css-tricks.com/essential-meta-tags-social-media/
```

::: linkcard https://css-tricks.com/essential-meta-tags-social-media/

This generator uses the `fetcher` helper.
Thus, the first fetch will be cached for later generations.

## Options


`url`
: The url to embed as card

`wideimage` (bool, default True)
: Whether the featured image will be shown wide, if not, a small thumb will be shown

`*args`
: any extra positional value will be added as class to the top level element

Additionally you can provide the following keyword parameters
to override information extracted from the url:

- `image`: the image heading the card
- `title`: the caption
- `description`: the text describing the link (though using content is recommended)
- `siteurl`: a link to the main site
- `sitename`: the name of the main site
- `siteicon`: the site icon

Content, if provided, will be used as description instead of the summary in the page.


## Styling

The above example uses [this css](css/linkcard.css).

## Examples

```markdown
::: linkcard nowideimage https://css-tricks.com/essential-meta-tags-social-media/
```

::: linkcard nowideimage https://css-tricks.com/essential-meta-tags-social-media/

## TODO

- Global default options
- Improve the css layout
- Image placeholder while loading
- Display author metadata
- Support Mediawiki excerpts

