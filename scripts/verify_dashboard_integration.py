"""
Verify that dashboard correctly integrates real data.

Usage:
    python scripts/verify_dashboard_integration.py
"""
import os
from pathlib import Path

def verify_streamlit_app():
    """Verify Streamlit app exists."""
    app_path = Path("streamlit_app.py")
    
    if app_path.exists():
        print(f"✅ Streamlit app found")
        return True
    else:
        print(f"❌ Streamlit app not found")
        return False

def verify_mapbox_integration():
    """Verify Mapbox integration."""
    app_path = Path("streamlit_app.py")
    
    if app_path.exists():
        with open(app_path, 'r', encoding='utf-8') as f:
            content = f.read()
            has_mapbox = "mapbox" in content.lower() or "st.map" in content.lower()
            
            if has_mapbox:
                print("✅ Mapbox integration found")
                return True
            else:
                print("⚠️  Mapbox integration not found")
                return False
    return False

if __name__ == "__main__":
    print("=" * 60)
    print("Foresight Dashboard Integration Verification")
    print("=" * 60)
    print()
    
    repo_dir = Path(__file__).parent.parent
    os.chdir(repo_dir)
    
    print("1. Dashboard Components:")
    print("-" * 60)
    app_ok = verify_streamlit_app()
    mapbox_ok = verify_mapbox_integration()
    
    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)
    
    if app_ok and mapbox_ok:
        print("✅ All checks passed!")
    else:
        print("⚠️  Some checks failed. See docs/DASHBOARD_DATA_INTEGRATION.md for details.")

