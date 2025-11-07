# Crime Heatmap Visualization - Setup Guide

## Overview

Interactive crime prediction heatmap using React Leaflet and FastAPI backend. This feature demonstrates geospatial analytics and data visualization skills for law enforcement applications.

## Features

✅ Interactive map with color-coded crime hotspots  
✅ Popup details showing predictions for each grid cell  
✅ Dynamic filtering by city, crime type, and time window  
✅ Risk level badges and visual indicators  
✅ Real-time data updates when changing filters  
✅ Professional map legend and info panels  

## Backend Setup

### 1. Install Dependencies

```bash
cd project/repo-foresight
pip install scipy --break-system-packages
# OR add to requirements.txt (already added)
pip install -r requirements.txt
```

### 2. Start Backend Server

```bash
cd project/repo-foresight
python -m uvicorn src.api.main:app --reload --port 8000
```

The backend API will be available at:
- `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

### 3. Test Backend Endpoints

```bash
# Test heatmap endpoint
curl http://localhost:8000/api/crime-map/hotspots?city=chicago

# Test temporal patterns
curl http://localhost:8000/api/crime-map/temporal-patterns?grid_id=grid_0_0
```

## Frontend Setup

### 1. Install Dependencies

```bash
cd project/repo-foresight/frontend
npm install
```

This will install:
- `react` and `react-dom`
- `react-router-dom`
- `leaflet` and `react-leaflet`
- `axios`
- `tailwindcss` and related build tools

### 2. Start Frontend Development Server

```bash
cd project/repo-foresight/frontend
npm run dev
```

The frontend will be available at:
- `http://localhost:5173`
- Crime Map: `http://localhost:5173/crime-map`

### 3. Verify CORS Configuration

Make sure the backend CORS middleware allows requests from `http://localhost:5173`. The backend is already configured with `allow_origins=["*"]` for development.

## Architecture

### Backend (`src/api/routers/crime_map.py`)

- **GET `/api/crime-map/hotspots`** - Returns grid-based crime predictions with intensity scores
  - Query params: `city`, `crime_type`, `date`, `time_window`
  - Returns: `HeatmapData` with hotspots array

- **GET `/api/crime-map/temporal-patterns`** - Returns temporal patterns for a grid cell
  - Query params: `grid_id`, `days`
  - Returns: Hourly and daily patterns

### Frontend (`frontend/src/components/CrimeHeatmap.jsx`)

- React component using React Leaflet for map visualization
- Integrated with FastAPI backend
- Dynamic filtering and state management
- Responsive UI with Tailwind CSS

### UI Components

Custom UI components created in `frontend/src/components/ui/`:
- `card.jsx` - Card container components
- `select.jsx` - Dropdown select component
- `badge.jsx` - Badge component for risk levels

## Testing

### Manual Testing Steps

1. **Start Backend**
   ```bash
   cd project/repo-foresight
   python -m uvicorn src.api.main:app --reload
   ```

2. **Start Frontend**
   ```bash
   cd project/repo-foresight/frontend
   npm run dev
   ```

3. **Navigate to Crime Map**
   - Open browser: `http://localhost:5173/crime-map`
   - Verify map loads with hotspots
   - Test filters (city, crime type, time window)
   - Click on hotspots to see popup details
   - Verify legend and info panels display correctly

### Expected Output

- Interactive map centered on Chicago (default)
- Color-coded circles representing crime hotspots
  - Red: Critical (>80% intensity)
  - Orange: High (60-80% intensity)
  - Amber: Medium (30-60% intensity)
  - Yellow: Low (<30% intensity)
- Filter controls at the top
- Map legend in bottom right
- Prediction summary in top left

## Troubleshooting

### Backend Issues

**Import Error: `scipy`**
```bash
pip install scipy --break-system-packages
```

**Router Not Found**
- Verify `src/api/routers/__init__.py` exists
- Check `main.py` includes: `app.include_router(crime_map.router)`

### Frontend Issues

**Leaflet Icons Not Showing**
- The component includes a fix for Leaflet default icons
- Icons load from CDN automatically

**Map Not Rendering**
- Check browser console for errors
- Verify backend is running on port 8000
- Check CORS configuration in backend

**Tailwind CSS Not Working**
- Ensure `tailwind.config.js` exists
- Verify `postcss.config.js` is configured
- Check `src/index.css` imports Tailwind directives

**Select Component Not Working**
- Verify custom Select component in `src/components/ui/select.jsx`
- Check that onClick handlers are properly connected

## Next Steps

### Integration with Real ML Models

Replace synthetic data generation in `crime_map.py` with:
- Actual crime prediction model outputs
- Real-time data from database
- Historical crime data integration

### Enhanced Features

- [ ] Time-based animation (show predictions over time)
- [ ] Heatmap gradient instead of circles
- [ ] Click on hotspot to see temporal patterns
- [ ] Export heatmap data as CSV/GeoJSON
- [ ] Integration with patrol route optimization
- [ ] Multi-city support with dynamic center coordinates

## Skills Demonstrated

- ✅ Geospatial data visualization
- ✅ React Leaflet integration
- ✅ FastAPI endpoint design
- ✅ Grid-based spatial analytics
- ✅ Interactive filtering and state management
- ✅ Professional UI/UX for law enforcement tools
- ✅ Component architecture and reusability

## References

- [React Leaflet Documentation](https://react-leaflet.js.org/)
- [Leaflet Documentation](https://leafletjs.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)

