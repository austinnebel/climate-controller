import http.server
from http.server import SimpleHTTPRequestHandler
import socketserver
from bs4 import BeautifulSoup as Soup

class Server:

    DHT = None
    HEATER = None
    HUMIDIFIER = None
    PORT = None

    HTML = None
    HTML_DEFAULT = None

    def __init__(self, dht, heater, humidifier, port):
        Server.DHT = dht
        Server.HEATER = heater
        Server.HUMIDIFIER = humidifier
        Server.PORT = port
        Server.HTML_DEFAULT = Server.open_html()

    @staticmethod
    def open_html():
        return open("server/display.html").read()

    @staticmethod
    def generate_page():
        new_html = Server.HTML_DEFAULT
        current_stats = Server.DHT.get_buffers()
        for s in current_stats:
            new_html = Server.insert(str(new_html), "content", s)

        Server.HTML = str(new_html)

    def insert(html, location, data):
        soup = Soup(html, features="html.parser")

        content = soup.find(class_=location)
        temp = soup.new_tag('p')
        temp.string = str(data)
        content.append(temp)

        return soup

    def start(self):
        # prevents port collisions
        socketserver.TCPServer.allow_reuse_address = True
        server = socketserver.TCPServer(("", Server.PORT), self.Handler)

        print("serving at port", Server.PORT)
        server.serve_forever()

    class Handler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            Server.generate_page()
            self.wfile.write(bytes(Server.HTML, "utf-8"))
