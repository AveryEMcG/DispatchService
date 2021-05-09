from server import DispatchServer
from http.server import BaseHTTPRequestHandler, HTTPServer
import asyncio

hostName = "localhost"
serverPort = 8080


def start_server():
    """Starts an asyncio server"""

    loop = asyncio.get_event_loop()

    coroutine = loop.create_server(HTTPServer((hostName, serverPort), DispatchServer))
    server = loop.run_until_complete(coroutine)

    print('Starting server on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass


start_server()
'''

if __name__ == "__main__":        
    dispatchServer =HTTPServer((hostName, serverPort), DispatchServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        dispatchServer.serve_forever()
    except KeyboardInterrupt:
        pass

    dispatchServer.server_close()
    print("Server stopped.")
'''