import subprocess
import webbrowser
import time
import os
import sys
import socket


def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex(('localhost', port)) == 0


if getattr(sys, 'frozen', False):
    base_dir = os.path.dirname(sys.executable)
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

# ── Find Python in python_runtime ────────────────────────────
# Windows: python_runtime\Scripts\python.exe
# Mac/Linux: python_runtime/bin/python3
if sys.platform == "win32":
    python_path = os.path.join(base_dir, "python_runtime", "Scripts", "python.exe")
else:
    python_path = os.path.join(base_dir, "python_runtime", "bin", "python3")

app_path = os.path.join(base_dir, "app.py")
port     = 8501

if not is_port_in_use(port):
    subprocess.Popen([
        python_path,
        "-m",
        "streamlit",
        "run",
        app_path,
        "--server.headless=true",
        f"--server.port={port}",
    ])

    # Wait until Streamlit is ready
    print("Starting Tent Card Generator...")
    for _ in range(60):
        time.sleep(1)
        if is_port_in_use(port):
            print("Ready!")
            break

    time.sleep(2)

webbrowser.open(f"http://localhost:{port}")

# Keep alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
