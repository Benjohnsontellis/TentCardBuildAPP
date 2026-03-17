import subprocess
import webbrowser
import time
import os
import sys

if getattr(sys, 'frozen', False):
    base_dir = os.path.dirname(sys.executable)
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

python_path = os.path.join(base_dir, "python_runtime", "Scripts", "python.exe")
app_path = os.path.join(base_dir, "app.py")

subprocess.Popen([
    python_path,
    "-m",
    "streamlit",
    "run",
    app_path,
    "--server.headless=true"
])

time.sleep(5)

webbrowser.open("http://localhost:8501")