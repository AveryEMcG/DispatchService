"""Server
This module runs an HTTPserver, listening for user events to pass down the queues. 

The data is not verified or validated, but functions have been put in place for that to happen in the future

HTTPserver is not considered secure - so it's not good for production. I chose it for the scope of prompt as it's so simple to roll out.

"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import message_types


class DispatchServer(BaseHTTPRequestHandler):
    """Create an HTTP server which can handle various events from the user."""

    def __init__(self, queues, *args, **kwargs):

        self.queues = queues
        self.event_queue = queues["event_in"]
        self.error_queue = queues["error_in"]

        # The intialization of this is funky because of how HTTPserver works. See launchServer in server_runner.py for more info
        super().__init__(*args, **kwargs)

    def user_verified(self, arguments):
        # TODO: Do this :)
        # this function will check that the user is verified to be requesting the event in question.
        return True

    def input_valid(self, arguments):
        # TODO: Do this :)
        # this function will check that necessary elements are in place for the given event
        # and that the data is legal JSON
        return True

    def write_response_to_user(self, message, code):
        """Issue response to user over HTTP.

        Arguments:

        Message(str) - what you send to the user
        Code (int) - response status code
        """

        self.send_response(code)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(
            bytes(message, "utf-8")
        )  # wfile.write is annoying, requires byte format.
        return

    def do_POST(self):
        """Manage POST commands send to server. Entry point for data pipeline."""

        # TODO: we can do JSON.load() here and manage verifying if it is indeed real and good and wholesome JSON
        arguments = self.rfile.read(int(self.headers["Content-Length"])).decode("utf-8")

        if not self.user_verified(arguments):
            self.error_queue.put(
                message_types.Error_data_packet(
                    arguments, message_types.ERROR_UNVERIFIED_USER_REQUEST
                )
            )
            self.write_response_to_user("You are not verified to do this action\n", 400)
            return

        if not self.input_valid(arguments):
            self.error_queue.put(
                message_types.Error_data_packet(
                    arguments, message_types.ERROR_INVALID_DATA_TO_API
                )
            )
            self.write_response_to_user(
                "The data you have provided is invalid. Please check your arguments.\n",
                400,
            )
            return

        self.write_response_to_user("Request recieved\n", 200)
        self.event_queue.put(message_types.Event_Data_Packet(arguments))

        return
