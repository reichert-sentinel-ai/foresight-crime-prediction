"""
Verify that datasets are properly loaded and used in pipelines.

Usage:
    python scripts/verify_dataset_usage.py
"""
import pandas as pd
import os
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def verify_chicago_dataset():
    """Verify Chicago Crimes dataset exists."""
    chicago_path = Path("data/raw/chicago_crimes.csv")
    
    if not chicago_path.exists():
        print("❌ Chicago Crimes dataset not found")
        print(f"   Expected location: {chicago_path.absolute()}")
        print("   Download from: https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2")
        return False
    
    try:
        df = pd.read_csv(chicago_path, nrows=1000)
        print(f"✅ Chicago Crimes dataset found: {len(df)} sample rows loaded")
        print(f"   Columns: {list(df.columns)}")
        return True
    except Exception as e:
        print(f"❌ Error loading Chicago Crimes: {e}")
        return False

def verify_etl_pipeline():
    """Verify ETL pipeline exists."""
    etl_path = Path("src/data/etl.py")
    
    if etl_path.exists():
        print(f"✅ ETL pipeline exists: {etl_path}")
        return True
    else:
        print(f"❌ ETL pipeline not found: {etl_path}")
        return False

def verify_geospatial_utils():
    """Verify geospatial utilities exist."""
    geo_path = Path("src/data/geospatial.py")
    
    if geo_path.exists():
        print(f"✅ Geospatial utilities exist: {geo_path}")
        return True
    else:
        print(f"⚠️  Geospatial utilities not found: {geo_path}")
        return False

def verify_prophet_model():
    """Verify Prophet model exists."""
    prophet_path = Path("src/models/prophet_forecaster.py")
    
    if prophet_path.exists():
        print(f"✅ Prophet forecaster exists: {prophet_path}")
        return True
    else:
        print(f"⚠️  Prophet forecaster not found: {prophet_path}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Foresight Dataset Usage Verification")
    print("=" * 60)
    print()
    
    # Change to repo directory
    repo_dir = Path(__file__).parent.parent
    os.chdir(repo_dir)
    
    results = []
    
    print("1. Dataset Files:")
    print("-" * 60)
    chicago_ok = verify_chicago_dataset()
    results.append(chicago_ok)
    
    print("\n2. Pipeline Components:")
    print("-" * 60)
    etl_ok = verify_etl_pipeline()
    geo_ok = verify_geospatial_utils()
    prophet_ok = verify_prophet_model()
    results.extend([etl_ok, geo_ok, prophet_ok])
    
    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)
    
    passed = sum(1 for r in results if r)
    total = len(results)
    
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✅ All checks passed!")
    else:
        print("⚠️  Some checks failed. See details above.")
        print("\nNote: Dataset verification requires datasets to be downloaded.")
        print("See DATA_ACQUISITION_GUIDE.md for download instructions.")

