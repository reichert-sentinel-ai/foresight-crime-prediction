# Foresight Frontend - Crime Heatmap Visualization

Interactive crime prediction heatmap using React and Leaflet.

## Setup

### Prerequisites
- Node.js 18+ and npm
- Backend API running on `http://localhost:8000`

### Installation

```bash
cd frontend
npm install
```

### Required Dependencies

```bash
npm install leaflet react-leaflet axios
npm install lucide-react  # For icons
npm install @radix-ui/react-select  # For Select component (if using shadcn/ui)
```

### Development

```bash
npm run dev
```

Visit `http://localhost:5173/crime-map` (or your configured port)

## Component Usage

```jsx
import CrimeHeatmap from './components/CrimeHeatmap';

// In your App.jsx or router
<Route path="/crime-map" element={<CrimeHeatmap />} />
```

## Features

- Interactive map with color-coded crime hotspots
- Dynamic filtering by city, crime type, and time window
- Risk level visualization (Critical, High, Medium, Low)
- Popup details showing predictions for each grid cell
- Real-time data updates when changing filters

## API Integration

The component expects the backend API at:
- `GET /api/crime-map/hotspots` - Get heatmap data
- `GET /api/crime-map/temporal-patterns?grid_id={id}` - Get temporal patterns

Make sure CORS is enabled on the backend for your frontend origin.

