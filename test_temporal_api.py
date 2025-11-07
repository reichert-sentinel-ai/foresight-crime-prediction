"""
Test script for Temporal Patterns API endpoints
Tests all endpoints return valid data structures
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_temporal_analysis():
    """Test /api/temporal/analysis endpoint"""
    print("\n" + "="*60)
    print("Testing /api/temporal/analysis endpoint")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/temporal/analysis", params={
            "crime_type": "all",
            "location": "downtown",
            "days_back": 30
        })
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        
        # Validate structure
        assert "hourly_patterns" in data, "Missing hourly_patterns"
        assert "day_of_week_patterns" in data, "Missing day_of_week_patterns"
        assert "time_series" in data, "Missing time_series"
        assert "peak_times" in data, "Missing peak_times"
        assert "insights" in data, "Missing insights"
        assert "seasonality_detected" in data, "Missing seasonality_detected"
        
        # Validate hourly patterns
        assert len(data["hourly_patterns"]) == 24, f"Expected 24 hourly patterns, got {len(data['hourly_patterns'])}"
        for pattern in data["hourly_patterns"]:
            assert "hour" in pattern and 0 <= pattern["hour"] < 24
            assert "incidents" in pattern and isinstance(pattern["incidents"], int)
            assert "avg_response_time" in pattern and isinstance(pattern["avg_response_time"], (int, float))
            assert "severity_score" in pattern and isinstance(pattern["severity_score"], (int, float))
        
        # Validate day of week patterns
        assert len(data["day_of_week_patterns"]) == 7, f"Expected 7 day patterns, got {len(data['day_of_week_patterns'])}"
        for pattern in data["day_of_week_patterns"]:
            assert "day" in pattern
            assert "day_num" in pattern and 0 <= pattern["day_num"] < 7
            assert "incidents" in pattern and isinstance(pattern["incidents"], int)
            assert "trend" in pattern and pattern["trend"] in ["increasing", "stable", "decreasing"]
        
        # Validate time series
        assert len(data["time_series"]) == 30, f"Expected 30 time series points, got {len(data['time_series'])}"
        for point in data["time_series"]:
            assert "timestamp" in point
            assert "actual_incidents" in point and isinstance(point["actual_incidents"], int)
            assert "predicted_incidents" in point and isinstance(point["predicted_incidents"], int)
            assert "confidence_lower" in point and isinstance(point["confidence_lower"], int)
            assert "confidence_upper" in point and isinstance(point["confidence_upper"], int)
            assert "accuracy" in point and isinstance(point["accuracy"], (int, float))
        
        # Validate peak times
        assert "hours" in data["peak_times"] and isinstance(data["peak_times"]["hours"], list)
        assert "days" in data["peak_times"] and isinstance(data["peak_times"]["days"], list)
        
        print("✅ All validations passed!")
        print(f"   - Hourly patterns: {len(data['hourly_patterns'])} entries")
        print(f"   - Day patterns: {len(data['day_of_week_patterns'])} entries")
        print(f"   - Time series points: {len(data['time_series'])} entries")
        print(f"   - Peak hours: {data['peak_times']['hours']}")
        print(f"   - Peak days: {data['peak_times']['days']}")
        print(f"   - Insights: {len(data['insights'])} items")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_forecast():
    """Test /api/temporal/forecast endpoint"""
    print("\n" + "="*60)
    print("Testing /api/temporal/forecast endpoint")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/temporal/forecast", params={
            "crime_type": "all",
            "location": "downtown",
            "forecast_days": 7
        })
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        
        # Validate structure
        assert "forecast_period" in data
        assert "generated_at" in data
        assert "location" in data
        assert "crime_type" in data
        assert "forecasts" in data
        assert "total_predicted" in data
        assert "avg_daily_incidents" in data
        
        # Validate forecasts
        assert len(data["forecasts"]) == 7, f"Expected 7 forecasts, got {len(data['forecasts'])}"
        for forecast in data["forecasts"]:
            assert "date" in forecast
            assert "day_of_week" in forecast
            assert "predicted_incidents" in forecast and isinstance(forecast["predicted_incidents"], int)
            assert "confidence" in forecast and isinstance(forecast["confidence"], (int, float))
            assert "risk_level" in forecast and forecast["risk_level"] in ["high", "medium", "low"]
            assert "recommended_patrol_units" in forecast and isinstance(forecast["recommended_patrol_units"], int)
        
        print("✅ All validations passed!")
        print(f"   - Forecast period: {data['forecast_period']}")
        print(f"   - Number of forecasts: {len(data['forecasts'])}")
        print(f"   - Total predicted incidents: {data['total_predicted']}")
        print(f"   - Average daily incidents: {data['avg_daily_incidents']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_anomalies():
    """Test /api/temporal/anomalies endpoint"""
    print("\n" + "="*60)
    print("Testing /api/temporal/anomalies endpoint")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/temporal/anomalies", params={
            "days_back": 30,
            "threshold": 2.0
        })
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        
        # Validate structure
        assert "analysis_period_days" in data
        assert "threshold_std_dev" in data
        assert "anomalies_detected" in data
        assert "anomalies" in data
        assert "recommendation" in data
        
        # Validate anomalies
        assert isinstance(data["anomalies"], list)
        for anomaly in data["anomalies"]:
            assert "date" in anomaly
            assert "expected_incidents" in anomaly and isinstance(anomaly["expected_incidents"], int)
            assert "actual_incidents" in anomaly and isinstance(anomaly["actual_incidents"], int)
            assert "deviation" in anomaly and isinstance(anomaly["deviation"], (int, float))
            assert "severity" in anomaly and anomaly["severity"] in ["high", "medium", "low"]
            assert "possible_causes" in anomaly and isinstance(anomaly["possible_causes"], list)
            assert "similar_historical_events" in anomaly and isinstance(anomaly["similar_historical_events"], list)
        
        print("✅ All validations passed!")
        print(f"   - Analysis period: {data['analysis_period_days']} days")
        print(f"   - Threshold: {data['threshold_std_dev']}σ")
        print(f"   - Anomalies detected: {data['anomalies_detected']}")
        print(f"   - Recommendation: {data['recommendation']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_query_parameters():
    """Test endpoints with different query parameters"""
    print("\n" + "="*60)
    print("Testing query parameter variations")
    print("="*60)
    
    try:
        # Test different crime types
        for crime_type in ["all", "theft", "assault"]:
            response = requests.get(f"{BASE_URL}/api/temporal/analysis", params={"crime_type": crime_type})
            assert response.status_code == 200, f"Failed for crime_type={crime_type}"
        
        # Test different locations
        for location in ["downtown", "northside", "southside"]:
            response = requests.get(f"{BASE_URL}/api/temporal/analysis", params={"location": location})
            assert response.status_code == 200, f"Failed for location={location}"
        
        # Test different days_back
        for days in [7, 14, 30]:
            response = requests.get(f"{BASE_URL}/api/temporal/analysis", params={"days_back": days})
            assert response.status_code == 200, f"Failed for days_back={days}"
            data = response.json()
            assert len(data["time_series"]) == days, f"Expected {days} time series points"
        
        # Test forecast with different days
        for days in [1, 7, 14]:
            response = requests.get(f"{BASE_URL}/api/temporal/forecast", params={"forecast_days": days})
            assert response.status_code == 200, f"Failed for forecast_days={days}"
            data = response.json()
            assert len(data["forecasts"]) == days, f"Expected {days} forecasts"
        
        print("✅ All query parameter variations work correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n" + "="*60)
    print("TEMPORAL PATTERNS API TEST SUITE")
    print("="*60)
    
    results = []
    
    # Test endpoints
    results.append(("Temporal Analysis", test_temporal_analysis()))
    results.append(("Forecast", test_forecast()))
    results.append(("Anomalies", test_anomalies()))
    results.append(("Query Parameters", test_query_parameters()))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Backend endpoints are working correctly.")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")

