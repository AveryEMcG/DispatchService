
"""Server_Runner

This script does the necessary steps to set up the dispatch service on a single machine. 

* Sets up the communication queues
* Assigns tasks which listen to their corresponding queues
* Launches the HTTP server which listens for user events

"""
import server
from http.server import BaseHTTPRequestHandler, HTTPServer

import processors
import multiprocessing
import message_types
from functools import partial
import loggers

workers = 3 # value arbitrarily chosen to test parallelism

def setupWorkerTasks():

    # Establish communication queues
    event_queue_in = multiprocessing.JoinableQueue()
    event_queue_out = multiprocessing.JoinableQueue()    

    error_queue_in = multiprocessing.JoinableQueue()
    error_queue_out = multiprocessing.JoinableQueue()

    output_queue_in = multiprocessing.JoinableQueue()
    output_queue_out = multiprocessing.JoinableQueue()

    queues = {"output_in": output_queue_in, "error_in": error_queue_in, "event_in":event_queue_in,"output_out": output_queue_out, "error_out": error_queue_out, "event_out":event_queue_out}

    # Start event Handlers
    print('Creating %d event handlers' % workers)

    #make an arbitrary amount of event processors
    event_workers = [ processors.EventProcessor(queues)for i in range(workers) ]
    for e in event_workers:
        e.start()

    # Start Output Handlers
    print('Creating %d output handlers' % workers)

    #make an arbitrary amount of output processors
    output_workers = [ processors.OutputProcessor(queues) for i in range(workers) ]
    for o in output_workers:
        o.start()

    #Start Loggers
    event_logger = loggers.GenericLogger(event_queue_in,event_queue_out,"event_logger")
    event_logger.start()

    output_logger = loggers.GenericLogger(output_queue_in,output_queue_out,"output_logger")
    output_logger.start()

    error_logger = loggers.GenericLogger(error_queue_in,error_queue_out,"error_log")
    error_logger.start()

    return queues


def launchServer(queues):
    # We "partially apply" the first three arguments to the ExampleHandler
    handler = partial(server.DispatchServer, queues)
    # .. then pass it to HTTPHandler as normal:
    webServer = HTTPServer(('localhost', 8080), handler)

    print("Server started http://%s:%s" % ('localhost', 8080))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

if __name__ == '__main__':
    queues = setupWorkerTasks()
    launchServer(queues)
