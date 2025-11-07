"""
Quick Test Runner for F2 Temporal Patterns
Tests backend endpoints and provides frontend testing instructions
"""
import requests
import json
import sys
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def print_success(message):
    print(f"✅ {message}")

def print_error(message):
    print(f"❌ {message}")

def print_info(message):
    print(f"ℹ️  {message}")

def test_backend_connection():
    """Test if backend is running"""
    print_header("TEST 1: Backend Connection")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print_success("Backend is running and healthy!")
            return True
        else:
            print_error(f"Backend returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to backend. Is it running on port 8000?")
        print_info("Start backend with: cd project/repo-foresight/src/api && uvicorn main:app --reload")
        return False
    except Exception as e:
        print_error(f"Error connecting to backend: {e}")
        return False

def test_temporal_analysis():
    """Test /api/temporal/analysis endpoint"""
    print_header("TEST 2: Temporal Analysis Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/api/temporal/analysis", params={
            "crime_type": "all",
            "location": "downtown",
            "days_back": 30
        }, timeout=10)
        
        if response.status_code != 200:
            print_error(f"Status {response.status_code}: {response.text}")
            return False
            
        data = response.json()
        
        # Validate structure
        checks = [
            ("hourly_patterns", len(data.get("hourly_patterns", [])) == 24, "24 hourly patterns"),
            ("day_of_week_patterns", len(data.get("day_of_week_patterns", [])) == 7, "7 day patterns"),
            ("time_series", len(data.get("time_series", [])) == 30, "30 time series points"),
            ("peak_times", "hours" in data.get("peak_times", {}), "peak_times.hours exists"),
            ("insights", len(data.get("insights", [])) > 0, "insights array"),
            ("seasonality_detected", isinstance(data.get("seasonality_detected"), bool), "seasonality_detected boolean")
        ]
        
        all_passed = True
        for field, check, description in checks:
            if check:
                print_success(f"{description}")
            else:
                print_error(f"{description} - FAILED")
                all_passed = False
        
        if all_passed:
            print(f"\n   Sample data:")
            print(f"   - Peak hours: {data['peak_times']['hours'][:3]}")
            print(f"   - Peak days: {data['peak_times']['days'][:2]}")
            print(f"   - Insights: {len(data['insights'])} items")
            return True
        return False
        
    except Exception as e:
        print_error(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_forecast():
    """Test /api/temporal/forecast endpoint"""
    print_header("TEST 3: Forecast Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/api/temporal/forecast", params={
            "crime_type": "all",
            "location": "downtown",
            "forecast_days": 7
        }, timeout=10)
        
        if response.status_code != 200:
            print_error(f"Status {response.status_code}: {response.text}")
            return False
            
        data = response.json()
        
        checks = [
            ("forecasts", len(data.get("forecasts", [])) == 7, "7 forecasts"),
            ("forecast_period", "forecast_period" in data, "forecast_period field"),
            ("total_predicted", isinstance(data.get("total_predicted"), int), "total_predicted number"),
            ("avg_daily_incidents", isinstance(data.get("avg_daily_incidents"), (int, float)), "avg_daily_incidents number")
        ]
        
        all_passed = True
        for field, check, description in checks:
            if check:
                print_success(f"{description}")
            else:
                print_error(f"{description} - FAILED")
                all_passed = False
        
        if all_passed:
            print(f"\n   Sample forecast:")
            if data.get("forecasts"):
                first = data["forecasts"][0]
                print(f"   - Date: {first.get('date')}")
                print(f"   - Predicted: {first.get('predicted_incidents')} incidents")
                print(f"   - Risk: {first.get('risk_level')}")
                print(f"   - Patrol units: {first.get('recommended_patrol_units')}")
            return True
        return False
        
    except Exception as e:
        print_error(f"Test failed: {e}")
        return False

def test_anomalies():
    """Test /api/temporal/anomalies endpoint"""
    print_header("TEST 4: Anomalies Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/api/temporal/anomalies", params={
            "days_back": 30,
            "threshold": 2.0
        }, timeout=10)
        
        if response.status_code != 200:
            print_error(f"Status {response.status_code}: {response.text}")
            return False
            
        data = response.json()
        
        checks = [
            ("anomalies", isinstance(data.get("anomalies"), list), "anomalies array"),
            ("anomalies_detected", isinstance(data.get("anomalies_detected"), int), "anomalies_detected count"),
            ("recommendation", "recommendation" in data, "recommendation field")
        ]
        
        all_passed = True
        for field, check, description in checks:
            if check:
                print_success(f"{description}")
            else:
                print_error(f"{description} - FAILED")
                all_passed = False
        
        if all_passed:
            print(f"\n   Anomaly details:")
            print(f"   - Detected: {data.get('anomalies_detected')} anomalies")
            if data.get("anomalies"):
                first = data["anomalies"][0]
                print(f"   - Example: {first.get('date')} - {first.get('actual_incidents')} incidents (expected {first.get('expected_incidents')})")
                print(f"   - Deviation: {first.get('deviation')}σ")
                print(f"   - Severity: {first.get('severity')}")
            print(f"   - Recommendation: {data.get('recommendation')}")
            return True
        return False
        
    except Exception as e:
        print_error(f"Test failed: {e}")
        return False

def test_query_parameters():
    """Test endpoints with different query parameters"""
    print_header("TEST 5: Query Parameter Variations")
    try:
        tests = [
            ("Different crime types", lambda: requests.get(f"{BASE_URL}/api/temporal/analysis", params={"crime_type": "theft"})),
            ("Different locations", lambda: requests.get(f"{BASE_URL}/api/temporal/analysis", params={"location": "northside"})),
            ("Different days_back", lambda: requests.get(f"{BASE_URL}/api/temporal/analysis", params={"days_back": 7})),
            ("Forecast 14 days", lambda: requests.get(f"{BASE_URL}/api/temporal/forecast", params={"forecast_days": 14}))
        ]
        
        all_passed = True
        for name, test_func in tests:
            try:
                response = test_func()
                if response.status_code == 200:
                    print_success(f"{name}")
                else:
                    print_error(f"{name} - Status {response.status_code}")
                    all_passed = False
            except Exception as e:
                print_error(f"{name} - Error: {e}")
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print_error(f"Test failed: {e}")
        return False

def print_frontend_instructions():
    """Print instructions for frontend testing"""
    print_header("FRONTEND TESTING INSTRUCTIONS")
    print("\nTo test the frontend components:")
    print("\n1. Start the frontend server:")
    print("   cd project/repo-foresight/frontend")
    print("   npm install  # If recharts not installed")
    print("   npm run dev")
    print("\n2. Open browser: http://localhost:5173/temporal-patterns")
    print("\n3. Manual checks:")
    print("   ✅ Hourly chart displays 24 bars with severity line")
    print("   ✅ Weekly chart shows 7 days with trend badges")
    print("   ✅ Forecast chart shows actual vs predicted with confidence bands")
    print("   ✅ Anomalies tab shows alert cards")
    print("   ✅ Forecast table shows 7-day predictions")
    print("   ✅ Tabs switch smoothly")
    print("   ✅ Filters update charts when changed")
    print("   ✅ Charts are responsive (resize browser)")
    print("   ✅ Tooltips appear on hover")
    print("\n4. Check browser console for errors (F12)")
    print("5. Check Network tab to verify API calls")

if __name__ == "__main__":
    print("\n" + "="*70)
    print("  F2 TEMPORAL PATTERNS - QUICK TEST RUNNER")
    print("="*70)
    
    results = []
    
    # Test backend connection first
    if not test_backend_connection():
        print("\n⚠️  Backend is not running. Please start it first:")
        print("   cd project/repo-foresight/src/api")
        print("   uvicorn main:app --reload")
        print("\nThen run this test again.")
        sys.exit(1)
    
    # Run backend tests
    results.append(("Temporal Analysis", test_temporal_analysis()))
    results.append(("Forecast", test_forecast()))
    results.append(("Anomalies", test_anomalies()))
    results.append(("Query Parameters", test_query_parameters()))
    
    # Summary
    print_header("TEST SUMMARY")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {status}: {name}")
    
    print(f"\n  Backend Tests: {passed}/{total} passed")
    
    if passed == total:
        print("\n🎉 All backend tests passed!")
        print_frontend_instructions()
    else:
        print("\n⚠️  Some backend tests failed. Check errors above.")
        print_frontend_instructions()

