import requests
import signal
import sys
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

class ApiProxy:
    def start_server(self):
        class ProxyHTTPRequestHandler(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.0"

            def do_GET(self):
                self._handle_request("get", requests.get)

            def do_DELETE(self):
                self._handle_request("delete", requests.delete)

            def do_POST(self):
                self._handle_request("post", requests.post)

            def do_PUT(self):
                self._handle_request("put", requests.put)

            def do_PATCH(self):
                self._handle_request("patch", requests.patch)

            def _handle_request(self, method, requests_func):

                print(f"Incoming request for {self.path}")

                # url = self._resolve_url()
                # if (url is None):
                #     print(f"Unable to resolve the URL {self.path}")
                #     self.send_response(404)
                #     self.send_header("Content-Type", "application/json")
                #     self.end_headers()
                #     return

                # body = self.rfile.read(int(self.headers["content-length"]))
                # headers = dict(self.headers)

                # # Set any custom headers that would be provided through API Management inbound policies
                # headers['Api-Version'] = 'v1'
                # headers['Api-Path'] = '/internal'
		
                # resp = requests_func(url, data=body, headers=headers)
                
                #self.send_response(resp.status_code)
                # for key in headers:
                #     self.send_header(key, headers[key])
                # self.end_headers()
                # self.wfile.write(resp.content)
                #self.send_response(200)
                #self.wfile.write(bytes("HALLO","utf-8"))

            def _resolve_url(self):
                return "http://www.google.de"

        server_address = ('', 8001)
        self.httpd = HTTPServer(server_address, ProxyHTTPRequestHandler)
        print('proxy server is running')
        self.httpd.serve_forever()


def exit_now(signum, frame):
    sys.exit(0)

if __name__ == '__main__':
    proxy = ApiProxy()
    signal.signal(signal.SIGTERM, exit_now)
    proxy.start_server()

