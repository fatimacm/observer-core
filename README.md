# Observer Core

Lightweight system monitoring API built with FastAPI. Provides endpoints to check system health, status, and metrics. Built for learning system monitoring fundamentals with FastAPI.

## API Endpoints

### Health Check
```
GET /health
```
Quick check if the service is running.

**Response:**
```json
{
  "status": "healthy",
  "service": "observer-core",
  "timestamp": "2025-08-21T15:30:45.123456"
}
```

### System Status
```
GET /status
```
System information and uptime.

**Response:**
```json
{
  "service": "observer-core",
  "version": "0.1.0",
  "timestamp": "2025-08-21T15:30:45.123456",
  "uptime_seconds": 3600,
  "system": {
    "platform": "Linux",
    "python_version": "3.11.5",
    "cpu_count": 8,
    "memory_total_gb": 16.0
  }
}
```

### Real-time Metrics
```
GET /metrics
```
CPU and memory usage.

**Response:**
```json
{
  "timestamp": "2025-08-21T15:30:45.123456",
  "cpu_percent": 25.4,
  "memory": {
    "total_gb": 16.0,
    "available_gb": 10.2,
    "used_gb": 5.8,
    "free_gb": 4.2,
    "percent": 36.25
  }
}
```

## Quick Start

1. **Clone the repo:**
   ```bash
   git clone git@github.com:fatimacm/observer-core.git
   cd observer-core
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the API:**
   ```bash
   uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
   # --reload: auto-restart on code changes
   # --host 0.0.0.0: accept connections from any IP
   ```

5. **Test endpoints:**
   ```bash
   curl http://localhost:8000/health
   curl http://localhost:8000/status
   curl http://localhost:8000/metrics
   ```

## Project Structure

```
observer-core/
├── api/
│   ├── __pycache__/       
│   └── main.py            
├── venv/                  
├── .gitignore
├── README.md
└── requirements.txt
```

## Dependencies

- **FastAPI**: Modern web framework for building APIs
- **psutil**: Cross-platform system and process utilities  
- **uvicorn**: ASGI server for running FastAPI