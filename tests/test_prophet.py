"""
Tests for Prophet forecaster
"""

import pytest
import pandas as pd
from datetime import datetime, timedelta
from src.models.prophet_forecaster import CrimeForecaster
from src.data.etl import CrimeDataETL


def test_forecaster_initialization():
    """Test forecaster initialization"""
    forecaster = CrimeForecaster()
    assert forecaster is not None
    assert forecaster.yearly_seasonality is True


def test_prepare_data():
    """Test data preparation"""
    etl = CrimeDataETL()
    df = etl.process()
    
    forecaster = CrimeForecaster()
    prophet_df = forecaster.prepare_data(df, target_column='total_crimes')
    
    assert prophet_df is not None
    assert 'ds' in prophet_df.columns
    assert 'y' in prophet_df.columns
    assert len(prophet_df) > 0


def test_create_holidays():
    """Test holiday creation"""
    forecaster = CrimeForecaster()
    holidays_df = forecaster.create_holidays()
    
    assert holidays_df is not None
    assert len(holidays_df) > 0
    assert 'holiday' in holidays_df.columns
    assert 'ds' in holidays_df.columns


def test_forecast():
    """Test forecast generation"""
    etl = CrimeDataETL()
    df = etl.process()
    
    forecaster = CrimeForecaster()
    forecaster.fit(df, target_column='total_crimes')
    
    forecast = forecaster.forecast(periods=7, include_history=False)
    
    assert forecast is not None
    assert len(forecast) == 7
    assert 'ds' in forecast.columns
    assert 'yhat' in forecast.columns
    assert 'yhat_lower' in forecast.columns
    assert 'yhat_upper' in forecast.columns

