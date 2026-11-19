import secrets
import subprocess
import time
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Header, HTTPException

BASE = Path.home() / "Android-Server"
TOKEN_FILE = BASE / ".admin_token"

app = FastAPI(title="Android Home Server Manager")


def verify_token(x_admin_token: Optional[str] = Header(default=None)):
    if not TOKEN_FILE.exists():
        raise HTTPException(503, "Admin token unavailable")

    token = TOKEN_FILE.read_text().strip()

    if not x_admin_token or not secrets.compare_digest(x_admin_token, token):
        raise HTTPException(401, "Invalid admin token")


def probe(url):
    try:
        result = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", url],
            capture_output=True, text=True, timeout=3
        )
        return result.stdout
    except Exception:
        return ""


def tmux_running(name):
    return subprocess.run(
        ["tmux", "has-session", "-t", name],
        capture_output=True
    ).returncode == 0


def nginx_start():
    if tmux_running("nginx"):
        return "Nginx session already exists"

    result = subprocess.run([
        "tmux", "new-session", "-d", "-s", "nginx",
        'proot-distro login debian -- nginx -g "daemon off;"'
    ], capture_output=True, text=True, timeout=10)

    if result.returncode != 0:
        raise RuntimeError(result.stderr or "Could not start Nginx")

    return "Nginx start command sent"


def jellyfin_start():
    if tmux_running("jellyfin"):
        return "Jellyfin session already exists"

    command = (
        "proot-distro login debian -- "
        "runuser -u jellyfin -- /usr/bin/jellyfin "
        "--datadir /opt/android-server/media/config/data "
        "--configdir /opt/android-server/media/config/config "
        "--cachedir /opt/android-server/media/cache "
        "--logdir /opt/android-server/media/log "
        "--webdir /usr/share/jellyfin/web "
        "--ffmpeg /usr/lib/jellyfin-ffmpeg/ffmpeg"
    )

    result = subprocess.run(
        ["tmux", "new-session", "-d", "-s", "jellyfin", command],
        capture_output=True, text=True, timeout=10
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr or "Could not start Jellyfin")

    return "Jellyfin start command sent"


def stop_tmux_service(name):
    if not tmux_running(name):
        return f"{name} session already stopped"

    subprocess.run(
        ["tmux", "send-keys", "-t", name, "C-c"],
        capture_output=True
    )
    time.sleep(3)

    if tmux_running(name):
        subprocess.run(
            ["tmux", "kill-session", "-t", name],
            capture_output=True
        )

    return f"{name} stop command sent"


def nginx_stop():
    return stop_tmux_service("nginx")


def jellyfin_stop():
    return stop_tmux_service("jellyfin")


@app.get("/health")
def health():
    return {"manager": "online"}


@app.get("/services")
def services():
    api = probe("http://127.0.0.1:8000/health")
    web = probe("http://127.0.0.1:8080/")
    media = probe("http://127.0.0.1:8096/")

    return {
        "manager": "online",
        "api": "online" if api.startswith("2") else "offline",
        "nginx": "online" if web.startswith(("2", "3")) else "offline",
        "jellyfin": "online" if media.startswith(("2", "3")) else "offline"
    }


@app.post("/services/{service}/{action}")
def control_service(
    service: str,
    action: str,
    x_admin_token: Optional[str] = Header(default=None)
):
    verify_token(x_admin_token)

    if service not in ("api", "nginx", "jellyfin"):
        raise HTTPException(400, "Unknown service")

    if action not in ("start", "stop", "restart"):
        raise HTTPException(400, "Unknown action")

    try:
        if service == "api":
            script = BASE / "scripts"

            if action == "start":
                result = subprocess.run(
                    ["bash", str(script / "start-server.sh")],
                    capture_output=True, text=True, timeout=20
                )
            elif action == "stop":
                result = subprocess.run(
                    ["bash", str(script / "stop-server.sh")],
                    capture_output=True, text=True, timeout=15
                )
            else:
                subprocess.run(
                    ["bash", str(script / "stop-server.sh")],
                    capture_output=True, text=True, timeout=15
                )
                result = subprocess.run(
                    ["bash", str(script / "start-server.sh")],
                    capture_output=True, text=True, timeout=20
                )

            if result.returncode != 0:
                raise RuntimeError(result.stderr or result.stdout)

            message = result.stdout[-1000:]

        elif service == "nginx":
            if action == "start":
                message = nginx_start()
            elif action == "stop":
                message = nginx_stop()
            else:
                nginx_stop()
                time.sleep(1)
                message = nginx_start()

        else:
            if action == "start":
                message = jellyfin_start()
            elif action == "stop":
                message = jellyfin_stop()
            else:
                jellyfin_stop()
                time.sleep(1)
                message = jellyfin_start()

        return {
            "success": True,
            "service": service,
            "action": action,
            "message": message
        }

    except Exception as error:
        raise HTTPException(500, str(error))
