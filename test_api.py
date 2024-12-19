import pytest
import requests
import docker
import time

# Define test constants
CONTAINER_IMAGE = "flask-api:latest"
BASE_URL = "http://localhost:5000"

@pytest.fixture(scope="session", autouse=True)
def setup_container():
    # Initialize Docker client
    client = docker.from_env()
    container = client.containers.run(
        CONTAINER_IMAGE,
        detach=True,
        ports={"5000/tcp": 5000},
    )
    time.sleep(5)  # Wait for the container to initialize
    yield
    container.stop()
    container.remove()

# Test API 1 (reverse API)
def test_reverse():
    response = requests.get(f"{BASE_URL}/reverse", params={"in": "The quick brown fox jumps over the lazy dog"})
    assert response.status_code == 200
    assert response.json()["result"] == "dog lazy the over jumps fox brown quick The"

# Test API 2 (restore API)
def test_restore():
    requests.get(f"{BASE_URL}/reverse", params={"in": "The quick brown fox jumps over the lazy dog"})
    response = requests.get(f"{BASE_URL}/restore")
    assert response.status_code == 200
    assert response.json()["result"] == "dog lazy the over jumps fox brown quick The"

# Test API 1 (reverse API with missing query parameter)
def test_reverse_missing_param():
    response = requests.get(f"{BASE_URL}/reverse")
    assert response.status_code == 400
    assert "error" in response.json()


