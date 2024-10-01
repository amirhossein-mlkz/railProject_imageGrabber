import threading
import os
import time
import shutil


from persiantools.jdatetime import JalaliDateTime


class moviesSorting(threading.Thread):
    
    def __init__(self, train_id:str, cycle_time_sec:int, src_path:str, dst_path:str) -> None:
        super().__init__()
        self.src_path = src_path
        self.dst_path = dst_path
        self.train_id = train_id
        self.cycle_time_sec = cycle_time_sec

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
                continue
            if old[fname]['size'] == new[fname]['size']:
                res.append( new[fname])
        return res

    
    def move_files(self, files:list[dict]):
        for f in files:
            try:
                res_path, res_fname = self.generate_res_path(f)
                if not os.path.exists(res_path):
                    os.makedirs(res_path)

                res_full_path = os.path.join(res_path, res_fname)
                shutil.move(f['full_path'], res_full_path)

            except Exception as e:
                print(e)

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
        res_fname = res_fname +  '_' + self.train_id + '_' + camera_name + file_extension

        return path, res_fname
    
    def run(self,):
        while True:
            if not os.path.exists(self.src_path):
                time.sleep(10)
                continue
            
            t = time.time()
            self.current_files = self.get_files_list()

            files_should_move = self.check_not_changed_files(self.previous_files, self.current_files)

            self.previous_files = self.current_files.copy()
                
            if len(files_should_move):
                self.move_files(files_should_move)

            t = time.time() - t
            t = round(t)
            wait_time = max(self.cycle_time_sec - t, 1)
            time.sleep(wait_time)



if __name__ == '__main__':
    ms = moviesSorting('11BGC11', 10, 'temp_videos', 'c://image_share')
    ms.run()