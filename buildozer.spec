[app]
title = JARVIS
package.name = jarvis
package.domain = com.jarvis.app
source.dir = .
source.include_exts = py,png,jpg,kv,json
version = 0.1
requirements = python3,kivy,plyer,pyjnius,pillow,pytesseract,requests,SpeechRecognition
orientation = portrait

[buildozer]
log_level = 2

[app:android]
permissions = CALL_PHONE,SEND_SMS,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,CAMERA,RECORD_AUDIO,VIBRATE,INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.build_tools_version = 33.0.2
android.accept_sdk_license_agreement = True
android.archs = arm64-v8a, armeabi-v7a