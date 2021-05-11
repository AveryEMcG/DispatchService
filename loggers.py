import multiprocessing
import datetime
import message_types
  
class GenericLogger(multiprocessing.Process):
    def __init__(self, queue_in, queue_out, logger_name):
        super().__init__()          
        self.queue_in = queue_in
        self.queue_out = queue_out
        self.logger_name = logger_name #used for generating our logfiles

    def run(self):
        while True:
            #Take message, log it, and pass it along
            message = (self.queue_in.get())
            #terminate gracefully
            if message == message_types.TERMINATE_MESSAGE:
                print("Terminating logger task")
                self.queue_in.task_done()
                return
    
            self.log(message)
            self.queue_out.put(message)
            self.queue_in.task_done()
        return    

    def log(self,message):
        #TODO: This should go to a persistent storage medium (cloud database, local disk, etc). For the purposes of this exercise, it's going to a log.txt file.

        with open(self.logger_name+"_log.txt","a") as fp:

            #make our timestmap
            now = datetime.datetime.now()
            nowString = now.strftime("%H:%M:%S.%f - %b %d %Y")
            
            #log everything
            output_message = "--------------\n"
            output_message += self.logger_name+": "
            output_message += nowString+"\n"
            output_message += message.get_string()+"\n"

            print(output_message,file=fp)


