"""
Tests for hotspot detection
"""

import pytest
import pandas as pd
import numpy as np
from src.models.dbscan_hotspots import CrimeHotspotDetector
from src.data.etl import CrimeDataETL


def test_hotspot_detector_initialization():
    """Test hotspot detector initialization"""
    detector = CrimeHotspotDetector()
    assert detector is not None
    assert detector.eps == 0.01


def test_prepare_coordinates():
    """Test coordinate preparation"""
    df = pd.DataFrame({
        'latitude': [41.8781, 41.8881, 41.8681],
        'longitude': [-87.6298, -87.6398, -87.6198]
    })
    
    detector = CrimeHotspotDetector()
    coords = detector.prepare_coordinates(df)
    
    assert coords is not None
    assert coords.shape == (3, 2)


def test_detect_hotspots():
    """Test hotspot detection"""
    etl = CrimeDataETL()
    df = etl.load_chicago_data()
    
    # Sample data
    sample_df = df.sample(min(1000, len(df)))
    
    detector = CrimeHotspotDetector(eps=0.01, min_samples=5)
    hotspots_df = detector.detect_hotspots(sample_df)
    
    assert hotspots_df is not None
    assert 'cluster' in hotspots_df.columns
    assert 'is_hotspot' in hotspots_df.columns


def test_calculate_hotspot_density():
    """Test density calculation"""
    etl = CrimeDataETL()
    df = etl.load_chicago_data()
    
    sample_df = df.sample(min(1000, len(df)))
    
    detector = CrimeHotspotDetector()
    hotspots_df = detector.detect_hotspots(sample_df)
    
    density_df = detector.calculate_hotspot_density(hotspots_df)
    
    assert density_df is not None
    if len(density_df) > 0:
        assert 'cluster_id' in density_df.columns
        assert 'density_per_km2' in density_df.columns

