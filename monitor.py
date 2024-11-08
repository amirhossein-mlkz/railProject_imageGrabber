import subprocess
import time
import psutil
import os
import json
import shutil

FILE_PATH = r'imageGrabber.exe'
UPDTER_NAME = r'updater.exe'
SRCIPT_DIRECTORY = r'C:\imageGrabber'
UPDATE_DIRECTORY = r'C:\imageGrabber\update'
UPDATER_PATH = os.path.join(UPDATE_DIRECTORY, UPDTER_NAME)
MANIFEST_JSON = 'manifest.json'


def is_main_py_running():
    """Check if main.py is running by inspecting all Python processes."""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if proc.info['cmdline'] is not None:  # Check if it's a Python process
            # print(proc.info['name'])
            if FILE_PATH in proc.info['name']:  # Check if it's running main.py
                print('Exist'*10)
                return True  # main.py is running
    print('NOT'*20)
    return False  # main.py is not running

def run_app():
    """Start main.py as an administrator and return the process."""
    # Set the directory where main.py is located

    # Use PowerShell to run the script with elevated privileges
    return subprocess.Popen(
        ["powershell", "-Command", "Start-Process", FILE_PATH, "-Verb", "runAs"],
        cwd=SRCIPT_DIRECTORY  # Set the working directory
    )

def run_updater():
    """Start main.py as an administrator and return the process."""
    # Set the directory where main.py is located

    # Use PowerShell to run the script with elevated privileges
    return subprocess.Popen(
        ["powershell", "-Command", "Start-Process", UPDTER_NAME, "-Verb", "runAs"],
        cwd=UPDATE_DIRECTORY  # Set the working directory
    )

def terminate_ffmpeg_processes():
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] == 'ffmpeg.exe':
                print(f'Terminating FFmpeg process with PID: {proc.info["pid"]}')
                proc.terminate()
        except Exception as e:
            print(e)

def add_last_update_to_manifest(path, mtime):
    # Load the JSON data from the file
    with open(path, 'r') as file:
        data = json.load(file)

    # Modify the data (for example, add a new item)
    data['last_updater'] = mtime

    # Write the updated data back to the JSON file
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)

def get_last_update_from_manifest(path):
    with open(path, 'r') as file:
        data:dict = json.load(file)
    return data.get('last_updater', 0)

def monitor_main_py():
    """Monitor the main.py process and restart it if it closes."""
    print('start monitor')
    try:
        if os.path.exists(UPDATE_DIRECTORY):
            shutil.rmtree(UPDATE_DIRECTORY)
            if os.path.exists(UPDATE_DIRECTORY):
                os.rmdir(UPDATE_DIRECTORY)
    except Exception as e:
        print(e)

    terminate_ffmpeg_processes()
    time.sleep(10)
    run_app()  # Start main.py
    print(f"Started main.py")
    time.sleep(3)  # Wait for 30 seconds before restarting

    
    last_update_modify = get_last_update_from_manifest(MANIFEST_JSON)

    while True:
        if not is_main_py_running():  # Check if main.py is still running
            terminate_ffmpeg_processes()
            print("closed. Restarting in 5 seconds...")
            time.sleep(10)  # Wait for 5 seconds before restarting

            if os.path.exists(UPDATER_PATH):
                mtime = os.path.getmtime(UPDATER_PATH)
                if mtime != last_update_modify:
                    add_last_update_to_manifest(MANIFEST_JSON, mtime)
                    print('RUN UPDATER')
                    run_updater()
                    time.sleep(10)
                    break
            else:
                run_app()  # Restart main.py
                print(f"Restarted main.py")
        time.sleep(5)  # Check every 30 second



if __name__ == "__main__":
    monitor_main_py()
