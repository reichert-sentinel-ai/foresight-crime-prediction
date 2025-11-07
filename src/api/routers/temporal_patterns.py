from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional, Union, Any
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

router = APIRouter(prefix="/api/temporal", tags=["temporal-patterns"])

class HourlyPattern(BaseModel):
    hour: int
    incidents: int
    avg_response_time: float  # minutes
    severity_score: float  # 0-10 scale

class DayOfWeekPattern(BaseModel):
    day: str
    day_num: int
    incidents: int
    trend: str  # "increasing", "stable", "decreasing"

class TimeSeriesPoint(BaseModel):
    timestamp: str
    actual_incidents: int
    predicted_incidents: int
    confidence_lower: int
    confidence_upper: int
    accuracy: float

class TemporalAnalysis(BaseModel):
    hourly_patterns: List[HourlyPattern]
    day_of_week_patterns: List[DayOfWeekPattern]
    time_series: List[TimeSeriesPoint]
    peak_times: Dict[str, List[Union[int, str]]]  # hours are int, days are str
    insights: List[str]
    seasonality_detected: bool

@router.get("/analysis", response_model=TemporalAnalysis)
async def get_temporal_analysis(
    crime_type: str = Query("all", description="Crime type to analyze"),
    location: str = Query("downtown", description="Location/district"),
    days_back: int = Query(30, description="Days of historical data")
):
    """
    Comprehensive temporal pattern analysis for crime prediction.
    """
    
    # Generate hourly patterns (24 hours)
    hourly_patterns = []
    for hour in range(24):
        # Simulate realistic crime patterns (higher at night/evening)
        if 0 <= hour < 6:  # Late night/early morning
            base_incidents = 15
        elif 6 <= hour < 12:  # Morning
            base_incidents = 8
        elif 12 <= hour < 18:  # Afternoon
            base_incidents = 12
        else:  # Evening/night
            base_incidents = 25
        
        incidents = int(base_incidents * np.random.uniform(0.7, 1.3))
        
        hourly_patterns.append(HourlyPattern(
            hour=hour,
            incidents=incidents,
            avg_response_time=round(np.random.uniform(3.5, 8.5), 1),
            severity_score=round(np.random.uniform(3, 8), 1)
        ))
    
    # Generate day of week patterns
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_of_week_patterns = []
    
    for idx, day in enumerate(days):
        # Weekend has higher crime rates
        if idx >= 5:  # Weekend
            base_incidents = 180
        else:  # Weekday
            base_incidents = 120
        
        incidents = int(base_incidents * np.random.uniform(0.8, 1.2))
        
        # Determine trend
        if idx in [4, 5, 6]:  # Friday, Saturday, Sunday
            trend = "increasing"
        elif idx in [0, 1]:  # Monday, Tuesday
            trend = "decreasing"
        else:
            trend = "stable"
        
        day_of_week_patterns.append(DayOfWeekPattern(
            day=day,
            day_num=idx,
            incidents=incidents,
            trend=trend
        ))
    
    # Generate time series data (last 30 days)
    time_series = []
    start_date = datetime.now() - timedelta(days=days_back)
    
    for day in range(days_back):
        date = start_date + timedelta(days=day)
        
        # Base prediction with trend
        base_prediction = 100 + (day * 0.5)  # Slight upward trend
        
        # Add weekly seasonality
        day_of_week = date.weekday()
        if day_of_week >= 5:  # Weekend
            seasonal_factor = 1.4
        else:
            seasonal_factor = 1.0
        
        predicted = int(base_prediction * seasonal_factor)
        actual = int(predicted * np.random.uniform(0.85, 1.15))
        
        # Confidence intervals
        confidence_range = predicted * 0.15
        
        # Calculate accuracy
        accuracy = max(0, 1 - abs(actual - predicted) / predicted)
        
        time_series.append(TimeSeriesPoint(
            timestamp=date.strftime("%Y-%m-%d"),
            actual_incidents=actual,
            predicted_incidents=predicted,
            confidence_lower=int(predicted - confidence_range),
            confidence_upper=int(predicted + confidence_range),
            accuracy=round(accuracy, 3)
        ))
    
    # Identify peak times
    sorted_hours = sorted(hourly_patterns, key=lambda x: x.incidents, reverse=True)[:5]
    peak_hours = [h.hour for h in sorted_hours]
    sorted_days = sorted(day_of_week_patterns, key=lambda x: x.incidents, reverse=True)[:3]
    peak_days = [d.day for d in sorted_days]
    
    peak_times = {
        "hours": peak_hours,
        "days": peak_days
    }
    
    # Generate insights
    insights = [
        f"Peak crime hours: {', '.join([f'{h}:00' for h in peak_hours[:3]])}",
        f"Highest risk days: {', '.join(peak_days)}",
        f"Weekend incidents are {int((180/120 - 1) * 100)}% higher than weekdays",
        f"Average prediction accuracy: {round(np.mean([ts.accuracy for ts in time_series]) * 100, 1)}%",
        f"Night hours (8 PM - 2 AM) account for 45% of total incidents"
    ]
    
    return TemporalAnalysis(
        hourly_patterns=hourly_patterns,
        day_of_week_patterns=day_of_week_patterns,
        time_series=time_series,
        peak_times=peak_times,
        insights=insights,
        seasonality_detected=True
    )


@router.get("/forecast")
async def get_crime_forecast(
    crime_type: str = Query("all"),
    location: str = Query("downtown"),
    forecast_days: int = Query(7, ge=1, le=30)
):
    """
    Generate crime incident forecast for next N days.
    """
    
    forecast_data = []
    base_date = datetime.now()
    
    for day in range(forecast_days):
        date = base_date + timedelta(days=day + 1)
        day_of_week = date.weekday()
        
        # Weekend adjustment
        if day_of_week >= 5:
            base_incidents = 180
        else:
            base_incidents = 120
        
        # Add some variation
        predicted = int(base_incidents * np.random.uniform(0.9, 1.1))
        
        forecast_data.append({
            "date": date.strftime("%Y-%m-%d"),
            "day_of_week": date.strftime("%A"),
            "predicted_incidents": predicted,
            "confidence": round(np.random.uniform(0.70, 0.90), 2),
            "risk_level": "high" if predicted > 160 else "medium" if predicted > 120 else "low",
            "recommended_patrol_units": max(5, int(predicted / 30))
        })
    
    return {
        "forecast_period": f"{forecast_days} days",
        "generated_at": datetime.now().isoformat(),
        "location": location,
        "crime_type": crime_type,
        "forecasts": forecast_data,
        "total_predicted": sum(f["predicted_incidents"] for f in forecast_data),
        "avg_daily_incidents": round(sum(f["predicted_incidents"] for f in forecast_data) / forecast_days, 1)
    }


@router.get("/anomalies")
async def detect_temporal_anomalies(
    days_back: int = Query(30),
    threshold: float = Query(2.0, description="Standard deviations from mean")
):
    """
    Detect anomalous crime spikes in historical data.
    """
    
    anomalies = []
    
    # Generate some anomaly examples
    anomaly_dates = [
        datetime.now() - timedelta(days=5),
        datetime.now() - timedelta(days=12),
        datetime.now() - timedelta(days=23)
    ]
    
    for date in anomaly_dates:
        anomalies.append({
            "date": date.strftime("%Y-%m-%d"),
            "expected_incidents": 120,
            "actual_incidents": 215,
            "deviation": 3.2,
            "severity": "high",
            "possible_causes": [
                "Major sporting event",
                "Holiday weekend",
                "Increased foot traffic"
            ],
            "similar_historical_events": [
                {
                    "date": (date - timedelta(days=365)).strftime("%Y-%m-%d"),
                    "description": "Similar spike observed last year"
                }
            ]
        })
    
    return {
        "analysis_period_days": days_back,
        "threshold_std_dev": threshold,
        "anomalies_detected": len(anomalies),
        "anomalies": anomalies,
        "recommendation": "Increase patrol presence during similar upcoming events"
    }

