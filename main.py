import os
import time
import shutil
import signal
import sys

import numpy as np
import dorsa_logger
import psutil


from ffmpegCamera import ffmpegCamera
from imageSaver import imageSave
from configReader import configReader 
from fileManager import fileManager, PERMITION
from storgeManager import storageManager
from filesSorting import moviesSorting
from configUpdateChecker import configUpdateChecker
from pathsConstans import pathsConstans

class App:
    

    def __init__(self) -> None:
        self.terminate_ffmpeg_processes()
        self.mkdirs()
        
        self.logger = dorsa_logger.logger(
                                        main_folderpath=pathsConstans.LOGS_SHARE_FOLDER,
                                        date_type=dorsa_logger.date_types.AD_DATE,
                                        date_format=dorsa_logger.date_formats.YYMMDD,
                                        time_format=dorsa_logger.time_formats.HHMMSS,
                                        file_level=dorsa_logger.log_levels.DEBUG,
                                        console_level=dorsa_logger.log_levels.DEBUG,
                                        console_print=True,
                                        current_username="admin",
                                        line_seperator='-')
        self.config:configReader = None
        self.config_mtime = None

        while True:
            self.update_config()

            if self.config is not None:
                #-----------------------------------------------------------
                log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.DEBUG,
                                            text=f"config update success", 
                                            code="Ainit000")
                self.logger.create_new_log(message=log_msg)
                #-----------------------------------------------------------
                break
            
            else:
                #-----------------------------------------------------------
                log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.ERROR,
                                            text=f"no config exists", 
                                            code="Ainit000")
                self.logger.create_new_log(message=log_msg)
                #-----------------------------------------------------------
                time.sleep(30)
            
                    

        
        self.configUpdateChecker = configUpdateChecker(path=pathsConstans.CONFIG_SHARE_PATH,
                                                       mtime=self.config_mtime,
                                                       logger=self.logger)
        self.configUpdateChecker.start()
        
        #-----------------------------------------------------------
        log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.ERROR,
                                            text=f"RUN APP With Config:{self.config.config}", 
                                            code="Ainit001")
        self.logger.create_new_log(message=log_msg)
        #-----------------------------------------------------------
        
        self.grabbers:dict[str, ffmpegCamera] = {}
        self.movieSorting = moviesSorting(train_id=self.config.train_id,
                                          cycle_time_sec=30,
                                          src_path=pathsConstans.TEMP_VIDEOS_FOLDER,
                                          dst_path=pathsConstans.IMAGES_SHARE_FOLDER,
                                          logger= self.logger)
        



        try:
            
            _, name = os.path.split(pathsConstans.SHARE_FOLDER)
            #-----------------------------------------------------------
            log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.DEBUG,
                                                text=f"share folder {pathsConstans.SHARE_FOLDER} as name {name}", 
                                                code="Ainit002")
            self.logger.create_new_log(message=log_msg)
            #-----------------------------------------------------------
            fileManager.remove_share(share_name=name)
            fileManager.create_and_share_folder(os.path.abspath(pathsConstans.SHARE_FOLDER), 
                                                share_name=name, 
                                                permissions=PERMITION)
        except Exception as e:
            #-----------------------------------------------------------
            log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.ERROR,
                                                text=f"Excaption happend for sharing folder:{e}", 
                                                code="Ainit003")
            self.logger.create_new_log(message=log_msg)
            #-----------------------------------------------------------

        self.storageManager = storageManager(path=pathsConstans.IMAGES_SHARE_FOLDER, 
                                             logs_path=pathsConstans.LOGS_SHARE_FOLDER,
                                             max_usage=self.config.max_allowed_storage,
                                             max_log_count=100,
                                             cleaning_evry_sec=2000,
                                             logger= self.logger)
        
    def terminate_ffmpeg_processes(self,):
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                print( proc.info['name'])
                if proc.info['name'] == 'ffmpeg.exe':
                    print(f'Terminating FFmpeg process with PID: {proc.info["pid"]}')
                    proc.terminate()
            except Exception as e:
                print(e)

    def mkdirs(self,):
        if not os.path.exists(pathsConstans.SHARE_FOLDER):
            os.makedirs(pathsConstans.SHARE_FOLDER)
        
        if not os.path.exists(pathsConstans.UTILS_SHARE_FOLDER):
            os.makedirs(pathsConstans.UTILS_SHARE_FOLDER)

        
        if not os.path.exists(pathsConstans.IMAGES_SHARE_FOLDER):
            os.makedirs(pathsConstans.IMAGES_SHARE_FOLDER)


        if not os.path.exists(pathsConstans.LOGS_SHARE_FOLDER):
            os.makedirs(pathsConstans.LOGS_SHARE_FOLDER)

        
    def update_config(self,):
        if os.path.exists(pathsConstans.CONFIG_SHARE_PATH):
            self.config_mtime = os.path.getmtime(pathsConstans.CONFIG_SHARE_PATH)
            try:
                shutil.copy(pathsConstans.CONFIG_SHARE_PATH, configReader.PATH)
            except Exception as e:
                #-----------------------------------------------------------
                log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.ERROR,
                                           text=f"""copy config error {e}""", 
                                           code="AUC000")
                self.logger.create_new_log(message=log_msg)
                #-----------------------------------------------------------

        if os.path.exists(configReader.PATH):
            self.config = configReader()

    def signal_handler(self, sig, frame):
        print('Shutting down...')
        # Terminate all ffmpegCamera subprocesses
        for grabber in self.grabbers.values():
            grabber.terminate_ffmpeg()  # Ensure you have this method to terminate subprocesses.
        sys.exit(0)

    def load_grabbers(self,):
        for camera_info in self.config.cameras:
            #-----------------------------------------------------------
            log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.DEBUG,
                                           text=f"""creat camera object {camera_info}""", 
                                           code="ALG000")
            self.logger.create_new_log(message=log_msg)
            #-----------------------------------------------------------
            grab = ffmpegCamera( name=camera_info['name'], 
                                username=camera_info['username'],
                                password= camera_info['password'],
                                ip=camera_info['ip'],
                                train_id= self.config.train_id,
                                fps=self.config.video_fps,
                                temp_folder=pathsConstans.TEMP_VIDEOS_FOLDER,
                                segments=self.config.video_duration,
                                codec=self.config.video_codec,
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
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

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
    