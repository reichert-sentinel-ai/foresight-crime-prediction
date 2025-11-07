from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import numpy as np
from scipy.spatial import distance

router = APIRouter(prefix="/api/crime-map", tags=["crime-map"])

class CrimeHotspot(BaseModel):
    lat: float
    lng: float
    intensity: float  # 0-1 scale
    crime_type: str
    predicted_incidents: int
    confidence: float
    grid_id: str
    risk_level: str  # "low", "medium", "high", "critical"

class HeatmapData(BaseModel):
    hotspots: List[CrimeHotspot]
    prediction_date: str
    model_version: str
    coverage_area: dict
    grid_resolution: str
    total_predicted_incidents: int

@router.get("/hotspots", response_model=HeatmapData)
async def get_crime_hotspots(
    city: str = Query("chicago", description="City name"),
    crime_type: str = Query("all", description="Crime type filter"),
    date: Optional[str] = Query(None, description="Prediction date (YYYY-MM-DD)"),
    time_window: str = Query("24h", description="Time window: 24h, 7d, 30d")
):
    """
    Get crime prediction hotspots for heatmap visualization.
    
    Returns grid-based predictions with intensity scores for mapping.
    """
    
    # Generate synthetic hotspot data (replace with actual ML predictions)
    prediction_date = date or datetime.now().strftime("%Y-%m-%d")
    
    # Chicago coordinates (example)
    city_center = {"chicago": (41.8781, -87.6298)}
    center = city_center.get(city.lower(), (41.8781, -87.6298))
    
    # Generate hotspots in a grid pattern
    hotspots = []
    grid_size = 0.02  # ~2km grid cells
    
    for i in range(-10, 10):
        for j in range(-10, 10):
            lat = center[0] + i * grid_size
            lng = center[1] + j * grid_size
            
            # Calculate intensity based on distance from center
            dist = np.sqrt(i**2 + j**2)
            intensity = max(0, 1 - (dist / 15))
            
            # Add some randomness
            intensity *= np.random.uniform(0.5, 1.5)
            intensity = min(1.0, max(0.0, intensity))
            
            if intensity > 0.1:  # Only include significant hotspots
                predicted_incidents = int(intensity * 10)
                
                # Determine risk level
                if intensity > 0.8:
                    risk_level = "critical"
                elif intensity > 0.6:
                    risk_level = "high"
                elif intensity > 0.3:
                    risk_level = "medium"
                else:
                    risk_level = "low"
                
                hotspots.append(CrimeHotspot(
                    lat=lat,
                    lng=lng,
                    intensity=round(intensity, 3),
                    crime_type=crime_type,
                    predicted_incidents=predicted_incidents,
                    confidence=round(np.random.uniform(0.65, 0.95), 2),
                    grid_id=f"grid_{i}_{j}",
                    risk_level=risk_level
                ))
    
    return HeatmapData(
        hotspots=hotspots,
        prediction_date=prediction_date,
        model_version="v2.3.1",
        coverage_area={
            "center": {"lat": center[0], "lng": center[1]},
            "radius_km": 20
        },
        grid_resolution="2km",
        total_predicted_incidents=sum(h.predicted_incidents for h in hotspots)
    )


@router.get("/temporal-patterns")
async def get_temporal_patterns(
    grid_id: str = Query(..., description="Grid cell ID"),
    days: int = Query(7, description="Number of days to analyze")
):
    """
    Get temporal crime patterns for a specific grid cell.
    Shows hourly and daily patterns.
    """
    
    # Generate synthetic temporal data
    hours = list(range(24))
    hourly_incidents = [
        int(20 * (1 + 0.5 * np.sin((h - 6) * np.pi / 12)))  # Peak at evening
        for h in hours
    ]
    
    days_data = []
    for d in range(days):
        date = (datetime.now() - timedelta(days=d)).strftime("%Y-%m-%d")
        days_data.append({
            "date": date,
            "incidents": int(np.random.uniform(50, 150)),
            "prediction_accuracy": round(np.random.uniform(0.65, 0.85), 2)
        })
    
    return {
        "grid_id": grid_id,
        "hourly_pattern": [
            {"hour": h, "incidents": hourly_incidents[h]}
            for h in hours
        ],
        "daily_pattern": days_data,
        "peak_hours": [18, 19, 20, 21, 22],
        "safest_hours": [3, 4, 5, 6]
    }

