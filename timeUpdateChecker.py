import time
import os
import threading
import signal
import json
import subprocess
from datetime import datetime

import dorsa_logger

class timeUpdateChecker(threading.Thread):


    def __init__(self, path, logger:dorsa_logger.logger) -> None:
        super(timeUpdateChecker, self).__init__()
        self.path = path
        self.logger = logger
      

    
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



    def set_system_datetime(self, new_datetime: datetime):
        try:
            # تاریخ و زمان را به رشته‌های فرمت شده تبدیل می‌کنیم
            date_str = new_datetime.strftime('%Y-%m-%d')
            time_str = new_datetime.strftime('%H:%M:%S')

            # تنظیم تاریخ و زمان با استفاده از PowerShell
            subprocess.run([
                "powershell", "-Command",
                f'Set-Date -Date "{date_str} {time_str}"'
            ], shell=True, check=True)

            return True
        
        except Exception as e:
            # لاگ خطا در صورت بروز مشکل
            log_msg = dorsa_logger.log_message(
                level=dorsa_logger.log_levels.ERROR,
                text=f"Error on setting Windows time: {e}",
                code="TUCSSD000"
            )
            self.logger.create_new_log(message=log_msg)
            return False

        


    def check_time_setting(self,):
        if os.path.exists(self.path):
            #-----------------------------------------------------------
            log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.DEBUG,
                                            text=f"clock setting detected", 
                                            code="TUCCTS000")
            self.logger.create_new_log(message=log_msg)
            #-----------------------------------------------------------
            with open(self.path, "r") as file:
                setting:dict = json.load(file)
            
            timeozne = setting.get('timezone')
            if timeozne:
                self.set_timezone(timeozne)  
            
            
                src_time_str = setting.get('src')
                dst_time_str = setting.get('dst')
                if src_time_str and dst_time_str:
                    
                    src_time = datetime.strptime(src_time_str, '%Y-%m-%d_%H-%M-%S')
                    dst_time = datetime.strptime(dst_time_str, '%Y-%m-%d_%H-%M-%S')
                    realtime_dst_time = (dst_time - src_time) + datetime.now()
                    flag = self.set_system_datetime(realtime_dst_time)

                    if flag:
                        #-----------------------------------------------------------
                        log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.DEBUG,
                                                            text=f"clock setting detected", 
                                                            code="TUCCTS000")
                        self.logger.create_new_log(message=log_msg)
                        #-----------------------------------------------------------
            os.remove(self.path)

    
    def close_software(self,):
        #-----------------------------------------------------------
        log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.DEBUG,
                                            text=f"close sofware for config updated", 
                                            code="CUCCCS000")
        self.logger.create_new_log(message=log_msg)
        #-----------------------------------------------------------
        os.kill(os.getpid(), signal.SIGTERM)
    

    def run(self, ):
        #-----------------------------------------------------------
        log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.DEBUG,
                                            text=f"config file update checker thread run", 
                                            code="CUCR000")
        self.logger.create_new_log(message=log_msg)
        #-----------------------------------------------------------
        while True:
            self.check_time_setting()

            time.sleep(5)
