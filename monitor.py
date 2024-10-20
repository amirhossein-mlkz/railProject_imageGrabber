import subprocess
import time
import psutil


FILE_PATH = r'main.py'

def is_main_py_running():
    """Check if main.py is running by inspecting all Python processes."""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if 'python' in proc.info['name']:  # Check if it's a Python process
            if FILE_PATH in proc.info['cmdline']:  # Check if it's running main.py
                return True  # main.py is running
    return False  # main.py is not running

def run_main_py():
    """Start main.py as an administrator and return the process."""
    # Set the directory where main.py is located
    script_directory = r'C:\Users\milad\Desktop\PythonWork\RailWay\railProject_imageGrabber'

    # Use PowerShell to run the script with elevated privileges
    return subprocess.Popen(
        ["powershell", "-Command", "Start-Process", "python", "'main.py'", "-Verb", "runAs"],
        cwd=script_directory  # Set the working directory
    )

def monitor_main_py():
    """Monitor the main.py process and restart it if it closes."""
    run_main_py()  # Start main.py
    print(f"Started main.py")
    time.sleep(30)  # Wait for 30 seconds before restarting


    while True:
        if not is_main_py_running():  # Check if main.py is still running
            print("main.py closed. Restarting in 5 seconds...")
            time.sleep(5)  # Wait for 5 seconds before restarting
            run_main_py()  # Restart main.py
            print(f"Restarted main.py")
        time.sleep(30)  # Check every 30 second



if __name__ == "__main__":
    monitor_main_py()
