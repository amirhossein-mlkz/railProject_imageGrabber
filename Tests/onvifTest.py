from onvif import ONVIFCamera #pip install onvif-zeep


# اتصال به دوربین با استفاده از ONVIF
camera = ONVIFCamera('192.168.1.2', 80, 'admin', 'Milad1375422@', 'Tests/wsdl')

# دریافت جریان‌های رسانه‌ای
media_service = camera.create_media_service()
profiles = media_service.GetProfiles()
stream_setup = {
    'Stream': 'RTP-Unicast',  # یا 'RTP-Multicast'
    'Transport': {
        'Protocol': 'RTSP'  # یا 'UDP' یا 'TCP'
    }
}

# درخواست URL جریان RTSP با استفاده از StreamSetup
stream_uri = media_service.GetStreamUri({
    'StreamSetup': stream_setup,
    'ProfileToken': profiles[0].token
})

print(stream_uri.Uri)