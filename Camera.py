import threading
import queue
import time

from onvif import ONVIFCamera #pip install onvif-zeep
from persiantools.jdatetime import JalaliDateTime
import cv2
import numpy as np


THREAD = False

class Frame:
    def __init__(self, image, time, name) -> None:
        self.time:JalaliDateTime = time
        self.image:np.ndarray = image
        self.cam_name:str = name


class Camera(threading.Thread):
    MAX_ERROR_COUNT = 5
    TIME_OUT = 2

    

    def __init__(self,
                 name:str, 
                 username:str, 
                 password:str, 
                 train_id:str,
                 ip:str, 
                 images:queue.Queue, 
                 interval_delay, 
                 res_size=None,
                 fps=25,
                 codec='H264',
                 buffer_size=0) -> None:
        super().__init__()
        self.name = name
        self.username = username
        self.password = password
        self.train_id = train_id
        self.ip = ip
        self.images = images
        self.res_size = res_size
        self.fps = fps
        self.buffer_size = buffer_size
        self.codec = codec
        self.interval_delay = interval_delay
        self.lockVcap = threading.Lock()

        self.stream_url = self.get_stream_url()
        self.grabb_image_func = None
        self.videoCap = None

        #self.__play_flag = threading.Event()
        #self.__play_flag.set()  # Set the flag to True initially
        self.__play_flag = True
        
        self.open_camera_thread = None
        self.grabbing_thread = None

    def get_stream_url(self,):
        # url = f'rtsp://{self.username}:{self.password}@{self.ip}:554/mainstream1'
        # return url

        camera = ONVIFCamera('192.168.1.2', 80, 'admin', 'Milad1375422@', 'Tests/wsdl')

        media_service = camera.create_media_service()
        profiles = media_service.GetProfiles()
        stream_setup = {
            'Stream': 'RTP-Unicast',  
            'Transport': {
                'Protocol': 'RTSP' 
            }
        }

        stream_uri = media_service.GetStreamUri({
            'StreamSetup': stream_setup,
            'ProfileToken': profiles[0].token
        })

        return stream_uri.Uri
    
    def write_info(self, img, date:JalaliDateTime, train_id:str, cam_name:str, font = cv2.FONT_ITALIC, font_scale=1.5, thickness=2, padding=10, bg_color=(20,20,20), gap=20):
        
        date_str = date.strftime('%Y/%m/%d %H:%M:%S')
        origin = (20,75)
        text_size = cv2.getTextSize(date_str, font, font_scale, thickness)[0]
        pt1, pt2 = self.__get_text_box(origin, text_size, padding)
        cv2.rectangle(img, pt1, pt2, bg_color, thickness=-1)
        img = cv2.putText(img, date_str, org=origin, fontFace=font, fontScale=font_scale, color=(255,255,255) , thickness=thickness)
        #-------------------------TRAIN ID-----------------------------
        text = 'Train: ' + train_id
        origin = (origin[0] + text_size[0] + padding + gap , origin[1])
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
        pt1, pt2 = self.__get_text_box(origin, text_size, padding)
        cv2.rectangle(img, pt1, pt2, bg_color, thickness=-1)
        img = cv2.putText(img, text, org=origin, fontFace=font, fontScale=font_scale, color=(255,255,255) , thickness=thickness)

        #-------------------------TRAIN ID-----------------------------
        text = 'Camera: ' + cam_name
        origin = (origin[0] + text_size[0] + padding + gap , origin[1])
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
        pt1, pt2 = self.__get_text_box(origin, text_size, padding)
        cv2.rectangle(img, pt1, pt2, bg_color, thickness=-1)
        img = cv2.putText(img, text, org=origin, fontFace=font, fontScale=font_scale, color=(255,255,255) , thickness=thickness)
        return img
    
    def __get_text_box(self, origin, size, padding):
        x1= max(origin[0] - padding, 0)
        y1= max(origin[1] - size[1] - padding, 0)
        x2 = origin[0] + size[0] + padding
        y2 = origin[1] +  padding
        return (x1,y1), (x2,y2)


    def run(self):
        """Capture images and send signals with the captured image to the queue."""
        self.running = True

        while self.running:
            
            #try connect----------------------------------------------------
            while self.running:
                self.videoCap = cv2.VideoCapture(self.stream_url, cv2.CAP_FFMPEG)

                if self.videoCap.isOpened():
                    time.sleep(1)
                    settings = {
                        'fps':          (cv2.CAP_PROP_FPS, self.fps),
                        'buffer_size':  (cv2.CAP_PROP_BUFFERSIZE, self.buffer_size),
                        #'width':        (cv2.CAP_PROP_FRAME_WIDTH, self.res_size[0]),
                        #'height':       (cv2.CAP_PROP_FRAME_HEIGHT, self.res_size[1]),
                        'codec':        (cv2.CAP_PROP_FOURCC , cv2.VideoWriter_fourcc(*self.codec)),
                        # 'latency':      (cv2.CAP_PROP_LATENCY, 0) ,
                    }
                    #--------------print default values
                    for name in settings.keys():
                        setting_flag, value = settings[name]
                        print(name, self.videoCap.get(setting_flag))

                    for name in settings.keys():
                        setting_flag, value = settings[name]
                        res = self.videoCap.set(setting_flag, value)
                        print(name, res)
                    
                    # #--------------print values after setup
                    for name in settings.keys():
                        setting_flag, value = settings[name]
                        print(name,'value: ', self.videoCap.get(setting_flag), 'value should: ', value)
                    
             
                    
                    break
                else:
                    try:
                        self.videoCap.release()
                    except:
                        pass

                    print(f"Failed to open camera")
                    time.sleep(10)
                    
            
            #grabbing-------------------------------------------------------
            while self.running:
                ret, img = self.videoCap.read()

                if ret:
                    now = JalaliDateTime.now()
                    if self.images:
                        if self.res_size:
                            img = cv2.resize(img, self.res_size)
                        
                        img = self.write_info(img, now,cam_name=self.name, train_id=self.train_id)

                        frame = Frame(img, now, self.name)
                        self.images.put(frame)
                        #cv2.imshow('frame', cv2.resize(img, None, fx=0.6,  fy=0.6))
                        # 
                        # cv2.waitKey(self.interval_delay)

                else:
                    print(f"Failed to capture image from camera")
                    break

                # cv2.waitKey(self.interval_delay)
            #---------------------------------------------------------------
            try:
                self.videoCap.release()
            except Exception as e:
                print(e)

            
    def stop(self,):
        self.running = False
    

def grabbing():
    
    cap = cv2.VideoCapture('rtsp://192.168.1.2/media/video1')
    while True:
            _, frame = cap.read()

            cv2.imshow('frame', cv2.resize(frame, None, fx=0.6,  fy=0.6))
            cv2.waitKey(5)

if __name__ == '__main__':

    # "rtsp://admin:Milad1375422@@192.168.1.13:554/stream1"
    images = queue.Queue()
    cam = Camera( name='left', 
                          username='admin',
                          password= 'Milad1375422@',
                          ip ='192.168.1.2',
                          train_id= '1132BG',
                          images= images,
                          interval_delay=2 ,
                          res_size= None,#(1920,1088),
                          )
    cam.start()

    # grabbing()
    # threading.Thread(target=grabbing, daemon=False).start()

#     #cam.grabbing()







    