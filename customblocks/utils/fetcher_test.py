import unittest
import responses
from yamlns import namespace as ns
from pathlib import Path
from .fetcher import Fetcher

class InlineResource_Test(unittest.TestCase):

    from yamlns.testutils import assertNsEqual

    def setUp(self):
        self.cachedir = Path('testcache')
        self.clearCache()
        self.cachedir.mkdir(parents=True)

    def tearDown(self):
        self.clearCache()

    def clearCache(self):
        if not self.cachedir.exists(): return
        for item in reversed(list(self.cachedir.glob('**'))):
            if item.is_dir():
                item.rmdir()
            else:
                item.unlink()

    def assertResponseEqual(self, response, expected):
        result = ns(
            status=response.status_code,
            headers=ns(response.headers),
        )
        if (
            'text' in response.headers['Content-Type']
        ):
            result.update(text=response.text)
        elif 'json' in response.headers['Content-Type']:
            result.update(json=response.json())
        else:
            result.update(content=response.content)

        self.assertNsEqual(result, expected)

    def test_get_real_text(self):
        self.maxDiff = None
        f = Fetcher(cache=self.cachedir)
        response = f.get('https://httpbin.org/base64/Q3VzdG9tQmxvY2tzIHJvY2tzIQ==')
        self.assertResponseEqual(response, """\
            status: 200
            headers:
              Content-Type: text/plain
              Access-Control-Allow-Credentials: 'true'
              Access-Control-Allow-Origin: '*'
              Connection: keep-alive
              Content-Length: '19'
              Content-Type: text/html; charset=utf-8
              Date: {Date}
              Server: gunicorn/19.9.0
            status: 200
            text: CustomBlocks rocks!
        """.format(**response.headers))

    def test_get_real_binary(self):
        self.maxDiff = None
        f = Fetcher(cache=self.cachedir)
        response = f.get('https://dummyimage.com/6x4/f00/f00')
        self.assertResponseEqual(response, """\
        status: 200
        content: !!binary |
          iVBORw0KGgoAAAANSUhEUgAAAAYAAAAEAQMAAACXytwAAAAABlBMVEX/AAD/AAD/OybuAAAACXBI
          WXMAAA7EAAAOxAGVKw4bAAAAC0lEQVQImWNggAAAAAgAAa9T6iIAAAAASUVORK5CYII=
        headers:
          Content-Type: image/png
          Access-Control-Allow-Headers: DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range
          Access-Control-Allow-Methods: GET, POST, OPTIONS
          Access-Control-Allow-Origin: '*'
          Access-Control-Expose-Headers: Content-Length,Content-Range
          Cache-Control: public, max-age=7776000
          Connection: keep-alive
          Content-Length: '107'
          Content-Type: image/png
          Date: {Date} # always change
          Expires: {Expires} # always change
          Last-Modified: {Date} # always change but equal to Date
          Server: nginx
          X-SRCache-Fetch-Status: MISS
          X-SRCache-Store-Status: STORE
        """.format(**response.headers))
 
    @responses.activate
    def test_get_faked(self):
        f = Fetcher(cache=self.cachedir)
        responses.add(
            method='GET',
            url=('http://google.com'),
            status=200,
            body=u"hello world",
            content_type='text/plain',
            )
        response = f.get('http://google.com')
        self.assertResponseEqual(response, """\
        status: 200
        headers:
          Content-Type: text/plain
        text: hello world 
        """)

    def test_url2path_justDomain(self):
        f = Fetcher(cache=self.cachedir)
        self.assertEqual(
            f._url2path('https://www.google.com'),
            self.cachedir / 'https_www.google.com')

    def test_url2path_noSchema(self):
        f = Fetcher(cache=self.cachedir)
        self.assertEqual(
            f._url2path('//www.google.com'),
            self.cachedir / '_www.google.com')

    def test_url2path_justDomain(self):
        f = Fetcher(cache=self.cachedir)
        self.assertEqual(
            f._url2path('https://www.google.com/path/file'),
            self.cachedir / 'https_www.google.com_path_file')


# vim: et ts=4 sw=4
