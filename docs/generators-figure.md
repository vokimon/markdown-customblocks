# Figure (`customblocks.generators.figure`)

An image as captioned figure.
The content is taken as caption.
## Options

`url`
: the url to the image

`alt` (keyword only)
: image alt attribute

`title` (keyword only)
: image title attribute

`lightbox` (bool)
: if true, on click, the image will open in a lightbox instead of a new tab which is the default.

`embed` (bool)
: if true inline the image as data url

`local` (bool)
: if true and url is remote, download the image and make it a local one

`thumb` (bool)
: if true generate a reduced size image which expands to a better resolution

`*args`
: additional classes for root `<figure>` tag

`**kwds`
: additional attributes for root `<figure>` tag

## Styling

A [figure css](css/figure.css) is provided.

The `lightbox` mode relies heavily on this css in order to work without using javascript.

## Examples

```markdown
::: figure https://www.w3schools.com/howto/img_lights.jpg alt='an image' nice
    This is a **nice** image.
```

Renders into:

```html
<figure class="nice">
  <a href="https://www.w3schools.com/howto/img_lights.jpg" target="_blank">
    <img src="https://www.w3schools.com/howto/img_lights.jpg" alt="an image" />
  </a>
  <figcaption>
    <p>This is a <b>nice</b> image</p>
  </figcaption>
</figure>
```

::: figure https://www.w3schools.com/howto/img_lights.jpg alt='an image' nice
    This is a **nice** image.

The `lightbox` option generates a slighty different markup:

```markdown
:::figure lightbox https://www.w3schools.com/howto/img_lights.jpg pull-right style="width:40%"
    what a gorgeus image
```

```html
<figure class="lightbox" id="fafb8273-ef7c-47b4-a31f-57d9e0387fc1" style="width:40%">
  <a class="lightbox-background" href="javascript:history.back()"></a>
  <a href="#fafb8273-ef7c-47b4-a31f-57d9e0387fc1">
    <img src="https://www.w3schools.com/howto/img_snow.jpg" />
  </a>
  <figcaption>
    <p>what a gorgeus image</p>
  </figcaption>
</figure>

```

:::figure https://www.w3schools.com/howto/img_lights.jpg lightbox style="width:40%"
    what a gorgeus image


## TODO (you can help!)

- configurable saving place for `local`
- global settings to avoid changing every figure
- figure enumeration ("Figure N:")
- thumbnails
- fetch external images to make them local
- css for placement classes (left, centered, right...)
- improve css

