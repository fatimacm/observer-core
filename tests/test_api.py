import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_health_endpoint():
    """Test /health endpoint returns correct structure and status"""
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    
    # Validate required fields
    assert "status" in data
    assert "service" in data
    assert "timestamp" in data
    
    # Validate field values
    assert data["status"] == "healthy"
    assert data["service"] == "observer-core"
    assert isinstance(data["timestamp"], str)

def test_status_endpoint():
    """Test /status endpoint returns system information"""
    response = client.get("/status")
    
    assert response.status_code == 200
    data = response.json()
    
    # Validate required fields
    required_fields = ["service", "version", "timestamp", "uptime_seconds", "system"]
    for field in required_fields:
        assert field in data
    
    # Validate system info structure
    system = data["system"]
    system_fields = ["platform", "python_version", "cpu_count", "memory_total_gb"]
    for field in system_fields:
        assert field in system
    
    # Validate data types
    assert isinstance(data["uptime_seconds"], int)
    assert isinstance(system["cpu_count"], int)
    assert isinstance(system["memory_total_gb"], (int, float))

def test_metrics_endpoint():
    """Test /metrics endpoint returns real-time system metrics"""
    response = client.get("/metrics")
    
    assert response.status_code == 200
    data = response.json()
    
    # Validate required fields
    assert "timestamp" in data
    assert "cpu" in data
    assert "memory" in data
    
    # Validate CPU structure

    cpu = data["cpu"]
    assert isinstance(cpu, dict)
    # CPU should have percentage fields with valid ranges
    percent_fields = [key for key in cpu.keys() if key.endswith("_percent")]
    assert percent_fields, "No CPU percentage fields found"
    for key in percent_fields:
        value = cpu[key]
        assert isinstance(value, (int, float)), f"{key} is not numeric"
        assert 0 <= value <= 100, f"{key} out of valid range: {value}"

    
    # Validate memory structure
    memory = data["memory"]
    memory_fields = ["total_gb", "available_gb", "used_gb", "free_gb", "percent"]
    for field in memory_fields:
        assert field in memory
    
    # Validate data types and ranges
    assert isinstance(memory["percent"], (int, float))
    assert 0 <= memory["percent"] <= 100
    
    # Memory values should be positive
    assert memory["total_gb"] > 0
    assert memory["available_gb"] >= 0

def test_all_endpoints_return_json():
    """Test all endpoints return valid JSON with correct content-type"""
    endpoints = ["/health", "/status", "/metrics"]
    
    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
        
        # Ensure response is valid JSON
        data = response.json()
        assert isinstance(data, dict)

def test_nonexistent_endpoint():
    """Test 404 for nonexistent endpoints"""
    response = client.get("/nonexistent")
    assert response.status_code == 404