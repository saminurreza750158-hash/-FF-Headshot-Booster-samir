FF HEADSHOT BOOSTER PANEL — Android / Kivy project
=================================================

WHAT IT DOES
- Offline sensitivity notes for six Free Fire settings.
- Built-in Balanced, Fast Drag and Precision starter presets.
- Custom preset storage in local JSON.
- Headshot percentage calculator.
- Offline tap-response drill and local session history.
- HUD ergonomics guide and device/FPS checklist.
- English, বাংলা and हिन्दी UI labels.
- No root, game connection, game-file edits, memory access, automation or anti-cheat bypass.

IMPORTANT
The sensitivity values are manual suggestions only. They are not guaranteed headshot settings.
The app cannot read or change Free Fire settings. Copy values manually into the game's settings.
The aim drill is an independent practice screen, not an in-game overlay or aiming tool.

PROJECT
main.py                 Kivy application
requirements.txt        Python dependency
buildozer.spec          Android packaging configuration
assets/icon.png         App icon
assets/presplash.png    Splash image

BUILD ON LINUX / WSL2 (recommended)
1. Install system dependencies:
   sudo apt update
   sudo apt install -y python3 python3-pip python3-venv git zip unzip        openjdk-17-jdk build-essential autoconf libtool pkg-config        zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake        libffi-dev libssl-dev

2. Create environment and install:
   python3 -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip setuptools wheel
   pip install buildozer "cython<3"

   (If that Cython pin is rejected by your Python version, use:
    pip install "cython<3")

3. From this project folder:
   buildozer android debug

4. APK output:
   bin/ffheadshotbooster-1.0.0-arm64-v8a_armeabi-v7a-debug.apk
   (Exact filename can vary by Buildozer/python-for-android version.)

ANDROID INSTALL
- Copy the APK to your Android phone.
- Allow installation from the file manager when Android prompts.
- Install and open. No special permissions are requested.

TERMUX NOTE
Buildozer's Android toolchain is not reliably supported natively inside Termux.
Use a Linux PC, Ubuntu in WSL2, or a cloud Linux environment. You can edit/test
Python source in Termux, but build the APK in supported Linux.

TESTING
- Python syntax: python -m py_compile main.py
- Desktop smoke test (after installing Kivy): python main.py
- Android packaging: buildozer android debug

BUILD TROUBLESHOOTING
- Run `buildozer android clean` then `buildozer -v android debug`.
- Use JDK 17.
- Ensure Android SDK/NDK licenses are accepted.
- Do not build as root; use a normal Linux user.
- If SDK/NDK download fails, check network and rerun the build.
- Keep android.api and android.ndk values compatible with the installed
  python-for-android release; Buildozer may select a newer compatible toolchain.

No APK is prebuilt here because Android SDK/NDK toolchains are environment-specific.
A real Android build must be run on your Linux build machine.
