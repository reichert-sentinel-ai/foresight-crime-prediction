"""
Verify that models are trained and meet performance targets.

Usage:
    python scripts/verify_model_training.py
"""
import pickle
import os
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def verify_prophet_model():
    """Verify Prophet model exists."""
    model_path = Path("models/prophet_model.pkl")
    
    if not model_path.exists():
        print("❌ Prophet model not found")
        print(f"   Expected location: {model_path.absolute()}")
        print("   Run: python src/models/prophet_forecaster.py")
        return False
    
    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        print(f"✅ Prophet model found")
        return True
    except Exception as e:
        print(f"❌ Error loading Prophet model: {e}")
        return False

def verify_performance_targets():
    """Verify performance targets are documented."""
    targets = {
        'forecast_accuracy': 0.725,
        'hotspot_precision': 0.893,
    }
    
    print("\nPerformance Targets:")
    for metric, target in targets.items():
        print(f"   {metric}: ≥{target:.2%}")
    
    print("\n⚠️  Model performance verification requires:")
    print("   1. Trained models")
    print("   2. Test data")
    print("   3. Running evaluation script")
    
    return False

if __name__ == "__main__":
    print("=" * 60)
    print("Foresight Model Training Verification")
    print("=" * 60)
    print()
    
    repo_dir = Path(__file__).parent.parent
    os.chdir(repo_dir)
    
    print("1. Model Files:")
    print("-" * 60)
    model_ok = verify_prophet_model()
    
    print("\n2. Performance Targets:")
    print("-" * 60)
    verify_performance_targets()
    
    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)
    
    if model_ok:
        print("✅ Model found!")
    else:
        print("⚠️  Model not found. See docs/MODEL_TRAINING_VERIFICATION.md for details.")

