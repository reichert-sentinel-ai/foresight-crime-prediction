"""
Mapbox Integration Utilities

Helper functions for Mapbox GL visualization and geospatial operations.
"""

from typing import List, Dict, Tuple, Optional
import pandas as pd
import numpy as np


class MapboxVisualizer:
    """Utilities for Mapbox visualization"""
    
    def __init__(self, mapbox_token: Optional[str] = None):
        """
        Initialize Mapbox visualizer
        
        Args:
            mapbox_token: Optional Mapbox API token (for custom styles)
        """
        self.mapbox_token = mapbox_token or ""
        self.default_style = "open-street-map"
        
    def create_hotspot_map_data(
        self,
        hotspots_df: pd.DataFrame,
        density_df: Optional[pd.DataFrame] = None
    ) -> Dict:
        """
        Create GeoJSON-like data structure for hotspot visualization
        
        Args:
            hotspots_df: DataFrame with hotspot locations
            density_df: Optional density statistics
            
        Returns:
            Dictionary with map data
        """
        map_data = {
            'type': 'FeatureCollection',
            'features': []
        }
        
        if density_df is not None:
            for _, row in density_df.iterrows():
                feature = {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [row['center_longitude'], row['center_latitude']]
                    },
                    'properties': {
                        'cluster_id': int(row['cluster_id']),
                        'n_incidents': int(row['n_incidents']),
                        'density_per_km2': float(row['density_per_km2']),
                        'area_km2': float(row['area_km2'])
                    }
                }
                map_data['features'].append(feature)
        else:
            # Fallback to hotspots_df
            if 'latitude' in hotspots_df.columns and 'longitude' in hotspots_df.columns:
                for _, row in hotspots_df.iterrows():
                    feature = {
                        'type': 'Feature',
                        'geometry': {
                            'type': 'Point',
                            'coordinates': [row['longitude'], row['latitude']]
                        },
                        'properties': {
                            'cluster_id': int(row.get('cluster', -1))
                        }
                    }
                    map_data['features'].append(feature)
        
        return map_data
    
    def create_route_map_data(
        self,
        routes: List,
        depot_lat: float,
        depot_lon: float
    ) -> Dict:
        """
        Create map data for patrol routes
        
        Args:
            routes: List of PatrolRoute objects
            depot_lat: Depot latitude
            depot_lon: Depot longitude
            
        Returns:
            Dictionary with route map data
        """
        route_data = {
            'depot': {
                'latitude': depot_lat,
                'longitude': depot_lon
            },
            'routes': []
        }
        
        for route in routes:
            route_points = {
                'officer_id': route.officer_id,
                'hotspots': [],
                'total_distance': route.total_distance,
                'duration': route.estimated_duration
            }
            
            for hotspot in route.hotspots:
                route_points['hotspots'].append({
                    'cluster_id': hotspot.cluster_id,
                    'latitude': hotspot.center_lat,
                    'longitude': hotspot.center_lon,
                    'priority': hotspot.priority,
                    'density': hotspot.density
                })
            
            route_data['routes'].append(route_points)
        
        return route_data
    
    def get_map_center_and_zoom(
        self,
        df: pd.DataFrame,
        buffer: float = 0.01
    ) -> Tuple[float, float, float]:
        """
        Calculate map center and zoom from data bounds
        
        Args:
            df: DataFrame with latitude/longitude columns
            buffer: Buffer in degrees for zoom calculation
            
        Returns:
            Tuple of (center_lat, center_lon, zoom_level)
        """
        if 'latitude' not in df.columns or 'longitude' not in df.columns:
            # Default to Chicago
            return 41.8781, -87.6298, 10.0
        
        min_lat = df['latitude'].min()
        max_lat = df['latitude'].max()
        min_lon = df['longitude'].min()
        max_lon = df['longitude'].max()
        
        center_lat = (min_lat + max_lat) / 2
        center_lon = (min_lon + max_lon) / 2
        
        # Calculate zoom based on bounding box
        lat_range = max_lat - min_lat + buffer * 2
        lon_range = max_lon - min_lon + buffer * 2
        
        # Simple zoom calculation (can be improved)
        max_range = max(lat_range, lon_range)
        if max_range > 1.0:
            zoom = 7.0
        elif max_range > 0.5:
            zoom = 8.0
        elif max_range > 0.1:
            zoom = 9.0
        elif max_range > 0.05:
            zoom = 10.0
        else:
            zoom = 11.0
        
        return center_lat, center_lon, zoom
    
    def create_heatmap_data(
        self,
        df: pd.DataFrame,
        intensity_column: str = 'crime_intensity'
    ) -> pd.DataFrame:
        """
        Prepare data for heatmap visualization
        
        Args:
            df: DataFrame with crime incidents
            intensity_column: Column name for intensity
            
        Returns:
            DataFrame prepared for heatmap
        """
        if intensity_column not in df.columns:
            # Create intensity column from density or counts
            if 'latitude' in df.columns and 'longitude' in df.columns:
                # Calculate density per location
                df = df.copy()
                df[intensity_column] = 1.0  # Default intensity
            else:
                df[intensity_column] = 1.0
        
        return df[[intensity_column, 'latitude', 'longitude']].dropna()


if __name__ == "__main__":
    # Example usage
    visualizer = MapboxVisualizer()
    
    # Sample data
    sample_df = pd.DataFrame({
        'latitude': [41.8781, 41.8881, 41.8681],
        'longitude': [-87.6298, -87.6398, -87.6198],
        'crime_intensity': [10, 15, 8]
    })
    
    center_lat, center_lon, zoom = visualizer.get_map_center_and_zoom(sample_df)
    print(f"Map Center: {center_lat}, {center_lon}")
    print(f"Zoom Level: {zoom}")

