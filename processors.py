import multiprocessing
import time
import message_types
import json
import offsitedata
from datetime import datetime

class GenericProcessor(multiprocessing.Process):
    
    def __init__(self):
        multiprocessing.Process.__init__(self)

    def process(self):
        pass

    def processDispatchEvent(self):
        pass    

class EventProcessor(GenericProcessor):
    def __init__(self, queues):
        super().__init__()
        self.event_queue = queues["event_out"]
        self.output_queue = queues["output_in"]
        self.error_queue = queues["error_in"]       
        
    def run(self):
        self.proc_name = self.name
        while True:
            event = (self.event_queue.get()).data

            self.process_event(event)

            self.event_queue.task_done()
        return

    def process_event(self,event):
        json_event_data = json.loads(event)
        if json_event_data["event_type"] == "market_dispatch":
            self.processDispatchEvent(json_event_data)
        else:
             self.error_queue.put(message_types.Error_data_packet(event, message_types.ERROR_UNSUPPORTED_EVENT))    

    def processDispatchEvent(self,json_event_data):
        for output in offsitedata.program[json_event_data["program_id"]]:
            self.output_queue.put(message_types.Output_data_packet(json_event_data, output)) 

class OutputProcessor(GenericProcessor):


    def __init__(self, queues):
        super().__init__()
        self.output_queue = queues["output_out"]
        self.error_queue = queues["error_in"]       
    
    def parse_timestamp(self, timeString):
        time = datetime.strptime(timeString, "%m/%d/%Y %H:%M")
        return time.strftime("%I:%M %p")

    def generate_output_text(self,output):
        start_time = output.data["start_time"]
        end_time = output.data["end_time"]

        message = "Dear Voltan,\n You have been dispatched as part of the Program \"Voltus Interview\".\nPlease have your full curtailment plan in effect between the hours of " + self.parse_timestamp(start_time)+ " and " + self.parse_timestamp(end_time)

        return message

    def process_output(self,output):
        #TODO: This only works if the dispatch is within -0hrs/+24hrs of the current time. 
        # For the past - we should send a message to the error handler to respond. 
        # For the future - the coding prompt only asked for time and not date, so it's not really an 'error' case per-se, but we can also pass that to the error handler.
        if output.output_info[0] == "Email":
            self.process_output_email(output)
        else:
             self.error_queue.put(message_types.Error_data_packet(event, message_types.ERROR_UNSUPPORTED_OUTPUT_TYPE))    
       
    def process_output_email(self,output):
        #TODO: Actually send the e-mail :)
        print("\n Send E-mail to: "+output.output_info[1]+" with message contents: \n "+self.generate_output_text(output))

    def run(self):
        self.proc_name = self.name
        while True:
            output = self.output_queue.get()
            self.process_output(output)
            self.output_queue.task_done()
        return
