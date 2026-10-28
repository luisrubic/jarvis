[app]
title = Jarvis
package.name = jarvis
package.domain = org.jarvis

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

version = 0.1

requirements = python3,kivy,plyer,pyjnius,pillow

orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2

[app:android]
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license_agreement = True
android.sdk_path = /usr/local/lib/android/sdk
android.ndk_path = /usr/local/lib/android/sdk/ndk/27.3.13750724

p4a.bootstrap = sdl2
p4a.port = 8000
