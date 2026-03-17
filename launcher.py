import subprocess
import webbrowser
import time
import sys
import os


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


app_path = resource_path("app.py")

subprocess.Popen([
    sys.executable,
    "-m",
    "streamlit",
    "run",
    app_path,
    "--server.headless=true"
])

time.sleep(4)
webbrowser.open("http://localhost:8501")
