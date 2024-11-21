import threading
import os
import time
import shutil

from persiantools.jdatetime import JalaliDateTime
import dorsa_logger 

class moviesSorting(threading.Thread):
    
    def __init__(self, train_id:str, cycle_time_sec:int, src_path:str, dst_path:str, logger:dorsa_logger.logger|None=None) -> None:
        super().__init__()
        self.src_path = src_path
        self.dst_path = dst_path
        self.train_id = train_id
        self.cycle_time_sec = cycle_time_sec
        self.logger = logger

        self.current_files = {}
        self.previous_files = {}

        self.daemon = True



    def get_files_list(self,):
        
        res = {}
        for camera_name in os.listdir(self.src_path):
            cam_path = os.path.join(self.src_path, camera_name)

            for fname in os.listdir(cam_path):
                path = os.path.join(cam_path, fname)
                ctime = os.path.getctime(path)
                creat_jdate_time = JalaliDateTime.fromtimestamp(ctime)
                mtime = os.path.getmtime(path)
                modify_jdate_time = JalaliDateTime.fromtimestamp(mtime)
                size = os.path.getsize(path)
                #-----------------------------------------------------------
                log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.DEBUG,
                                                   text=f"{fname} cam:{camera_name},ctime:{ctime} found in temp folder", 
                                                   code="MSGFL000")
                self.logger.create_new_log(message=log_msg)
                #-----------------------------------------------------------
                res[fname] = {
                        'name':fname,
                        'camera_name': camera_name,
                        'full_path': path,
                        'ctime': creat_jdate_time,
                        'mtime': modify_jdate_time,
                        'size':size,
                    }
                

        return res
    
    def check_not_changed_files(self, old:dict[str,dict], new:dict[str,dict]):
        res = []
        for fname in new.keys():
            if fname not in old:
                #-----------------------------------------------------------
                log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.DEBUG,
                                                   text=f"{fname} file is new", 
                                                   code="MSCNCF000")
                self.logger.create_new_log(message=log_msg)
                #-----------------------------------------------------------
                continue
            #-----------------------------------------------------------
            log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.DEBUG,
                                                   text=f"{fname} prev size:{old[fname]['size']} - new size:{new[fname]['size']}", 
                                                   code="MSCNCF001")
            self.logger.create_new_log(message=log_msg)
            #-----------------------------------------------------------
            if old[fname]['size'] == new[fname]['size']:
                res.append( new[fname])
        return res

    
    def move_files(self, files:list[dict]):
        for f in files:
            try:
                res_path, res_fname = self.generate_res_path(f)
                #-----------------------------------------------------------
                log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.DEBUG,
                                                   text=f"{f['name']} cam:{f['camera_name']} ctime:{f['ctime']} move to {res_path}//{res_fname}", 
                                                   code="MSMF000")
                self.logger.create_new_log(message=log_msg)
                #-----------------------------------------------------------
                if not os.path.exists(res_path):
                    os.makedirs(res_path)

                res_full_path = os.path.join(res_path, res_fname)
                shutil.move(f['full_path'], res_full_path)

                #-----------------------------------------------------------
                log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.DEBUG,
                                                   text="move done",
                                                   code="MSMF001")
                self.logger.create_new_log(message=log_msg)
                #-----------------------------------------------------------

            except Exception as e:
                #-----------------------------------------------------------
                log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.ERROR,
                                                   text=f"error happend for move temp file {e}", 
                                                   code="MSMF002")
                self.logger.create_new_log(message=log_msg)
                #-----------------------------------------------------------
                

    def generate_res_path(self, info:dict):
        ctime:JalaliDateTime = info['ctime']
        camera_name = info['camera_name']
        fname = info['name']

        path = os.path.join(
                            self.dst_path,
                            self.train_id,
                            camera_name,
                            str(ctime.year),
                            str(ctime.month),
                            str(ctime.day),
                            str(ctime.hour),
                            str(ctime.minute),
                        )

        _, file_extension = os.path.splitext(fname)

        res_fname = ctime.strftime('%Y-%m-%d_%H-%M-%S-%f')
        res_fname = f"{res_fname}_{self.train_id}_{camera_name}_new{file_extension}"

        return path, res_fname
    
    def run(self,):
        #-----------------------------------------------------------
        log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.DEBUG,
                                           text=f"moviesSorting thread start", 
                                           code="MSR000")
        self.logger.create_new_log(message=log_msg)
        #-----------------------------------------------------------
        while True:
            if not os.path.exists(self.src_path):
                #-----------------------------------------------------------
                log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.WARNING,
                                                   text=f"temp folder not exist :{self.src_path}", 
                                                   code="MSR001")
                self.logger.create_new_log(message=log_msg)
                #-----------------------------------------------------------
                time.sleep(10)
                continue
            
            t = time.time()
            self.current_files = self.get_files_list()

            files_should_move = self.check_not_changed_files(self.previous_files, self.current_files)

            self.previous_files = self.current_files.copy()
                
            if len(files_should_move):
                #-----------------------------------------------------------
                log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.WARNING,
                                                   text=f"start moving from temp folder :{files_should_move}", 
                                                   code="MSR002")
                self.logger.create_new_log(message=log_msg)
                #-----------------------------------------------------------
                self.move_files(files_should_move)

            t = time.time() - t
            t = round(t)
            wait_time = max(self.cycle_time_sec - t, 1)
            time.sleep(wait_time)



if __name__ == '__main__':
    ms = moviesSorting('11BGC11', 10, 'temp_videos', 'c://image_share')
    ms.run()