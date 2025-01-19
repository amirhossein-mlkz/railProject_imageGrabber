import os
import shutil
import sys
import time
import cv2
from PySide6 import QtCore as sQtCore
from PySide6.QtGui import QFont,QIcon

from PySide6.QtWidgets import QStatusBar
from PySide6.QtWidgets import QMainWindow as sQMainWindow
from PySide6.QtCore import QTimer
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QApplication,

)
import dorsa_logger

from configReader import configReader
from pathsConstans import pathsConstans
from main import App
from UIFiles.main_UI import Ui_MainWindow

class ImageDisplayApp(sQMainWindow):
    """Main application window."""
    def __init__(self):
        super(ImageDisplayApp, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # self.all_style_repoblish()
        self.language = 'English'

        self.setWindowTitle("Sepanta RailWay Monitoring")
        # window setup
        self.setWindowTitle("Iran RailWay Monitoring")
        # Set the window icon
        self.setWindowIcon(QIcon(":/icons/icons/download.png"))

        # window setup
        flags = sQtCore.Qt.WindowFlags(
            sQtCore.Qt.FramelessWindowHint
        )  # remove the windows frame of ui
        self.pos_ = self.pos()
        self.setWindowFlags(flags)
        self._old_pos = None

        # Create a QStatusBar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Set the maximum height for the status bar (e.g., 30 pixels)
        self.status_bar.setMaximumHeight(10)


                # Set the background color and text color using a stylesheet
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background-color: #262632;  /* Background color */
            }
        """)

        self.resize(800, 600)
        self.create_logger()

        self.ui.btn_show_live.clicked.connect(self.set_show_live)

        # Create a QTimer for mainchecker new version of main loop
        self.timer_main_checker = QTimer(self)
        self.timer_main_checker.timeout.connect(self.mainchecker)  # Connect the timeout signal to the function

        
        self.update_config = UpdateConfigThread(parent=self)
        self.update_config.config_updated.connect(self.update_rec_status)
        self.update_config.finished.connect(self.create_app_object)
        self.update_config.start()

    

        # Timer Setup
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        rem_time = self.ui.spinBox.value()
        self.remaining_time = 120  # Set the countdown duration (in seconds), here 2 minutes

        # self.ui.btn_show_live.setDisabled(True)

        self.ui.maximize_btn.clicked.connect(self.toggle_maximize)
        self.ui.minimize_btn.clicked.connect(self.minimize_win)
        self.ui.btn_side_settings.clicked.connect(self.set_page_setting)
        self.ui.btn_side_playback.clicked.connect(self.set_page_playback)




        # self.timer.start(5000)  # Interval in milliseconds (5000 ms = 5 seconds)


    def set_page_setting(self):
        self.ui.pages_stackwidget.setCurrentIndex(1)

    def set_page_playback(self):
        self.ui.pages_stackwidget.setCurrentIndex(0)



    def minimize_win(self):
        self.showMinimized()


        
    def toggle_maximize(self):
        """Function to toggle between maximizing and restoring the window."""
        if self.isMaximized():
            self.showNormal()  # Restore the window to its original size
        else:
            self.showMaximized()  # Maximize the window



    def set_show_live(self):
        """Start reverse timer and perform work when time is up."""
        if not self.timer.isActive():
            rem_time = self.ui.spinBox.value()
            self.remaining_time = 120  # Reset to 2 minutes
            self.update_timer_label()
            self.timer.start(1000)  # Timer updates every 1 second
            self.ui.btn_show_live.setDisabled(True)
            self.app_thread.set_show_flag(mode=True)

    def update_timer(self):
        """Update the timer display and check when time is up."""
        self.remaining_time -= 1
        self.update_timer_label()

        if self.remaining_time <= 0:
            self.timer.stop()  # Stop the timer
            self.perform_work()  # Perform the desired action

    def update_timer_label(self):
        """Update the timer label in mm:ss format."""
        minutes = self.remaining_time // 60
        seconds = self.remaining_time % 60
        self.ui.btn_show_live.setText(f"Live Time : {minutes:02}:{seconds:02}")

    def perform_work(self):
        """Perform work after the timer ends."""
        self.ui.btn_show_live.setText("Show Live")
        self.ui.btn_show_live.setEnabled(True)
        self.app_thread.set_show_flag(mode=False)





    def create_qt_image(self,frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        return qt_image

    def show_image1(self,frame):
        """Process the raw frame and display it."""
        qt_image = self.create_qt_image(frame=frame)
        # Update the QLabel
        self.ui.lbl_camera_1.setPixmap(QPixmap.fromImage(qt_image))
    def show_image2(self,frame):
        """Process the raw frame and display it."""
        qt_image = self.create_qt_image(frame=frame)
        # Update the QLabel
        self.ui.lbl_camera_2.setPixmap(QPixmap.fromImage(qt_image))
    def show_image3(self,frame):
        """Process the raw frame and display it."""
        qt_image = self.create_qt_image(frame=frame)
        # Update the QLabel
        self.ui.lbl_camera_3.setPixmap(QPixmap.fromImage(qt_image))
    def show_image4(self,frame):
        """Process the raw frame and display it."""
        qt_image = self.create_qt_image(frame=frame)
        # Update the QLabel
        self.ui.lbl_camera_4.setPixmap(QPixmap.fromImage(qt_image))


    def update_rec_status(self,msg,mode=True):
        # print('msg'*80,msg)
        if mode:
            self.ui.lbl_status.setStyleSheet(""" color:green  """)
        else:
            self.ui.lbl_status.setStyleSheet(""" color:red  """)
        self.ui.lbl_status.setText(msg)


    def create_logger(self):

        
        self.logger =  dorsa_logger.logger(
                                            main_folderpath=pathsConstans.SELF_LOGS_SHARE_FOLDER,
                                            date_type=dorsa_logger.date_types.AD_DATE,
                                            date_format=dorsa_logger.date_formats.YYMMDD,
                                            time_format=dorsa_logger.time_formats.HHMMSS,
                                            file_level=dorsa_logger.log_levels.DEBUG,
                                            console_level=dorsa_logger.log_levels.DEBUG,
                                            console_print=True,
                                            current_username="admin",
                                            line_seperator='-')



    def create_app_object(self):

        self.config = self.update_config.config
        self.config_mtime = self.update_config.config_mtime


        # Create the thread and worker
        self.app_thread = App(logger=self.logger, config=self.config, config_mtime=self.config_mtime)
        self.app_thread.signal_cam_0.connect(self.show_image1)
        self.app_thread.signal_cam_1.connect(self.show_image2)
        self.app_thread.signal_cam_2.connect(self.show_image3)
        self.app_thread.signal_cam_3.connect(self.show_image4)
        self.app_thread.vid_gear_load_grabbers()
        self.app_thread.start()
     
        self.timer_main_checker.start(5000)
        # self.app_thread.start_test()
        self.ui.btn_show_live.setEnabled(True)
        


    def mainchecker(self):
        self.app_thread.minCheckker()






    def start_camera(self, camera_index):
        # Stop any existing camera threads for the selected camera
        if self.camera_threads[camera_index] is not None:
            self.camera_threads[camera_index].stop()
            self.camera_threads[camera_index] = None

        # Start a new camera thread
        # thread = CameraThread(camera_index, camera_index)
        # thread.frame_signal.connect(self.update_image)
        # thread.status_signal.connect(self.update_status)
        # thread.start()
        # self.camera_threads[camera_index] = thread

    def update_image(self, label_index, image):
        # Update the QLabel with the new frame
        self.image_labels[label_index].setPixmap(QPixmap.fromImage(image))

    def update_status(self, message):
        # Update the status line edit
        self.status_line_edit.setText(message)

    def closeEvent(self, event):
        # Stop all camera threads on close
        for thread in self.camera_threads:
            if thread is not None:
                thread.stop()
        event.accept()





    def mousePressEvent(self, event):
        if event.button() == sQtCore.Qt.LeftButton and not self.isMaximized():
            # accept event only on top bar
            if (
                event.position().y() <= self.ui.softeware_top_frame.height()
            ):
                self._old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        if event.button() == sQtCore.Qt.LeftButton:
            self._old_pos = None



    def mouseMoveEvent(self, event):
        if not self._old_pos:
            return
        delta = sQtCore.QPoint(event.globalPosition().toPoint() - self._old_pos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self._old_pos = event.globalPosition().toPoint()




class UpdateConfigThread(QThread):
    # Signals to communicate with the main thread
    config_updated = Signal(str)  # Emits the result of the loop to update the label
    finished = Signal()           # Emits when the thread finishes

    def __init__(self, parent=None):
        super().__init__(parent)
        self.pathsConstans = pathsConstans  # Use your variables here
        self.configReader = configReader    # Adjust as needed
        self.logger = parent.logger         # Assuming logger is passed via the parent




    def start(self):
    
        config_mtime=None
        while True:
            if os.path.exists(pathsConstans.SELF_CONFIG_SHARE_PATH):
                config_mtime = os.path.getmtime(pathsConstans.SELF_CONFIG_SHARE_PATH)
                try:
                    shutil.copy(pathsConstans.SELF_CONFIG_SHARE_PATH, configReader.PATH)
                except Exception as e:
                    #-----------------------------------------------------------
                    log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.ERROR,
                                                text=f"""copy config error {e}""", 
                                                code="AUC000")
                    self.logger.create_new_log(message=log_msg)
                    #-----------------------------------------------------------

            if os.path.exists(configReader.PATH):
                config = configReader()




            if config is not None:
                #-----------------------------------------------------------
                log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.DEBUG,
                                            text=f"config update success", 
                                            code="Ainit000")
                self.logger.create_new_log(message=log_msg)
                #-----------------------------------------------------------
                self.config_updated.emit("Config update success!")
                break
            
            else:
                #-----------------------------------------------------------
                log_msg = dorsa_logger.log_message(level=dorsa_logger.log_levels.ERROR,
                                            text=f"no config exists", 
                                            code="Ainit000")
                self.config_updated.emit("No config exists. Retrying...")
                self.logger.create_new_log(message=log_msg)
                #-----------------------------------------------------------
                time.sleep(30)


        self.config = config
        self.config_mtime = config_mtime
        self.finished.emit()

        # return config,config_mtime


if __name__ == "__main__":



    app = QApplication(sys.argv)
    main_window = ImageDisplayApp()
    main_window.show()
    sys.exit(app.exec())
