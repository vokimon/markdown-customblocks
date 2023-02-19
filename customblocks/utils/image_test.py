from ..testutils import sandbox_dir
from .image import embed, thumbnail, local
from markdown import test_tools
from PIL import Image, ImageDraw
from pathlib import Path
import magic

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
            self.assertEqual(im.size, (width, height))

    def test_thumbnail(self):
        with sandbox_dir() as sandbox:
            imagefile = 'myimage.jpg'
            self.sample_image(imagefile)

            thumb = thumbnail(imagefile)

            self.assertEqual(thumb, Path('myimage.thumb-200x200.jpg'))
            self.assertImageSize(thumb, width=200, height=113)

    def test_thumbnail__with_target(self):
        with sandbox_dir() as sandbox:
            imagefile = 'myimage.jpg'
            self.sample_image(imagefile)
            target=Path('thumbnails')

            thumb = thumbnail(imagefile, target=target)

            self.assertEqual(thumb, target / Path('myimage.thumb-200x200.jpg'))
            self.assertImageSize(thumb, width=200, height=113)

    def test_thumbnail__with_maxWidth(self):
        with sandbox_dir() as sandbox:
            imagefile = 'myimage.jpg'
            self.sample_image(imagefile)
            target=Path('thumbnails')

            thumb = thumbnail(imagefile, target=target, max_width=100, max_height=120)

            self.assertEqual(thumb, target / Path('myimage.thumb-100x120.jpg'))
            self.assertImageSize(thumb, width=100, height=56)

    def test_thumbnail__with_maxWidth_maxHeight(self):
        with sandbox_dir() as sandbox:
            imagefile = 'myimage.jpg'
            self.sample_image(imagefile)
            target=Path('thumbnails')

            thumb = thumbnail(imagefile, target=target, max_width=100, max_height=50)

            self.assertEqual(thumb, target / Path('myimage.thumb-100x50.jpg'))
            self.assertImageSize(thumb, width=89, height=50)

    def test_thumbnail__with_svg_idempotent(self):
        with sandbox_dir() as sandbox:
            svgfile = Path("drawing.svg")
            svgfile.write_text("<svg />")
            self.assertEqual(thumbnail(svgfile), svgfile)

    remote_webp_sample='https://www.gstatic.com/webp/gallery/5.webp'
    remote_jpeg_sample='https://www.gstatic.com/webp/gallery/5.jpg'
    remote_svg_sample='https://getsamplefiles.com/download/svg/sample-1.svg'

    def test_local(self):
        with sandbox_dir() as sandbox:
            localfile = local(self.remote_jpeg_sample)
            self.assertEqual(localfile, Path('5.jpg'))

    def test_local__usupported_mime__takes_remote_extension(self):
        with sandbox_dir() as sandbox:
            localfile = local(self.remote_webp_sample)
            self.assertEqual(localfile, Path('5.webp'))

    def test_local__svg(self):
        with sandbox_dir() as sandbox:
            localfile = local(self.remote_svg_sample)
            self.assertEqual(localfile, Path('sample-1.svg'))
            self.assertEqual(magic.from_file(localfile, mime=True), 'image/svg+xml')

    def test_local__target_directory(self):
        with sandbox_dir() as sandbox:
            outputdir = sandbox/'outputdir'
            localfile = local(self.remote_webp_sample, target=outputdir)
            self.assertEqual(localfile, outputdir / '5.webp')

    def test_local__saves_content(self):
        with sandbox_dir() as sandbox:
            localfile = local(self.remote_jpeg_sample)
            self.assertEqual(magic.from_file(localfile, mime=True), 'image/jpeg')
            self.assertImageSize(localfile, width=1024, height=752)

    def test_local__with_local_idempotent(self):
        with sandbox_dir() as sandbox:
            already_local = 'this/is/a/file'
            localfile = local(already_local)
            self.assertEqual(localfile, Path(already_local))

# vim: et ts=4 sw=4
