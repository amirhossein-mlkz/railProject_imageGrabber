import os
import time

import numpy as np

from ffmpegCamera import ffmpegCamera
from imageSaver import imageSave
from configReader import configReader 
from fileManager import fileManager, PERMITION
from storgeManager import storageManager

class App:
    LIVE_FPS = 25
    def __init__(self) -> None:
        self.config = configReader()
        self.isaver = imageSave(self.config.path, self.config.train_id)
        self.grabbers:dict[str, ffmpegCamera] = {}

        try:
            _, name = os.path.split(self.config.path)
            fileManager.remove_share(share_name=name)
            fileManager.create_and_share_folder(os.path.abspath(self.config.path), 
                                                share_name=name, 
                                                permissions=PERMITION)
        except Exception as e:
            print(e)

        self.storageManager = storageManager(self.config.path, max_usage=self.config.max_allowed_storage)

    def load_grabbers(self,):
        for camera_info in self.config.cameras:
            grab = ffmpegCamera( name=camera_info['name'], 
                                username=camera_info['username'],
                                password= camera_info['password'],
                                ip=camera_info['ip'],
                                train_id= self.config.train_id,
                                fps=25,
                                )
            
            self.grabbers[camera_info['name']] = grab


    def start(self,):
        for name, grabber in self.grabbers.items():
            grabber.run()


if __name__:

    app = App()
    app.load_grabbers()
    app.start()
    while True:
        time.sleep(1)
    