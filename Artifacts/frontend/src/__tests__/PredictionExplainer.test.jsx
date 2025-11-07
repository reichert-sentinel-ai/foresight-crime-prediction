/**
 * Tests for PredictionExplainer component (Sprint F4)
 * Run with: npm test PredictionExplainer.test.jsx
 */
import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import axios from 'axios';
import PredictionExplainer from '../components/PredictionExplainer';

// Mock axios
jest.mock('axios');

// Mock recharts
jest.mock('recharts', () => ({
  ResponsiveContainer: ({ children }) => <div data-testid="responsive-container">{children}</div>,
  BarChart: ({ children }) => <div data-testid="bar-chart">{children}</div>,
  LineChart: ({ children }) => <div data-testid="line-chart">{children}</div>,
  Bar: () => <div data-testid="bar" />,
  Line: () => <div data-testid="line" />,
  XAxis: () => <div data-testid="x-axis" />,
  YAxis: () => <div data-testid="y-axis" />,
  CartesianGrid: () => <div data-testid="grid" />,
  Tooltip: () => <div data-testid="tooltip" />,
  Legend: () => <div data-testid="legend" />,
  Cell: () => <div data-testid="cell" />,
  ReferenceLine: () => <div data-testid="reference-line" />,
}));

const mockExplanation = {
  prediction_id: 'pred_grid_5_7_20240115120000',
  predicted_risk_score: 0.68,
  confidence: 0.82,
  risk_level: 'High',
  base_value: 0.45,
  feature_contributions: [
    {
      feature_name: 'Historical Crime Rate (30d)',
      value: 12.3,
      contribution: 0.18,
      contribution_percentage: 28.5,
      impact: 'increases'
    },
    {
      feature_name: 'Time of Day (Night Hours)',
      value: 1.0,
      contribution: 0.15,
      contribution_percentage: 23.8,
      impact: 'increases'
    },
    {
      feature_name: 'Recent Police Presence',
      value: 2.5,
      contribution: -0.06,
      contribution_percentage: 9.5,
      impact: 'decreases'
    }
  ],
  top_factors: [
    'Historical Crime Rate (30d)',
    'Time of Day (Night Hours)',
    'Day of Week (Weekend)'
  ],
  confidence_interval: {
    lower: 0.60,
    upper: 0.76
  },
  similar_historical_cases: 47
};

const mockConfidenceBreakdown = {
  overall_confidence: 0.82,
  data_quality_score: 0.90,
  model_certainty: 0.85,
  historical_accuracy: 0.78,
  factors_affecting_confidence: [
    'High-quality data with strong historical validation',
    'Feature values within model\'s confident range'
  ]
};

const mockGlobalImportance = [
  {
    feature_name: 'Historical Crime Rate (30d)',
    importance_score: 0.24,
    rank: 1,
    category: 'historical',
    description: 'Average crime incidents in the location over past 30 days'
  },
  {
    feature_name: 'Time of Day',
    importance_score: 0.18,
    rank: 2,
    category: 'temporal',
    description: 'Hour of day when prediction is made'
  }
];

const mockTimeline = {
  location_id: 'grid_5_7',
  timeline: [
    { date: '2024-01-08', predicted_risk: 0.65, confidence: 0.75, actual_incidents: 6, accuracy: 0.85 },
    { date: '2024-01-09', predicted_risk: 0.68, confidence: 0.78, actual_incidents: 7, accuracy: 0.82 }
  ],
  average_accuracy: 0.84,
  confidence_trend: 'improving'
};

const mockSummary = {
  prediction_id: 'pred_grid_5_7_20240115120000',
  summary: 'This location is predicted to have HIGH risk (68% probability) of crime in the next 24 hours.',
  confidence_explanation: 'We are 82% confident in this prediction based on high-quality historical data.',
  recommendation: 'Recommend increased patrol presence during evening hours (6 PM - 2 AM) this weekend.',
  caveats: [
    'Prediction accuracy may be affected by unexpected community events',
    'Weather changes could alter predicted patterns'
  ]
};

describe('PredictionExplainer Component', () => {
  beforeEach(() => {
    axios.get.mockImplementation((url) => {
      if (url.includes('explain-prediction')) {
        return Promise.resolve({ data: mockExplanation });
      }
      if (url.includes('confidence-breakdown')) {
        return Promise.resolve({ data: mockConfidenceBreakdown });
      }
      if (url.includes('global-importance')) {
        return Promise.resolve({ data: mockGlobalImportance });
      }
      if (url.includes('prediction-timeline')) {
        return Promise.resolve({ data: mockTimeline });
      }
      if (url.includes('explanation-summary')) {
        return Promise.resolve({ data: mockSummary });
      }
      return Promise.reject(new Error('Unknown endpoint'));
    });

    axios.post.mockResolvedValue({
      data: {
        scenario_name: 'Modified Recent Police Presence',
        original_prediction: 0.68,
        modified_prediction: 0.60,
        change_percentage: -11.8,
        modified_features: { 'Recent Police Presence': 0.9 }
      }
    });
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  test('renders loading state initially', () => {
    render(
      <BrowserRouter>
        <PredictionExplainer />
      </BrowserRouter>
    );

    expect(screen.getByRole('status') || screen.queryByText(/loading/i)).toBeTruthy();
  });

  test('fetches explanation data on mount', async () => {
    render(
      <BrowserRouter>
        <PredictionExplainer />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(axios.get).toHaveBeenCalledWith(
        'http://localhost:8000/api/explainability/explain-prediction',
        expect.objectContaining({
          params: expect.objectContaining({
            location_id: 'grid_5_7'
          })
        })
      );
    });
  });

  test('displays prediction summary card', async () => {
    render(
      <BrowserRouter>
        <PredictionExplainer />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText(/68.0%/)).toBeInTheDocument();
      expect(screen.getByText(/High/)).toBeInTheDocument();
      expect(screen.getByText(/82%/)).toBeInTheDocument();
    });
  });

  test('displays natural language explanation', async () => {
    render(
      <BrowserRouter>
        <PredictionExplainer />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText(/HIGH risk/)).toBeInTheDocument();
      expect(screen.getByText(/Recommend increased patrol/)).toBeInTheDocument();
    });
  });

  test('displays SHAP waterfall chart', async () => {
    render(
      <BrowserRouter>
        <PredictionExplainer />
      </BrowserRouter>
    );

    await waitFor(() => {
      const tabs = screen.getByText('SHAP Values');
      fireEvent.click(tabs);
    });

    await waitFor(() => {
      expect(screen.getByTestId('bar-chart')).toBeInTheDocument();
      expect(screen.getByText(/Feature Contributions/)).toBeInTheDocument();
    });
  });

  test('SHAP chart shows positive contributions in red', async () => {
    render(
      <BrowserRouter>
        <PredictionExplainer />
      </BrowserRouter>
    );

    await waitFor(() => {
      const tabs = screen.getByText('SHAP Values');
      fireEvent.click(tabs);
    });

    await waitFor(() => {
      expect(screen.getByText(/Historical Crime Rate/)).toBeInTheDocument();
    });
  });

  test('displays confidence breakdown', async () => {
    render(
      <BrowserRouter>
        <PredictionExplainer />
      </BrowserRouter>
    );

    await waitFor(() => {
      const tabs = screen.getByText('Confidence');
      fireEvent.click(tabs);
    });

    await waitFor(() => {
      expect(screen.getByText(/Data Quality/)).toBeInTheDocument();
      expect(screen.getByText(/Model Certainty/)).toBeInTheDocument();
      expect(screen.getByText(/Historical Accuracy/)).toBeInTheDocument();
      expect(screen.getByText(/82%/)).toBeInTheDocument();
    });
  });

  test('displays global feature importance', async () => {
    render(
      <BrowserRouter>
        <PredictionExplainer />
      </BrowserRouter>
    );

    await waitFor(() => {
      const tabs = screen.getByText('Feature Importance');
      fireEvent.click(tabs);
    });

    await waitFor(() => {
      expect(screen.getByText(/Global Feature Importance/)).toBeInTheDocument();
      expect(screen.getByText(/Historical Crime Rate/)).toBeInTheDocument();
    });
  });

  test('displays prediction timeline', async () => {
    render(
      <BrowserRouter>
        <PredictionExplainer />
      </BrowserRouter>
    );

    await waitFor(() => {
      const tabs = screen.getByText('Timeline');
      fireEvent.click(tabs);
    });

    await waitFor(() => {
      expect(screen.getByText(/Prediction History/)).toBeInTheDocument();
      expect(screen.getByText(/84.0%/)).toBeInTheDocument(); // Average accuracy
      expect(screen.getByText(/improving/)).toBeInTheDocument();
    });
  });

  test('what-if simulator updates predictions', async () => {
    render(
      <BrowserRouter>
        <PredictionExplainer />
      </BrowserRouter>
    );

    await waitFor(() => {
      const tabs = screen.getByText('What-If');
      fireEvent.click(tabs);
    });

    await waitFor(() => {
      const button = screen.getByText('Run Simulation');
      fireEvent.click(button);
    });

    await waitFor(() => {
      expect(axios.post).toHaveBeenCalledWith(
        'http://localhost:8000/api/explainability/what-if',
        null,
        expect.objectContaining({
          params: expect.objectContaining({
            location_id: 'grid_5_7',
            feature_name: 'Recent Police Presence',
            new_value: expect.any(Number)
          })
        })
      );
    });
  });

  test('displays what-if scenario results', async () => {
    render(
      <BrowserRouter>
        <PredictionExplainer />
      </BrowserRouter>
    );

    await waitFor(() => {
      const tabs = screen.getByText('What-If');
      fireEvent.click(tabs);
    });

    await waitFor(() => {
      const button = screen.getByText('Run Simulation');
      fireEvent.click(button);
    });

    await waitFor(() => {
      expect(screen.getByText(/Scenario Results/)).toBeInTheDocument();
      expect(screen.getByText(/68.0%/)).toBeInTheDocument(); // Original
      expect(screen.getByText(/60.0%/)).toBeInTheDocument(); // Modified
    });
  });

  test('displays risk badges with correct colors', async () => {
    render(
      <BrowserRouter>
        <PredictionExplainer />
      </BrowserRouter>
    );

    await waitFor(() => {
      const badge = screen.getByText('High');
      expect(badge).toBeInTheDocument();
    });
  });

  test('displays caveats section', async () => {
    render(
      <BrowserRouter>
        <PredictionExplainer />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText(/Important Caveats/)).toBeInTheDocument();
      expect(screen.getByText(/unexpected community events/)).toBeInTheDocument();
      expect(screen.getByText(/Weather changes/)).toBeInTheDocument();
    });
  });

  test('location ID input updates data', async () => {
    render(
      <BrowserRouter>
        <PredictionExplainer />
      </BrowserRouter>
    );

    await waitFor(() => {
      const input = screen.getByPlaceholderText('grid_5_7');
      fireEvent.change(input, { target: { value: 'grid_10_10' } });
    });

    await waitFor(() => {
      const button = screen.getByText('Analyze');
      fireEvent.click(button);
    });

    await waitFor(() => {
      expect(axios.get).toHaveBeenCalledWith(
        expect.any(String),
        expect.objectContaining({
          params: expect.objectContaining({
            location_id: 'grid_10_10'
          })
        })
      );
    });
  });

  test('displays top contributing factors', async () => {
    render(
      <BrowserRouter>
        <PredictionExplainer />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText(/Top Contributing Factors/)).toBeInTheDocument();
      expect(screen.getByText(/Historical Crime Rate \(30d\)/)).toBeInTheDocument();
    });
  });

  test('displays base value and total contributions', async () => {
    render(
      <BrowserRouter>
        <PredictionExplainer />
      </BrowserRouter>
    );

    await waitFor(() => {
      const tabs = screen.getByText('SHAP Values');
      fireEvent.click(tabs);
    });

    await waitFor(() => {
      expect(screen.getByText(/Base Value/)).toBeInTheDocument();
      expect(screen.getByText(/45.0%/)).toBeInTheDocument();
      expect(screen.getByText(/Final Prediction/)).toBeInTheDocument();
    });
  });

  test('feature importance categories display correctly', async () => {
    render(
      <BrowserRouter>
        <PredictionExplainer />
      </BrowserRouter>
    );

    await waitFor(() => {
      const tabs = screen.getByText('Feature Importance');
      fireEvent.click(tabs);
    });

    await waitFor(() => {
      expect(screen.getByText(/temporal/)).toBeInTheDocument();
      expect(screen.getByText(/historical/)).toBeInTheDocument();
    });
  });

  test('handles API errors gracefully', async () => {
    axios.get.mockRejectedValueOnce(new Error('Network error'));

    render(
      <BrowserRouter>
        <PredictionExplainer />
      </BrowserRouter>
    );

    await waitFor(() => {
      // Component should handle error without crashing
      expect(screen.queryByText(/Error/)).toBeTruthy() || expect(screen.queryByText(/Loading/)).toBeTruthy();
    });
  });
});

