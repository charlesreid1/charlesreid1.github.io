Title: Creating Mock API Servers
Date: 2019-12-26 20:00
Category: Python
Tags: http, server, python, mock, mocking

# Introduction

## Mock API Server Class

```
class MockFusilladeHandler(BaseHTTPRequestHandler):
    _server = None
    _thread = None

    @staticmethod
    def get_addr_port():
        addr = "127.0.0.1"
        port = networking.unused_tcp_port()
        return addr, port

    @classmethod
    def start_serving(cls):
        Config.set_config(BucketConfig.TEST)
        cls._addr, cls._port = cls.get_addr_port()
        cls.stash_oidc_group_claim()
        cls.stash_openid_provider()
        Config._set_authz_url(f"http://{cls._addr}:{cls._port}")
        logger.info(f"Mock Fusillade server listening at {cls._addr}:{cls._port}")
        cls._server = HTTPServer((cls._addr, cls._port), cls)
        cls._thread = threading.Thread(target=cls._server.serve_forever)
        cls._thread.start()

    @classmethod
    def stop_serving(cls):
        cls.restore_oidc_group_claim()
        cls.restore_openid_provider()
        if cls._server is not None:
            cls._server.shutdown()
        cls._thread.join(timeout=10)
        assert not cls._thread.is_alive(), 'Mock Fusillade server failed to join thread'
        logger.info(f"Mock Fusillade server has shut down")

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

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
        # Only allow if principal is on whitelist
        if message["principal"] in self._whitelist:
            message["result"] = True
        else:
            message["result"] = False
        # Send it back
        self._set_headers()
        self.wfile.write(bytes(json.dumps(message), "utf8"))
```

