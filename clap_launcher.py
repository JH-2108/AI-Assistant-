import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import requests
import sounddevice as sd


ROOT = Path(__file__).resolve().parent
JARVIS_HEALTH_URL = "http://127.0.0.1:8765/api/health"
CLAP_THRESHOLD = 0.35
CLAP_GAP_MIN = 0.08
CLAP_GAP_MAX = 0.8
COOLDOWN_SECONDS = 4
SAMPLE_RATE = 16000
BLOCKSIZE = 1024


last_clap_time = 0.0
last_launch_time = 0.0


def jarvis_is_running():
    try:
        response = requests.get(JARVIS_HEALTH_URL, timeout=0.6)
        return response.ok
    except requests.RequestException:
        return False


def launch_jarvis():
    global last_launch_time

    now = time.time()
    if now - last_launch_time < COOLDOWN_SECONDS:
        return

    if jarvis_is_running():
        last_launch_time = now
        return

    pythonw = Path(sys.executable).with_name("pythonw.exe")
    runner = str(pythonw if pythonw.exists() else Path(sys.executable))

    subprocess.Popen(
        [runner, str(ROOT / "desktop_app.py")],
        cwd=str(ROOT),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    last_launch_time = now


def audio_callback(indata, frames, time_info, status):
    global last_clap_time

    volume = float(np.max(np.abs(indata)))
    if volume < CLAP_THRESHOLD:
        return

    now = time.time()
    gap = now - last_clap_time

    if CLAP_GAP_MIN <= gap <= CLAP_GAP_MAX:
        launch_jarvis()
        last_clap_time = 0.0
        return

    last_clap_time = now


def main():
    print("Jarvis clap listener running. Double clap to open the app.")
    with sd.InputStream(
        channels=1,
        callback=audio_callback,
        samplerate=SAMPLE_RATE,
        blocksize=BLOCKSIZE,
    ):
        while True:
            time.sleep(1)


if __name__ == "__main__":
    main()