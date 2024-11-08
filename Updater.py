import platform
import os,time
import shutil
import argparse
import subprocess



# Set up argument parsing
# parser = argparse.ArgumentParser(description="Process some inputs.")
# parser.add_argument("--app_path", type=str, help="path of application")
# parser.add_argument("--age", type=int, help="Your age")
# # Parse arguments
# args = parser.parse_args()
# # Use the arguments
# #APP_PATH = args.app_path
APP_PATH = r'c:\imageGrabber'
UPDATE_PATH = os.path.join(os.getcwd(), 'app')
UPDATE_IS_IN_APP_PATH = True
UPDATE_FOLDER_IN_APP = 'update'
BACKUP_DIR = r'c:\backup\imageGrabber'

class Backup:
    
    @staticmethod
    def mkdir_backup():
        if os.path.exists(BACKUP_DIR):
            try:
                shutil.rmtree(BACKUP_DIR)
            except Exception as e:
                print(e)
                return False

        os.makedirs(BACKUP_DIR)
        return True
    
    def save_backup():
        try:
            shutil.copytree(APP_PATH, BACKUP_DIR, dirs_exist_ok=True)

            if UPDATE_IS_IN_APP_PATH:
                bu_update_dir = os.path.join(BACKUP_DIR, UPDATE_FOLDER_IN_APP)
                shutil.rmtree(bu_update_dir)
                if os.path.exists(bu_update_dir):
                    os.rmdir(bu_update_dir)

            return True
        except Exception as e:
            print(e)
            return False
        
    def load_backup():

        contents = os.listdir(BACKUP_DIR)
        for name in contents:
            content_src_path = os.path.join(BACKUP_DIR, name)
            content_dst_path = os.path.join(APP_PATH, name)

            if os.path.isdir(content_src_path):
                shutil.copytree(content_src_path, content_dst_path,  dirs_exist_ok=True)
            else:
                shutil.copy2(content_src_path, content_dst_path)



class Update:

    @staticmethod
    def get_current_data():
        should_restor = [
            'config.json',
            'temp_videos'
        ]

        for name in should_restor:
            src_path = os.path.join(APP_PATH, name)
            dst_path = os.path.join(UPDATE_PATH, name)


            if os.path.isdir(src_path):
                shutil.copytree(src_path, dst_path,  dirs_exist_ok=True)
            else:
                shutil.copy2(src_path, dst_path)

    @staticmethod
    def remove_old_version():
        contents = os.listdir(APP_PATH)
        for name in contents:
            if UPDATE_IS_IN_APP_PATH and name == UPDATE_FOLDER_IN_APP:
                continue

            path = os.path.join(APP_PATH, name)
            if os.path.isdir(path):
                shutil.rmtree(path)
                if os.path.exists(path):
                    os.rmdir(path)
            
            else:
                os.remove(path)


    @staticmethod
    def replace_new_version():
        contents = os.listdir(UPDATE_PATH)
        for name in contents:
            src_path = os.path.join(UPDATE_PATH, name)
            dst_path = os.path.join(APP_PATH, name)

            if os.path.isdir(src_path):
                shutil.copytree(src_path, dst_path,  dirs_exist_ok=True)
            else:
                shutil.copy2(src_path, dst_path)


    @staticmethod
    def reset_system():
        # Get the current operating system
        current_os = platform.system()
        try:
            if current_os == "Windows":
                # Windows restart command
                subprocess.run(["shutdown", "/r", "/t", "10"], check=True)
            elif current_os == "Linux" or current_os == "Darwin": # Darwin is macOS
                # Linux and macOS restart command
                subprocess.run(["sudo", "reboot"], check=True)
            else:
                print("Unsupported operating system.")
        except Exception as e:
            print(f"An error occurred: {e}")



def main():
    print('start Updater')
    time.sleep(10)
    status = Backup.mkdir_backup()
    if not status:
        return
    print('makdir backup')
    
    
    status = Backup.save_backup()
    if not status:
        print('failed to backup')
        return
    print('backup save')

    
    try:
        Update.get_current_data()
        print('current data')
        Update.remove_old_version()
        print('remove old version')
        Update.replace_new_version()
        print('replace new version')
    except Exception as e:
        print(e)
        status = Backup.load_backup()
        print('backup load')

    Update.reset_system()



    
if __name__ == '__main__':
    main()
    