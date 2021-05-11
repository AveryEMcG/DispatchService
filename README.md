# DispatchService
Dispatch Service Take Home

This dispatch service has been written based against the [prompt](https://github.com/AveryEMcG/DispatchService/blob/main/Dispatch%20Service%20Take%20Home.pdf) for a take home assignment. 

<<<<<<< HEAD
The dispatch service 
=======
The server is launched via the server_runner.py script.
>>>>>>> 9d29b3b898c05f116e5c4190f0037a1eed9ba149

Users can issue dispatches through commands like this:<br>
```curl -X POST -H 'Content-type: application/json' --data   '{"start_time":"08/27/2019 21:04", "end_time":"08/27/2019 22:04",   "program_id":1, "event_type":"market_dispatch"}' http://localhost:8080/ ```



Architecture below.


![Diagram of architecture](https://github.com/AveryEMcG/DispatchService/blob/main/architecture.png)<br>
Note that proposed but not yet implemented features are outlined with dashes.

Sequence:
1. Users can request events via HTTP.
2. The server validates the request and verifies the user is authorized to issue that request (TBD)
3. The server passes the request along to a logger who logs the event to persistent memory, and then puts it into a queue for processing.
4. Event processors watch the queue, and pop off events to be handled. These are further sorted into subsequent actions. Currently the only event supported is dispatch, which trigger 'output' actions - output actions are pushed into the output queue where it is collected and logged to persistent memory before being passed to an output processor.
5. Output processors pick up outputs from the output queue and then perform relevant actions. For example - an 'Email' output will result in an email being composed and sent.

An error logger is provided but not fully implemented. The intent of this log is to provide the potential for resilience through an error recovery engine. The engine would pick up errors from the error queue and take steps to mitigate and manage them - such as re-issuing events, or escalating the issue to human administrators. The recovery engine would also monitor tasks with a heartbeat, in the case of task death it would re-push their event into the relevent queue to be re-processed.  
