# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
from functools import partial
import time
import message_types

class DispatchServer(BaseHTTPRequestHandler):

    def __init__(self,queues, *args, **kwargs):
        self.queues = queues
        self.event_queue = queues["event_in"]
        super().__init__(*args, **kwargs)

        
    def do_POST(self):
        arguments = self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8')
        
        self.event_queue.put(message_types.Event_Data_Packet(arguments))
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("Request Recieved \n", "utf-8"))

