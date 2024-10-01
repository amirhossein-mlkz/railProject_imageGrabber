import json


class configReader:
    PATH = 'config.json'

    def __init__(self) -> None:
        self.config = {}
        self.load()
        
        self.path:str = self.config['path']
        self.max_allowed_storage = float(self.config['max_allowed_storage'])
        self.cameras:list[dict] = self.config['cameras']
        self.train_id = self.config['train_id']
        self.output_type = self.config['output']
        self.video_duration = int(self.config['video_duration'])
        self.video_fps = int(self.config['video_fps'])
        self.motion = self.config['motion'].lower() == 'true'
        self.motion_sens = int(self.config['motion_sens'])
        self.temp_folder = self.config['temp_folder']

        



    def load(self,):
        with open(self.PATH) as f:
            self.config = json.load(f)
        

configReader()