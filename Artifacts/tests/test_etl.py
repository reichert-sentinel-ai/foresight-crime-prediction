"""
Tests for ETL pipeline
"""

import pytest
import pandas as pd
from datetime import datetime
from src.data.etl import CrimeDataETL


def test_etl_initialization():
    """Test ETL initialization"""
    etl = CrimeDataETL()
    assert etl is not None
    assert etl.data_dir is not None


def test_sample_data_creation():
    """Test sample data creation"""
    etl = CrimeDataETL()
    df = etl._create_sample_data()
    
    assert df is not None
    assert len(df) > 0
    assert 'incident_date' in df.columns
    assert 'crime_type' in df.columns
    assert 'latitude' in df.columns
    assert 'longitude' in df.columns


def test_aggregate_daily_counts():
    """Test daily aggregation"""
    etl = CrimeDataETL()
    df = etl._create_sample_data()
    
    daily_counts = etl.aggregate_daily_counts(df)
    
    assert daily_counts is not None
    assert len(daily_counts) > 0
    assert 'incident_date' in daily_counts.columns


def test_add_temporal_features():
    """Test temporal feature addition"""
    etl = CrimeDataETL()
    df = etl._create_sample_data()
    daily_counts = etl.aggregate_daily_counts(df)
    
    processed_df = etl.add_temporal_features(daily_counts)
    
    assert processed_df is not None
    assert 'year' in processed_df.columns
    assert 'month' in processed_df.columns
    assert 'day_of_week' in processed_df.columns
    assert 'is_weekend' in processed_df.columns


def test_etl_pipeline():
    """Test complete ETL pipeline"""
    etl = CrimeDataETL()
    df = etl.process()
    
    assert df is not None
    assert len(df) > 0

