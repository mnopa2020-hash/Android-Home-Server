"""System telemetry utility for Android Termux Home Server."""

import os
import platform
import shutil
import time
from datetime import datetime

def get_prop(prop_name: str) -> str | None:
    """Retrieve an Android system property via getprop."""
    try:
        val = os.popen(f"getprop {prop_name}").read().strip()
        return val if val else None
    except Exception:
        return None

def get_uptime_info() -> dict:
    """Read system uptime safely without relying on /proc/uptime."""
    human_str = "unknown"
    uptime_sec = 0.0
    try:
        val = os.popen("uptime -p").read().strip()
        if val:
            human_str = val

        boot_str = os.popen("uptime -s").read().strip()
        if boot_str:
            boot_dt = datetime.strptime(boot_str, "%Y-%m-%d %H:%M:%S")
            uptime_sec = round((datetime.now() - boot_dt).total_seconds(), 1)
    except Exception:
        pass
    return {"uptime_seconds": uptime_sec, "uptime_human": human_str}

def get_meminfo() -> dict:
    """Parse /proc/meminfo for memory metrics."""
    metrics = {}
    try:
        with open("/proc/meminfo", "r") as f:
            for line in f:
                parts = line.split(":")
                if len(parts) == 2:
                    k = parts[0].strip()
                    v = parts[1].strip().split()[0]
                    if k in [
                        "MemTotal", "MemFree", "MemAvailable",
                        "Buffers", "Cached", "SwapTotal", "SwapFree"
                    ]:
                        metrics[k] = int(v) * 1024

        total = metrics.get("MemTotal", 0)
        avail = metrics.get("MemAvailable", 0)
        used = total - avail if total and avail else 0
        percent_used = round((used / total) * 100, 1) if total else 0.0

        return {
            "total_bytes": total,
            "available_bytes": avail,
            "used_bytes": used,
            "total_gb": round(total / (1024**3), 2),
            "available_gb": round(avail / (1024**3), 2),
            "used_gb": round(used / (1024**3), 2),
            "percent_used": percent_used,
            "swap_total_gb": round(metrics.get("SwapTotal", 0) / (1024**3), 2),
            "swap_free_gb": round(metrics.get("SwapFree", 0) / (1024**3), 2)
        }
    except Exception as e:
        return {"error": str(e)}

def get_storage(path: str) -> dict:
    """Get storage statistics for a specified path."""
    try:
        total, used, free = shutil.disk_usage(path)
        return {
            "path": path,
            "total_bytes": total,
            "used_bytes": used,
            "free_bytes": free,
            "total_gb": round(total / (1024**3), 2),
            "used_gb": round(used / (1024**3), 2),
            "free_gb": round(free / (1024**3), 2),
            "percent_free": round((free / total) * 100, 1) if total else 0.0
        }
    except Exception as e:
        return {"path": path, "error": str(e)}

def get_system_summary() -> dict:
    """Collect full system summary."""
    uptime_info = get_uptime_info()

    return {
        "device": {
            "model": get_prop("ro.product.model") or "Realme 10 Pro+",
            "manufacturer": get_prop("ro.product.manufacturer") or "Realme",
            "device_name": get_prop("ro.product.device") or "RE58A6L1",
            "android_version": get_prop("ro.build.version.release") or "14",
            "security_patch": get_prop("ro.build.version.security_patch"),
            "build_id": get_prop("ro.build.display.id")
        },
        "cpu": {
            "architecture": platform.machine(),
            "cores": os.cpu_count() or 8,
            "system": platform.system(),
            "release": platform.release()
        },
        "uptime": uptime_info,
        "memory": get_meminfo(),
        "storage": {
            "termux_home": get_storage(os.path.expanduser("~")),
            "shared_storage": get_storage("/storage/emulated/0")
        }
    }
