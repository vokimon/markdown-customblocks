# Vimeo (`customblocks.generators.vimeo`)

This generator generates an embeded vimeo video.

## Example

```markdown
::: vimeo 139579122 
```

::: vimeo 139579122

## Options

`autoplay/noautoplay` (flag, default False)
: starts the video as soon as it is loaded

`loop/noloop` (flag, default False)
: restart again the video once finished

`bylabel/nobylabel` (flag, default True)
: Shows the video author's name

`portrait/noportrait` (flag, default False)
: Shows the video author's avatar

`*args`
: added as additional class for the outter div

`**kwds`
: added as additional attributes for the outter div

Content is ignored.


