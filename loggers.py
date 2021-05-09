import multiprocessing
import datetime;
  
class GenericLogger(multiprocessing.Process):
    
    def __init__(self, queue_in, queue_out, logger_name):
        super().__init__()          
        self.queue_in = queue_in
        self.queue_out = queue_out
        self.logger_name = logger_name #used for generating our logfiles

    def setup(self):
        self.proc_name = self.name

    def run(self):
        self.setup()

        while True:
            #Take message, log it, and pass it along
            message = (self.queue_in.get())
            self.log(message)
            self.queue_out.put(message)
            self.queue_in.task_done()
        return    

    def log(self,message):
        #TODO: This should go to a persistent storage medium (cloud database, local disk, etc). For the purposes of this exercise, it's going to a log.txt file.

        #open file for appending
        log_file_pointer= open(self.logger_name+"_log.txt","a")

        #make our timestmap
        now = datetime.datetime.now()
        nowString = now.strftime("%H:%M:%S.%f - %b %d %Y")
        
        #log everything
        log_file_pointer.write("--------------\n")   
        log_file_pointer.write(self.logger_name+": ")
        log_file_pointer.write(nowString+"\n")
        log_file_pointer.write(message.get_string()+"\n")

        #close back up
        log_file_pointer.close()

