import base64
import http.server
import logging
import socketserver
from threading import Thread
from http.server import SimpleHTTPRequestHandler
import time

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
        f = open("server/display.html")
        data = f.read()
        f.close()
        return data

    @staticmethod
    def generate_page():
        new_html = Server.HTML_DEFAULT

        # insert current thermostat info
        therm_info = str(Server.DHT.avg).rsplit(" ", 1)
        therm_info, therm_time = (therm_info[0], therm_info[1])
        new_html = Server.insert(str(new_html), "content", "h1", text = therm_info, options = {"class": "infoheader"})
        new_html = Server.insert(str(new_html), "content", "h1", text = therm_time, options = {"class": "infosubheader"})

        # insert stats header
        new_html = Server.insert(str(new_html), "content", "h1", text = "Statistics", options = {"class": "contentheader"})

        # insert graphs
        temp_graph_bytes = base64.b64encode(open("server/files/temps.png", 'rb').read()).decode('utf-8')
        hum_graph_bytes = base64.b64encode(open("server/files/hum.png", 'rb').read()).decode('utf-8')
        temp_graph = {
            "class": "graph",
            "src": f"data:image/png;base64,{temp_graph_bytes}",
            "alt": "Temperatures unavailable.",
        }
        hum_graph = {
            "class": "graph",
            "src": f"data:image/png;base64,{hum_graph_bytes}",
            "alt": "Humidity data unavailable.",
        }
        new_html = Server.insert(str(new_html), "content", "image", options = temp_graph)
        new_html = Server.insert(str(new_html), "content", "image", options = hum_graph)

        # insert stats
        current_stats = Server.DHT.get_buffers()
        for stats in current_stats:
            new_html = Server.insert(str(new_html), "content", "p", text = stats)

        Server.HTML = str(new_html)

    def insert(html, parent, tag, text = None, options = None):
        """
        Inserts an HTML tag into the document.

        Args:
            html (str): HTML string to parse and insert into.
            parent (str): Class name of the tag to insert into.
            parent (str): Type of tag to insert into `location
            text (str, Optional): String to insert into the tag.

        Returns:
            bs4.Soup: New BS4 soup instance.
        """
        soup = Soup(html, features="html.parser")

        content = soup.find(class_=parent)
        tag = soup.new_tag(tag)
        if text:
            tag.string = str(text)
        if options:
            for k in options.keys():
                tag[k] = options[k]
        content.append(tag)

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
            s = time.time()
            Server.generate_page()
            LOGGER.debug(f"HTML generated in {time.time() - s} seconds.")
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", str(len(Server.HTML)))
            self.end_headers()

            self.wfile.write(bytes(Server.HTML, "utf-8"))
