import os

class pathsConstans:

    

    SHARE_FOLDER = "c:/rail_share"
    TEMP_VIDEOS_FOLDER = "temp_videos"
    MANIFEST_NAME = 'manifest.json'
    UPDATER_NAME = 'updater.exe'
    UPDATE_NAME = 'update.rar'


    SELF_IMAGES_SHARE_FOLDER = os.path.join(SHARE_FOLDER,'images')
    #----------------------------------------------------------------
    SELF_UTILS_SHARE_FOLDER = os.path.join(SHARE_FOLDER,'utils')
    SELF_LOGS_SHARE_FOLDER = os.path.join(SELF_UTILS_SHARE_FOLDER,'logs')
    SELF_CONFIG_SHARE_PATH = os.path.join(SELF_UTILS_SHARE_FOLDER,'config.json')
    SELF_CLOCK_SHARE_PATH = os.path.join(SELF_UTILS_SHARE_FOLDER,'clock.json')

    #----------------------------------------------------------------
    SELF_UPDATES_PATH = os.path.join(SHARE_FOLDER,'updates')
    SELF_UPDATE_IMAGEGRABBER_PATH = os.path.join(SELF_UPDATES_PATH,'imageGrabber')
    #----------------------------------------------------------------

