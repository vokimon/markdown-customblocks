import requests
from yamlns import namespace as ns
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import base64
from markdown.util import etree

def container(ctx, *args, **kwds):
	div = etree.SubElement(ctx.parent, 'div')
	div.set('class', '%s' % (' '.join(
		'-'.join(cl.split())
		for cl in [ctx.type]+list(args)
	)))
	for k,v in kwds.items():
		div.set(k,v)
	ctx.parser.parseChunk(div, ctx.content)

def admonition(ctx, title=None, *args, **kwds):
	div = etree.SubElement(ctx.parent, 'div')
	div.set('class', 'admonition %s' % (' '.join(
		'-'.join(cl.split())
		for cl in [ctx.type]+list(args)
	)))
	if title is None:
		title = ctx.type.title()
	titlediv = etree.SubElement(div, 'div')
	titlediv.set('class', 'admonition-title')
	titlediv.text = title
	for k,v in kwds.items():
		div.set(k,v)
	ctx.parser.parseChunk(div, ctx.content)



def figure(ctx, url, *args, **kwds):
	figure = etree.Element('figure')

	title = kwds.pop('title', None)
	alt = kwds.pop('alt', None)

	classes = ' '.join(args)
	if classes:
		figure.set('class', classes)
	for attribute, value in kwds.items():
		figure.set(attribute, value)

	link = etree.SubElement(figure, 'a')
	link.set('href', url)
	img = etree.SubElement(link, 'img')
	img.set('src', url)
	if title:
		img.set('title', title)
	if alt:
		img.set('alt', alt)

	caption = etree.SubElement(figure, 'figcaption')
	content = ctx.parser.parseChunk(caption, ctx.content)
	return figure
	

def linkcard(url, embedimage=False):
	response = requests.get(url)
	soup = BeautifulSoup(response.text, 'html.parser')
	#print(soup)
	def meta(property):
		metatag = soup.find('meta', property=property)
		if not metatag:
			metatag = soup.find('meta', attrs=dict(name=property))
		if not metatag:
			return None
		return metatag.get('content')
	def tag(name):
		tag = soup.find(name)
		if not tag: return None
		return tag.text
	def rellink(rel):
		tag = soup.find('link', rel=rel)
		if not tag: return None
		return tag.get('href')

	parsedurl = urlparse(url)
	siteName = (
		meta('og:site_name') or
		parsedurl.hostname or
		''
	)
	title = (
		meta('og:title') or
		tag('title') or
		siteName
	)
	description = (
		meta('og:description') or 
		meta('twiiter:description') or
		meta('description') or
		''
	)
	websiteicon = (
		rellink('icon') or
		rellink('shortcut icon') or # legacy
		urljoin(url, '/favicon.ico') or
		None
	)
	image = (
		meta('og:image') or
		meta('twitter:image') or
		websiteicon
	)

	if embedimage:
		imageresponse = requests.get(image, stream=True)
		if imageresponse.ok:
			imageBytes = imageresponse.raw.read()
			b64image = base64.b64encode(imageBytes).decode('ascii')
			# TODO: thumb it
			image = 'data:image/jpg;base64,'+ b64image
		
	return f"""\
<div class='linkcard'>
<a href='{url}'><img src='{image}' style="float:right; width=30%" /></a>
<div class='link-sitename'>{siteName.upper()}</div>
<h3><a href='{url}'>{title}</a></h3>
<div class='linkcard-description'>
<p>{description}</p>
</div>
<div class='readmore'><a href='{url}'>Read More</a></div>
</div>
"""

def youtube(id, *, autoplay=False, controls=True, loop=False):
	options = []
	if autoplay: options.append('autoplay=1')
	if not controls: options.append('controls=0')
	if loop: options.append('loop=1')
	options = ('?' + '&'.join(options))  if options else ''
	url = f"https://www.youtube.com/embed/{id}{options}"
	iframe = etree.Element('iframe')
	iframe.set('width', '420')
	iframe.set('height', '315')
	iframe.set('class', 'youtube')
	iframe.set('src', url)
	return iframe

def twitter(user,
	tweet=None,
	theme=None,
	hideimages=False,
	align=None,
	conversation=False,
):
	options = ''
	options += f'&theme={theme}' if theme in ('dark', 'light') else ''
	options += '&cards=hidden' if hideimages else ''
	options += f'&align={align}' if align in ('right', 'center', 'left') else ''
	options += f'&conversation=none' if not conversation else ''

	response = requests.get(f'https://publish.twitter.com/oembed?url=https://twitter.com/{user}/status/{tweet}&dnt=True{options}')
	result = ns(response.json())
	#print("oembed result:", result.dump())
	soup = BeautifulSoup(result.html, 'html.parser')
	return type(u'')(soup.find('blockquote'))


"""
if __name__ == '__main__':
	print(twitter(
		user = 'marcmushu',
		tweet = '1270395360163307530',
		theme = 'dark',
		hideimages = True,
		align = 'right',
		conversation = True,
	))


	print(link('https://www.eldiario.es/economia/Congreso-decreto-ingreso-minimo-vital_0_1036596743.html'))
	print(link('https://twitter.com/marcmushu/status/1270395360163307530'))
	print(link('https://twitter.com/BESTIAFOSCARET1/status/1270668511807930374'))
"""
