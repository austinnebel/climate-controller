import atexit
import http.server
from http.server import SimpleHTTPRequestHandler
import socketserver

PORT = 8080
class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        display = open("server/display.html")
        out = display.read()
        self.wfile.write(bytes(out, "utf-8"))


socketserver.TCPServer.allow_reuse_address = True
server = socketserver.TCPServer(("", PORT), Handler)

atexit.register(server.server_close)

print("serving at port", PORT)
server.serve_forever()