import cv2
import numpy as np
import queue

from Camera import Camera, Frame
from imageSaver import imageSave
from configReader import configReader 
from fileManager import fileManager, PERMITION
from storgeManager import storageManager
import os
import time

WEBCAM_DEBUG = False

class App:
    LIVE_FPS = 25
    def __init__(self) -> None:
        self.config = configReader()
        self.isaver = imageSave(self.config.path, self.config.train_id)
        self.cameras:dict[str, Camera] = {}
        self.shared_images = queue.Queue(100)


        self.last_refresh_time = 0
        self.last_image = dict()

        try:
            _, name = os.path.split(self.config.path)
            fileManager.remove_share(share_name=name)
            fileManager.create_and_share_folder(os.path.abspath(self.config.path), 
                                                share_name=name, 
                                                permissions=PERMITION)
        except Exception as e:
            print(e)

        self.storageManager = storageManager(self.config.path, max_usage=self.config.max_allowed_storage)
        self.isaver.VIDEO_FPS = self.config.video_fps
        self.isaver.VIDEO_FRAME_COUNT = self.config.video_frames_count
        self.isaver.VIDEO_TIME = self.config.video_time
        self.t = 0



        

    def load_camera(self,):
        for camera_info in self.config.cameras:
            cam = Camera( name=camera_info['name'], 
                          username=camera_info['username'],
                          password= camera_info['password'],
                          ip=camera_info['ip'],
                          train_id= self.config.train_id,
                          images= self.shared_images,
                          interval_delay=2 ,
                          res_size= (1920,1088),
                          )
            
            self.cameras[camera_info['name']] = cam
            

    def is_motion(self, camera_name:str, image):
        if self.last_image[camera_name] is not None:
            diff = cv2.absdiff(self.last_image[camera_name], image)
            self.last_image[camera_name] = image

            _, thresh = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)
            changed_pixel = np.sum(thresh) / 255
            if changed_pixel > self.config.motion_sens:
                return True
            return False
        else:
            self.last_image[camera_name] = image
            return True


    
    def start_grabbing(self,):
        self.storageManager.start()
        
        for camera in self.cameras.values():
            camera.daemon = True
            camera.start()


        while True:
            if not self.shared_images.empty():
                frame:Frame = self.shared_images.get()
                
                t = time.time()
                # if t - self.last_refresh_time > 1/self.LIVE_FPS:
                    # self.last_refresh_time = t
                cv2.imshow('main: ' + frame.cam_name, cv2.resize(frame.image, None, fx=0.75, fy=0.75))        
                cv2.waitKey(1)
                if self.config.motion:
                    if not self.is_motion(frame.cam_name, frame.image):
                        continue
            
                if self.config.output_type == 'image':
                    self.isaver.save(frame)
        
                elif self.config.output_type == 'stack_image':
                    self.isaver.save_stack(frame)
                
                else:
                    self.isaver.save_video_time(frame)

                t = time.time() - t
                # print(t)



app = App()
app.load_camera()
app.start_grabbing()


#while True:
#    pass