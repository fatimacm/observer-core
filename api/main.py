from fastapi import FastAPI
from datetime import datetime
import psutil
import platform

app = FastAPI(title="Observer Core", version="0.1.0")

@app.get("/health")
def health_check():
    """
    Simple endpoint to confirm that the service is responding
    """
    return {
        "status": "healthy",
        "service": "observer-core",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/status")
def system_status():
    """
    Returns basic system and app information
    """
    uptime_seconds = int(datetime.utcnow().timestamp() - psutil.boot_time())
    return {
        "service": "observer-core",
        "version": "0.1.0",
        "timestamp": datetime.utcnow().isoformat(),
        "uptime_seconds": uptime_seconds,
        "system": {
            "platform": platform.system(),
            "python_version": platform.python_version(),
            "cpu_count": psutil.cpu_count(logical=True),
            "memory_total_gb": psutil.virtual_memory().total // (1024**3)
        }
    }

