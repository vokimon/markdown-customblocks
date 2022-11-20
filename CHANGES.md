# Release history

## markdown-customblocks 1.4.0 (2022-11-20)

- Third party generators can be registered by using project
  metadata's entry points for `markdown.customblocks.generators`
- New block types
    - `wikipedia`: produces a linkcard for a lemma
    - `mastodon`: embed a mastodon post
    - `peertube`: embed a peertube video
- `linkcard`:
    - Keyless values are added as classes to the top level element
    - Extract descriptions from MediaWiki based sites (wikipedia...)
    - Html class `squared` renamed `side`, used to identify side images
    - Configurable CSS variables in the recommended stylesheet
    - Improved image layout in the recommended styleshet
    - Side image turns wide image on small devices
- `vimeo`:
    - Wrapping inside `div.video.vimeo` analog to other video inserts
    - Accepts exceding key and positional parameters like `container`
- `youtube`:
    - Fix: iframe border removed by default

## markdown-customblocks 1.3.1 (2022-11-06)

- Tests passing
- Documentation fixes

## markdown-customblocks 1.3.0 (2022-11-06)

- [New documentation]( https:://vokimon.github.io/markdown-customblocks) based on mkdocs
- New block types:
    - `map`: to embed OSM maps
    - `facebook`: to embed facebook posts (draft: still privacy invasive)
    - `instagram`: to embed instagram posts (draft: still privacy invasive)
- `linkcard`: Links are openened in a new tab/window

## markdown-customblocks 1.2.0 (2022-03-08)

- Figures open the image in a new window
- Figures lightbox visualization (requires some css)
- GDPR friendly embeds:
    - youtube: Use youtube-nocookie.com to avoid youtube cookies
    - vimeo: Use dnt=1 option to avoid vimeo cookies

## markdown-customblocks 1.1.4 (2022-03-05)

- FIX: match trailing spaces after the header. Fixes #6

## markdown-customblocks 1.1.3 (2022-02-22)

- Metadata fix: The license is Affero not MIT

## markdown-customblocks 1.1.2 (2022-02-22)

- FIX: youtube custom classes were not added (PR #05, Alexey Leshchenko @leshchenko1979, thanks!)
- FIX: linkcard: link-card-site-icon class was set twice
- workflows for continuous integration and release

## markdown-customblocks 1.1.1 (2020-08-08)

- documentation fixes

## markdown-customblocks 1.1.0 (2020-08-08)

- `utils.Fetcher`: Helper for catched downloads
- `utils.PageInfo`: Page information retrieval helper
- `utils.E`: Helper to generate HTML using hyperscript idiom
- `utils.Markdown`: Helper to include markdown in hyperscript
- `linkcard`: Example style emulating Wordpress' embedded link
- `linkcard`: Explicit image, description, title...
- `linkcard`: Fix: relative links to images and icons
- `linkcard`: Removed half implemented embedimage flag
- `twitter`: Cache twitter info downloads

## markdown-customblocks 1.0.0 (2020-06-27)

- Register a generator with a string like `'module.submodule:function'`
- Support single quoted values

## markdown-customblocks 0.3.0 (2020-06-27)

- Provide `ctx.config` from `extension_configs.customblocks.config`
- New generators: vimeo, verkami, goteo
- admonition: title should be a `<p>` not a `<div>` for ReST styles to work
- youtube: responsive/fluid sizing
- documented all generators

## markdown-customblocks 0.2.0 (2020-06-25)

- Improve documentation (parameter passing, toc...)
- Provide `ctx.metadata` to access Markdown.Meta (from `extra.meta`, `full_yaml_metadata`... extensions)
- `figure`: link to the image

## markdown-customblocks 0.1.0 (2020-06-23)

- First public version
- Support for function based generators
- Default generator: container
- Example generators: admonition, twitter, youtube, figure, linkcard




