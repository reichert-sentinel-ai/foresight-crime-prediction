"""
Quick script to start backend and verify it's running
"""
import subprocess
import sys
import os
import time
import requests

def check_port_8000():
    """Check if port 8000 is in use"""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', 8000))
    sock.close()
    return result == 0

def start_backend():
    """Start the backend server"""
    print("Starting backend server...")
    print("=" * 60)
    
    # Change to api directory
    api_dir = os.path.join(os.path.dirname(__file__), 'src', 'api')
    if not os.path.exists(api_dir):
        print(f"❌ Error: Directory not found: {api_dir}")
        print("Current directory:", os.getcwd())
        return False
    
    os.chdir(api_dir)
    print(f"Changed to: {os.getcwd()}")
    
    # Start uvicorn
    print("\nStarting uvicorn server on port 8000...")
    print("Press CTRL+C to stop the server")
    print("=" * 60)
    
    try:
        subprocess.run([
            sys.executable, '-m', 'uvicorn', 
            'main:app', 
            '--reload', 
            '--port', '8000',
            '--host', '0.0.0.0'
        ])
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
        return True
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False

def test_backend():
    """Test if backend is accessible"""
    print("\nTesting backend connectivity...")
    try:
        response = requests.get('http://localhost:8000/health', timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running and accessible!")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Backend returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Is it running?")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("FORESIGHT BACKEND SERVER STARTER")
    print("=" * 60)
    
    # Check if already running
    if check_port_8000():
        print("\n⚠️  Port 8000 is already in use!")
        print("   Testing if it's our backend...")
        if test_backend():
            print("\n✅ Backend is already running!")
            print("   You can use it now.")
            sys.exit(0)
        else:
            print("\n❌ Port 8000 is in use by something else.")
            print("   Please stop the other service or use a different port.")
            sys.exit(1)
    
    # Start backend
    print("\n📡 Starting backend server...")
    start_backend()
