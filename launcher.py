import sys
import os
import socket
import threading
import webbrowser
import time


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


def run_streamlit(app_path, port):
    # Set environment so Streamlit knows where its static files are
    os.environ["STREAMLIT_SERVER_HEADLESS"]        = "true"
    os.environ["STREAMLIT_SERVER_PORT"]            = str(port)
    os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"

    from streamlit.web import cli as stcli
    sys.argv = [
        "streamlit", "run", app_path,
        "--server.headless=true",
        f"--server.port={port}",
        "--server.enableCORS=false",
        "--server.enableXsrfProtection=false",
    ]
    stcli.main()


def main():
    port     = 8501
    app_path = resource_path("app.py")

    if not is_port_in_use(port):
        # Run Streamlit in background thread
        t = threading.Thread(
            target=run_streamlit,
            args=(app_path, port),
            daemon=True
        )
        t.start()

        # Wait until ready (max 30 seconds)
        print("Starting Tent Card Generator...")
        for _ in range(30):
            time.sleep(1)
            if is_port_in_use(port):
                print("Ready!")
                break

    # Open browser once
    webbrowser.open(f"http://localhost:{port}")

    # Keep process alive until user closes
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
