import os
import sys
import time
import threading
from persiantools.jdatetime import JalaliDateTime , timedelta
import shutil

class Space:
    def __init__(self, bytes) -> None:
        self.bytes = int(bytes)

    def toGB(self,):
        return round(self.bytes / pow(1024,3),2)
    
    def toMB(self,):
        return round(self.bytes / pow(1024,2),2)
    
    def toKB(self,):
        return round(self.bytes / pow(1024,1),2)
    
    def toByte(self,):
        return self.bytes
    
    def __add__(self, other):
        return Space(self.bytes + other.bytes)
    
    def __add__(self, other):
        return Space(self.bytes - other.bytes)
    
    def __eq__(self, other):
        return self.bytes == other.bytes

    def __lt__(self, other):
        return self.bytes < other.bytes

    def __gt__(self, other):
        return self.bytes > other.bytes


    def __str__(self) -> str:
        return f'GB: {self.toGB()}'
    







class storageManager(threading.Thread):

    def __init__(self, path, max_usage=0.8, cleaning_evry_sec=2000) -> None:
        super().__init__()

        self.path = path
        self.max_usage = max_usage
        self.cleaning_evry_sec = cleaning_evry_sec

        self.last_cleaning_time = JalaliDateTime.now()
        self.last_cleaning_time = self.last_cleaning_time.replace(year= 1376)


    def get_disk_usage(self, path):
        total, used, free = shutil.disk_usage(path)
        total = Space(total)
        used = Space(used)
        free = Space(free)
        max_allowed = Space( total.toByte() * self.max_usage)
        return total, used, free, max_allowed
    

    def remove_empty_dirs(self, directory):
        # لیست تمام محتویات دایرکتوری را می‌گیرد
        is_empty = True
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            
            # اگر محتویات یک زیرشاخه باشد، به صورت بازگشتی آن را بررسی می‌کنیم
            if os.path.isdir(item_path):
                if not self.remove_empty_dirs(item_path):
                    is_empty = False  # اگر زیرشاخه خالی نبود، این دایرکتوری را حذف نمی‌کنیم
            else:
                is_empty = False  # اگر فایلی وجود داشت، دایرکتوری خالی نیست
        
        # اگر این دایرکتوری خالی بود، آن را حذف می‌کنیم
        if is_empty:
            os.rmdir(directory)
            print(f"Removed empty directory: {directory}")
            return True  # نشان می‌دهد که این دایرکتوری حذف شد
        else:
            return False  # نشان می‌دهد که این دایرکتوری حذف نشد
    

    def __sort_file_number(self, files:list[str]):
        def key(x):
            try:
                return int(x)
            except:
                return 0
        files.sort(key=key)
        return files


    def get_lasts_files(self,path, n=1) -> list[list[str]]:
        results = []
        for train in os.listdir(path):
            train_path = os.path.join(self.path, train)
            if not os.path.isdir(train_path):
                continue

            for cam in os.listdir(train_path):
                cam_path = os.path.join(train_path, cam)
                if not os.path.isdir(cam_path):
                    continue
                
                years = os.listdir(cam_path)
                years = self.__sort_file_number(years)

                last_hours_paths_per_cam = []

                for year in years:
                    year_path = os.path.join(cam_path, year)
                    if not os.path.isdir(year_path):
                        continue
                    months = os.listdir(year_path)
                    months = self.__sort_file_number(months)
                    for month in months:
                        month_path = os.path.join(year_path, month)
                        if not os.path.isdir(month_path):
                            continue
                        days = os.listdir(month_path)
                        days = self.__sort_file_number(days)
                        for day in days:
                            day_path = os.path.join(month_path, day)
                            if not os.path.isdir(day_path):
                                continue
                            hours = os.listdir(day_path)
                            hours = self.__sort_file_number(hours)

                            for hour in hours:
                                houre_path = os.path.join(day_path, hour)
                                if not os.path.isdir(houre_path):
                                    continue
                                last_hours_paths_per_cam.append(houre_path)
                                if len(last_hours_paths_per_cam) >= n:
                                    break
                            if len(last_hours_paths_per_cam) >= n:
                                break
                        if len(last_hours_paths_per_cam) >= n:
                                break
                    if len(last_hours_paths_per_cam) >= n:
                                break
                
                results.append(last_hours_paths_per_cam)
        return results
                
                
    def remove(self, path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.isfile(path):
            os.remove(path)


    def run(self,):
        while True:
            try:
                now = JalaliDateTime.now()
                delta:timedelta = now - self.last_cleaning_time

                if delta.total_seconds() < self.cleaning_evry_sec:
                    time.sleep(1)
                    continue
                #-------------------------------------------------------------------------------------------
                self.last_cleaning_time = now
                print("checking storage")
                total, used, free, max_allowed= self.get_disk_usage(self.path)
                print(f"total: {total.toGB()} ---- used: {used.toGB()} ---- free:{free.toGB()}  ----- allowed: {max_allowed.toGB()}")
                
                while used > max_allowed:
                    print('Cleaning')
                    
                    try:
                        res = self.get_lasts_files(self.path, 1) #get first 50 hours folder of each camera
                    except Exception as e:
                        print(e)
                        break

                    is_any_file_to_remove = False
                    for camera_last_hours in res:
                        if len(camera_last_hours):
                            is_any_file_to_remove = True

                        for path in camera_last_hours:
                            try:
                                print(f'try remove {path}')
                                self.remove(path)
                                print('remove success')
                            except Exception as e:
                                print(f'Remove failed :{e}')      

                    if not is_any_file_to_remove:
                        print('WARNING: there is not any file to remove')
                        break
                    total, used, free, max_allowed= self.get_disk_usage(self.path)
                    #end while remove
                #-------------------------------------------------------------------------------------------
                total, used, free, max_allowed= self.get_disk_usage(self.path)
                print('Statistics after cleaning:')
                print(f"- total: {total.toGB()} ---- used: {used.toGB()} ---- free:{free.toGB()}  ----- allowed: {max_allowed.toGB()}")
                #-------------------------------------------------------------------------------------------
                try:
                    print('remove empty files')
                    self.remove_empty_dirs(self.path)
                except Exception as e:
                    print(f'remove empty failed {e}')

            except Exception as e:
                print(e)





            self.last_cleaning_time
    

if __name__ == '__main__':
    sm = storageManager('C:\image_share', max_usage=0.17)
    sm.daemon = True
    sm.start()
    while True:
        pass