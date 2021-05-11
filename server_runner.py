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

workers = 3  # value arbitrarily chosen to test parallelism


def setupWorkerTasks():
    """Setup worker tasks
    Creates the various queues and processes which will be used in our data pipeline.
    """

    # Establish communication queues. See README for more info about the structure of the queues.
    # Basic idea: IN means INTO logger, and OUT means OUT of logger. Loggers sit between other tasks.
    event_queue_in = multiprocessing.JoinableQueue()
    event_queue_out = multiprocessing.JoinableQueue()

    error_queue_in = multiprocessing.JoinableQueue()
    error_queue_out = multiprocessing.JoinableQueue()

    output_queue_in = multiprocessing.JoinableQueue()
    output_queue_out = multiprocessing.JoinableQueue()

    queues = {
        "output_in": output_queue_in,
        "error_in": error_queue_in,
        "event_in": event_queue_in,
        "output_out": output_queue_out,
        "error_out": error_queue_out,
        "event_out": event_queue_out,
    }

    tasks = []

    # make an arbitrary amount of event processors
    event_workers = [processors.EventProcessor(queues) for i in range(workers)]
    for e in event_workers:
        e.start()
        tasks.append(e)

    # make an arbitrary amount of output processors
    output_workers = [processors.OutputProcessor(queues) for i in range(workers)]
    for o in output_workers:
        o.start()
        tasks.append(o)

    # Start Loggers
    event_logger = loggers.GenericLogger(
        event_queue_in, event_queue_out, "event_logger"
    )
    event_logger.start()
    tasks.append(event_logger)

    output_logger = loggers.GenericLogger(
        output_queue_in, output_queue_out, "output_logger"
    )
    output_logger.start()
    tasks.append(output_logger)

    error_logger = loggers.GenericLogger(
        error_queue_in, error_queue_out, "error_logger"
    )
    error_logger.start()
    tasks.append(output_logger)

    return queues, tasks


def launchServer(queues):
    # We "partially apply" the first three arguments to the ExampleHandler
    # This is because the HTTPServer mechanism does not allow additional arguments
    # and so we need to play some weird games and partially fill the arguments in before passing
    # the handler over to the HTTPserver module.
    handler = partial(server.DispatchServer, queues)

    # .. then pass it to HTTPHandler as normal:
    webServer = HTTPServer(("localhost", 8080), handler)

    print("Server started http://%s:%s" % ("localhost", 8080))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("\nServer stopped.\n")


# TODO: Termination is not completely implemented There are some bugs, (I think related to catching keyboard interrupts in the subprocesses?). Finish it.
def terminate_processes(queues, tasks):
    event_queue_out = queues["event_out"]
    for w in range(workers):
        event_queue_out.put(message_types.TERMINATE_MESSAGE)

    output_queue_out = queues["output_out"]
    for w in range(workers):
        output_queue_out.put(message_types.TERMINATE_MESSAGE)

    output_queue_in = queues["output_in"]
    output_queue_in.put(message_types.TERMINATE_MESSAGE)

    event_queue_in = queues["event_in"]
    event_queue_in.put(message_types.TERMINATE_MESSAGE)

    error_queue_in = queues["error_in"]
    error_queue_in.put(message_types.TERMINATE_MESSAGE)

    for t in tasks:
        t.join()


if __name__ == "__main__":
    queues, tasks = setupWorkerTasks()
    launchServer(queues)

    # TODO: Gracefully exit processes, not finished implementing
    # terminate_processes(queues,tasks)
