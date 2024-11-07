import requests
import signal
import sys
import ssl
import os
import glob
import json
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

DEBUG = True
DBGIDX = 0

class ApiProxy: 
    global DEBUG, DBGIDX

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
                global DBGIDX, DEBUG

                print(f"req: {method} on {self.path} ")

                url = self._resolve_url(self.path)
                if (url is None):
                    print(f"Unable to resolve the URL {self.path}")
                    self.send_response(404)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    return

                if "content-length" in self.headers:
                    body = self.rfile.read(int(self.headers["content-length"]))
                else: 
                    body = ""

                headers = dict(self.headers)

                resp = requests_func(url, data=body, headers=headers)
                
                resp_body = resp.content
                resp_headers = resp.headers

                self.send_response(resp.status_code)
                for key in resp_headers:
                    self.send_header(key, resp_headers[key])

                self.end_headers()
                self.wfile.write(resp_body)

                if DEBUG:
                    if DBGIDX is None:
                        DBGIDX = 0
                    DBGIDX = DBGIDX + 1
                    f = open(f"./debug/debg-{DBGIDX}.log", "w")
                    f.write(f"REQUEST:\n")
                    f.write(f"request: {method} on {self.path}\n")
                    f.write(f"url: {url}\n")
                    #json.dump(self.headers, f)
                    f.write(f"headers: {self.headers.items()}\n")
                    if "content-length" in self.headers:
                        f.write(f"body: {body.decode('utf-8')}\n")
                    f.write(f"\n\nRESPONSE:\n")
                    f.write(f"request: {resp.status_code}\n")
                    f.write(f"headers: {resp_headers}\n")
                    if resp_body is not None:
                        f.write(f"body: {resp_body.decode('utf-8')}\n")
                    f.close()



            def _resolve_url(self, path):
                return "http://192.168.1.109:8000" + path

        server_address = ('', 8000)
        self.httpd = HTTPServer(server_address, ProxyHTTPRequestHandler)

        #self.httpd.socket = ssl.wrap_socket (self.httpd.socket, 
        #    keyfile="keys/key.pem", 
        #    certfile='keys/cert.pem', 
        #    server_side=True)

        print('proxy server is running')
        self.httpd.serve_forever()


def exit_now(signum, frame):
    sys.exit(0)

def cleanup_debug_logs():
    os.system('rm -rf ./debug/*')

if __name__ == '__main__':
    if DEBUG:
        cleanup_debug_logs()

    proxy = ApiProxy()
    signal.signal(signal.SIGTERM, exit_now)
    proxy.start_server()


