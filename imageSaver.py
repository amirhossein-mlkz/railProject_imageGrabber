import os
# from datetime import datetime
from persiantools.jdatetime import JalaliDateTime
import threading

import numpy as np
import cv2
import imageio #pip install imageio[ffmpeg]
from onvif import ONVIFCamera #pip install onvif-zeep    
from Camera import Frame

from fileManager import fileManager


#pip install imageio[ffmpeg]
#pip install imageio imageio-ffmpeg


class imageSave:
    image_extention = '.jpeg'
    video_extention = '.mp4'

    encode_param = [int(cv2.IMWRITE_JPEG_LUMA_QUALITY), 80]
    
    UPDATE_LIST_DIR_FPS = 100

    VIDEO_FRAME_COUNT = 100
    VIDEO_TIME = 5
    VIDEO_FPS = 20
    
    IMAGE_STACK = 5

    


    def __init__(self, path:str, train_id) -> None:
        self.path = path
        self.train_id = train_id
        self.start_time = {
            'left':JalaliDateTime.now(),
            'right':JalaliDateTime.now()
        }

    

        self.__video:dict[str:dict] = {
            'left': {'video': None, 'frame':0, 'start_time':None},
            'right':{'video': None, 'frame':0, 'start_time':None},
        }

        self.saved_image_path = os.path.join(self.path, self.train_id)
        
        if not os.path.exists(self.saved_image_path):
            os.makedirs(self.saved_image_path) 
        
        self.__stack_images:dict[str,: dict] = {
            'left':  {'image':None, 'counter':0},
            'right': {'image':None, 'counter':0},

        }




    def generate_path(self, now:JalaliDateTime, cam_name:str):
        path = os.path.join(self.saved_image_path,
                            cam_name,
                            str(now.year),
                            str(now.month),
                            str(now.day),
                            str(now.hour),
                            str(now.minute),
                            )
        return path   

    def gen_file_name(self,now:JalaliDateTime, camera_name:str):
        #now = datetime.now()
        
        file_name = now.strftime('%Y-%m-%d_%H-%M-%S-%f')
        file_name = file_name +  '_' + self.train_id + '_' + camera_name
        return file_name
    
    def save(self,frame:Frame):
        self.start_time[frame.cam_name] = JalaliDateTime.now()
        file_name = self.gen_file_name(self.start_time[frame.cam_name], frame.cam_name)
        file_name = file_name + self.image_extention
        img_path = self.generate_path(self.start_time[frame.cam_name], frame.cam_name)
        if not os.path.exists(img_path):
            os.makedirs(img_path)
        img_path = os.path.join(img_path, file_name)

        

        cv2.imwrite(img_path, frame.image, self.encode_param)

        #append saved image name

    
    def save_stack(self,frame:Frame):
        h,w = frame.image.shape[:2]
        if self.__stack_images[frame.cam_name]['image'] is None:
            self.start_time[frame.cam_name] = JalaliDateTime.now()
            if len(frame.image.shape) == 2:
                self.__stack_images[frame.cam_name]['image'] = np.zeros((h*self.IMAGE_STACK, w))
            else:
                self.__stack_images[frame.cam_name]['image'] = np.zeros((h*self.IMAGE_STACK, w, 3))


        res:np.ndarray = self.__stack_images[frame.cam_name]['image']
        cnt = self.__stack_images[frame.cam_name]['counter']
        res[cnt * h: (cnt+1)*h, :,:] = frame.image
        cnt+=1

        

        if cnt >= self.IMAGE_STACK:
            file_name = self.gen_file_name(self.start_time[frame.cam_name], frame.cam_name)
            file_name = file_name + self.image_extention
            img_path = self.generate_path(self.start_time[frame.cam_name], frame.cam_name)
            if not os.path.exists(img_path):
                os.makedirs(img_path)
            img_path = os.path.join(img_path, file_name)
            cv2.imwrite(img_path, res, self.encode_param)

            self.__stack_images[frame.cam_name]['image'] = None
            self.__stack_images[frame.cam_name]['counter'] = 0

        
        else:
            self.__stack_images[frame.cam_name]['image'] = res
            cnt = self.__stack_images[frame.cam_name]['counter'] = cnt




    def save_video_time(self, frame:Frame):

        if self.__video[frame.cam_name]['video'] is None:
            file_name = self.gen_file_name(self.start_time[frame.cam_name], frame.cam_name)
            file_name = file_name + self.video_extention

            file_name = self.gen_file_name(self.start_time[frame.cam_name], frame.cam_name)
            file_name = file_name + self.video_extention
            video_path = self.generate_path(self.start_time[frame.cam_name], frame.cam_name)
            if not os.path.exists(video_path):
                os.makedirs(video_path)
            video_path = os.path.join(video_path, file_name)

            self.__video[frame.cam_name]['video'] =  imageio.get_writer(video_path, fps=self.VIDEO_FPS, codec='libx264',)
            self.__video[frame.cam_name]['start_time'] = JalaliDateTime.now()

        


        if self.__video[frame.cam_name]['video'] is not None:
            image = cv2.cvtColor(frame.image, cv2.COLOR_BGR2RGB)
            self.start_time[frame.cam_name] = JalaliDateTime.now()
            self.__video[frame.cam_name]['video'].append_data(image)
            self.__video[frame.cam_name]['frame'] +=1

            now = JalaliDateTime.now()
            delta = now -  self.__video[frame.cam_name]['start_time']
            if delta.total_seconds() >= self.VIDEO_TIME:
                prev_video = self.__video[frame.cam_name]['video']
                prev_video.close()
                threading.Thread(target=prev_video.close).start()
                self.__video[frame.cam_name]['video'] = None
  
        
        
        


 




        


if __name__ == '__main__':
    ims = imageSave('images')