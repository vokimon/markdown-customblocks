# Road map

## Common infrastructure

- Flags: coerce to bool?
- Annotations: coerce to any type

## Generators

- Linkcard:
	- Mediawiki: Short description and main image: https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts|pageimages&exintro=&explaintext=&titles=Sant%20Joan%20Desp%C3%AD
- Youtube:
    - Take aspect ratio and sizes from Youtube api
    - Use covers https://i.ytimg.com/vi/{code}/hqdefault.jpg
- Twitter
    - Privacy safe mode
- Instagram
- Map:
    - Adding parameters
- peertube
```html
<iframe title="Onion Rice from 1977: The Instruction the Recipe Submitter gives is Priceless!" src="https://tilvids.com/videos/embed/bb6057d2-427b-4c31-9b8c-0a8c7d0a29c9?start=4m51s&amp;stop=5m1s&amp;loop=1&amp;autoplay=1&amp;muted=1" allowfullscreen="" sandbox="allow-same-origin allow-scripts allow-popups" width="560" height="315" frameborder="0"></iframe>
```
- Figure flags:
	- no flag
		- Un modified url
	- local (when remote url)
		- download
		- place it on a given dir
		- set url to local path
	- inline
		- download
		- detect mime type
		- compute base 64
		- set url to data url
	- thumb
		- download
		- generate a thumb
		- place the thumb on thumb dir
		- when combined with 'inline'
			- url to the local path
		- when combined with 'local'
			- link to the image
	- [x] lightbox
	- sized

## Helpers

- Fetcher:
	- configurable cache dir
	- file name too long
	- handle connection errors






