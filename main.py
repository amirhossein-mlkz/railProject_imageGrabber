import os
import time
import shutil
import signal
import sys
import subprocess
import threading

import numpy as np
import dorsa_logger
import psutil
from VidGearCamera import vidGear
from ffmpegCamera import ffmpegCamera
from configReader import configReader 
from fileManager import fileManager, PERMITION
from storgeManager import storageManager
from filesSorting import moviesSorting
from configUpdateChecker import configUpdateChecker
from UpdateChecker import UpdateChecker
from timeUpdateChecker import timeUpdateChecker
from pathsConstans import pathsConstans
from PySide6.QtCore import Qt, QThread, Signal

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QProgressBar , QPushButton , QMessageBox , QHBoxLayout,QSpacerItem, QSizePolicy
)


class App(QThread):
    

    signal_cam_0 = Signal(object)
    signal_cam_1 = Signal(object)
    signal_cam_2 = Signal(object)
    signal_cam_3 = Signal(object)



    def __init__(self,logger:dorsa_logger,config,config_mtime,parent=None) -> None:
        super().__init__(parent)
        
        self.mkdirs()
        
        self.logger =logger
        self.config:configReader = config
        self.config_mtime = config_mtime
        self.show_flag = False
    
        self.close_event = threading.Event()
        self.terminate_ffmpeg_processes()


        # self.set_timezone('Iran Standard Time')

        # while True:
        #     self.update_config()

        #     if self.config is not None:
        #         #-----------------------------------------------------------
        #         log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.DEBUG,
        #                                     text=f"config update success", 
        #                                     code="Ainit000")
        #         self.logger.create_new_log(message=log_msg)
        #         #-----------------------------------------------------------
        #         break
            
        #     else:
        #         #-----------------------------------------------------------
        #         log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.ERROR,
        #                                     text=f"no config exists", 
        #                                     code="Ainit000")
        #         self.logger.create_new_log(message=log_msg)
        #         #-----------------------------------------------------------
        #         time.sleep(30)
            
                    

        #-----------------------------------------------------------
        #software update checker
        share_minifest_path = os.path.join(pathsConstans.SELF_UPDATE_IMAGEGRABBER_PATH, pathsConstans.MANIFEST_NAME)
        self_minifest_path = os.path.join(pathsConstans.MANIFEST_NAME)

        self.appUpdateChecker = UpdateChecker( share_minifest_path=share_minifest_path,
                                              self_manifest_path=self_minifest_path,
                                              close_event=self.close_event,
                                              logger=self.logger) 
        self.appUpdateChecker.start()
        #-----------------------------------------------------------
        #config update checker
        self.configUpdateChecker = configUpdateChecker(path=pathsConstans.SELF_CONFIG_SHARE_PATH,
                                                       mtime=self.config_mtime,
                                                       close_event=self.close_event,
                                                       logger=self.logger)
        self.configUpdateChecker.start()
        
        #-----------------------------------------------------------
        
        self.timeSettingChecker = timeUpdateChecker(path=pathsConstans.SELF_CLOCK_SHARE_PATH,
                                                    logger=self.logger)
        self.timeSettingChecker.start()
        
        #-----------------------------------------------------------
        log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.INFO,
                                            text=f"RUN APP With Config:{self.config.config}", 
                                            code="Ainit001")
        self.logger.create_new_log(message=log_msg)
        #-----------------------------------------------------------
        
        self.grabbers:dict[str, ffmpegCamera] = {}
        self.movieSorting = moviesSorting(train_id=self.config.train_id,
                                          cycle_time_sec=30,
                                          src_path=pathsConstans.TEMP_VIDEOS_FOLDER,
                                          dst_path=pathsConstans.SELF_IMAGES_SHARE_FOLDER,
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

        self.storageManager = storageManager(path=pathsConstans.SELF_IMAGES_SHARE_FOLDER, 
                                             logs_path=pathsConstans.SELF_LOGS_SHARE_FOLDER,
                                             max_usage=self.config.max_allowed_storage,
                                             max_log_count=100,
                                             cleaning_evry_sec=2000,
                                             logger= self.logger)

    def set_timezone(self, timezone):
        try:
            # Set timezone using tzutil command
            subprocess.run(["tzutil", "/s", timezone], check=True)
            #-----------------------------------------------------------
            log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.DEBUG,
                                                text=f"Timezone set to {timezone} successfully.", 
                                                code="Ainit002")
            self.logger.create_new_log(message=log_msg)

        except subprocess.CalledProcessError as e:
            #-----------------------------------------------------------
            log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.ERROR,
                                                text=f"Failed to set timezone:{e}", 
                                                code="Ainit002")
            self.logger.create_new_log(message=log_msg)
            #-----------------------------------------------------------



    def terminate_ffmpeg_processes(self,):
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                # print( proc.info['name'])
                if proc.info['name'] == 'ffmpeg.exe':
                    log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.ERROR,
                                           text=f'Terminating FFmpeg process with PID: {proc.info["pid"]}', 
                                           code="ATFP000")
                    self.logger.create_new_log(message=log_msg)
                    proc.terminate()
            except Exception as e:
                #-----------------------------------------------------------
                log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.ERROR,
                                           text=f"""error on terminate ffmpeg {e}""", 
                                           code="ATFP001")
                self.logger.create_new_log(message=log_msg)
                #-----------------------------------------------------------

    def mkdirs(self,):
        if not os.path.exists(pathsConstans.SHARE_FOLDER):
            os.makedirs(pathsConstans.SHARE_FOLDER)
        
        if not os.path.exists(pathsConstans.SELF_UTILS_SHARE_FOLDER):
            os.makedirs(pathsConstans.SELF_UTILS_SHARE_FOLDER)

        
        if not os.path.exists(pathsConstans.SELF_IMAGES_SHARE_FOLDER):
            os.makedirs(pathsConstans.SELF_IMAGES_SHARE_FOLDER)


        if not os.path.exists(pathsConstans.SELF_LOGS_SHARE_FOLDER):
            os.makedirs(pathsConstans.SELF_LOGS_SHARE_FOLDER)

        if not os.path.exists(pathsConstans.SELF_UPDATES_PATH):
            os.makedirs(pathsConstans.SELF_UPDATES_PATH)

        if not os.path.exists(pathsConstans.SELF_UPDATE_IMAGEGRABBER_PATH):
            os.makedirs(pathsConstans.SELF_UPDATE_IMAGEGRABBER_PATH)

        
    def update_config(self,):
        if os.path.exists(pathsConstans.SELF_CONFIG_SHARE_PATH):
            self.config_mtime = os.path.getmtime(pathsConstans.SELF_CONFIG_SHARE_PATH)
            try:
                shutil.copy(pathsConstans.SELF_CONFIG_SHARE_PATH, configReader.PATH)
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
            if (    'name' in camera_info
                and 'password' in camera_info
                and 'username' in camera_info
                and 'port' in camera_info
                and 'ip' in camera_info
            ):

                grab = ffmpegCamera( name=camera_info['name'], 
                                    username=camera_info['username'],
                                    password= camera_info['password'],
                                    ip=camera_info['ip'],
                                    port=camera_info['port'],
                                    train_id= self.config.train_id,
                                    fps=self.config.video_fps,
                                    temp_folder=pathsConstans.TEMP_VIDEOS_FOLDER,
                                    segments=self.config.video_duration,
                                    codec=self.config.video_codec,
                                    logger = self.logger
                                    )
                
                self.grabbers[camera_info['name']] = grab
            else:
                
                #-----------------------------------------------------------
                log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.ERROR,
                                            text=f"camera info is not complete {camera_info}", 
                                            code="ALG001")
                self.logger.create_new_log(message=log_msg)
                #-----------------------------------------------------------
    






    def run(self):
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



    def set_show_flag(self,mode=False):

        for name, grabber in self.grabbers.items():
            grabber.set_show_flag(mode)


    def vid_gear_load_grabbers(self):

        signals = [self.signal_cam_0,self.signal_cam_1,self.signal_cam_2,self.signal_cam_3]


        for iter, camera_info in enumerate(self.config.cameras):
            #-----------------------------------------------------------
            log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.DEBUG,
                                           text=f"""create camera object {camera_info}""", 
                                           code="ALG000")
            self.logger.create_new_log(message=log_msg)
            #-----------------------------------------------------------
            if (    'name' in camera_info
                and 'password' in camera_info
                and 'username' in camera_info
                and 'port' in camera_info
                and 'ip' in camera_info
            ):

                grab = vidGear( name=camera_info['name'], 
                                    username=camera_info['username'],
                                    password= camera_info['password'],
                                    ip=camera_info['ip'],
                                    port=camera_info['port'],
                                    train_id= self.config.train_id,
                                    fps=self.config.video_fps,
                                    temp_folder=pathsConstans.TEMP_VIDEOS_FOLDER,
                                    segments=self.config.video_duration,
                                    codec=self.config.video_codec,
                                    logger = self.logger,
                                    signal_show=signals[iter],
                                    show_flag=self.show_flag,
                                    motion=self.config.motion
                                    )
                
                self.grabbers[camera_info['name']] = grab
            else:
                
                #-----------------------------------------------------------
                log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.ERROR,
                                            text=f"camera info is not complete {camera_info}", 
                                            code="ALG001")
                self.logger.create_new_log(message=log_msg)
                #-----------------------------------------------------------











    def start(self):


        # print('milad'*80)
        #-----------------------------------------------------------
        log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.WARNING,
                                           text=f"start app", 
                                           code="AS000")
        self.logger.create_new_log(message=log_msg)
        #-----------------------------------------------------------
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

        self.storageManager.start()

        # self.grabbers['cam1'].run()
        # self.grabbers['cam2'].run()


        for key in self.grabbers.keys():

            print(key ,self.grabbers[key], 'started')
            self.grabbers[key].start()
        time.sleep(1)
        self.movieSorting.start()
        #-----------------------------------------------------------
        log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.WARNING,
                                           text=f"start app finish success", 
                                           code="AS000")
        self.logger.create_new_log(message=log_msg)
        #-----------------------------------------------------------








    def close_software(self,):
        #-----------------------------------------------------------
        log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.DEBUG,
                                            text=f"stop camera threads", 
                                            code="ACS000")
        self.logger.create_new_log(message=log_msg)
        #-----------------------------------------------------------
        for name, grabber in self.grabbers.items():
            print('start stop')
            grabber.stop_thread()
            print('set stop')
        time.sleep(5)
        self.terminate_ffmpeg_processes()
        time.sleep(5)
        os.kill(os.getpid(), signal.SIGTERM)

    
    def mainloop(self,):
        while True:
            if self.close_event.is_set():
                self.close_software()

            time.sleep(1)

    def minCheckker(self):
        if self.close_event.is_set():
            self.close_software()



        


if __name__=='__main__':

    app = App()
    app.load_grabbers()
    app.run()
    app.mainloop()
    