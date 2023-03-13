# from http.server import HTTPServer
import http
import http.server
import os
import logging
# from urlparse import urlparse, urljoin
from urllib.parse import urlparse, urljoin
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from urllib.request import Request
import json

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

FOLLOW_REDIRECT = True
PROXY_RULES = {
    '/xurlapi/' : 'http://localhost:5000/',
}


class Proxy(http.server.SimpleHTTPRequestHandler):
    def __do_proxy(self):
        prefix = None
        for key in PROXY_RULES.keys():
            if self.path.startswith(key):
                prefix = key
                break

        if prefix:
            # Strip off the prefix.
            url = urljoin(PROXY_RULES[prefix], self.path.partition(prefix)[2])
            hostname = urlparse(PROXY_RULES[prefix]).netloc

            body = None
            logger.debug('headers: %s', self.headers)
            logger.debug('hostname: %s', self.headers['shophost'])

            host_name = self.headers['shophost']
            host_parts = host_name.split(':')
            host_w = host_parts[0].split('.')
            
            
            if self.headers['content-length'] is not None:
                content_len = int(self.headers.getheader('content-length'))
                body = self.rfile.read(content_len)
            logger.debug('body: %s', body)

            new_headers = {'x-xurl-shopid': host_w[0]}
            for name, value in self.headers.items():
                new_headers[name] = value

            new_headers['host'] = hostname
            try:
                del new_headers['accept-encoding']
            except KeyError:
                pass

            try:
                # self.copyfile(self.__do_request(url, body, new_headers), self.wfile)
                logger.debug(f'__do_request: {url} {body} {new_headers}')
                return self.__do_request(url, body, new_headers)
            except IOError as e:
                print(f"ERROR: {e}")
        else:
            logger.debug('do_GET: %s', self.path)
            http.server.SimpleHTTPRequestHandler.do_GET(self)


    def _set_headers(self, code=200):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def __do_request(self, url, body, headers):
        req = Request(url, body, headers)

        # we need to add the x-xurl-shopid header to the request
        # req.add_header('x-xurl-shopid', "707d6cb060")
        logger.debug('req url: %s', req.full_url)
        
        try:
            with urlopen(req) as response:
                data = response.read()

                # set new headers
                self.send_response(response.status)
                self.send_header('Content-Type', response.getheader('Content-Type'))
                self.send_header('Content-Length', len(data))
                self.send_header('Access-Control-Allow-Origin', "*")
                self.send_header('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE, OPTIONS")
                self.send_header('Access-Control-Allow-Headers', "Content-Type, Authorization, x-xurl-user, x-xurl-shopid")
                self.send_header('Access-Control-Max-Age', "86400")
                self.send_header('Access-Control-Allow-Credentials', "true")
                self.send_header('Access-Control-Expose-Headers', "Content-Length, Content-Range")
                self.end_headers()
                self.wfile.write(data)
        except HTTPError as e:
            self._set_headers(e.code)
            error_message = e.read()
            logger.debug('response error: %s', error_message)
            e_m = json.loads(error_message.decode('utf-8'))
            j_body = {'error': e.reason, "data": e_m}
            # if data is not None:
            #     j_body['data'] = json.loads(data)
            self.wfile.write(json.dumps(j_body).encode('utf-8'))
            # self.send_error(e.code, e.reason)   

    def do_GET(self):
        response = self.__do_proxy()
        logger.debug('response GET: %s', response)
        return response

    def do_POST(self):
        return self.__do_proxy()

class CustomHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        logger.debug('do_GET: %s', self.path)
        self.path = f'./htdocs/{self.path}'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

def run(server_class=http.server.HTTPServer, handler_class=Proxy):
    server_address = ('0.0.0.0', int(os.getenv('HTTPD_PROXY_PORT', 5003)))
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == "__main__":
    run()
