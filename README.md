# Observer Core

Lightweight system monitoring API built with FastAPI. Provides endpoints to check system health, system status, and real-time metrics. Designed as a foundation for DevOps fundamentals: monitoring, testing, and containerization.

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
  "cpu": {
    "user_percent": 12.3,
    "system_percent": 8.1,
    "idle_percent": 79.6,
    "iowait_percent": 0.0,
    "irq_percent": 0.0,
    "nice_percent": 0.0
  },
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

### Option 1: Local Development (Python)

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

### Option 2: Docker

1. **Build Docker image:**
   ```bash
   docker build -t observer-core .
   ```

2. **Run container:**
   ```bash
   docker run -p 8000:8000 observer-core
   ```

- The API will be available at http://localhost:8000

### Option 3: Docker Compose (recommended)

1. **Start service:**
   ```bash
   docker-compose up -d
   ```

2. **View logs:**
   ```bash
   docker-compose logs -f observer-core
   ```

2. **Stop services:**
   ```bash
   docker-compose down
   ```

Compose provides:

- Healthcheck integration (/health probed automatically).
- Environment variables injected (API_PORT, SERVICE_NAME).
- Easy orchestration for future services (databases, cache, observability).

## Quick Validation

Minimal script to check all endpoints after deployment:

   ```bash
   ./smoke-test.sh
   ```

- Runs /health, /status, /metrics.
- Exits 0 if all succeed, non-zero otherwise.
- Suitable for CI/CD pipelines.

## Testing

### Unit Tests(pytest)

   ```bash
   pytest -v
   ```

or inside container:

   ```bash
   docker run --rm observer-core pytest -v
   ```

## Docker Commands Reference

```bash
   # Build image
   docker build -t observer-core .

   # Run container (basic)
   docker run -p 8000:8000 observer-core

   # Run container in background
   docker run -d -p 8000:8000 --name observer-core observer-core

   # View logs
   docker logs observer-core

   # Stop container
   docker stop observer-core

   # Remove container
   docker rm observer-core

   # Run tests in container
   docker run --rm observer-core pytest -v

   # Interactive shell in container
   docker run -it --rm observer-core /bin/bash

   ```


## Project Structure

```
observer-core/
├── api/
│   └── main.py
├── tests/
│   ├── __init__.py
│   └── test_api.py
├── .dockerignore        
├── .gitignore
├── docker-compose.yml
├── Dockerfile           
├── README.md
├── requirements.txt
└── smoke-test.sh   
```

## Dependencies

- **FastAPI**: Modern web framework for building APIs
- **psutil**: Cross-platform system and process utilities  
- **uvicorn**: ASGI server for running FastAPI
- **pytest**: Testing framework
- **pytest-asyncio**: Async testing support
- **httpx**: HTTP client for integration testing
