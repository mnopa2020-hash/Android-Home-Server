
"""FastAPI server for Android Home Server."""

import time
from fastapi import FastAPI
from .system import get_system_summary, get_uptime_info

START_TIME = time.time()

app = FastAPI(
    title="Android Home Server API",
    description="Lightweight control and telemetry API running inside Termux on Realme 10 Pro+",
    version="1.0.0"
)

@app.get("/")
def get_root():
    """Server information endpoint."""
    return {
        "name": "Android Home Server API",
        "device": "Realme 10 Pro+ 5G (RMX3686)",
        "platform": "Termux (Android 14 ARM64)",
        "version": "1.0.0",
        "status": "online",
        "docs_url": "/docs",
        "endpoints": {
            "root": "/",
            "health": "/health",
            "system": "/system"
        }
    }

@app.get("/health")
def get_health():
    """Health check endpoint."""
    uptime_since_start = round(time.time() - START_TIME, 2)
    uptime_info = get_uptime_info()
    return {
        "status": "healthy",
        "service": "android-home-server-api",
        "uptime_service_seconds": uptime_since_start,
        "system_uptime": uptime_info
    }

@app.get("/system")
def get_system():
    """Android system and hardware metrics."""
    return get_system_summary()

@app.get("/services")
def get_services():
    """Check server services."""
    import subprocess

    nginx = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
         "http://127.0.0.1:8080/"],
        capture_output=True,
        text=True,
        timeout=3
    )

    return {
        "api": "online",
        "nginx": "online" if nginx.stdout.startswith("2") else "offline",
        "dashboard": nginx.stdout
    }
