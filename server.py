from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import requests

cache = dict()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/favicon.ico':
            self.handle_favico()
        else: 
            self.handle_regular_req()
    
    # favicon requests can't be handled like other requests
    # the browser sends the get request to http://localhost:8080/favicon.ico
    # instead of http://localhost:8080/${HOST}/favicon.ico
    def handle_favico(self):
        try:
            file = open('./favicon.ico', 'rb')
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            self.wfile.write(file.read())

        except Exception as err:
            print(err)
            self.send_response(404)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            self.wfile.write('404 not found'.encode())

    def handle_regular_req(self):
        if self.path in cache: 
            res = cache[self.path]
            self.respond(res)
            return

        res = requests.get(
            url='https://' + self.path[1:], 
            headers=self.create_header(),
        )
        cache[self.path] = res
        self.respond(res)
            
    def create_header(self): 
        headers = dict((x, y) for x, y in self.headers._headers)
        headers.pop("Host") # ignore the host header as the "host" in the request is the server itself.
        return headers

    def respond(self, res):
        self.send_response(res.status_code)
        for key in res.headers:
            self.send_header(key, res.headers[key])
        self.end_headers()

        self.wfile.write(res.content)

class MultiThreadedServer(ThreadingMixIn, HTTPServer):
    pass

def main():
    PORT = 8080
    server = MultiThreadedServer(('', PORT), Handler)
    # server = SocketServer(('', PORT), Handler)
    print('Server listening on port %s', PORT)
    server.serve_forever()


if __name__ == '__main__':
    main()