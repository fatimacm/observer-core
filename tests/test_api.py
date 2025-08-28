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

def test_metrics_json_endpoint():
    """Test /metrics-json endpoint returns JSON format metrics"""
    response = client.get("/metrics-json")
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    
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

def test_metrics_prometheus_endpoint():
    """Test /metrics endpoint returns Prometheus format metrics"""
    response = client.get("/metrics")
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/plain; charset=utf-8"
    
    content = response.text
    
    # Verify Prometheus exposition format
    assert "# HELP" in content
    assert "# TYPE" in content
    assert "observer_core_cpu_percent" in content
    assert "observer_core_memory_percent" in content
    
    # Verify numeric values are present
    lines = content.strip().split('\n')
    metric_lines = [line for line in lines if not line.startswith('#') and line.strip()]
    
    for metric_line in metric_lines:
        parts = metric_line.split()
        assert len(parts) >= 2, f"Invalid metric line: {metric_line}"
        metric_value = parts[1]
        
        # Verify value is numeric
        try:
            float(metric_value)
        except ValueError:
            pytest.fail(f"Metric value is not numeric: {metric_value}")

def test_all_endpoints_return_correct_content_type():
    """Test all endpoints return correct content-type"""
    endpoints_content_types = [
        ("/health", "application/json"),
        ("/status", "application/json"),
        ("/metrics-json", "application/json"),
        ("/metrics", "text/plain; charset=utf-8")
    ]
    
    for endpoint, expected_content_type in endpoints_content_types:
        response = client.get(endpoint)
        assert response.status_code == 200
        assert response.headers["content-type"] == expected_content_type

def test_metrics_values_within_ranges():
    """Test metrics endpoint returns values within reasonable ranges"""
    response = client.get("/metrics-json")
    data = response.json()
    
    # CPU percentages should be between 0-100
    assert 0 <= data["cpu"]["user_percent"] <= 100
    assert 0 <= data["cpu"]["system_percent"] <= 100
    assert 0 <= data["cpu"]["idle_percent"] <= 100
    
    # Memory percentage should be between 0-100  
    assert 0 <= data["memory"]["percent"] <= 100
    
    # Memory values should be positive
    assert data["memory"]["total_gb"] > 0
    assert data["memory"]["available_gb"] >= 0
    assert data["memory"]["used_gb"] >= 0

def test_nonexistent_endpoint():
    """Test 404 for nonexistent endpoints"""
    response = client.get("/nonexistent")
    assert response.status_code == 404