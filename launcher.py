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


# ── Find base directory ───────────────────────────────────────
if getattr(sys, 'frozen', False):
    base_dir = os.path.dirname(sys.executable)
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

# ── Log file so we can see what's happening ───────────────────
log_path = os.path.join(base_dir, "launcher_log.txt")

def log(msg):
    print(msg)
    with open(log_path, "a") as f:
        f.write(msg + "\n")

log("=== Tent Card Generator Starting ===")
log(f"Base dir: {base_dir}")

# ── Find Python ───────────────────────────────────────────────
if sys.platform == "win32":
    python_path = os.path.join(base_dir, "python_runtime", "Scripts", "python.exe")
else:
    python_path = os.path.join(base_dir, "python_runtime", "bin", "python3")

app_path = os.path.join(base_dir, "app.py")
port     = 8501

log(f"Python path: {python_path}")
log(f"Python exists: {os.path.exists(python_path)}")
log(f"App path: {app_path}")
log(f"App exists: {os.path.exists(app_path)}")

# ── Check everything exists ───────────────────────────────────
if not os.path.exists(python_path):
    log("ERROR: python_runtime not found!")
    log("Contents of base_dir:")
    for f in os.listdir(base_dir):
        log(f"  {f}")
    input("Press Enter to exit...")
    sys.exit(1)

if not os.path.exists(app_path):
    log("ERROR: app.py not found!")
    input("Press Enter to exit...")
    sys.exit(1)

# ── Start Streamlit ───────────────────────────────────────────
if not is_port_in_use(port):
    log("Starting Streamlit...")
    proc = subprocess.Popen(
        [python_path, "-m", "streamlit", "run", app_path,
         "--server.headless=true", f"--server.port={port}"],
        cwd=base_dir
    )
    log(f"Process started: PID {proc.pid}")

    for i in range(60):
        time.sleep(1)
        if is_port_in_use(port):
            log(f"Streamlit ready after {i+1} seconds!")
            break
    else:
        log("ERROR: Streamlit did not start in 60 seconds!")
        input("Press Enter to exit...")
        sys.exit(1)

    time.sleep(2)
else:
    log("Streamlit already running, opening browser...")

log("Opening browser...")
webbrowser.open(f"http://localhost:{port}")

# Keep alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
