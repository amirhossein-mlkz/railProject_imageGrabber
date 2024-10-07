import os
import time

import numpy as np
import dorsa_logger

from ffmpegCamera import ffmpegCamera
from imageSaver import imageSave
from configReader import configReader 
from fileManager import fileManager, PERMITION
from storgeManager import storageManager
from filesSorting import moviesSorting

class App:
    IMAGES_FOLDER = 'images'
    UTILS_FOLDER = 'utils'
    LOGS_FOLDER = 'logs'

    def __init__(self) -> None:
        self.config = configReader()

        self.images_path = os.path.join(self.config.path, self.IMAGES_FOLDER)
        self.utils_path = os.path.join(self.config.path, self.UTILS_FOLDER)
        self.logs_path = os.path.join(self.config.path, self.UTILS_FOLDER, self.LOGS_FOLDER)

        self.mkdirs()
        
        self.logger = dorsa_logger.logger(
                                        main_folderpath=self.logs_path,
                                        date_type=dorsa_logger.date_types.AD_DATE,
                                        date_format=dorsa_logger.date_formats.YYMMDD,
                                        time_format=dorsa_logger.time_formats.HHMMSS,
                                        file_level=dorsa_logger.log_levels.DEBUG,
                                        console_level=dorsa_logger.log_levels.DEBUG,
                                        console_print=True,
                                        current_username="admin",
                                        line_seperator='-')
        
        #-----------------------------------------------------------
        log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.ERROR,
                                            text=f"RUN APP With Config:{self.config.config}", 
                                            code="Ainit000")
        self.logger.create_new_log(message=log_msg)
        #-----------------------------------------------------------
        
        self.grabbers:dict[str, ffmpegCamera] = {}
        self.movieSorting = moviesSorting(train_id=self.config.train_id,
                                          cycle_time_sec=30,
                                          src_path=self.config.temp_folder,
                                          dst_path=self.config.path,
                                          logger= self.logger)
        



        try:
            _, name = os.path.split(self.config.path)
            #-----------------------------------------------------------
            log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.DEBUG,
                                                text=f"share folder {self.config.path} as name {name}", 
                                                code="Ainit001")
            self.logger.create_new_log(message=log_msg)
            #-----------------------------------------------------------
            fileManager.remove_share(share_name=name)
            fileManager.create_and_share_folder(os.path.abspath(self.config.path), 
                                                share_name=name, 
                                                permissions=PERMITION)
        except Exception as e:
            #-----------------------------------------------------------
            log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.ERROR,
                                                text=f"Excaption happend for sharing folder:{e}", 
                                                code="Ainit002")
            self.logger.create_new_log(message=log_msg)
            #-----------------------------------------------------------

        self.storageManager = storageManager(path=self.config.path, 
                                             logs_path=self.logs_path,
                                             max_usage=self.config.max_allowed_storage,
                                             max_log_count=100,
                                             cleaning_evry_sec=2000,
                                             logger= self.logger)

    def mkdirs(self,):
        if not os.path.exists(self.config.path):
            os.makedirs(self.config.path)
        
        if not os.path.exists(self.utils_path):
            os.makedirs(self.utils_path)

        if not os.path.exists(self.images_path):
            os.makedirs(self.images_path)

        if not os.path.exists(self.logs_path):
            os.makedirs(self.logs_path)
        
        

    def load_grabbers(self,):
        for camera_info in self.config.cameras:
            #-----------------------------------------------------------
            log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.DEBUG,
                                           text=f"""creat canera object {camera_info}""", 
                                           code="ALG000")
            self.logger.create_new_log(message=log_msg)
            #-----------------------------------------------------------
            grab = ffmpegCamera( name=camera_info['name'], 
                                username=camera_info['username'],
                                password= camera_info['password'],
                                ip=camera_info['ip'],
                                train_id= self.config.train_id,
                                fps=25,
                                temp_folder=self.config.temp_folder,
                                segments=self.config.video_duration,
                                logger = self.logger
                                )
            
            self.grabbers[camera_info['name']] = grab
 

    def start(self,):
        #-----------------------------------------------------------
        log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.WARNING,
                                           text=f"start app", 
                                           code="AS000")
        self.logger.create_new_log(message=log_msg)
        #-----------------------------------------------------------
        self.storageManager.start()
        for name, grabber in self.grabbers.items():
            grabber.start()
        time.sleep(1)
        self.movieSorting.start()
        #-----------------------------------------------------------
        log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.WARNING,
                                           text=f"start app finish success", 
                                           code="AS000")
        self.logger.create_new_log(message=log_msg)
        #-----------------------------------------------------------



if __name__:

    app = App()
    app.load_grabbers()
    app.start()
    while True:
        time.sleep(1)
    