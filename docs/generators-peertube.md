# Peertube (`customblocks.generators.peertube`)

[Peertube](https://joinpeertube.org/)
is a decentralized alternative to video sites like youtube.


Videos are uploaded to a federated instance (host),
and then distributed to the others so that download can be done 
downloaded using all instances.

## Options

`instance`
: The domain hosting the video

`uuid`
: uuid in the embed url (Not the regular one!!)

`start` (keyword only, format as `3m23s`)
: starting playback point

`stop` (keyword only, format as `3m23s`)
: stopping playback point

`autoplay/noautoplay` (flag, default False)
: play as the video is available

`loop/noloop` (flag, default False)
: loop or not the video after end

`title/notitle` (flag, default True)
: show or hide the video title overlay

`controls/nocontrols` (flag, default True)
: show or hide the playback controls

`muted` (flag, default False)
: mute the video on loading

`p2p/nop2p` (flag, default True)
: use p2p to download the video

`*args`
: excess

## Styling

The component can be selected as `div.videowrapper.peertube`.

Note that the `videowrapper` class is common with other video embeds
and has a [recommended css](css/videowrapper.css).


## Examples

```markdown
::: peertube tilvids.com bb6057d2-427b-4c31-9b8c-0a8c7d0a29c9  loop autoplay
```

::: peertube tilvids.com bb6057d2-427b-4c31-9b8c-0a8c7d0a29c9  loop autoplay

```markdown
::: peertube video.blender.org  e8351755-4cf7-43b0-87b8-5e037db106ba start=1m stop=1m5s autoplay
```

::: peertube video.blender.org  e8351755-4cf7-43b0-87b8-5e037db106ba start=1m stop=1m5s autoplay


## TODO

- Infer UUID from base64 ids
- Infer UUID and pod from video url


