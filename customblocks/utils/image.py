from pathlib import Path
import magic
import base64
from PIL import Image

def embed(localfile):
    mime = magic.from_file(localfile, mime=True)
    with Path(localfile).open('rb') as f:
        encoded = base64.b64encode(f.read()).decode('ascii')
        return f"data:{mime};base64,{encoded}"

def thumbnail(localfile, max_width=200, max_height=200):
    localfile = Path(localfile)
    im = Image.open(localfile)
    thumbnailfile = localfile.with_stem(localfile.stem+'.thumb')
    im.thumbnail((max_width, max_height))
    im.save(thumbnailfile)
    return thumbnailfile


# vim: et ts=4 sw=4
