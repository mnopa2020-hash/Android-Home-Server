#!/data/data/com.termux/files/usr/bin/bash

BASE="$HOME/Android-Server"
LOG="$BASE/logs/boot.log"

mkdir -p "$BASE/logs" "$BASE/run"

exec >> "$LOG" 2>&1

echo "===== HOME SERVER BOOT: $(date) ====="

# Keep Android awake
termux-wake-lock

# Start SSH
sshd

# Start API
"$BASE/scripts/start-server.sh"

# Start Manager
cd "$BASE"
if ! curl -fsS http://127.0.0.1:8001/health >/dev/null; then
    nohup ./venv/bin/python -m uvicorn manager:app \
        --host 127.0.0.1 --port 8001 \
        >> logs/manager.log 2>&1 &
fi

# Start Nginx in tmux
if ! tmux has-session -t nginx 2>/dev/null; then
    tmux new-session -d -s nginx \
        'proot-distro login debian -- nginx -g "daemon off;"'
fi

# Start Jellyfin in tmux
if ! tmux has-session -t jellyfin 2>/dev/null; then
    tmux new-session -d -s jellyfin \
        'proot-distro login debian -- runuser -u jellyfin -- /usr/bin/jellyfin --datadir /opt/android-server/media/config/data --configdir /opt/android-server/media/config/config --cachedir /opt/android-server/media/cache --logdir /opt/android-server/media/log --webdir /usr/share/jellyfin/web --ffmpeg /usr/lib/jellyfin-ffmpeg/ffmpeg'
fi


# Start My Cloud (File Browser Next) in tmux
if ! proot-distro login debian -- curl -fsS http://127.0.0.1:8081/ >/dev/null 2>&1; then
    if ! tmux has-session -t cloud 2>/dev/null; then
        tmux new-session -d -s cloud \
            'proot-distro login debian -- /opt/android-server/cloud-app/filebrowser --database /opt/android-server/cloud-app/data/filebrowser.db --root /storage/emulated/0/Android-Server-Cloud --address 127.0.0.1 --port 8081'
    fi
fi

echo "===== BOOT SCRIPT COMPLETED: $(date) ====="

# Start Cloudflare Named Tunnel
if ! tmux has-session -t named-cloud 2>/dev/null; then
    tmux new-session -d -s named-cloud \
        'proot-distro login debian -- bash -c "cloudflared tunnel run --token \$(cat /root/.cloudflare-tunnel-token)"'
fi
