"""
Quick test to verify explainability endpoints are working
Run this after starting the backend server
"""
import requests
import sys

BASE_URL = "http://localhost:8000"

def test_backend_health():
    """Test if backend is running"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        if response.status_code == 200:
            print("✅ Backend server is running")
            return True
        else:
            print(f"❌ Backend returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend server is NOT running")
        print("   Start it with: cd project/repo-foresight/src/api && python -m uvicorn main:app --reload --port 8000")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_explainability_endpoint():
    """Test explainability endpoint"""
    try:
        response = requests.get(
            f"{BASE_URL}/api/explainability/explain-prediction",
            params={"location_id": "grid_5_7"},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            print("✅ Explainability endpoint is working")
            print(f"   Prediction ID: {data.get('prediction_id', 'N/A')}")
            print(f"   Risk Score: {data.get('predicted_risk_score', 'N/A')}")
            print(f"   Confidence: {data.get('confidence', 'N/A')}")
            return True
        else:
            print(f"❌ Explainability endpoint returned status {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_all_endpoints():
    """Test all explainability endpoints"""
    endpoints = [
        ("/api/explainability/global-importance", "GET"),
        ("/api/explainability/prediction-timeline?location_id=grid_5_7", "GET"),
    ]
    
    results = []
    for endpoint, method in endpoints:
        try:
            if method == "GET":
                response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
            else:
                response = requests.post(f"{BASE_URL}{endpoint}", timeout=5)
            
            if response.status_code == 200:
                print(f"✅ {endpoint}")
                results.append(True)
            else:
                print(f"❌ {endpoint} - Status: {response.status_code}")
                results.append(False)
        except Exception as e:
            print(f"❌ {endpoint} - Error: {e}")
            results.append(False)
    
    return all(results)

if __name__ == "__main__":
    print("\n" + "="*60)
    print("EXPLAINABILITY API QUICK TEST")
    print("="*60 + "\n")
    
    # Test 1: Backend health
    if not test_backend_health():
        print("\n⚠️  Please start the backend server first!")
        sys.exit(1)
    
    print()
    
    # Test 2: Main explainability endpoint
    if not test_explainability_endpoint():
        print("\n⚠️  Explainability endpoint is not working!")
        sys.exit(1)
    
    print()
    
    # Test 3: Other endpoints
    print("Testing other endpoints...")
    if test_all_endpoints():
        print("\n🎉 All tests passed! Frontend should work now.")
    else:
        print("\n⚠️  Some endpoints failed, but main endpoint works.")

