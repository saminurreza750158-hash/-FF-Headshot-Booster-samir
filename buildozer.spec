
[app]

title = FF HEADSHOT BOOSTER PANEL
package.name = ffheadshotbooster
package.domain = com.saminur

source.dir = .
source.include_exts = py,png,jpg,kv,json,txt
version = 1.0.0

requirements = python3==3.12.9,hostpython3==3.12.9,kivy==2.3.1

orientation = portrait
fullscreen = 0

android.permissions =
android.api = 36
android.minapi = 23
android.ndk = 29
android.archs = arm64-v8a
android.accept_sdk_license = True
android.debug_artifact = apk
android.release_artifact = aab

p4a.bootstrap = sdl2

[buildozer]

log_level = 2
warn_on_root = 1
p4a.branch = master
