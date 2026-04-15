"""
Tests for the summarizer API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "timestamp" in data
    assert "version" in data

def test_text_summarization():
    """Test text summarization endpoint"""
    test_text = "Artificial intelligence is transforming industries by automating tasks and providing insights from data. Machine learning algorithms can analyze patterns and make predictions. This technology is being used in healthcare, finance, and transportation."
    
    response = client.post(
        "/api/v1/summarize/text",
        json={"text": test_text, "language": "en"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "status" in data
    assert "message" in data

def test_text_summarization_empty():
    """Test text summarization with empty text"""
    response = client.post(
        "/api/v1/summarize/text",
        json={"text": "", "language": "en"}
    )
    
    assert response.status_code == 422  # Validation error

def test_text_summarization_too_short():
    """Test text summarization with text that's too short"""
    response = client.post(
        "/api/v1/summarize/text",
        json={"text": "short", "language": "en"}
    )
    
    assert response.status_code == 422  # Validation error

def test_get_summary_not_found():
    """Test getting a summary that doesn't exist"""
    response = client.get("/api/v1/summarize/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404

if __name__ == "__main__":
    pytest.main([__file__, "-v"])