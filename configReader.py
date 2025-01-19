import json
import os

class configReader:
    PATH = 'config.json'

    def __init__(self) -> None:
        self.config = {}
        self.is_valid = False
        self.load()
        
        self.max_allowed_storage = float(self.config['max_allowed_storage'])
        self.cameras:list[dict] = self.config['cameras']
        self.train_id = self.config['train_id']
        self.video_duration = int(self.config['video_duration'])
        self.video_fps = int(self.config['video_fps'])
        self.video_codec = self.config['video_codec']
        self.motion = self.config['motion']

        



    def load(self,):
        if os.path.exists(configReader.PATH):
            with open(self.PATH) as f:
                self.config = json.load(f)
                self.is_valid = True

