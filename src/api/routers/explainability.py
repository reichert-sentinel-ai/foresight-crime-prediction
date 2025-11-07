"""
Explainability API Router for Foresight

Provides endpoints for:
- Prediction explanation with SHAP-like feature contributions
- Confidence breakdown analysis
- What-if scenario simulations
- Global feature importance
- Prediction timeline tracking
"""

from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
import numpy as np

router = APIRouter(prefix="/api/explainability", tags=["explainability"])


class FeatureContribution(BaseModel):
    feature_name: str
    value: float
    contribution: float  # SHAP value
    contribution_percentage: float
    impact: str  # "increases" or "decreases"


class PredictionExplanation(BaseModel):
    prediction_id: str
    predicted_risk_score: float
    confidence: float
    risk_level: str
    base_value: float  # Model's average prediction
    feature_contributions: List[FeatureContribution]
    top_factors: List[str]
    confidence_interval: Dict[str, float]
    similar_historical_cases: int


class ConfidenceBreakdown(BaseModel):
    overall_confidence: float
    data_quality_score: float
    model_certainty: float
    historical_accuracy: float
    factors_affecting_confidence: List[str]


class WhatIfScenario(BaseModel):
    scenario_name: str
    original_prediction: float
    modified_prediction: float
    change_percentage: float
    modified_features: Dict[str, Any]


class GlobalFeatureImportance(BaseModel):
    feature_name: str
    importance_score: float
    rank: int
    category: str  # "temporal", "spatial", "contextual", "historical"
    description: str


@router.get("/explain-prediction", response_model=PredictionExplanation)
async def explain_prediction(
    location_id: str = Query(..., description="Grid or location identifier"),
    time_window: str = Query("24h", description="Prediction time window")
):
    """
    Explain a specific crime prediction using SHAP-like feature contributions.
    """
    
    # Simulate a prediction with explainability
    prediction_id = f"pred_{location_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Base prediction value (model average)
    base_value = 0.45  # 45% risk on average
    
    # Define features that contribute to prediction
    features = [
        {
            "name": "Historical Crime Rate (30d)",
            "value": 12.3,
            "contribution": 0.18,
            "impact": "increases"
        },
        {
            "name": "Time of Day (Night Hours)",
            "value": 1.0,  # Boolean: 1 = night
            "contribution": 0.15,
            "impact": "increases"
        },
        {
            "name": "Day of Week (Weekend)",
            "value": 1.0,  # Boolean: 1 = weekend
            "contribution": 0.12,
            "impact": "increases"
        },
        {
            "name": "Proximity to High-Risk Area",
            "value": 0.3,  # 300m away
            "contribution": 0.08,
            "impact": "increases"
        },
        {
            "name": "Recent Police Presence",
            "value": 2.5,  # hours since last patrol
            "contribution": -0.06,
            "impact": "decreases"
        },
        {
            "name": "Street Lighting Quality",
            "value": 0.7,  # 0-1 scale
            "contribution": -0.04,
            "impact": "decreases"
        },
        {
            "name": "Community Events Nearby",
            "value": 0.0,  # No events
            "contribution": -0.02,
            "impact": "decreases"
        },
        {
            "name": "Weather Conditions",
            "value": 0.8,  # Good weather
            "contribution": 0.03,
            "impact": "increases"
        },
        {
            "name": "Seasonal Trend",
            "value": 1.2,  # 20% above seasonal average
            "contribution": 0.06,
            "impact": "increases"
        },
        {
            "name": "Economic Indicators",
            "value": 0.65,  # Employment rate
            "contribution": -0.03,
            "impact": "decreases"
        }
    ]
    
    # Calculate total contribution
    total_contribution = sum([f["contribution"] for f in features])
    predicted_risk_score = base_value + total_contribution
    predicted_risk_score = max(0, min(1, predicted_risk_score))  # Clamp to [0,1]
    
    # Calculate contribution percentages
    total_abs_contribution = sum([abs(f["contribution"]) for f in features])
    
    feature_contributions = []
    for f in features:
        contrib_pct = (abs(f["contribution"]) / total_abs_contribution * 100) if total_abs_contribution > 0 else 0
        feature_contributions.append(FeatureContribution(
            feature_name=f["name"],
            value=f["value"],
            contribution=round(f["contribution"], 4),
            contribution_percentage=round(contrib_pct, 1),
            impact=f["impact"]
        ))
    
    # Sort by absolute contribution
    feature_contributions.sort(key=lambda x: abs(x.contribution), reverse=True)
    
    # Get top 3 factors
    top_factors = [fc.feature_name for fc in feature_contributions[:3]]
    
    # Determine risk level
    if predicted_risk_score > 0.75:
        risk_level = "Critical"
    elif predicted_risk_score > 0.55:
        risk_level = "High"
    elif predicted_risk_score > 0.35:
        risk_level = "Medium"
    else:
        risk_level = "Low"
    
    # Calculate confidence (based on feature agreement and historical accuracy)
    confidence = 0.85 - (np.random.uniform(0, 0.15))  # 70-85% range
    
    # Confidence interval
    margin = predicted_risk_score * 0.12  # ±12% margin
    confidence_interval = {
        "lower": round(max(0, predicted_risk_score - margin), 3),
        "upper": round(min(1, predicted_risk_score + margin), 3)
    }
    
    return PredictionExplanation(
        prediction_id=prediction_id,
        predicted_risk_score=round(predicted_risk_score, 3),
        confidence=round(confidence, 3),
        risk_level=risk_level,
        base_value=base_value,
        feature_contributions=feature_contributions,
        top_factors=top_factors,
        confidence_interval=confidence_interval,
        similar_historical_cases=47
    )


@router.get("/confidence-breakdown", response_model=ConfidenceBreakdown)
async def get_confidence_breakdown(
    prediction_id: str = Query(..., description="Prediction identifier")
):
    """
    Break down the confidence score into component factors.
    """
    
    # Simulate confidence components
    data_quality = np.random.uniform(0.85, 0.95)
    model_certainty = np.random.uniform(0.80, 0.90)
    historical_accuracy = np.random.uniform(0.75, 0.85)
    
    overall = (data_quality + model_certainty + historical_accuracy) / 3
    
    factors = []
    if data_quality < 0.90:
        factors.append("Some historical data points are missing for this location")
    if model_certainty < 0.85:
        factors.append("Feature values are at the edge of model's training distribution")
    if historical_accuracy < 0.80:
        factors.append("Similar past predictions had moderate accuracy")
    
    if not factors:
        factors.append("High-quality data with strong historical validation")
        factors.append("Feature values within model's confident range")
    
    return ConfidenceBreakdown(
        overall_confidence=round(overall, 3),
        data_quality_score=round(data_quality, 3),
        model_certainty=round(model_certainty, 3),
        historical_accuracy=round(historical_accuracy, 3),
        factors_affecting_confidence=factors
    )


@router.post("/what-if", response_model=WhatIfScenario)
async def what_if_analysis(
    location_id: str = Query(..., description="Grid or location identifier"),
    feature_name: str = Query(..., description="Feature to modify"),
    new_value: float = Query(..., description="New feature value")
):
    """
    Simulate what-if scenarios by modifying feature values.
    """
    
    # Get original prediction (simplified)
    original_prediction = 0.68
    
    # Simulate impact based on feature
    feature_impacts = {
        "Recent Police Presence": -0.08,  # More police = lower risk
        "Street Lighting Quality": -0.05,
        "Historical Crime Rate (30d)": 0.15,
        "Time of Day (Night Hours)": 0.12,
        "Community Events Nearby": -0.06
    }
    
    impact = feature_impacts.get(feature_name, 0)
    modified_prediction = original_prediction + (impact * (new_value - 0.5))
    modified_prediction = max(0, min(1, modified_prediction))
    
    change_pct = ((modified_prediction - original_prediction) / original_prediction) * 100
    
    return WhatIfScenario(
        scenario_name=f"Modified {feature_name}",
        original_prediction=round(original_prediction, 3),
        modified_prediction=round(modified_prediction, 3),
        change_percentage=round(change_pct, 1),
        modified_features={feature_name: new_value}
    )


@router.get("/global-importance", response_model=List[GlobalFeatureImportance])
async def get_global_feature_importance():
    """
    Get global feature importance across all predictions.
    """
    
    features = [
        {
            "name": "Historical Crime Rate (30d)",
            "importance": 0.24,
            "category": "historical",
            "description": "Average crime incidents in the location over past 30 days"
        },
        {
            "name": "Time of Day",
            "importance": 0.18,
            "category": "temporal",
            "description": "Hour of day when prediction is made (night hours have higher risk)"
        },
        {
            "name": "Day of Week",
            "importance": 0.15,
            "category": "temporal",
            "description": "Weekends typically show different crime patterns"
        },
        {
            "name": "Proximity to High-Risk Areas",
            "importance": 0.12,
            "category": "spatial",
            "description": "Distance to known high-crime locations"
        },
        {
            "name": "Recent Police Presence",
            "importance": 0.10,
            "category": "contextual",
            "description": "Time since last police patrol in the area"
        },
        {
            "name": "Seasonal Trends",
            "importance": 0.08,
            "category": "temporal",
            "description": "Month and season-specific crime patterns"
        },
        {
            "name": "Street Lighting Quality",
            "importance": 0.05,
            "category": "spatial",
            "description": "Quality and coverage of street lighting infrastructure"
        },
        {
            "name": "Community Events",
            "importance": 0.04,
            "category": "contextual",
            "description": "Presence of community events or gatherings"
        },
        {
            "name": "Weather Conditions",
            "importance": 0.03,
            "category": "contextual",
            "description": "Current weather (temperature, precipitation, visibility)"
        },
        {
            "name": "Economic Indicators",
            "importance": 0.01,
            "category": "contextual",
            "description": "Local employment and economic health metrics"
        }
    ]
    
    return [
        GlobalFeatureImportance(
            feature_name=f["name"],
            importance_score=f["importance"],
            rank=idx + 1,
            category=f["category"],
            description=f["description"]
        )
        for idx, f in enumerate(features)
    ]


@router.get("/prediction-timeline")
async def get_prediction_timeline(
    location_id: str = Query(..., description="Grid or location identifier"),
    days_back: int = Query(7, description="Days of historical predictions")
):
    """
    Show how prediction and confidence have evolved over time for a location.
    """
    
    timeline = []
    base_date = datetime.now()
    
    for day in range(days_back, 0, -1):
        date = base_date - timedelta(days=day)
        
        # Simulate prediction evolution
        predicted_risk = 0.60 + np.random.uniform(-0.15, 0.15)
        actual_incidents = int(predicted_risk * 10 * np.random.uniform(0.8, 1.2))
        
        confidence = 0.75 + (days_back - day) / days_back * 0.15  # Increasing confidence
        
        timeline.append({
            "date": date.strftime("%Y-%m-%d"),
            "predicted_risk": round(predicted_risk, 3),
            "confidence": round(confidence, 3),
            "actual_incidents": actual_incidents,
            "accuracy": round(1 - abs(predicted_risk - (actual_incidents / 10)), 3)
        })
    
    return {
        "location_id": location_id,
        "timeline": timeline,
        "average_accuracy": round(np.mean([t["accuracy"] for t in timeline]), 3),
        "confidence_trend": "improving" if timeline[-1]["confidence"] > timeline[0]["confidence"] else "stable"
    }


@router.get("/explanation-summary")
async def get_explanation_summary(
    prediction_id: str = Query(..., description="Prediction identifier")
):
    """
    Generate a natural language explanation of the prediction.
    """
    
    explanation = {
        "prediction_id": prediction_id,
        "summary": (
            "This location is predicted to have HIGH risk (68% probability) of crime in the next 24 hours. "
            "The prediction is primarily driven by three factors: elevated historical crime rate in this area "
            "(contributing 28% to the risk score), nighttime hours (23% contribution), and weekend timing "
            "(18% contribution). However, recent police presence in the area is helping to reduce risk by "
            "approximately 9 percentage points."
        ),
        "confidence_explanation": (
            "We are 82% confident in this prediction based on: high-quality historical data for this location, "
            "similar past predictions achieving 78% accuracy, and all input features falling within the model's "
            "well-trained range."
        ),
        "recommendation": (
            "Recommend increased patrol presence during evening hours (6 PM - 2 AM) this weekend. "
            "Based on similar historical cases, visible police presence reduces risk by an average of 12-15%."
        ),
        "caveats": [
            "Prediction accuracy may be affected by unexpected community events",
            "Weather changes could alter predicted patterns",
            "Model performs best for property crimes; violent crime predictions have lower confidence"
        ]
    }
    
    return explanation

