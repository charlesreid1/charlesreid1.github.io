Title: Using Mock API Servers
Date: 2020-03-09 19:00
Category: Python
Tags: http, server, python, mock, mocking, api, flask, web server

[TOC]

# Summary

In a prior post, we covered how to write a mock API server that stored a thread
as a class attribute and used it to run the server in the background by starting
a thread.

However, we neglected to cover how to actually _use_ the mock API server. So here
we include some examples of how you can use the mock API server to write better
tests for components that require interacting with APIs.

# The MockAPIServer Class

Let's start with a recap of the mock API server class. Major features included:

* Inheriting from the base HTTP server class in Python, to take advantage of
  the methods available through it

* Using a singleton design pattern to start and stop the fake API server

Basically we create the server, call `start_serving()`, and that starts the
server on a thread in the background.

Here is the source code:

```python
class MockAPIServer(BaseHTTPRequestHandler):
    _server = None
    _thread = None

    @staticmethod
    def get_addr_port():
        addr = "127.0.0.1"
        port = "9876"
        return addr, port

    @classmethod
    def start_serving(cls):
        # Get the bind address and port
        cls._addr, cls._port = cls.get_addr_port()

        # Create an HTTP server
        cls._server = HTTPServer((cls._addr, cls._port), cls)

        # Create a thread to run the server
        cls._thread = threading.Thread(target=cls._server.serve_forever)

        # Start the server
        cls._thread.start()

    @classmethod
    def stop_serving(cls):
        # Shut down the server
        if cls._server is not None:
            cls._server.shutdown()

        # Let the thread rejoin the worker pool
        cls._thread.join(timeout=10)
        assert not cls._thread.is_alive()

    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.get("content-type"))
        # Enforce rule: JSON only
        if ctype != "application/json":
            self.send_response(400)
            self.end_headers()
            return
        # Convert received JSON to dict
        length = int(self.headers.get("content-length"))
        message = json.loads(self.rfile.read(length))

        # Process the json

        # Send a response
        response = bytes(json.dumps(message), "utf8")
        self._set_headers()
        self.wfile.write(response)

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
```

# A Basic Unit Test with MockAPIServer

Let's make a basic test that uses the `MockAPIServer` class. We'll use
`unittest` for simplicity, other testing frameworks offer similar
functionality.

Before testing our code, we'll need to make sure the API URL is configurable,
sicne we will need to get the mock API server's bind address and port and use
those to instruct our code where to find the API server.

Here is a short example function that we'll test:

**`foobar.py`**:

```python
import urllib.parse

def make_api_call(api_url)
    """
    A simple function that gets an API endpoint
    and returns if no problems raised.
    """
    # Assemble our API call
    endpoint = '/hello/world'
    url = urllib.parse.urljoin(api_url, endpoint)
    params = dict(foo=bar)

    # The basic mock server will just echo our request back
    data = requests.get(url)
    data = resp.json()
    return
```

Now we write a short test for our foobar script:

**`test_foobar.py`**:

```python
from foobar import make_api_call
import unittest

class TestAPICalls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = MockAPIServer()
        cls.app.start_serving()

    def test_api_call():
        addr, port = self.app
        api_url = urllib.parse.urljoin(
            'http://', addr, port
        )
        make_api_cal(api_url)

    @classmethod
    def tearDownClass(cls):
        cls.app.stop_serving()
```

Stay tuned for more complicated examples in the future - we are currently working on
extending this mock API server to mock calls to the Github API.
