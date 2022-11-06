# Map (`customblocks.generators.map`)

Embeds a map for the specified location.

Currently, [OSM](https://openstreetmap.org) services are used
both for geolocation during generation time and and the embed in browsing time.

## Options

`location`
: The location to display in the map

`marker`/`nomarker` (bool, default True)
: Whether to show or not the location with a marker


## Examples

```markdown
::: map "City of London" nomarker
```
::: map "City of London" nomarker

```markdown
::: map "Lanteira"
```
::: map "Lanteira"

```markdown
::: map "Països catalans"
```
::: map "Països catalans"

```markdown
::: map "Germany"
```
::: map "Germany"



