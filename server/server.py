import base64
import logging
import socketserver
from http.server import SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn, TCPServer
from threading import Thread
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
        """
        Serves HTTP request to clients consisting of thermostat data and statistics.

        Args:
            dht (devices.TempSensor): TempSensor object.
            heater (devices.Heater): Heater object.
            humidifier (devices.Humidifier): Humiditiy object.
            port (int): Port to serve requests on.
        """
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
        """
        Generates an HTML page and saves it to this class.
        """
        new_html = Server.HTML_DEFAULT

        # insert current thermostat info
        therm_info = str(Server.DHT.get_avg()).split()
        temp, hum, therm_time = (therm_info[0], therm_info[1], therm_info[2])
        new_html = Server.insert(str(new_html), "content", "h1", text = f"{temp}\n{hum}", options = {"class": "infoheader"})
        new_html = Server.insert(str(new_html), "content", "h1", text = therm_time, options = {"class": "infosubheader"})

        # insert stats header
        new_html = Server.insert(str(new_html), "content", "h1", text = "Statistics", options = {"class": "contentheader"})

        # insert graphs
        temp_graph_bytes = base64.b64encode(open("server/files/graphs.png", 'rb').read()).decode('utf-8')
        graphs = {
            "class": "graph",
            "src": f"data:image/png;base64,{temp_graph_bytes}",
            "alt": "Graph data unavailable.",
        }
        new_html = Server.insert(str(new_html), "content", "image", options = graphs)

        # insert stats
        #current_stats = Server.DHT.get_buffers()
        #for stats in current_stats:
        #    new_html = Server.insert(str(new_html), "content", "p", text = stats)

        Server.HTML = str(new_html)

    def insert(html, parent, tag, text = None, options = None):
        """
        Inserts an HTML tag into the provided HTML.

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
        #sets connection threads to daemon mode
        ThreadingMixIn.daemon_threads = True
        server = Server.ThreadedTCPServer(("", Server.PORT), self.Handler)

        LOGGER.info(f"Serving at port {Server.PORT}")
        server.serve_forever(poll_interval=0.25)

    class ThreadedTCPServer(ThreadingMixIn, TCPServer):
        """
        Uses ThreadingMixIn to overide TCPServer methods to implement multithreading.
        """
        pass

    class Handler(SimpleHTTPRequestHandler):
        """
        Handles all incoming requests. Uses outer Server class to generate response.
        """
        def do_GET(self):
            s = time.time()
            Server.generate_page()
            LOGGER.debug(f"HTML generated in {time.time() - s} seconds.")
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(str(Server.HTML)))
            self.end_headers()

            self.wfile.write(bytes(Server.HTML, "utf-8"))
