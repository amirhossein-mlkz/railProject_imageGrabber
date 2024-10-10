import time
import os
import threading
import signal

import dorsa_logger

class configUpdateChecker(threading.Thread):


    def __init__(self, path, mtime, logger:dorsa_logger.logger) -> None:
        super(configUpdateChecker, self).__init__()
        self.path = path
        self.init_mtime = mtime
        self.logger = logger


    def check_file_modification(self,):
        if os.path.exists(self.path):
            current_mod_time = os.path.getmtime(self.path)      
              
            if self.init_mtime is None or current_mod_time != self.init_mtime:
                print("File modified. Closing the software...")
                #-----------------------------------------------------------
                log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.DEBUG,
                                            text=f"config file modify detected", 
                                            code="CUCCFM000")
                self.logger.create_new_log(message=log_msg)
                #-----------------------------------------------------------
                return True
        return False
    
    def close_software(self,):
        #-----------------------------------------------------------
        log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.DEBUG,
                                            text=f"close sofware for config updated", 
                                            code="CUCCFM000")
        self.logger.create_new_log(message=log_msg)
        #-----------------------------------------------------------
        os.kill(os.getpid(), signal.SIGTERM)
    

    def run(self, ):
        #-----------------------------------------------------------
        log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.DEBUG,
                                            text=f"config file update checker thread run", 
                                            code="CUCCFM000")
        self.logger.create_new_log(message=log_msg)
        #-----------------------------------------------------------
        while True:
            is_changed = self.check_file_modification()
            if is_changed:
                self.close_software()

            time.sleep(5)
