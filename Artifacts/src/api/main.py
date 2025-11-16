"""
FastAPI Application for Foresight Crime Prediction

Provides REST API endpoints for:
- Crime forecasting
- Hotspot detection
- Patrol route optimization
- Border analytics
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List, Dict
from datetime import datetime, timedelta
import logging

from pydantic import BaseModel
# Lazy imports for optional dependencies
# Path is already set above

try:
    from src.models.prophet_forecaster import CrimeForecaster
    from src.models.dbscan_hotspots import CrimeHotspotDetector
    from src.models.route_optimizer import PatrolRouteOptimizer, Hotspot, PatrolRoute
    from src.data.etl import CrimeDataETL
    HAS_FULL_DEPS = True
except ImportError:
    # Allow server to start even if prophet/other dependencies aren't installed
    # Crime map endpoint doesn't require these
    HAS_FULL_DEPS = False
    CrimeForecaster = None
    CrimeHotspotDetector = None
    PatrolRouteOptimizer = None
    Hotspot = None
    PatrolRoute = None
    CrimeDataETL = None

# Import routers - using absolute imports from project root
import sys
import os
# Add project root to path
project_root = os.path.join(os.path.dirname(__file__), '..', '..')
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.api.routers import crime_map
from src.api.routers import temporal_patterns
from src.api.routers import bias_analysis
from src.api.routers import explainability

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Foresight Crime Prediction API",
    description="Predictive crime intelligence platform",
    version="1.0.0"
)

# CORS middleware - allow Vercel deployments and local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://foresight-crime-prediction.vercel.app",
        "http://localhost:5174",  # Local frontend dev server
        "http://localhost:5173",  # Alternative local port
    ],
    allow_origin_regex=r"https://foresight-crime-prediction-.*\.vercel\.app",  # Preview deployments
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(crime_map.router)
app.include_router(temporal_patterns.router)
app.include_router(bias_analysis.router)
app.include_router(explainability.router)

# Global model instances (in production, use dependency injection)
forecaster = None
hotspot_detector = None
route_optimizer = None


# Pydantic models
class ForecastRequest(BaseModel):
    periods: int = 7
    crime_type: Optional[str] = None


class ForecastResponse(BaseModel):
    dates: List[str]
    predictions: List[float]
    lower_bound: List[float]
    upper_bound: List[float]
    accuracy: Optional[float] = None


class HotspotRequest(BaseModel):
    eps: float = 0.01
    min_samples: int = 10
    min_days: Optional[int] = None


class HotspotResponse(BaseModel):
    cluster_id: int
    center_latitude: float
    center_longitude: float
    n_incidents: int
    density_per_km2: float
    area_km2: float


class RouteRequest(BaseModel):
    hotspots: List[Dict]
    num_officers: int
    depot_latitude: float
    depot_longitude: float
    max_route_distance_km: float = 50.0


class RouteResponse(BaseModel):
    officer_id: int
    hotspot_ids: List[int]
    total_distance_km: float
    estimated_duration_hours: float


@app.on_event("startup")
async def startup_event():
    """Initialize models on startup"""
    global forecaster, hotspot_detector, route_optimizer
    
    if not HAS_FULL_DEPS:
        logger.warning("Some dependencies not available. Crime map endpoint will work, but forecast/hotspot endpoints may not.")
        return
    
    logger.info("Initializing Foresight API models")
    
    forecaster = CrimeForecaster()
    hotspot_detector = CrimeHotspotDetector()
    route_optimizer = PatrolRouteOptimizer()
    
    logger.info("Foresight API ready")


@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "Foresight Crime Prediction API",
        "version": "1.0.0",
            "endpoints": {
            "forecast": "/api/v1/forecast",
            "hotspots": "/api/v1/hotspots",
            "route": "/api/v1/route",
            "stats": "/api/v1/stats",
            "crime-map": "/api/crime-map/hotspots",
            "temporal-analysis": "/api/temporal/analysis",
            "temporal-forecast": "/api/temporal/forecast",
            "temporal-anomalies": "/api/temporal/anomalies",
            "bias-analysis": "/api/bias/analysis",
            "bias-interventions": "/api/bias/interventions",
            "bias-disparity": "/api/bias/disparity-report",
            "explainability": "/api/explainability/explain-prediction",
            "confidence-breakdown": "/api/explainability/confidence-breakdown",
            "what-if": "/api/explainability/what-if",
            "global-importance": "/api/explainability/global-importance",
            "prediction-timeline": "/api/explainability/prediction-timeline",
            "explanation-summary": "/api/explainability/explanation-summary"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@app.post("/api/v1/forecast", response_model=ForecastResponse)
async def get_forecast(request: ForecastRequest):
    """
    Generate crime forecast for specified period
    
    Args:
        request: Forecast parameters
        
    Returns:
        Forecast with predictions and confidence intervals
    """
    if forecaster is None:
        raise HTTPException(status_code=503, detail="Forecaster not initialized")
    
    try:
        # Load and process data
        etl = CrimeDataETL()
        df = etl.process()
        
        # Fit model
        target_column = request.crime_type if request.crime_type else 'total_crimes'
        forecaster.fit(df, target_column=target_column)
        
        # Generate forecast
        forecast = forecaster.forecast(periods=request.periods, include_history=False)
        
        # Evaluate accuracy
        metrics = forecaster.evaluate(df, forecast, target_column=target_column)
        accuracy = metrics.get('accuracy') if metrics else None
        
        # Format response
        response = ForecastResponse(
            dates=[d.strftime('%Y-%m-%d') for d in forecast['ds']],
            predictions=forecast['yhat'].tolist(),
            lower_bound=forecast['yhat_lower'].tolist(),
            upper_bound=forecast['yhat_upper'].tolist(),
            accuracy=accuracy
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Forecast error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/hotspots", response_model=List[HotspotResponse])
async def get_hotspots(request: HotspotRequest):
    """
    Detect crime hotspots using DBSCAN
    
    Args:
        request: Hotspot detection parameters
        
    Returns:
        List of detected hotspots
    """
    if hotspot_detector is None:
        raise HTTPException(status_code=503, detail="Hotspot detector not initialized")
    
    try:
        # Load data
        etl = CrimeDataETL()
        df = etl.load_chicago_data()
        
        # Filter to recent data (last 90 days)
        if 'incident_date' in df.columns:
            cutoff_date = df['incident_date'].max() - timedelta(days=90)
            df = df[df['incident_date'] >= cutoff_date]
        
        # Detect hotspots
        hotspot_detector.eps = request.eps
        hotspot_detector.min_samples = request.min_samples
        
        hotspots_df = hotspot_detector.detect_hotspots(df)
        
        # Filter stable hotspots if requested
        if request.min_days:
            hotspots_df = hotspot_detector.filter_stable_hotspots(
                hotspots_df,
                min_days=request.min_days
            )
            hotspots_df = hotspots_df[hotspots_df['is_stable_hotspot']]
        
        # Calculate density metrics
        density_df = hotspot_detector.calculate_hotspot_density(hotspots_df)
        
        # Format response
        responses = []
        for _, row in density_df.iterrows():
            responses.append(HotspotResponse(
                cluster_id=int(row['cluster_id']),
                center_latitude=float(row['center_latitude']),
                center_longitude=float(row['center_longitude']),
                n_incidents=int(row['n_incidents']),
                density_per_km2=float(row['density_per_km2']),
                area_km2=float(row['area_km2'])
            ))
        
        return responses
        
    except Exception as e:
        logger.error(f"Hotspot detection error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/route", response_model=List[RouteResponse])
async def optimize_route(request: RouteRequest):
    """
    Optimize patrol routes for officers
    
    Args:
        request: Route optimization parameters
        
    Returns:
        List of optimized patrol routes
    """
    if route_optimizer is None:
        raise HTTPException(status_code=503, detail="Route optimizer not initialized")
    
    try:
        # Convert hotspots to Hotspot objects
        hotspots = []
        for hotspot_data in request.hotspots:
            hotspot = Hotspot(
                cluster_id=hotspot_data.get('cluster_id', 0),
                center_lat=hotspot_data['latitude'],
                center_lon=hotspot_data['longitude'],
                priority=hotspot_data.get('priority', 1.0),
                density=hotspot_data.get('density', 0.0)
            )
            hotspots.append(hotspot)
        
        # Optimize routes
        route_optimizer.max_route_distance_km = request.max_route_distance_km
        
        routes = route_optimizer.optimize(
            hotspots=hotspots,
            num_officers=request.num_officers,
            depot_lat=request.depot_latitude,
            depot_lon=request.depot_longitude
        )
        
        # Format response
        responses = []
        for route in routes:
            responses.append(RouteResponse(
                officer_id=route.officer_id,
                hotspot_ids=[h.cluster_id for h in route.hotspots],
                total_distance_km=route.total_distance,
                estimated_duration_hours=route.estimated_duration
            ))
        
        return responses
        
    except Exception as e:
        logger.error(f"Route optimization error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/stats")
async def get_stats():
    """
    Get crime statistics summary
    
    Returns:
        Dictionary with crime statistics
    """
    try:
        # Load data
        etl = CrimeDataETL()
        df = etl.load_chicago_data()
        
        # Calculate statistics
        total_incidents = len(df)
        
        if 'incident_date' in df.columns:
            date_range = {
                'start': df['incident_date'].min().isoformat(),
                'end': df['incident_date'].max().isoformat()
            }
        else:
            date_range = None
        
        if 'crime_type' in df.columns:
            top_crimes = df['crime_type'].value_counts().head(5).to_dict()
        else:
            top_crimes = {}
        
        stats = {
            'total_incidents': total_incidents,
            'date_range': date_range,
            'top_crime_types': top_crimes,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        return stats
        
    except Exception as e:
        logger.error(f"Stats error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=8000)

