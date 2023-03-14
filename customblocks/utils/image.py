from pathlib import Path
from urllib.parse import urlparse
import magic
import base64
import mimetypes
from typing import Union
from PIL import Image, UnidentifiedImageError
from .fetcher import Fetcher

def embed(localfile: Union[Path, str]) -> str:
    """
    Turns a localfile into a base64 encoded data url to embed
    """
    localfile=Path(localfile)
    mime = magic.from_file(localfile, mime=True)
    with localfile.open('rb') as f:
        encoded = base64.b64encode(f.read()).decode('ascii')
        return f"data:{mime};base64,{encoded}"

def thumbnail(localfile: Union[Path, str], max_width:int=200, max_height:int=200, target:Path=Path()) -> Path:
    """
    Generates a new image file with limited size to be used
    as thumbnail.
    """
    localfile = Path(localfile)
    try:
        im = Image.open(localfile)
    except UnidentifiedImageError as e:
        return localfile
    target.mkdir(parents=True, exist_ok=True)
    thumbnailfile = target / (localfile.stem + f'.thumb-{max_width}x{max_height}' + localfile.suffix)
    im.thumbnail((max_width, max_height))
    im.save(thumbnailfile)
    return thumbnailfile

def local(url:str, target: Union[Path,str]=Path()):
    """
    Generates a local file based on the remote file content.
    """
    parsedurl = urlparse(url)
    target = Path(target)
    if not parsedurl.netloc:
        return Path(url) # Local file
    response = Fetcher('testcache').get(url)
    remotepath = Path(parsedurl.path)
    mime = response.headers.get('Content-Type', None)
    extension = None
    if mime:
        extension = mimetypes.guess_extension(mime)
    if not extension:
        extension = remotepath.suffix
    if not extension: # TODO: Untested
        extension = '.dat'
    localfile = target / (remotepath.stem+extension)
    localfile.parent.mkdir(parents=True, exist_ok=True)
    localfile.write_bytes(response.content)
    return localfile


# vim: et ts=4 sw=4
