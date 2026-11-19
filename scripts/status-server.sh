#!/data/data/com.termux/files/usr/bin/bash
# status-server.sh — Checks the status of the Android Home Server API

BASE_DIR="$HOME/Android-Server"
PID_FILE="$BASE_DIR/run/server.pid"
LOG_FILE="$BASE_DIR/logs/server.log"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if kill -0 "$PID" 2>/dev/null; then
        echo "[STATUS] Server is RUNNING (PID: $PID)"
        echo "[QUERY] Testing http://127.0.0.1:8000/health..."
        if command -v curl >/dev/null 2>&1; then
            curl -s http://127.0.0.1:8000/health
            echo ""
        fi
        exit 0
    else
        echo "[STATUS] Stale PID file found (PID: $PID is not running)."
        exit 1
    fi
else
    echo "[STATUS] Server is STOPPED."
    exit 0
fi
