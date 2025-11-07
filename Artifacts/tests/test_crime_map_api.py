"""
Tests for Crime Map API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from src.api.main import app
import json

client = TestClient(app)


class TestCrimeMapAPI:
    """Test suite for crime map API endpoints"""

    def test_hotspots_endpoint_basic(self):
        """Test 1.1-1.2: Basic endpoint returns valid data"""
        response = client.get("/api/crime-map/hotspots")
        
        assert response.status_code == 200
        data = response.json()
        
        # Check required fields
        assert "hotspots" in data
        assert isinstance(data["hotspots"], list)
        assert "prediction_date" in data
        assert "model_version" in data
        assert "coverage_area" in data
        assert "grid_resolution" in data
        assert "total_predicted_incidents" in data
        
        # Check response time
        assert response.elapsed.total_seconds() < 0.5

    def test_hotspots_have_required_fields(self):
        """Test 1.3: Each hotspot has required fields"""
        response = client.get("/api/crime-map/hotspots")
        data = response.json()
        
        assert len(data["hotspots"]) > 0
        
        hotspot = data["hotspots"][0]
        
        # Check required fields
        assert "lat" in hotspot
        assert "lng" in hotspot
        assert "intensity" in hotspot
        assert "crime_type" in hotspot
        assert "predicted_incidents" in hotspot
        assert "confidence" in hotspot
        assert "grid_id" in hotspot
        assert "risk_level" in hotspot
        
        # Check data types and ranges
        assert isinstance(hotspot["lat"], float)
        assert isinstance(hotspot["lng"], float)
        assert isinstance(hotspot["intensity"], (int, float))
        assert 0 <= hotspot["intensity"] <= 1
        assert isinstance(hotspot["predicted_incidents"], int)
        assert isinstance(hotspot["confidence"], (int, float))
        assert 0 <= hotspot["confidence"] <= 1
        assert hotspot["risk_level"] in ["low", "medium", "high", "critical"]
        
        # Check valid coordinates (Chicago area)
        assert 41.0 <= hotspot["lat"] <= 42.0
        assert -88.0 <= hotspot["lng"] <= -87.0

    def test_hotspots_query_parameters(self):
        """Test 1.4: Query parameters work correctly"""
        # Test city parameter
        response = client.get("/api/crime-map/hotspots?city=chicago")
        assert response.status_code == 200
        data = response.json()
        assert data["coverage_area"]["center"]["lat"] == 41.8781
        
        # Test crime_type parameter
        response = client.get("/api/crime-map/hotspots?crime_type=theft")
        assert response.status_code == 200
        data = response.json()
        # All hotspots should have crime_type "theft"
        if data["hotspots"]:
            assert data["hotspots"][0]["crime_type"] == "theft"
        
        # Test time_window parameter
        response = client.get("/api/crime-map/hotspots?time_window=24h")
        assert response.status_code == 200
        
        # Test date parameter
        response = client.get("/api/crime-map/hotspots?date=2024-01-15")
        assert response.status_code == 200
        data = response.json()
        assert data["prediction_date"] == "2024-01-15"
        
        # Test multiple parameters
        response = client.get(
            "/api/crime-map/hotspots?city=chicago&crime_type=theft&time_window=24h"
        )
        assert response.status_code == 200

    def test_temporal_patterns_endpoint(self):
        """Test temporal patterns endpoint"""
        response = client.get("/api/crime-map/temporal-patterns?grid_id=grid_0_0&days=7")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "grid_id" in data
        assert data["grid_id"] == "grid_0_0"
        assert "hourly_pattern" in data
        assert "daily_pattern" in data
        assert "peak_hours" in data
        assert "safest_hours" in data
        
        # Check hourly pattern structure
        assert len(data["hourly_pattern"]) == 24
        assert all("hour" in item and "incidents" in item for item in data["hourly_pattern"])
        
        # Check daily pattern structure
        assert len(data["daily_pattern"]) == 7
        assert all("date" in item and "incidents" in item for item in data["daily_pattern"])

    def test_coverage_area_structure(self):
        """Test coverage area structure"""
        response = client.get("/api/crime-map/hotspots")
        data = response.json()
        
        coverage = data["coverage_area"]
        assert "center" in coverage
        assert "radius_km" in coverage
        assert "lat" in coverage["center"]
        assert "lng" in coverage["center"]
        assert isinstance(coverage["radius_km"], (int, float))
        assert coverage["radius_km"] > 0

    def test_risk_level_distribution(self):
        """Test that risk levels are properly assigned"""
        response = client.get("/api/crime-map/hotspots")
        data = response.json()
        
        risk_levels = [h["risk_level"] for h in data["hotspots"]]
        valid_levels = {"low", "medium", "high", "critical"}
        
        assert all(level in valid_levels for level in risk_levels)
        
        # Check that risk levels match intensity
        for hotspot in data["hotspots"]:
            intensity = hotspot["intensity"]
            risk_level = hotspot["risk_level"]
            
            if intensity > 0.8:
                assert risk_level == "critical"
            elif intensity > 0.6:
                assert risk_level == "high"
            elif intensity > 0.3:
                assert risk_level == "medium"
            else:
                assert risk_level == "low"

    def test_hotspot_intensity_range(self):
        """Test that hotspot intensities are in valid range"""
        response = client.get("/api/crime-map/hotspots")
        data = response.json()
        
        for hotspot in data["hotspots"]:
            assert 0 <= hotspot["intensity"] <= 1
            assert hotspot["intensity"] > 0.1  # Only significant hotspots included

    def test_response_consistency(self):
        """Test that multiple calls return consistent structure"""
        response1 = client.get("/api/crime-map/hotspots")
        response2 = client.get("/api/crime-map/hotspots")
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        data1 = response1.json()
        data2 = response2.json()
        
        # Structure should be consistent
        assert set(data1.keys()) == set(data2.keys())
        assert len(data1["hotspots"]) == len(data2["hotspots"])

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

