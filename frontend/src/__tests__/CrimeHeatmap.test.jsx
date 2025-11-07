/**
 * Tests for CrimeHeatmap component
 * Run with: npm test
 */
import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import axios from 'axios';
import CrimeHeatmap from '../components/CrimeHeatmap';

// Mock axios
jest.mock('axios');

// Mock react-leaflet
jest.mock('react-leaflet', () => ({
  MapContainer: ({ children, center, zoom }) => (
    <div data-testid="map-container" data-center={JSON.stringify(center)} data-zoom={zoom}>
      {children}
    </div>
  ),
  TileLayer: () => <div data-testid="tile-layer" />,
  Circle: ({ center, radius, pathOptions, children }) => (
    <div
      data-testid="circle"
      data-center={JSON.stringify(center)}
      data-radius={radius}
      data-color={pathOptions.fillColor}
      data-intensity={pathOptions.intensity}
    >
      {children}
    </div>
  ),
  Popup: ({ children }) => <div data-testid="popup">{children}</div>,
  useMap: () => ({
    fitBounds: jest.fn(),
  }),
}));

const mockHeatmapData = {
  hotspots: [
    {
      lat: 41.8781,
      lng: -87.6298,
      intensity: 0.85,
      crime_type: 'theft',
      predicted_incidents: 8,
      confidence: 0.92,
      grid_id: 'grid_0_0',
      risk_level: 'critical',
    },
    {
      lat: 41.8881,
      lng: -87.6398,
      intensity: 0.45,
      crime_type: 'assault',
      predicted_incidents: 4,
      confidence: 0.75,
      grid_id: 'grid_1_1',
      risk_level: 'medium',
    },
  ],
  prediction_date: '2024-01-15',
  model_version: 'v2.3.1',
  coverage_area: {
    center: { lat: 41.8781, lng: -87.6298 },
    radius_km: 20,
  },
  grid_resolution: '2km',
  total_predicted_incidents: 12,
};

describe('CrimeHeatmap Component', () => {
  beforeEach(() => {
    axios.get.mockResolvedValue({ data: mockHeatmapData });
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  test('renders map container', async () => {
    render(
      <BrowserRouter>
        <CrimeHeatmap />
      </BrowserRouter>
    );

    await waitFor(() => {
      const mapContainer = screen.getByTestId('map-container');
      expect(mapContainer).toBeInTheDocument();
    });
  });

  test('displays loading state initially', () => {
    render(
      <BrowserRouter>
        <CrimeHeatmap />
      </BrowserRouter>
    );

    // Should show loading spinner or indicator
    expect(screen.getByRole('status') || screen.queryByText(/loading/i)).toBeTruthy();
  });

  test('fetches heatmap data on mount', async () => {
    render(
      <BrowserRouter>
        <CrimeHeatmap />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(axios.get).toHaveBeenCalledWith(
        'http://localhost:8000/api/crime-map/hotspots',
        expect.objectContaining({
          params: expect.objectContaining({
            city: 'chicago',
            crime_type: 'all',
            time_window: '24h',
          }),
        })
      );
    });
  });

  test('renders hotspots with correct color coding', async () => {
    render(
      <BrowserRouter>
        <CrimeHeatmap />
      </BrowserRouter>
    );

    await waitFor(() => {
      const circles = screen.getAllByTestId('circle');
      expect(circles.length).toBeGreaterThan(0);

      // Check critical hotspot (intensity > 0.8) is red
      const criticalCircle = circles.find(
        (circle) => circle.getAttribute('data-color') === '#dc2626'
      );
      expect(criticalCircle).toBeTruthy();

      // Check medium hotspot (intensity 0.3-0.6) is amber
      const mediumCircle = circles.find(
        (circle) => circle.getAttribute('data-color') === '#f59e0b'
      );
      expect(mediumCircle).toBeTruthy();
    });
  });

  test('updates map when city filter changes', async () => {
    render(
      <BrowserRouter>
        <CrimeHeatmap />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(axios.get).toHaveBeenCalled();
    });

    // Find and change city select (simplified - actual implementation may vary)
    const citySelect = screen.getByLabelText(/city/i) || screen.getByText(/chicago/i);
    
    if (citySelect) {
      fireEvent.change(citySelect, { target: { value: 'new-york' } });

      await waitFor(() => {
        expect(axios.get).toHaveBeenCalledWith(
          expect.any(String),
          expect.objectContaining({
            params: expect.objectContaining({
              city: 'new-york',
            }),
          })
        );
      });
    }
  });

  test('displays risk summary badges', async () => {
    render(
      <BrowserRouter>
        <CrimeHeatmap />
      </BrowserRouter>
    );

    await waitFor(() => {
      // Should show critical and high risk counts
      expect(screen.getByText(/critical/i) || screen.queryByText(/1 Critical/)).toBeTruthy();
    });
  });

  test('displays map legend', async () => {
    render(
      <BrowserRouter>
        <CrimeHeatmap />
      </BrowserRouter>
    );

    await waitFor(() => {
      // Check legend exists
      expect(screen.getByText(/risk levels/i) || screen.getByText(/critical/i)).toBeTruthy();
      expect(screen.getByText(/high/i) || screen.getByText(/60-80%/i)).toBeTruthy();
      expect(screen.getByText(/medium/i) || screen.getByText(/30-60%/i)).toBeTruthy();
      expect(screen.getByText(/low/i) || screen.getByText(/<30%/i)).toBeTruthy();
    });
  });

  test('displays prediction summary info panel', async () => {
    render(
      <BrowserRouter>
        <CrimeHeatmap />
      </BrowserRouter>
    );

    await waitFor(() => {
      // Check info panel content
      expect(screen.getByText(/prediction summary/i)).toBeTruthy();
      expect(screen.getByText(/2024-01-15/)).toBeTruthy();
      expect(screen.getByText(/v2.3.1/)).toBeTruthy();
    });
  });

  test('handles API errors gracefully', async () => {
    axios.get.mockRejectedValueOnce(new Error('Network error'));

    render(
      <BrowserRouter>
        <CrimeHeatmap />
      </BrowserRouter>
    );

    await waitFor(() => {
      // Should show error state or no data message
      expect(screen.getByText(/no data available/i) || screen.queryByText(/error/i)).toBeTruthy();
    });
  });

  test('center coordinates match API response', async () => {
    render(
      <BrowserRouter>
        <CrimeHeatmap />
      </BrowserRouter>
    );

    await waitFor(() => {
      const mapContainer = screen.getByTestId('map-container');
      const centerAttr = mapContainer.getAttribute('data-center');
      const center = JSON.parse(centerAttr);

      expect(center.lat).toBe(41.8781);
      expect(center.lng).toBe(-87.6298);
    });
  });
});

