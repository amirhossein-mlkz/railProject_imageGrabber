import threading
import time
import subprocess
from datetime import datetime
import os

import ffmpeg
from onvif import ONVIFCamera
from persiantools import jdatetime


H256 = 'libx265'
H264 = 'libx264'
NONE_CODEC = 'copy'
MPEG = 'mpeg2video'
class ffmpegCamera(threading.Thread):
    
    def __init__(self,
                 name:str, 
                 username:str, 
                 password:str, 
                 train_id:str,
                 ip:str, 
                 fps:int,
                 codec= MPEG,
                 segments = 300,
                 org_fps = 25,
                 temp_folder = 'temp_videos',
                 
                 ) -> None:
        super().__init__()
        self.name = name
        self.username = username
        self.password = password
        self.train_id = train_id
        self.ip = ip
        self.codec = codec
        self.fps = fps
        self.org_fps = org_fps
        self.segments = segments
        self.temp_folder = temp_folder
        self.loop_index = 0

        self.daemon = True


    def get_stream_url(self,):
        try:
          camera = ONVIFCamera(host=self.ip, port=80, user=self.username, passwd=self.password)

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
        
        except Exception as e:
           print(e)
           return None 
    
    def add_write_info_filter(self, stream):
        
        stream = ffmpeg.filter(stream,
                              filter_name='drawtext', 
                              text='%{localtime}', #'%{localtime}'
                              fontfile='arial.ttf',
                              fontcolor='white',
                              fontsize=48,
                              box= 1,
                              boxborderw= 20,
                              boxcolor= 'black',
                              shadowx= 2,   
                              shadowy= 2,
                              x=25,
                              y=40)

        date = jdatetime.JalaliDateTime.now()
        text = date.strftime('%Y/%m/%d')
        stream = ffmpeg.filter(stream, 
                              filter_name='drawtext', 
                              text=text,
                              fontfile='arial.ttf',
                              fontcolor='white',
                              fontsize=48,
                              box= 1,
                              boxborderw= 20,   
                              boxcolor= 'black',
                              shadowx= 2,           
                              shadowy= 2,                     
                              x=30,
                              y=40)
        
        text = f'Train: {self.train_id} - Camera: {self.name} '
        stream = ffmpeg.filter(stream, 
                              filter_name='drawtext', 
                              text=text,
                              fontfile='arial.ttf',
                              fontcolor='white',
                              fontsize=48,
                              box= 1,
                              boxborderw= 20,   
                              boxcolor= 'black',
                              shadowx= 2,           
                              shadowy= 2,                     
                              x=600,
                              y=40)
        
        return stream
    

    def build_path(self, ):
        output_dir = os.path.join(self.temp_folder,self.name)
        if not os.path.exists(output_dir):
          print('temp path created')
          os.makedirs(output_dir)

        fname = f'video_{self.loop_index}_{self.name}' + '_%04d.mp4'
        self.loop_index+=1
        return output_dir, fname
    
    def build_and_run_stream(self,rstp_url, output_path):
        
        stream = ffmpeg.input(rstp_url, 
                              ss=0,
                              rtsp_transport='tcp',
                              timeout ='5000000', 
                                )
        # stream = self.add_write_info_filter(stream)
        # stream = ffmpeg.filter(stream, 'fps', fps=self.fps, round='up')

        stream = ffmpeg.output(stream, 
                       output_path, 
                       vcodec=self.codec,
                       f='segment',  # استفاده از فیلتر segment
                       segment_time=str( int(self.segments * self.fps/self.org_fps )),
                       reset_timestamps='1',
                    #    preset='fast',
                    #    preset='fast',  # کاهش سرعت پردازش
                    #    tune='zerolatency'
                     )
        
        stream = ffmpeg.overwrite_output(stream)

        try:
            out, err = ffmpeg.run(stream, quiet=False)         
        except ffmpeg.Error as e:
            print("Error occurred:", e.stderr.decode())
        except KeyboardInterrupt:
            print("Recording stopped manually.")
    

    def run(self,):
      while True:
        print('Try Connect')
        rstp_url = self.get_stream_url()  
        if rstp_url is None:
           time.sleep(5)
           continue
        
        try:
            output_dir, output_fname = self.build_path()
            output_path = os.path.join(output_dir, output_fname)
            
        except Exception as e:
           print(e)
           continue

        
        print('Connect Success')
        try:
           self.build_and_run_stream(rstp_url, output_path)
        except Exception as e:
           print(e)
        print('Stream Stop')

    
    
           
        

    

        # command  = ffmpeg.compile(stream)

        
    

# grabber = ffmpegCamera('left', 'admin', 'Milad1375422@', train_id='11BGDEF', ip='192.168.1.2', fps=25)
# grabber.start()

