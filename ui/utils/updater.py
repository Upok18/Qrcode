import os 
import sys
import subprocess
import requests
from tkinter import messagebox

CURRENT_VERSION = "1.0.2"
VERSION_URL = "https://raw.githubusercontent.com/Upok18/Qrcode/refs/heads/main/ui/utils/version.json"

def check_for_updates(parent_window=None):
    try:
        response = requests.get(VERSION_URL, timeout=5)
        if response.status_code == 200:
            data = response.json()
            latest_version = data.get("version")
            download_url = data.get("download_url")

            if latest_version > CURRENT_VERSION:
                if messagebox.askyesno(
                    "Update Available", 
                    f"A new version ({latest_version}) is available!\n\nWould you like to update now?"
                ):
                    apply_update(download_url)
    except Exception as e:
        print(f"Failed to check for updates: {e}")

def apply_update(download_url):
    current_exe = sys.executable
    new_exe = current_exe + ".new"
    bat_script = os.path.join(os.path.dirname(current_exe), "update.bat")

    # 1. Download the new version executable
    res = requests.get(download_url, stream=True)
    with open(new_exe, "wb") as f:
        for chunk in res.iter_content(chunk_size=8192):
            f.write(chunk)

    # 2. Write a batch file to wait for main app termination, replace file, and restart
    bat_content = f"""@echo off
timeout /t 2 /nobreak > nul
move /y "{new_exe}" "{current_exe}"
start "" "{current_exe}"
del "%~f0"
"""
    with open(bat_script, "w") as f:
        f.write(bat_content)

    # 3. Spawn batch script silently and quit main app
    subprocess.Popen([bat_script], shell=True)
    sys.exit()
