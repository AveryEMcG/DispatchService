
"""Message_Types
This module provides 2 main services:

* Provides definitions of data packets which can be used to communicate across queues.
* Defines generic error messages which can be used to indicate specific failure states.

"""

ERROR_UNSUPPORTED_EVENT = "Unsupported event type given"
ERROR_UNSUPPORTED_OUTPUT_TYPE = "Unsupported output type given"
ERROR_UNVERIFIED_USER_REQUEST = "User did not pass verification check"
ERROR_INVALID_DATA_TO_API = "User request to API was invalid"

TERMINATE_MESSAGE = 0

class Event_Data_Packet():
    def __init__(self, data):
        self.data = data

    def get_string(self):
        return "Data: "+str(self.data)

class Output_data_packet():
    def __init__(self, data, output_info):
        self.data = data
        self.output_info = output_info

    def get_string(self):
        return "Data: "+str(self.data)+ "output info: "+str(self.output_info)

class Error_data_packet():
    def __init__(self, data, error_message):
        self.data = data
        self.error_message = error_message

    def get_string(self):
        return "Data: "+str(self.data)+ "error info: "+str(self.error_message)