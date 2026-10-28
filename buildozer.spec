[app]
title = Jarvis
package.name = jarvis
package.domain = org.jarvis

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

version = 0.1
version.regex = __version__ = ['"]([^'"]+)['"]
version.filename = %(source.dir)s/main.py

requirements = python3,kivy,plyer,pyjnius,pillow

orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2

[app:android]
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license_agreement = True

# Non mettere qui pytesseract, requests, SpeechRecognition!
# Li aggiungeremo dopo dentro main.py

p4a.bootstrap = sdl2
p4a.port = 8000

[app:ios]
# lascia vuoto
