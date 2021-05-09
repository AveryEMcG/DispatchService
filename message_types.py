ERROR_UNSUPPORTED_EVENT = "Unsupported event type given"
ERROR_UNSUPPORTED_OUTPUT_TYPE = "Unsupported output type given"


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
        return "Data: "+str(self.data)+ "output info: "+str(self.output_info)