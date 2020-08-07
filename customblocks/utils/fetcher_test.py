import base64
import requests
import responses
import unittest
from pathlib import Path
from yamlns import namespace as ns
from .fetcher import Fetcher

offline=False

class Fetcher_Test(unittest.TestCase):

    from yamlns.testutils import assertNsEqual

    def setUp(self):
        self.cachedir = Path('testcache')
        self.clearCache()
        self.cachedir.mkdir(parents=True)

    def tearDown(self):
        self.clearCache()

    def clearCache(self):
        for item in reversed(list(self.cachedir.glob('**'))):
            if item.is_dir():
                item.rmdir()
            else:
                item.unlink()

    def assertResponseEqual(self, response, expected):
        result = Fetcher._response2namespace(response)
        self.assertNsEqual(result, expected)

    @unittest.skipIf(offline, 'this test requires network connection')
    def test_get_real_text(self):
        self.maxDiff = None
        f = Fetcher(cache=self.cachedir)
        response = f.get('https://httpbin.org/base64/Q3VzdG9tQmxvY2tzIHJvY2tzIQ==')
        self.assertResponseEqual(response, """\
            url: 'https://httpbin.org/base64/Q3VzdG9tQmxvY2tzIHJvY2tzIQ=='
            headers:
              Content-Type: text/plain
              Access-Control-Allow-Credentials: 'true'
              Access-Control-Allow-Origin: '*'
              Connection: keep-alive
              Content-Length: '19'
              Content-Type: text/html; charset=utf-8
              Date: {Date}
              Server: gunicorn/19.9.0
            status_code: 200
            text: CustomBlocks rocks!
        """.format(**response.headers))

    @unittest.skipIf(offline, 'this test requires network connection')
    def test_get_real_binary(self):
        self.maxDiff = None
        f = Fetcher(cache=self.cachedir)
        response = f.get('https://dummyimage.com/6x4/f00/f00')
        self.assertResponseEqual(response, """\
        url: https://dummyimage.com/6x4/f00/f00
        status_code: 200
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
            url='http://google.com',
            status=200,
            body=u"hello world",
            content_type='text/plain',
            )
        response = f.get('http://google.com')
        self.assertResponseEqual(response, """\
            url: http://google.com/
            status_code: 200
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

    @responses.activate
    def test_response2namespace_text(self):
        f = Fetcher(cache=self.cachedir)
        responses.add(
            method='GET',
            url='http://mysite.com/path/page',
            status=200,
            body=u"hello world",
            content_type='text/plain',
            )
        response = requests.get('http://mysite.com/path/page')
        self.assertNsEqual(f._response2namespace(response), """\
            url: http://mysite.com/path/page # this changes
            status_code: 200
            headers:
              Content-Type: text/plain
            text: hello world
        """)

    @responses.activate
    def test_response2namespace_binary(self):
        image = base64.b64decode(
            """iVBORw0KGgoAAAANSUhEUgAAAAYAAAAEAQMAAACXytwAAAAABlBMVEX/AAD/AAD/OybuAAAACXBI"""
            """WXMAAA7EAAAOxAGVKw4bAAAAC0lEQVQImWNggAAAAAgAAa9T6iIAAAAASUVORK5CYII="""
        )
        f = Fetcher(cache=self.cachedir)
        responses.add(
            method='GET',
            url='http://mysite.com/path/page',
            status=200,
            body=image,
            content_type='image/png',
            )
        response = requests.get('http://mysite.com/path/page')
        self.assertNsEqual(f._response2namespace(response), """\
            url: http://mysite.com/path/page # this changes
            status_code: 200
            headers:
              Content-Type: image/png
            content: !!binary |
                iVBORw0KGgoAAAANSUhEUgAAAAYAAAAEAQMAAACXytwAAAAABlBMVEX/AAD/AAD/OybuAAAACXBI
                WXMAAA7EAAAOxAGVKw4bAAAAC0lEQVQImWNggAAAAAgAAa9T6iIAAAAASUVORK5CYII=
        """)

    @responses.activate
    def test_response2namespace_json(self):
        f = Fetcher(cache=self.cachedir)
        responses.add(
            method='GET',
            url='http://mysite.com/path/page',
            status=200,
            body='{"data":"value"}',
            content_type='application/json',
            )
        response = requests.get('http://mysite.com/path/page')
        self.assertNsEqual(f._response2namespace(response), """\
            url: http://mysite.com/path/page # this changes
            status_code: 200
            headers:
              Content-Type: application/json
            json:
              data: value
        """)


# vim: et ts=4 sw=4
