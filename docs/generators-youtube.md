# Youtube (`customblocks.generators.youtube`)

This generator generates an embeded youtube video.

## Example

```markdown
::: youtube HUBNt18RFbo
```

```html
<div class="videowrapper youtube">
  <iframe src="https://www.youtube-nocookie.com/embed/HUBNt18RFbo"></iframe>
</div>
```

::: youtube HUBNt18RFbo

::: warning
	Even though, youtube-nocookie.com is suposed to avoid tracing cookies,
	google sets some tracing cookies from one of the included javascript files.

## Options

`autoplay` (flag, default False)
: starts the video as soon as it is loaded

`loop` (flag, default False)
: restart again the video once finished

`controls` (flag, default True)
: show the controls

`*args`
: added as additional class for the outter div

`**kwds`
: added as attributes for the outter div

Indented content is ignored.

Or you could set `youtube_inlineFluidStyle` config to `True`
and the style will be added inline to every video.

## Styling

The component can be selected as `div.videowrapper.youtube`.

Note that the `videowrapper` class is common with other video embeds
and has a [recommended css](../css/videowrapper.css).




