#!/usr/bin/env python3
"""
Development server for beautiful-ppt HTML previews.
Serves the preview/ directory on localhost.
"""

import argparse
import atexit
import http.server
import os
import platform
import signal
import socket
import subprocess
import sys

PID_FILE = "/tmp/beautiful-ppt-preview.pid"
PREVIEW_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# PID file helpers
# ---------------------------------------------------------------------------

def _read_pid_file():
    """Return (pid, port) from PID file, or (None, None) if missing/corrupt."""
    try:
        with open(PID_FILE, "r") as f:
            lines = f.read().strip().splitlines()
        pid = int(lines[0])
        port = int(lines[1]) if len(lines) > 1 else None
        return pid, port
    except (FileNotFoundError, ValueError, IndexError):
        return None, None


def _is_process_alive(pid):
    """Return True if the given PID is running."""
    try:
        os.kill(pid, 0)
        return True
    except (OSError, ProcessLookupError):
        return False


def _write_pid_file(pid, port):
    with open(PID_FILE, "w") as f:
        f.write(f"{pid}\n{port}\n")


def _remove_pid_file():
    try:
        os.remove(PID_FILE)
    except FileNotFoundError:
        pass


def setup_pid_file(port):
    """Check existing PID file, warn if alive, then write new entry."""
    existing_pid, existing_port = _read_pid_file()
    if existing_pid is not None:
        if _is_process_alive(existing_pid):
            print(
                f"[warn] A server may already be running "
                f"(pid={existing_pid}, port={existing_port}). "
                "Skipping PID file overwrite.",
                file=sys.stderr,
            )
            # Keep existing file; still register our own atexit just in case
        else:
            _write_pid_file(os.getpid(), port)
    else:
        _write_pid_file(os.getpid(), port)

    atexit.register(_remove_pid_file)


# ---------------------------------------------------------------------------
# Port selection
# ---------------------------------------------------------------------------

def _port_is_free(port):
    """Return True if the given TCP port is available on localhost."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind(("127.0.0.1", port))
            return True
        except OSError:
            return False


def find_free_port(start=8432, end=8440):
    """Try ports start..end (inclusive) and return the first free one."""
    for port in range(start, end + 1):
        if _port_is_free(port):
            return port
    raise RuntimeError(
        f"No free port found in range {start}-{end}. "
        "Stop other servers and try again."
    )


# ---------------------------------------------------------------------------
# Browser opening
# ---------------------------------------------------------------------------

def open_browser(url):
    system = platform.system()
    if system == "Darwin":
        cmd = ["open", url]
    elif system == "Linux":
        cmd = ["xdg-open", url]
    else:
        cmd = ["start", url]

    try:
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"[info] Could not open browser automatically: {e}", file=sys.stderr)


# ---------------------------------------------------------------------------
# Signal handlers
# ---------------------------------------------------------------------------

def _shutdown(signum, frame):
    print("\n[info] Shutting down server...")
    _remove_pid_file()
    sys.exit(0)


signal.signal(signal.SIGTERM, _shutdown)
signal.signal(signal.SIGINT, _shutdown)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Development preview server for beautiful-ppt"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8432,
        help="Preferred port (default: 8432; falls back to 8432-8440)",
    )
    args = parser.parse_args()

    # Resolve actual port
    if _port_is_free(args.port):
        port = args.port
    else:
        print(
            f"[info] Port {args.port} is in use, scanning 8432-8440...",
            file=sys.stderr,
        )
        port = find_free_port()

    setup_pid_file(port)

    # Change to the preview directory so SimpleHTTPRequestHandler serves it
    os.chdir(PREVIEW_DIR)

    handler = http.server.SimpleHTTPRequestHandler
    # Suppress default request logging noise (comment out to re-enable)
    handler.log_message = lambda *a, **kw: None

    server = http.server.HTTPServer(("", port), handler)
    url = f"http://localhost:{port}"
    print(f"Server running at {url}")
    print("Press Ctrl+C to stop.")

    open_browser(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[info] Interrupted, shutting down...")
        server.shutdown()
        _remove_pid_file()


if __name__ == "__main__":
    main()
