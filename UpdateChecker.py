import time
import os
import threading
import signal
import shutil

import dorsa_logger
from manifestLoader import manifestLoader
from pathsConstans import pathsConstans
from updateUtils import updateUtils

class UpdateChecker(threading.Thread):

    
    def __init__(self, share_minifest_path:str, close_event:threading.Event, self_manifest_path:str, logger:dorsa_logger.logger ) -> None:
        super(UpdateChecker, self).__init__()
        self.share_minifest_path = share_minifest_path
        self.self_manifest_path = self_manifest_path
        self.logger = logger

        self.self_manifest = manifestLoader(self.self_manifest_path)
        self.share_manifest = None
        self.close_event = close_event


    


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
        #os.kill(os.getpid(), signal.SIGTERM)
        self.close_event.set()
    
    def decrypt_update(self, path, dst_path):
        #file_hash = updateUtils.get_metadata_value(path, 'code')
        file_hash = self.share_manifest.get_id()
        if file_hash is None:
            return False
        
        #updateUtils.remove_specific_metadata(path, 'code')
        password = updateUtils.pass_generator(file_hash)
        status = updateUtils.decrypt_zip_file(path, password, dst_path )
        return status

    def check_size_not_change(self,path, delay=10):
        if not os.path.exists(path):
            return False
        size1 = os.path.getsize(path)

        time.sleep(delay)

        if not os.path.exists(path):
            return False
        size2 = os.path.getsize(path)

        if size1 != size2:
            #-----------------------------------------------------------
            log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.DEBUG,
                                                text=f"{path} is during file: {size1} -> {size2}", 
                                                code="UCCSNC000")
            self.logger.create_new_log(message=log_msg)
            #-----------------------------------------------------------
            return False
        else:
            return True
        
    def remove_file(self, path):
        try:
            os.remove(path)
        except Exception as e:
            #-----------------------------------------------------------
            log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.ERROR,
                                                text=f"fail to remove {path}: {e}", 
                                                code="UCRF000")
            self.logger.create_new_log(message=log_msg)
            #-----------------------------------------------------------

            

    def run(self, ):
        #-----------------------------------------------------------
        log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.DEBUG,
                                            text=f"software update checker thread run", 
                                            code="UCR000")
        self.logger.create_new_log(message=log_msg)
        #-----------------------------------------------------------
       
            
        idx = 0
        while True:
            idx +=1
            update_available = self.check_version()
            if update_available:
                update_enc_path = os.path.join(pathsConstans.SELF_UPDATE_IMAGEGRABBER_PATH, pathsConstans.UPADTE_ENC)
                if not os.path.exists(update_enc_path):
                    #-----------------------------------------------------------
                    log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.WARNING,
                                                            text=f"update needed but update.enc not found", 
                                                            code="UCR004")
                    self.logger.create_new_log(message=log_msg)
                    #-----------------------------------------------------------
                    try:
                        os.remove(self.share_minifest_path)
                    except:
                        pass
                        
                    continue
                
                flag = self.check_size_not_change(update_enc_path)
                if not flag:
                    #-----------------------------------------------------------
                    log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.WARNING,
                                                            text=f"update is during copy", 
                                                            code="UCR004")
                    self.logger.create_new_log(message=log_msg)
                    #-----------------------------------------------------------
                    continue


                status = self.decrypt_update(update_enc_path, pathsConstans.TEMP_UPDATE_DIR + '.zip')
                if not status:
                    #-----------------------------------------------------------
                    log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.WARNING,
                                                            text=f"update file was invalid due wrong licens", 
                                                            code="UCR004")
                    self.logger.create_new_log(message=log_msg)
                    #-----------------------------------------------------------
                    self.remove_file(self.share_minifest_path)
                    self.remove_file(update_enc_path)
                    continue


                #-----------------------------------------------------------
                log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.DEBUG,
                                                            text=f"update file was valid", 
                                                            code="UCR003")
                self.logger.create_new_log(message=log_msg)
                #-----------------------------------------------------------
                status , msg = updateUtils.extract_zip_to_directory(pathsConstans.TEMP_UPDATE_DIR + '.zip', pathsConstans.TEMP_UPDATE_DIR)
                if not status:
                    log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.ERROR,
                                                            text=f"error on zip extraction_" + msg, 
                                                            code="UCR004")
                    self.logger.create_new_log(message=log_msg)
                    continue
                #-----------------------------------------------------------
                self.remove_file(pathsConstans.TEMP_UPDATE_DIR + '.zip')

                self.close_software()
                    


            time.sleep(10)
