Title: Creating Mock API Servers
Date: 2020-02-26 22:00
Category: Python
Tags: http, server, python, mock, mocking, api, flask, web server

[TOC]

# Overview

In this post we discuss a way of mocking an API server during tests.
This technique will let you create a fake API server that can respond
to API calls however you want.

The technique is twofold:

* First, we create a mock API handler that extends `BaseHTTPRequestHandler`, which is the built-in HTTP server
  class in Python. We can extend the server class to control how it responds to requests - to implement a
  method to respond to POST requests, we implement a `do_POST()` method, to respond to GET requests
  we implement a `do_GET()` method, and so on. (In the example below, we restrict the types of requests
  to JSON content only.)

* Second, we use the Singleton design pattern, by implementing 
  two class methods, `start_serving()` and `stop_serving()`, that
  we can call before and after our tests to set up and tear down
  the fake API server. This method will take care of starting the
  HTTP server on a separate thread, so that it does not block 
  execution.

# Mock API Server Class

Let's start with the mock server class. This is going to extend the
`BaseHTTPRequestHandler` class from the `http.server` module, and
extend it.

We implement a stub method for the POST response behavior; this is the
only type of request that our mock API server will respond to.

We also have two stub class methods to start and stop the server.

```python
class MockAPIServer(BaseHTTPRequestHandler):
    _server = None
    _thread = None

    def do_POST(self):
        pass

    @classmethod
    def start_serving(cls):
        pass

    @classmethod
    def stop_serving(cls):
        pass
```

## Start/Stop Serving

We start with the two class methods to start and stop the server.

### Getting Bind Address/Port

Define another static method to get the address to bind to, and the
port to use; in this case we'll hard code values, but this function
could also find unused networking ports, etc.

```python
    @staticmethod
    def get_addr_port():
        addr = "127.0.0.1"
        port = "9876"
        return addr, port
```

### Start Serving

Next, the `start_serving()` method should start a thread
(using the `cls._thread` attribute to store it for later)
and create an underlying HTTP server (and using the `self._server`
attribute to store it for later):

```
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
```

### Stop Serving

The `stop_serving()` method stops the thread

```python
    @classmethod
    def stop_serving(cls):
        # Shut down the server
        if cls._server is not None:
            cls._server.shutdown()

        # Let the thread rejoin the worker pool
        cls._thread.join(timeout=10)
        assert not cls._thread.is_alive()
```

## Handling Requests

The mock API server should only process POST requests, and should
only accept JSON-formatted requests. We can implement those checks
and have the server return a 500 error if clients do not send a
properly formatted JSON request.

### Defining POST Response Method

To define a response to POST requests made to the API we are mocking,
we start by validating the JSON request that is received.

Note: this utilizes several built-in methods of the HTTP server class.

```python
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
        ...
```

Now, the JSON can be processed using a validate function,
for example, or generic success/failure responses returned
based on the contents of a request.

Let's do something very simple: have the API server return
whatever was sent in the request.

We can turn the dictionary `message` (a dictionary containing
the original request) back into a string, and the string into
a stream of bytes. Then we can write headers and the stream of
bytes into the response.

```python
        # Send a response
        response = bytes(json.dumps(message), "utf8")
        self._set_headers()
        self.wfile.write(response)
```

The `_set_headers()` method is a short method that just sends
(writes) the correct headers:

```python
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
```

Note: the `send_headers()` and `end_headers()` methods are built-in
to the HTTP server base class we are using.

# Putting it all together

Putting it all together, we get one final mock API server class:

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

