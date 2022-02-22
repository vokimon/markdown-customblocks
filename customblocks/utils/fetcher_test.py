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
        for item in list(self.cachedir.glob('**/*'))[::-1]:
            item.unlink()
        if self.cachedir.exists():
            self.cachedir.rmdir()

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
              Access-Control-Allow-Credentials: 'true'
              Access-Control-Allow-Origin: '*'
              Connection: keep-alive
              Content-Length: '19'
              Content-Type: text/html; charset=utf-8
              Date: {Date}
              Server: gunicorn/19.9.0
            status_code: 200
            text: CustomBlocks rocks!
            encoding: utf-8
        """.format(**response.headers))

    @unittest.skipIf(offline, 'this test requires network connection')
    def test_get_real_binary(self):
        self.maxDiff = None
        f = Fetcher(cache=self.cachedir)
        response = f.get('https://dummyimage.com/6x4/f00/f00')
        response.headers.setdefault('Age', '0')
        self.assertResponseEqual(response, """\
        url: https://dummyimage.com/6x4/f00/f00
        status_code: 200
        content: !!binary |
          iVBORw0KGgoAAAANSUhEUgAAAAYAAAAEAQMAAACXytwAAAAABlBMVEX/AAD/AAD/OybuAAAACXBI
          WXMAAA7EAAAOxAGVKw4bAAAAC0lEQVQImWNggAAAAAgAAa9T6iIAAAAASUVORK5CYII=
        headers:
          Accept-Ranges: bytes
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
          Last-Modified: {Last-Modified} # always change but equal to Date
          Server: cloudflAre
          Referrer-Policy: no-referrer, strict-origin-when-cross-origin
          Age: '{Age}'
          CF-Cache-Status: HIT
          CF-RAY: {CF-RAY}
          Expect-CT: max-age=604800, report-uri="https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct"
          NEL: '{{"success_fraction":0,"report_to":"cf-nel","max_age":604800}}'
          Report-To: '{Report-To}'
          Server: cloudflare
          Vary: Accept-Encoding
          alt-svc: h3=":443"; ma=86400, h3-29=":443"; ma=86400
          X-Content-Type-Options: nosniff
          X-Download-Options: noopen
          X-Frame-Options: SAMEORIGIN
          X-Powered-By: WordOps
          X-Xss-Protection: 1; mode=block
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
            encoding: ISO-8859-1
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

    def test_url2path_withPath(self):
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
            url: http://mysite.com/path/page
            status_code: 200
            headers:
              Content-Type: text/plain
            text: hello world
            encoding: ISO-8859-1
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
            url: http://mysite.com/path/page
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
            json=dict(data='value'),
            )
        response = requests.get('http://mysite.com/path/page')
        self.assertNsEqual(f._response2namespace(response), """\
            url: http://mysite.com/path/page
            status_code: 200
            headers:
              Content-Type: application/json
            json:
              data: value
        """)

    def test_namespace2response_text(self):
        namespace = ns.loads("""\
            url: http://mysite.com/path/page
            status_code: 200
            headers:
              Content-Type: text/plain
            text: hello world
            encoding: ISO-8859-1
        """)
        response = Fetcher._namespace2response(namespace)
        self.assertResponseEqual(response, """\
            url: http://mysite.com/path/page
            status_code: 200
            headers:
              Content-Type: text/plain
            text: hello world
            encoding: ISO-8859-1
        """)

    def test_namespace2response_binary(self):
        namespace = ns.loads("""\
            url: http://mysite.com/path/page
            status_code: 200
            headers:
              Content-Type: image/png
            content: !!binary |
                iVBORw0KGgoAAAANSUhEUgAAAAYAAAAEAQMAAACXytwAAAAABlBMVEX/AAD/AAD/OybuAAAACXBI
                WXMAAA7EAAAOxAGVKw4bAAAAC0lEQVQImWNggAAAAAgAAa9T6iIAAAAASUVORK5CYII=
        """)
        response = Fetcher._namespace2response(namespace)
        self.assertResponseEqual(response, """\
            url: http://mysite.com/path/page
            status_code: 200
            headers:
              Content-Type: image/png
            content: !!binary |
                iVBORw0KGgoAAAANSUhEUgAAAAYAAAAEAQMAAACXytwAAAAABlBMVEX/AAD/AAD/OybuAAAACXBI
                WXMAAA7EAAAOxAGVKw4bAAAAC0lEQVQImWNggAAAAAgAAa9T6iIAAAAASUVORK5CYII=
        """)

    def test_namespace2response_json(self):
        namespace = ns.loads("""\
            url: http://mysite.com/path/page
            status_code: 200
            headers:
              Content-Type: application/json
            json:
              data: value
        """)
        response = Fetcher._namespace2response(namespace)
        self.assertResponseEqual(response, """\
            url: http://mysite.com/path/page
            status_code: 200
            headers:
              Content-Type: application/json
            json:
              data: value
        """)
 
    @responses.activate
    def test_get_storesCache(self):
        f = Fetcher(cache=self.cachedir)
        responses.add(
            method='GET',
            url='http://google.com',
            status=200,
            body=u"hello world",
            )
        response = f.get('http://google.com')
        cacheFile = f._url2path('http://google.com')
        cached = cacheFile.read_text(encoding='utf8')
        self.assertNsEqual(cached, """\
            url: http://google.com/
            status_code: 200
            headers:
              Content-Type: text/plain
            text: hello world
            encoding: ISO-8859-1
        """)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_get_unicode(self):
        f = Fetcher(cache=self.cachedir)
        responses.add(
            method='GET',
            url='http://google.com',
            status=200,
            body=u"La caña",
        )
        response = f.get('http://google.com')
        cacheFile = f._url2path('http://google.com')
        cached = ns.load(str(cacheFile))
        self.assertNsEqual(cached, """\
            url: http://google.com/
            status_code: 200
            headers:
              Content-Type: text/plain; charset=utf-8
            text: La caña
            encoding: utf-8
        """)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_get_usesCache(self):
        f = Fetcher(cache=self.cachedir)
        responses.add(
            method='GET',
            url='http://google.com',
            status=200,
            body=u"hello world",
            content_type='text/plain',
            )
        cacheFile = f._url2path('http://google.com')
        cacheFile.write_text(
            encoding='utf8',
            data="""\
                url: http://google.com/
                status_code: 200
                headers:
                  Content-Type: text/plain
                text: A DIFFERENT TEXT
                encoding: ISO-8859-1
            """,
        )
        response = f.get('http://google.com')
        self.assertResponseEqual(response, """\
            url: http://google.com/
            status_code: 200
            headers:
              Content-Type: text/plain
            text: A DIFFERENT TEXT
            encoding: ISO-8859-1
        """)
        self.assertEqual(len(responses.calls), 0)

    @responses.activate
    def test_remove(self):
        f = Fetcher(cache=self.cachedir)
        responses.add(
            method='GET',
            url='http://google.com',
            status=200,
            body=u"hello world",
            content_type='text/plain',
            )
        cacheFile = f._url2path('http://google.com')
        cacheFile.write_text(
            encoding='utf8',
            data="""\
                url: http://google.com/
                status_code: 200
                headers:
                  Content-Type: text/plain
                text: A DIFFERENT TEXT
                encoding: ISO-8859-1
            """,
        )
        f.remove('http://google.com')
        response = f.get('http://google.com')
        self.assertResponseEqual(response, """\
            url: http://google.com/
            status_code: 200
            headers:
              Content-Type: text/plain
            text: hello world
            encoding: ISO-8859-1
        """)
        self.assertEqual(len(responses.calls), 1)

    def test_clear(self):
        f = Fetcher(cache=self.cachedir)
        f._url2path('http://google.com').touch()
        f._url2path('http://amazon.com').touch()
        f.clear()
        self.assertEqual(len(list(self.cachedir.glob('*'))), 0)
        self.assertFalse(self.cachedir.exists())

    def test_clear_missing(self):
        f = Fetcher(cache=self.cachedir)
        self.cachedir.rmdir()
        f.clear()
        self.assertEqual(len(list(self.cachedir.glob('*'))), 0)

    def test_init_createsDirIfMissing(self):
        self.cachedir.rmdir()
        f = Fetcher(cache=self.cachedir)
        self.assertTrue(self.cachedir.exists())

    def test_init_takesStrings(self):
        f = Fetcher(cache=str(self.cachedir))
        self.assertEqual(
            f._url2path('https://www.google.com'),
            self.cachedir / 'https_www.google.com')

    @responses.activate
    def test_get_doNotCatchFailures(self):
        f = Fetcher(cache=self.cachedir)
        responses.add(
            method='GET',
            url='http://google.com',
            status=400,
            body=u"bad request",
            content_type='text/plain',
            )
        responses.add(
            method='GET',
            url='http://google.com',
            status=200,
            body=u"hello world",
            content_type='text/plain',
            )
        response = f.get('http://google.com')
        response = f.get('http://google.com')
        self.assertResponseEqual(response, """\
            url: http://google.com/
            status_code: 200
            headers:
              Content-Type: text/plain
            text: hello world
            encoding: ISO-8859-1
        """)
        self.assertEqual(len(responses.calls), 2)



# vim: et ts=4 sw=4
