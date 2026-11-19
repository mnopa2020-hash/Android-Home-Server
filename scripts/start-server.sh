
#!/data/data/com.termux/files/usr/bin/bash
# start-server.sh — Starts the Android Home Server API

BASE_DIR="$HOME/Android-Server"
PID_FILE="$BASE_DIR/run/server.pid"
LOG_FILE="$BASE_DIR/logs/server.log"
VENV_PYTHON="$BASE_DIR/venv/bin/python3"
HOST="0.0.0.0"
PORT=8000
HEALTH_URL="http://127.0.0.1:$PORT/health"

mkdir -p "$BASE_DIR/run" "$BASE_DIR/logs"

# Check whether API is actually responding
if curl -fsS --max-time 2 "$HEALTH_URL" >/dev/null 2>&1; then
    PID=$(cat "$PID_FILE" 2>/dev/null)
    echo "[INFO] API is already healthy (PID: ${PID:-unknown})"
    exit 0
fi

# Remove stale PID file
if [ -f "$PID_FILE" ]; then
    echo "[WARN] API is not responding. Removing stale PID file..."
    rm -f "$PID_FILE"
fi

# Acquire wake-lock
if command -v termux-wake-lock >/dev/null 2>&1; then
    echo "[INFO] Acquiring Termux wake-lock..."
    termux-wake-lock
fi

echo "[INFO] Starting FastAPI server on http://$HOST:$PORT..."
cd "$BASE_DIR" || exit 1

nohup "$VENV_PYTHON" -m uvicorn app.main:app \
    --host "$HOST" --port "$PORT" >> "$LOG_FILE" 2>&1 &

SERVER_PID=$!
echo "$SERVER_PID" > "$PID_FILE"

# Wait for HTTP health check
for i in $(seq 1 10); do
    if curl -fsS --max-time 2 "$HEALTH_URL" >/dev/null 2>&1; then
        echo "[OK] API is healthy (PID: $SERVER_PID)"
        echo "     Bound to: http://$HOST:$PORT"
        echo "     Logs: $LOG_FILE"
        exit 0
    fi
    sleep 1
done

echo "[ERROR] API failed to become healthy. Last log lines:"
tail -n 10 "$LOG_FILE"
rm -f "$PID_FILE"

if command -v termux-wake-unlock >/dev/null 2>&1; then
    termux-wake-unlock
fi

exit 1
