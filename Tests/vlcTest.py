#pip install python-vlc
import vlc
import time

# ایجاد یک پخش‌کننده VLC
instance:vlc.Instance = vlc.Instance('--network-caching=50')
player = instance.media_player_new()
media = instance.media_new('rtsp://192.168.1.2/media/video1')

player.set_media(media)

# شروع پخش جریان RTSP
player.play()

# پخش برای مدت زمان معینی
time.sleep(1000)

# # توقف پخش
# player.stop()