import threading
import time

import webview

from web_app import HOST, PORT, run


def start_server():
    run()


def main():
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    url = f"http://{HOST}:{PORT}"
    time.sleep(1)

    webview.create_window(
        "Jarvis",
        url,
        width=1200,
        height=860,
        min_size=(900, 680),
    )
    webview.start()


if __name__ == "__main__":
    main()
