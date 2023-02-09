from ..testutils import sandbox_dir
from .image import embed, thumbnail
from markdown import test_tools
from PIL import Image, ImageDraw
from pathlib import Path


class Image_Test(test_tools.TestCase):

    def test_embed(self):
        with sandbox_dir() as sandbox:
            Path("drawing.svg").write_text("<svg />")
            self.assertEqual(embed("drawing.svg"),
                'data:image/svg+xml;base64,PHN2ZyAvPg=='
            )

    def sample_image(self, imagefile):
        with Image.new(mode='RGB', size=(1920,1080), color="pink") as im:
            draw = ImageDraw.Draw(im)
            draw.ellipse([(0,0),(1920,1000)], fill=(0xFF,0xFF,0))
            im.save(imagefile, 'JPEG')

    def assertImageSize(self, imagefile, width, height):
        with Image.open(imagefile) as im:
            self.assertEqual(im.size, (200, 113))

    def test_thumbnail(self):
        with sandbox_dir() as sandbox:
            imagefile = 'myimage.jpg'
            self.sample_image(imagefile)

            thumb = thumbnail(imagefile)

            self.assertEqual(str(thumb), 'myimage.thumb.jpg')
            self.assertImageSize(thumb, width=200, height=113)


# vim: et ts=4 sw=4
