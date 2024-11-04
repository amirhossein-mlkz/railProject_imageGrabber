import time
import os
import threading
import signal
import shutil

import dorsa_logger
from manifestLoader import manifestLoader
from pathsConstans import pathsConstans

class UpdateChecker(threading.Thread):


    def __init__(self, share_minifest_path:str, self_manifest_path:str, logger:dorsa_logger.logger ) -> None:
        super(UpdateChecker, self).__init__()
        self.share_minifest_path = share_minifest_path
        self.self_manifest_path = self_manifest_path
        self.logger = logger

        self.self_manifest = manifestLoader(self.self_manifest_path)
        self.share_manifest = None

    


    def check_version(self,):
        if os.path.exists(self.share_minifest_path):
            self.share_manifest = manifestLoader(self.share_minifest_path)
            
            v = self.self_manifest.get_version()
            share_v = self.share_manifest.get_version()
            if share_v > v :
                #-----------------------------------------------------------
                log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.DEBUG,
                                            text=f"New Update Found old version:{v} - new version:{share_v}", 
                                            code="UCCV000")
                self.logger.create_new_log(message=log_msg)
                #-----------------------------------------------------------
                return True
        return False
    
    def close_software(self,):
        #-----------------------------------------------------------
        log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.DEBUG,
                                            text=f"close sofware for updated software", 
                                            code="UCCS000")
        self.logger.create_new_log(message=log_msg)
        #-----------------------------------------------------------
        os.kill(os.getpid(), signal.SIGTERM)
    

    def run(self, ):
        #-----------------------------------------------------------
        log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.DEBUG,
                                            text=f"software update checker thread run", 
                                            code="UCR000")
        self.logger.create_new_log(message=log_msg)
        #-----------------------------------------------------------
        while True:
            update_available = self.check_version()
            if update_available:
                updater_path = os.path.join(pathsConstans.SELF_UPDATE_IMAGEGRABBER_PATH, pathsConstans.UPDATER_NAME)
                if os.path.exists(updater_path):
                    try:
                        shutil.copy2(updater_path, pathsConstans.UPDATER_NAME)
                        self.close_software()
                    except Exception as e:
                        #-----------------------------------------------------------
                        log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.ERROR,
                                                            text=f"error on copy updater and close software: {e}", 
                                                            code="UCR001")
                        self.logger.create_new_log(message=log_msg)
                        #-----------------------------------------------------------
                else:
                    #-----------------------------------------------------------
                    log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.ERROR,
                                                        text=f"couldnt found updater.exe", 
                                                        code="UCR002")
                    self.logger.create_new_log(message=log_msg)
                    #-----------------------------------------------------------


            time.sleep(10)
