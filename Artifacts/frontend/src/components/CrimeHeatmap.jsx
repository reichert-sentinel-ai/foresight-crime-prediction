import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Circle, Popup, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import axios from 'axios';
import L from 'leaflet';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Select, SelectItem } from './ui/select';
import { Badge } from './ui/badge';

// Fix Leaflet default icon issue
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Simple icon components (replace with lucide-react if available)
const Loader2 = ({ className }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
  </svg>
);

const AlertTriangle = ({ className }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
  </svg>
);

const TrendingUp = ({ className }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
  </svg>
);

// Heat gradient colors based on intensity
const getHeatColor = (intensity) => {
  if (intensity > 0.8) return '#dc2626'; // red-600 - Critical
  if (intensity > 0.6) return '#ea580c'; // orange-600 - High
  if (intensity > 0.3) return '#f59e0b'; // amber-500 - Medium
  return '#facc15'; // yellow-400 - Low
};

const getRiskBadge = (riskLevel) => {
  const variants = {
    critical: 'destructive',
    high: 'destructive',
    medium: 'warning',
    low: 'secondary'
  };
  return <Badge variant={variants[riskLevel]}>{riskLevel.toUpperCase()}</Badge>;
};

function HeatmapLayer({ hotspots }) {
  const map = useMap();
  
  useEffect(() => {
    if (hotspots.length > 0) {
      // Fit map to show all hotspots
      const bounds = hotspots.map(h => [h.lat, h.lng]);
      map.fitBounds(bounds, { padding: [50, 50] });
    }
  }, [hotspots, map]);
  
  return (
    <>
      {hotspots.map((hotspot, idx) => (
        <Circle
          key={idx}
          center={[hotspot.lat, hotspot.lng]}
          radius={hotspot.intensity * 500} // Size based on intensity
          pathOptions={{
            fillColor: getHeatColor(hotspot.intensity),
            fillOpacity: 0.6,
            color: getHeatColor(hotspot.intensity),
            weight: 1,
            opacity: 0.8
          }}
        >
          <Popup>
            <div className="p-2 space-y-2">
              <div className="flex items-center justify-between">
                <h3 className="font-bold text-sm text-gray-900 dark:text-[#e5e5e5]">Grid: {hotspot.grid_id}</h3>
                {getRiskBadge(hotspot.risk_level)}
              </div>
              <div className="text-xs space-y-1">
                <div className="flex justify-between">
                  <span className="text-gray-600 dark:text-[#a0a0a0]">Predicted Incidents:</span>
                  <span className="font-semibold text-gray-900 dark:text-[#e5e5e5]">{hotspot.predicted_incidents}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600 dark:text-[#a0a0a0]">Intensity:</span>
                  <span className="font-semibold text-gray-900 dark:text-[#e5e5e5]">{(hotspot.intensity * 100).toFixed(0)}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600 dark:text-[#a0a0a0]">Confidence:</span>
                  <span className="font-semibold text-gray-900 dark:text-[#e5e5e5]">{(hotspot.confidence * 100).toFixed(0)}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600 dark:text-[#a0a0a0]">Crime Type:</span>
                  <span className="font-semibold capitalize text-gray-900 dark:text-[#e5e5e5]">{hotspot.crime_type}</span>
                </div>
              </div>
            </div>
          </Popup>
        </Circle>
      ))}
    </>
  );
}

export default function CrimeHeatmap() {
  const [heatmapData, setHeatmapData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [city, setCity] = useState('chicago');
  const [crimeType, setCrimeType] = useState('all');
  const [timeWindow, setTimeWindow] = useState('24h');

  useEffect(() => {
    fetchHeatmapData();
  }, [city, crimeType, timeWindow]);

  const fetchHeatmapData = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get('/api/crime-map/hotspots', {
        params: { city, crime_type: crimeType, time_window: timeWindow }
      });
      setHeatmapData(response.data);
    } catch (error) {
      console.error('Error fetching heatmap data:', error);
      setError(error.message || 'Failed to fetch data. Make sure the backend server is running on port 8000.');
      setHeatmapData(null);
    } finally {
      setLoading(false);
    }
  };

  const criticalHotspots = heatmapData?.hotspots.filter(h => h.risk_level === 'critical').length || 0;
  const highRiskHotspots = heatmapData?.hotspots.filter(h => h.risk_level === 'high').length || 0;

  return (
    <div className="space-y-4 bg-transparent min-h-screen">
      {/* Header Controls */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="w-5 h-5" />
            Crime Prediction Heatmap
          </CardTitle>
        </CardHeader>
        <CardContent style={{ overflow: 'visible' }}>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4" style={{ overflow: 'visible' }}>
            {/* City Selector */}
            <div style={{ overflow: 'visible', position: 'relative' }}>
              <label className="text-sm font-medium mb-2 block text-gray-900 dark:text-[#e5e5e5]">City</label>
              <Select value={city} onValueChange={setCity}>
                <SelectItem value="chicago">Chicago</SelectItem>
                <SelectItem value="new-york">New York</SelectItem>
                <SelectItem value="los-angeles">Los Angeles</SelectItem>
              </Select>
            </div>

            {/* Crime Type Selector */}
            <div style={{ overflow: 'visible', position: 'relative' }}>
              <label className="text-sm font-medium mb-2 block text-gray-900 dark:text-[#e5e5e5]">Crime Type</label>
              <Select value={crimeType} onValueChange={setCrimeType}>
                <SelectItem value="all">All Crimes</SelectItem>
                <SelectItem value="theft">Theft</SelectItem>
                <SelectItem value="assault">Assault</SelectItem>
                <SelectItem value="burglary">Burglary</SelectItem>
                <SelectItem value="robbery">Robbery</SelectItem>
              </Select>
            </div>

            {/* Time Window Selector */}
            <div style={{ overflow: 'visible', position: 'relative' }}>
              <label className="text-sm font-medium mb-2 block text-gray-900 dark:text-[#e5e5e5]">Time Window</label>
              <Select value={timeWindow} onValueChange={setTimeWindow}>
                <SelectItem value="24h">Next 24 Hours</SelectItem>
                <SelectItem value="7d">Next 7 Days</SelectItem>
                <SelectItem value="30d">Next 30 Days</SelectItem>
              </Select>
            </div>

            {/* Stats Summary */}
            <div className="flex flex-col justify-center">
              <div className="text-sm text-gray-600 dark:text-[#a0a0a0]">Risk Summary</div>
              <div className="flex gap-2 mt-1">
                <Badge variant="destructive" className="text-xs">
                  {criticalHotspots} Critical
                </Badge>
                <Badge variant="destructive" className="text-xs">
                  {highRiskHotspots} High
                </Badge>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Map Display */}
      <Card>
        <CardContent className="p-0">
          {loading ? (
            <div className="h-[600px] flex items-center justify-center">
              <Loader2 className="w-8 h-8 animate-spin text-blue-600 dark:text-blue-400" />
            </div>
          ) : heatmapData ? (
            <div className="relative">
              <MapContainer
                center={[heatmapData.coverage_area.center.lat, heatmapData.coverage_area.center.lng]}
                zoom={12}
                style={{ height: '600px', width: '100%' }}
              >
                <TileLayer
                  url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                  attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                />
                <HeatmapLayer hotspots={heatmapData.hotspots} />
              </MapContainer>
              
              {/* Map Legend */}
              <div className="absolute bottom-4 right-4 bg-white dark:bg-[#1f1f1f] p-3 rounded-lg shadow-lg z-[1000] border border-gray-200 dark:border-[#2a2a2a]">
                <div className="text-xs font-semibold mb-2 text-gray-900 dark:text-[#e5e5e5]">Risk Levels</div>
                <div className="space-y-1 text-xs">
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-red-600" />
                    <span className="text-gray-900 dark:text-[#e5e5e5]">Critical (&gt;80%)</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-orange-600" />
                    <span className="text-gray-900 dark:text-[#e5e5e5]">High (60-80%)</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-amber-500" />
                    <span className="text-gray-900 dark:text-[#e5e5e5]">Medium (30-60%)</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-yellow-400" />
                    <span className="text-gray-900 dark:text-[#e5e5e5]">Low (&lt;30%)</span>
                  </div>
                </div>
              </div>

              {/* Info Panel */}
              <div className="absolute top-4 left-4 bg-white dark:bg-[#1f1f1f] p-3 rounded-lg shadow-lg z-[1000] max-w-xs border border-gray-200 dark:border-[#2a2a2a]">
                <div className="flex items-center gap-2 mb-2">
                  <AlertTriangle className="w-4 h-4 text-orange-600 dark:text-orange-500" />
                  <span className="text-sm font-semibold text-gray-900 dark:text-[#e5e5e5]">Prediction Summary</span>
                </div>
                <div className="text-xs space-y-1 text-gray-700 dark:text-[#a0a0a0]">
                  <div>Date: <span className="font-semibold text-gray-900 dark:text-[#e5e5e5]">{heatmapData.prediction_date}</span></div>
                  <div>Total Hotspots: <span className="font-semibold text-gray-900 dark:text-[#e5e5e5]">{heatmapData.hotspots.length}</span></div>
                  <div>Predicted Incidents: <span className="font-semibold text-gray-900 dark:text-[#e5e5e5]">{heatmapData.total_predicted_incidents}</span></div>
                  <div>Model: <span className="font-semibold text-gray-900 dark:text-[#e5e5e5]">{heatmapData.model_version}</span></div>
                  <div>Resolution: <span className="font-semibold text-gray-900 dark:text-[#e5e5e5]">{heatmapData.grid_resolution} grid</span></div>
                </div>
              </div>
            </div>
          ) : error ? (
            <div className="h-[600px] flex items-center justify-center">
              <div className="text-center p-6">
                <AlertTriangle className="w-12 h-12 text-red-600 dark:text-red-500 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-gray-900 dark:text-[#e5e5e5] mb-2">Error Loading Data</h3>
                <p className="text-sm text-gray-600 dark:text-[#a0a0a0] mb-4">{error}</p>
                <button
                  onClick={fetchHeatmapData}
                  className="px-4 py-2 bg-blue-600 dark:bg-blue-500 text-white rounded-md hover:bg-blue-700 dark:hover:bg-blue-600 text-sm transition-colors"
                >
                  Retry
                </button>
                <p className="text-xs text-gray-500 dark:text-[#a0a0a0] mt-4">
                  Make sure the backend server is running:<br />
                  <code className="bg-gray-100 dark:bg-[#1a1a1a] text-gray-900 dark:text-[#e5e5e5] px-2 py-1 rounded block mt-2">python -m uvicorn src.api.main:app --port 8000</code>
                </p>
              </div>
            </div>
          ) : (
            <div className="h-[600px] flex items-center justify-center text-gray-500 dark:text-[#a0a0a0]">
              No data available
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

