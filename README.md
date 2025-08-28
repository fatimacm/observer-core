# Observer Core

Minimal FastAPI service with health, status, and metrics endpoints. Now containerized and monitored with Prometheus for observability.

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

### Metrics (Prometheus Format)

```
GET /metrics
```
CPU and memory usage in Prometheus-native format.

**Response**
   ```text
   # HELP observer_core_cpu_percent CPU usage percentage
   # TYPE observer_core_cpu_percent gauge
   observer_core_cpu_percent 2.5
   # HELP observer_core_memory_percent Memory usage percentage
   # TYPE observer_core_memory_percent gauge
   observer_core_memory_percent 70.2
   ```

### Metrics (JSON Format)

CPU and memory usage in JSON format.

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

### Option 3: Docker Compose (recommended)

1. **Start service:**
   ```bash
   docker-compose up -d
   ```

This starts both observer-core and the Prometheus monitoring stack.

2. **View logs:**
   ```bash
   docker-compose logs -f observer-core
   ```

3. **Stop services:**
   ```bash
   docker-compose down
   ```

- The API will be available at http://localhost:8000
- Prometheus monitoring at http://localhost:9090

## Quick Validation

Minimal script to validate service health after deployment:

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

## Observability with Prometheus

Observer Core exposes custom metrics in Prometheus format at /metrics.
A Prometheus container is included in docker-compose.yml and scrapes these metrics automatically.

### Access Prometheus UI

- URL: http://localhost:9090

### Example Queries

- CPU usage percentage:
```bash
   observer_core_cpu_percent
   ```
- Memory usage percentage:
```bash
   observer_core_memory_percent
   ```
These metrics are refreshed in near real-time and reflect the state of the running container.

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
├── monitoring/
│   └── prometheus.yml
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
