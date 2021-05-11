
"""Processors
This module is designed to provide mutiprocessing processes to manage various kinds of events in a stable and scalable manner.
Each processor focuses on a specific task type. During init they are given a dictionary of all available 'JoinableQueue's, 
and they each extract out the necessary communication queues in their respective __init__() functions.

* EventProcessor takes arguments passed by the user into the http server (listening on the "event_out" queue - See the 
repo's README for more info on this queue system), and breaks them down into smaller building blocks. For example, it 
takes dispatch events and generates output events to be used by the output processor.

* OutputProcessor takes outputs written by the EventProcessor (listening on the "output_out" queue), and issues those outputs out one by one.
"""

from datetime import datetime
import json
import message_types
import multiprocessing
import offsitedata
import time


class EventProcessor(multiprocessing.Process):
    """Create a processor for events. Reads the event_out queue, and writes relevant outputs to the output_in queue."""

    def __init__(self, queues):
        super().__init__() #required for multiprocessing
        self.event_queue = queues["event_out"]
        self.output_queue = queues["output_in"]
        self.error_queue = queues["error_in"]       
        
    def process_event(self,event):
        """Take an event and sort it to an appropriate event-specific function which will handle it from there"""

        #TODO: If JSON is wrong, this breaks here. We should check for valid JSON in Server, but we can also implement a safety check here for sanity
        json_event_data = json.loads(event)
        if json_event_data["event_type"] == "market_dispatch":
            self.processDispatchEvent(json_event_data)
        else:
             self.error_queue.put(message_types.Error_data_packet(event, message_types.ERROR_UNSUPPORTED_EVENT))    

    def processDispatchEvent(self,json_event_data):
        """Take each person to be contacted from program, and add their prefered form of contact to the output queue"""

        #I am assuming the output data structure, see 'offsitedata' module for more info
        
        #TODO: Check if program exists, if not send error message
        for output in offsitedata.program[json_event_data["program_id"]]:
            self.output_queue.put(message_types.Output_data_packet(json_event_data, output)) 


    def run(self):
        """Run the task. This is how multiprocessor code ."""    
        
        self.proc_name = self.name
        while True:
            event = self.event_queue.get()
            
            #terminate gracefully
            if event == message_types.TERMINATE_MESSAGE:
                print("Terminating event task")
                self.event_queue.task_done()
                return
            event = event.data
            
            self.process_event(event)

            self.event_queue.task_done()

        return


class OutputProcessor(multiprocessing.Process):
    """Create a processor for outputs. Reads the output_out queue, and conducts necessary output operations."""

    def __init__(self, queues):
        super().__init__()  #required for multiprocessing
        self.output_queue = queues["output_out"]
        self.error_queue = queues["error_in"]       
    
    def parse_timestamp(self, timeString):
        """Takes a timestring and returns a format used in output messages"""
       
       #TODO: This is rigid. Make this handle a greater variety of times.
        time = datetime.strptime(timeString, "%m/%d/%Y %H:%M")

        return time.strftime("%I:%M %p")

    def generate_output_text(self,output):
        """Takes ann output message and generates a string from it to be sent to recipients"""

        start_time = output.data["start_time"]
        end_time = output.data["end_time"]

        message = "Dear Voltan,\n You have been dispatched as part of the Program \"Voltus Interview\".\nPlease have your full curtailment plan in effect between the hours of " + self.parse_timestamp(start_time)+ " and " + self.parse_timestamp(end_time)

        return message

    def process_output(self,output):
        """Take an output and sort it to an appropriate output-specific function which will handle it from there"""

        #TODO: This only works if the dispatch is within -0hrs/+24hrs of the current time. 
        # For the past - we should send a message to the error handler to respond. 
        # For the future - the coding prompt only asked for time and not date, so it's not really an 'error' case per-se, but we can also pass that to the error handler.
        if output.output_info[0] == "Email":
            self.process_output_email(output)
        else:
             self.error_queue.put(message_types.Error_data_packet(event, message_types.ERROR_UNSUPPORTED_OUTPUT_TYPE))    
       
    def process_output_email(self,output):
        """Send e-mail to specified recipient"""

        #TODO: Actually send the e-mail :)
        with open("emails.txt","a") as fp:
            output_message = "--------------\n"
            output_message+="\n Send E-mail to: "+output.output_info[1]+" with message contents: \n "+self.generate_output_text(output)
            print(output_message,file=fp) 
            
    def run(self):
        """Run the task. Necessary for mutiprocessor code."""

        while True:
            output = self.output_queue.get()

            #terminate gracefully
            if output == message_types.TERMINATE_MESSAGE:
                    print("Terminating output task")
                    self.output_queue.task_done()
                    return

            self.process_output(output)
            self.output_queue.task_done()
        return

        
