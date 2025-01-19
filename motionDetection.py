import time
from PySide6.QtCore import QObject, Signal
import cv2
import numpy as np

class motionDetection(QObject):
    motion_signal = Signal(bool)

    def __init__(self, frames:list[np.ndarray], thresh_light, thresh_motion):
        super().__init__()
        self.frames = frames
        self.thresh_light = thresh_light
        self.thresh_motion = thresh_motion

    def check_motion(self,):
        result = True

        self.gray_frames = []
        # print('start check')
        for frame in self.frames:
            gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            self.gray_frames.append(gray_frame)

        for i in range(len(self.gray_frames)-1):
            prev_frame =  self.gray_frames[i]

            new_frame =  self.gray_frames[i+1]
            diff = np.abs(new_frame - prev_frame)
            diff[diff< self.thresh_light] = 0
            motion_value = diff.sum() / 255
            result = result and (motion_value>=self.thresh_motion)
         
            if not result:
                break
            
        time.sleep(0.005)


        self.motion_signal.emit(result)

