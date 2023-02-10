# Road map

## Common infrastructure

- Flags: coerce to bool?
- Annotations: coerce to any type

## Generators

- Youtube:
    - Take aspect ratio and sizes from Youtube api
    - Use covers https://i.ytimg.com/vi/{code}/hqdefault.jpg
- Twitter
    - Privacy safe mode
- Instagram
- Map:
    - Adding parameters
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






