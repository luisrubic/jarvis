[app]
title = Jarvis
package.name = jarvis
package.domain = com.jarvis.app

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,ttf
version = 0.1
requirements = python3,kivy
orientation = portrait

[buildozer]
log_level = 2
warn_on_root = 0

[app:permissions]
INTERNET

[app:android]
android.api = 34
android.build_tools_version = 34.0.0
android.ndk_version = 25b
android.minapi = 21
android.accept_sdk_license_agreement = True
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
p4a.bootstrap = sdl2

# Se usi altre librerie aggiungile qui es: requirements = python3,kivy,kivymd,requests,plyer
