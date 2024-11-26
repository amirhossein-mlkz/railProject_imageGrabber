import threading
import time
import subprocess
from datetime import datetime
import os
from urllib.parse import urlparse, urlunparse

import ffmpeg
from onvif import ONVIFCamera
from persiantools import jdatetime
import dorsa_logger

H265 = 'libx265'
H264 = 'libx264'
NONE_CODEC = 'copy'
MPEG = 'mpeg2video'


class ffmpegCamera(threading.Thread):
    
    def __init__(self,
                 name:str, 
                 username:str, 
                 password:str, 
                 ip:str, 
                 port:str,
                 train_id:str,
                 fps:int,
                 codec,
                 segments = 300,
                 org_fps = 25,
                 temp_folder = 'temp_videos',

                 logger = dorsa_logger.logger
                 
                 ) -> None:
        super().__init__()
        self.name = name
        self.username = username
        self.password = password
        self.train_id = train_id
        self.port = port
        self.ip = ip
        self.fps = fps
        self.org_fps = org_fps
        self.segments = segments
        self.temp_folder = temp_folder
        self.loop_index = 0

        self.onvif_camera = None

        codesc = {
           'none':NONE_CODEC,
           'mpeg':MPEG,
           'h265':H265,
           'h264': H264
        }
        self.codec = codesc.get(codec, NONE_CODEC)

        self.logger = logger

        self.daemon = True
        self.proccess = None
        self.runing = True


    def get_stream_url(self):
        try:
            # اتصال به دوربین ONVIF
            self.onvif_camera = ONVIFCamera(host=self.ip, port=self.port, user=self.username, passwd=self.password)

            # دریافت سرویس مدیا و پروفایل
            media_service = self.onvif_camera.create_media_service()
            profiles = media_service.GetProfiles()

            stream_setup = {
                'Stream': 'RTP-Unicast',
                'Transport': {
                    'Protocol': 'RTSP'
                }
            }

            # دریافت StreamUri
            stream_uri = media_service.GetStreamUri({
                'StreamSetup': stream_setup,
                'ProfileToken': profiles[0].token
            })

            # تجزیه URL برای بررسی ساختار
            parsed_uri = urlparse(stream_uri.Uri)

            # اضافه کردن احراز هویت (username و password)
            netloc_with_auth = f"{self.username}:{self.password}@{parsed_uri.netloc}"
            updated_uri = parsed_uri._replace(netloc=netloc_with_auth)
            final_url = urlunparse(updated_uri)

            #-----------------------------------------------------------
            log_msg = dorsa_logger.log_message(
                level=dorsa_logger.log_levels.DEBUG,
                text=f"stream uri camera {self.name}: {final_url}",
                code="FCGSU000"
            )
            self.logger.create_new_log(message=log_msg)
            #-----------------------------------------------------------

            return final_url

        except Exception as e:
            # مدیریت خطا
            log_msg = dorsa_logger.log_message(
                level=dorsa_logger.log_levels.ERROR,
                text=f"Failed to get stream URL for camera {self.name}: {str(e)}",
                code="FCGSU001"
            )
            self.logger.create_new_log(message=log_msg)
            return None


    def setup_camera(self, ):
        try:
            media_service = self.onvif_camera.create_media_service()

            profiles = media_service.GetProfiles()

            # Use the first profile and Profiles have at least one
            token = profiles[0].token

            # Get all video encoder configurations
            configurations_list = media_service.GetVideoEncoderConfigurations()

            # Use the first profile and Profiles have at least one
            video_encoder_configuration = configurations_list[0]

            # Get video encoder configuration options
            options = media_service.GetVideoEncoderConfigurationOptions({'ProfileToken':token})

            # Setup stream configuration
            video_encoder_configuration.Encoding = 'H264'
            # Setup Resolution
            video_encoder_configuration.Resolution.Width = options.H264.ResolutionsAvailable[0].Width
            video_encoder_configuration.Resolution.Height = options.H264.ResolutionsAvailable[0].Height
            # Setup Quality
            video_encoder_configuration.Quality = int((options.QualityRange.Min + options.QualityRange.Max)/2)
            # Setup FramRate
            video_encoder_configuration.RateControl.FrameRateLimit = min(options.H264.FrameRateRange.Max, self.fps)
            # Setup Gov Lenght
            #video_encoder_configuration = max(min(options.H264.GovLengthRange.Max, self.fps), options.H264.GovLengthRange.Min)


            # Create request type instance
            request = media_service.create_type('SetVideoEncoderConfiguration')
            request.Configuration = video_encoder_configuration
            # ForcePersistence is obsolete and should always be assumed to be True
            request.ForcePersistence = True

            # Set the video encoder configuration
            media_service.SetVideoEncoderConfiguration(request)
        except Exception as e:
            #-----------------------------------------------------------
            log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.ERROR,
                                                text=f"error happend in setup camera {self.name}: {e}", 
                                                code="FCSC000")
            self.logger.create_new_log(message=log_msg)
            #-----------------------------------------------------------


    
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
          #-----------------------------------------------------------
          log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.DEBUG,
                                            text=f"ffmpegCamera build temp folder for camera {self.name}: {output_dir}", 
                                            code="FCBP000")
          self.logger.create_new_log(message=log_msg)
          #-----------------------------------------------------------
          os.makedirs(output_dir)

        fname = f'video_{self.loop_index}_{self.name}' + '_%04d.mp4'
        self.loop_index+=1
        return output_dir, fname
    
    def build_and_run_stream(self,rstp_url, output_path):
        self.proccess = None
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
                    #    crf=50,
                    #    preset='faster',  # کاهش سرعت پردازش
                    #    tune='zerolatency'
                     )
        
        stream = ffmpeg.overwrite_output(stream)

        try:
            self.proccess = ffmpeg.run(stream, quiet=False, ) 
            #-----------------------------------------------------------
            log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.WARNING,
                                           text=f"ffmpeg run output {self.name}: {self.proccess}", 
                                           code="FCR001")
            self.logger.create_new_log(message=log_msg)
            #-----------------------------------------------------------        
        except ffmpeg.Error as e:
            #-----------------------------------------------------------
            log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.ERROR,
                                               text=f"error occured in build_and_run_stream: {e.stderr.decode()}", 
                                               code="FCBARS000")
            self.logger.create_new_log(message=log_msg)
            #-----------------------------------------------------------
        except KeyboardInterrupt:
            #-----------------------------------------------------------
            log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.ERROR,
                                               text=f"recoed stop manualy {self.name}", 
                                               code="FCBARS001")
            self.logger.create_new_log(message=log_msg)
            #-----------------------------------------------------------
    def terminate_ffmpeg(self,):
        #-----------------------------------------------------------
        log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.DEBUG,
                                               text=f"terminate ffmpeg {self.name}", 
                                               code="FCTF000")
        self.logger.create_new_log(message=log_msg)
        #-----------------------------------------------------------
        if self.proccess is not None:
            try:
                self.proccess.terminate()
            except Exception as e:
                #-----------------------------------------------------------
                log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.ERROR,
                                                    text=f"terminate ffmpeg {self.name}:{e}", 
                                                    code="FCTF001")
                self.logger.create_new_log(message=log_msg)
                #-----------------------------------------------------------
    def stop_thread(self,):
        self.runing =False

    def run(self,):
      self.runing = True
      #-----------------------------------------------------------
      log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.DEBUG,
                                         text=f"run camera thread :{self.name}", 
                                         code="FCR000")
      self.logger.create_new_log(message=log_msg)
      #-----------------------------------------------------------
      while self.runing:
        #-----------------------------------------------------------
        log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.DEBUG,
                                           text=f"try connect to camera {self.name}", 
                                           code="FCR001")
        self.logger.create_new_log(message=log_msg)
        #-----------------------------------------------------------
        rstp_url = self.get_stream_url() 
        #self.setup_camera() 
        if rstp_url is None:
           time.sleep(5)
           continue
        
        try:
            output_dir, output_fname = self.build_path()
            output_path = os.path.join(output_dir, output_fname)
            
        except Exception as e:
           #-----------------------------------------------------------
           log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.ERROR,
                                              text=f"error happend in ffmpegCamera build path {self.name}: {e}", 
                                              code="FCR002")
           self.logger.create_new_log(message=log_msg)
           #-----------------------------------------------------------
           continue

        
        #-----------------------------------------------------------
        log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.DEBUG,
                                           text=f"connect to camera {self.name} success", 
                                           code="FCR003")
        self.logger.create_new_log(message=log_msg)
        #-----------------------------------------------------------
        try:
           self.build_and_run_stream(rstp_url, output_path)
        except Exception as e:
           #-----------------------------------------------------------
            log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.ERROR,
                                           text=f"error happend in run build_and_run_stream ffmpegCamera {self.name}: {e}", 
                                           code="FCR004")
            self.logger.create_new_log(message=log_msg)
            #-----------------------------------------------------------
        
        #-----------------------------------------------------------
        log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.DEBUG,
                                           text=f"stream stop {self.name}", 
                                           code="FCR005")
        self.logger.create_new_log(message=log_msg)
        #-----------------------------------------------------------

    
    
           
        

    

        # command  = ffmpeg.compile(stream)

        
    

# grabber = ffmpegCamera('left', 'admin', 'Milad1375422@', train_id='11BGDEF', ip='192.168.1.2', fps=25)
# grabber.start()

