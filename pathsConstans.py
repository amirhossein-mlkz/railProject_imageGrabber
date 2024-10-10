import os

class pathsConstans:

    

    SHARE_FOLDER = "c:/rail_share"
    TEMP_VIDEOS_FOLDER = "temp_videos"

    IMAGES_SHARE_FOLDER = os.path.join(SHARE_FOLDER,'images')
    UTILS_SHARE_FOLDER = os.path.join(SHARE_FOLDER,'utils')
    LOGS_SHARE_FOLDER = os.path.join(UTILS_SHARE_FOLDER,'logs')
    CONFIG_SHARE_PATH = os.path.join(UTILS_SHARE_FOLDER,'config.json')
