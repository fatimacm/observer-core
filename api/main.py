from fastapi import FastAPI, HTTPException
from datetime import datetime
import psutil
import platform

# START-UP TIME FOR REAL SERVICE UPTIME
SERVICE_START_TIME = datetime.utcnow()

# PRIMING CPU SO THAT THE FIRST CALL DOES NOT RETURN 0
psutil.cpu_percent(interval=None)

app = FastAPI(title="Observer Core", version="0.1.0")

# ENDPOINT /health — fast ping
@app.get("/health")
def health_check():
    """
    Quick endpoint to confirm service is alive.
    """
    return {
        "status": "healthy",
        "service": "observer-core",
        "timestamp": datetime.utcnow().isoformat()
    }

# ENDPOINT /status — system information
@app.get("/status")
def system_status():
    """
    Returns detailed system and service information.
    """
    try:
        uptime_seconds = int((datetime.utcnow() - SERVICE_START_TIME).total_seconds())
        return {
            "service": "observer-core",
            "version": "0.1.0",
            "timestamp": datetime.utcnow().isoformat(),
            "uptime_seconds": uptime_seconds,
            "system": {
                "platform": platform.system(),
                "python_version": platform.python_version(),
                "cpu_count": psutil.cpu_count(logical=True),
                "memory_total_gb": round(psutil.virtual_memory().total / (1024**3), 2)
            }
        }
    except Exception:
        raise HTTPException(status_code=500, detail="Unable to fetch system status at this time")


# ENDPOINT /metrics — real time metrics
@app.get("/metrics")
def system_metrics():
    """
    Returns real-time CPU and memory usage metrics.
    Uses cpu_times_percent for instant snapshot.
    Handles errors safely.
    """
    try:
        # CPU snapshot by type
        cpu_times = psutil.cpu_times_percent(interval=None, percpu=False)
        cpu_metrics = {
            "user_percent": cpu_times.user,
            "system_percent": cpu_times.system,
            "idle_percent": cpu_times.idle,
            "nice_percent": getattr(cpu_times, "nice", 0.0),
            "iowait_percent": getattr(cpu_times, "iowait", 0.0),
            "irq_percent": getattr(cpu_times, "irq", 0.0),
            "softirq_percent": getattr(cpu_times, "softirq", 0.0)
        }

        virtual_mem = psutil.virtual_memory()
        memory_metrics = {
            "total_gb": round(virtual_mem.total / (1024**3), 2),
            "available_gb": round(virtual_mem.available / (1024**3), 2),
            "used_gb": round(virtual_mem.used / (1024**3), 2),
            "free_gb": round(virtual_mem.free / (1024**3), 2),
            "percent": virtual_mem.percent
        }

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "cpu": cpu_metrics,
            "memory": memory_metrics
        }

    except Exception:
        # Security: no stack traces are exposed
        raise HTTPException(status_code=500, detail="Unable to fetch metrics at this time")
