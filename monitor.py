import subprocess
import time
import psutil


FILE_PATH = r'imageGrabber.exe'

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

def run_main_py():
    """Start main.py as an administrator and return the process."""
    # Set the directory where main.py is located
    script_directory = r'C:\imageGrabber'

    # Use PowerShell to run the script with elevated privileges
    return subprocess.Popen(
        ["powershell", "-Command", "Start-Process", FILE_PATH, "-Verb", "runAs"],
        cwd=script_directory  # Set the working directory
    )

def terminate_ffmpeg_processes():
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] == 'ffmpeg.exe':
                print(f'Terminating FFmpeg process with PID: {proc.info["pid"]}')
                proc.terminate()
        except Exception as e:
            print(e)

def monitor_main_py():
    """Monitor the main.py process and restart it if it closes."""
    terminate_ffmpeg_processes()
    time.sleep(20)
    run_main_py()  # Start main.py
    print(f"Started main.py")
    time.sleep(3)  # Wait for 30 seconds before restarting


    while True:
        if not is_main_py_running():  # Check if main.py is still running
            terminate_ffmpeg_processes()
            print("closed. Restarting in 5 seconds...")
            time.sleep(10)  # Wait for 5 seconds before restarting
            run_main_py()  # Restart main.py
            print(f"Restarted main.py")
        time.sleep(5)  # Check every 30 second



if __name__ == "__main__":
    monitor_main_py()
