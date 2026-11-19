#!/data/data/com.termux/files/usr/bin/bash
# stop-server.sh — Stops the Android Home Server API and releases wake-lock

BASE_DIR="$HOME/Android-Server"
PID_FILE="$BASE_DIR/run/server.pid"

if [ ! -f "$PID_FILE" ]; then
    echo "[INFO] No server PID file found. Server does not appear to be running."
    if command -v termux-wake-unlock >/dev/null 2>&1; then
        termux-wake-unlock
    fi
    exit 0
fi

PID=$(cat "$PID_FILE")

if kill -0 "$PID" 2>/dev/null; then
    echo "[INFO] Stopping server (PID: $PID)..."
    kill "$PID"

    # Wait up to 5 seconds for graceful shutdown
    COUNT=0
    while kill -0 "$PID" 2>/dev/null && [ "$COUNT" -lt 10 ]; do
        sleep 0.5
        COUNT=$((COUNT + 1))
    done

    if kill -0 "$PID" 2>/dev/null; then
        echo "[WARN] Server did not stop gracefully. Forcing kill..."
        kill -9 "$PID"
    fi
    echo "[OK] Server stopped."
else
    echo "[INFO] Process $PID is not running."
fi

rm -f "$PID_FILE"

# Release wake-lock to let device sleep
if command -v termux-wake-unlock >/dev/null 2>&1; then
    echo "[INFO] Releasing Termux wake-lock..."
    termux-wake-unlock
fi
