import http.server
import logging
import socketserver
from threading import Thread
from http.server import SimpleHTTPRequestHandler

from bs4 import BeautifulSoup as Soup

LOGGER = logging.getLogger()

class Server(Thread):

    DHT = None
    HEATER = None
    HUMIDIFIER = None
    PORT = None

    HTML = None
    HTML_DEFAULT = None

    def __init__(self, dht, heater, humidifier, port):
        Thread.__init__(self)
        self.daemon = True
        Server.DHT = dht
        Server.HEATER = heater
        Server.HUMIDIFIER = humidifier
        Server.PORT = port
        Server.HTML_DEFAULT = Server.open_html()

    @staticmethod
    def open_html():
        """
        Opens HTML file into a string for modification.

        Returns:
            str: String representation of loaded HTML file.
        """
        return open("server/display.html").read()

    @staticmethod
    def generate_page():
        new_html = Server.HTML_DEFAULT
        current_stats = Server.DHT.get_buffers()
        for s in current_stats:
            new_html = Server.insert(str(new_html), "content", "p", text = s)

        Server.HTML = str(new_html)

    def insert(html, location, tag, text = None):
        """
        Inserts an HTML tag into the document.

        Args:
            html (str): HTML string to parse and insert into.
            location (str): Class name of the tag to insert into.
            tag (str): Type of tag to insert into `location
            text (str, Optional): String to insert into the tag.

        Returns:
            bs4.Soup: New BS4 soup instance.
        """
        soup = Soup(html, features="html.parser")

        content = soup.find(class_=location)
        temp = soup.new_tag(tag)
        if text:
            temp.string = str(text)
            content.append(temp)

        return soup

    def run(self):
        """
        Starts serving on localhost.
        """
        # prevents port collisions
        socketserver.TCPServer.allow_reuse_address = True

        server = socketserver.TCPServer(("", Server.PORT), self.Handler)

        LOGGER.info(f"Serving at port {Server.PORT}")
        server.serve_forever(poll_interval=0.25)

    class Handler(http.server.SimpleHTTPRequestHandler):
        """
        Handles all incoming requests. Uses outer Server class to generate response.
        """
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            Server.generate_page()
            self.wfile.write(bytes(Server.HTML, "utf-8"))
