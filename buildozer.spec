name: Build APK
on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-22.04
    steps:
      - uses: actions/checkout@v5

      - name: Set up Java 17
        uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: 17

      - name: Set up Python 3.10
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y python3-pip zip unzip libltdl-dev libffi-dev libssl-dev libbz2-dev libncurses5-dev libsqlite3-dev libreadline-dev zlib1g-dev || true
          sudo dpkg --add-architecture i386 || true
          sudo apt-get update
          sudo apt-get install -y libc6:i386 libstdc++6:i386 zlib1g:i386 || true
          pip install --upgrade pip
          pip install buildozer cython==0.29.36 virtualenv

      - name: Fix buildozer.spec
        run: |
          set +e
          [ -f buildozer.spec ] || buildozer init || true
          python3 << 'PY'
          import pathlib, re
          p = pathlib.Path("buildozer.spec")
          if not p.exists():
              print("no spec found")
              exit(0)
          text = p.read_text()
          if "android.api" in text:
              text = re.sub(r"^android.api\s*=.*", "android.api = 34", text, flags=re.M)
          else:
              text += "\nandroid.api = 34\n"
          if "android.build_tools_version" in text:
              text = re.sub(r"^#*.*android.build_tools_version.*", "android.build_tools_version = 34.0.0", text, flags=re.M)
          else:
              text += "\nandroid.build_tools_version = 34.0.0\n"
          if "android.ndk_version" in text:
              text = re.sub(r"^#*.*android.ndk_version.*", "android.ndk_version = 25b", text, flags=re.M)
          else:
              text += "\nandroid.ndk_version = 25b\n"
          p.write_text(text)
          print(text[:3000])
          PY
          grep -E "android.api|build_tools|ndk_version" buildozer.spec || true

      - name: Install Android SDK
        run: |
          set +e
          SDK=$HOME/.buildozer/android/platform/android-sdk
          mkdir -p $SDK
          cd /tmp
          wget -q https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip -O cmdline-tools.zip
          unzip -q cmdline-tools.zip
          mkdir -p $SDK/cmdline-tools/latest
          mv cmdline-tools/* $SDK/cmdline-tools/latest/ 2>/dev/null || true
          mkdir -p ~/.android
          touch ~/.android/repositories.cfg
          mkdir -p $SDK/licenses
          echo "8933bad161af4178b1185d1a37fbf41ea5269c55" > $SDK/licenses/android-sdk-license
          echo "d56f5187479451eabf01fb78af6dfcb131a6481e" >> $SDK/licenses/android-sdk-license
          echo "24333f8a63b6825ea9c5514f83c1051b8f6b012" >> $SDK/licenses/android-sdk-license
          echo "y" | $SDK/cmdline-tools/latest/bin/sdkmanager --licenses --sdk_root=$SDK || true
          echo "y" | $SDK/cmdline-tools/latest/bin/sdkmanager --sdk_root=$SDK "platform-tools" "platforms;android-34" "build-tools;34.0.0" "ndk;25.1.8937393" || true
          ls $SDK/build-tools/ || true

      - name: Patch Build-Tools 37 + AIDL
        run: |
          SDK=$HOME/.buildozer/android/platform/android-sdk
          if [ -d "$SDK/build-tools/34.0.0" ]; then
            rm -rf $SDK/build-tools/37.0.0
            cp -r $SDK/build-tools/34.0.0 $SDK/build-tools/37.0.0
            echo "Fake 37 creato da 34"
          fi
          find $SDK/build-tools -name aidl -type f | while read P; do
            echo "Patch $P"
            if [ ! -f "$P.real" ]; then
              mv "$P" "$P.real"
              printf '#!/bin/bash\nDIR="$(dirname "$0")"\n[ $# -eq 0 ] && exit 0\nexec "$DIR/aidl.real" "$@"\n' > "$P"
              chmod +x "$P" "$P.real"
            fi
          done
          ls -lh $SDK/build-tools/34.0.0/aidl $SDK/build-tools/37.0.0/aidl || true

      - name: Build APK
        run: |
          buildozer android debug

      - name: Upload APK
        uses: actions/upload-artifact@v5
        with:
          name: jarvis-apk
          path: bin/*.apk
