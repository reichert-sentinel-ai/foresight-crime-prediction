import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { apiPath, API_BASE } from '../config/api.js';
import {
  BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer, Cell, ReferenceLine
} from 'recharts';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Badge } from './ui/badge';
import { Alert, AlertDescription } from './ui/alert';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import {
  Loader2, Brain, TrendingUp, AlertCircle, Info, Lightbulb,
  Target, Clock, MapPin, Shield, Activity, Layers
} from 'lucide-react';

const getRiskColor = (riskLevel) => {
  switch(riskLevel) {
    case 'Critical': return '#dc2626';
    case 'High': return '#ea580c';
    case 'Medium': return '#f59e0b';
    case 'Low': return '#22c55e';
    default: return '#6b7280';
  }
};

const getRiskBadgeVariant = (riskLevel) => {
  switch(riskLevel) {
    case 'Critical': return 'destructive';
    case 'High': return 'destructive';
    case 'Medium': return 'warning';
    case 'Low': return 'default';
    default: return 'secondary';
  }
};

export default function PredictionExplainer() {
  const [explanation, setExplanation] = useState(null);
  const [confidenceBreakdown, setConfidenceBreakdown] = useState(null);
  const [globalImportance, setGlobalImportance] = useState([]);
  const [timeline, setTimeline] = useState(null);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [locationId, setLocationId] = useState('grid_5_7');
  const [whatIfScenario, setWhatIfScenario] = useState(null);
  const [whatIfFeature, setWhatIfFeature] = useState('Recent Police Presence');
  const [whatIfValue, setWhatIfValue] = useState('0.5');

  useEffect(() => {
    fetchExplanationData();
  }, [locationId]);

  const fetchExplanationData = async () => {
    setLoading(true);
    setError(null);
    
    // First check if backend is reachable
    try {
      await axios.get(`${API_BASE}/health`, { timeout: 3000 });
    } catch (healthError) {
      setLoading(false);
      setError(
        'Backend server is not running or not accessible. ' +
        'Please start the backend server: cd project/repo-foresight/src/api && python -m uvicorn main:app --reload --port 8000'
      );
      return;
    }
    
    try {
      const axiosConfig = { timeout: 10000 }; // 10 second timeout
      
      const [explainRes, importanceRes, timelineRes] = await Promise.all([
        axios.get(apiPath('explainability/explain-prediction'), {
          params: { location_id: locationId },
          ...axiosConfig
        }),
        axios.get(apiPath('explainability/global-importance'), axiosConfig),
        axios.get(apiPath('explainability/prediction-timeline'), {
          params: { location_id: locationId },
          ...axiosConfig
        })
      ]);

      setExplanation(explainRes.data);
      setGlobalImportance(importanceRes.data);
      setTimeline(timelineRes.data);

      // Fetch confidence breakdown
      const confidenceRes = await axios.get(
        apiPath('explainability/confidence-breakdown'),
        { 
          params: { prediction_id: explainRes.data.prediction_id },
          ...axiosConfig
        }
      );
      setConfidenceBreakdown(confidenceRes.data);

      // Fetch summary
      const summaryRes = await axios.get(
        apiPath('explainability/explanation-summary'),
        { 
          params: { prediction_id: explainRes.data.prediction_id },
          ...axiosConfig
        }
      );
      setSummary(summaryRes.data);

    } catch (error) {
      console.error('Error fetching explanation data:', error);
      let errorMessage = 'Failed to fetch explanation data. ';
      
      if (error.code === 'ECONNABORTED') {
        errorMessage += 'Request timed out. Backend may be slow or not responding.';
      } else if (error.code === 'ERR_NETWORK' || error.message.includes('Network Error')) {
        errorMessage += 'Network error. Backend server may not be running.';
      } else if (error.response) {
        errorMessage += `API Error: ${error.response.status} - ${error.response.statusText}`;
      } else if (error.message) {
        errorMessage += `Error: ${error.message}`;
      } else {
        errorMessage += 'Please ensure the backend server is running.';
      }
      
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const runWhatIfScenario = async () => {
    try {
      const response = await axios.post(
        apiPath('explainability/what-if'),
        null,
        {
          params: {
            location_id: locationId,
            feature_name: whatIfFeature,
            new_value: parseFloat(whatIfValue)
          },
          timeout: 10000
        }
      );
      setWhatIfScenario(response.data);
    } catch (error) {
      console.error('Error running what-if scenario:', error);
      alert(`What-if scenario failed: ${error.message || 'Unknown error'}`);
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center h-96 space-y-4">
        <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
        <p className="text-sm text-gray-500 dark:text-[#a0a0a0]">Loading explanation data...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="space-y-6 p-6">
        <Card className="border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-900/20">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-red-900 dark:text-red-200">
              <AlertCircle className="w-5 h-5" />
              Error Loading Explainability Data
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <p className="text-sm text-red-800 dark:text-red-300">{error}</p>
              <div className="space-y-2">
                <p className="text-sm font-semibold text-red-900 dark:text-red-200">Troubleshooting Steps:</p>
                <ul className="list-disc list-inside space-y-1 text-sm text-red-800 dark:text-red-300">
                  <li>Ensure the backend server is running</li>
                  <li>Check if the API endpoint is accessible</li>
                  <li>Verify CORS settings allow requests from the frontend</li>
                  <li>Check browser console for detailed error messages</li>
                </ul>
              </div>
              <Button onClick={fetchExplanationData} className="mt-4">
                Retry
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  // Prepare SHAP-like waterfall data
  const waterfallData = explanation?.feature_contributions.map((fc, idx) => ({
    name: fc.feature_name,
    value: fc.contribution,
    absValue: Math.abs(fc.contribution),
    impact: fc.impact,
    percentage: fc.contribution_percentage
  })) || [];

  // Confidence components
  const confidenceComponents = confidenceBreakdown ? [
    { name: 'Data Quality', value: confidenceBreakdown.data_quality_score * 100 },
    { name: 'Model Certainty', value: confidenceBreakdown.model_certainty * 100 },
    { name: 'Historical Accuracy', value: confidenceBreakdown.historical_accuracy * 100 }
  ] : [];

  return (
    <div className="space-y-6">
      {/* Header */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center gap-2 text-2xl">
                <Brain className="w-6 h-6" />
                Prediction Explainability Dashboard
              </CardTitle>
              <p className="text-sm text-gray-500 dark:text-[#a0a0a0] mt-1">
                Understanding why predictions are made and how confident we are
              </p>
            </div>
            <div className="flex items-center gap-3">
              <div>
                <Label className="text-xs">Location ID</Label>
                <Input
                  value={locationId}
                  onChange={(e) => setLocationId(e.target.value)}
                  className="w-32 mt-1"
                  placeholder="grid_5_7"
                />
              </div>
              <Button onClick={fetchExplanationData} className="mt-5">
                Analyze
              </Button>
            </div>
          </div>
        </CardHeader>
      </Card>

      {/* Prediction Summary Card */}
      {explanation && (
        <Card className="border-2" style={{ borderColor: getRiskColor(explanation.risk_level) }}>
          <CardContent className="pt-6">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div className="col-span-2">
                <div className="flex items-center gap-3 mb-3">
                  <Target className="w-6 h-6" style={{ color: getRiskColor(explanation.risk_level) }} />
                  <div>
                    <div className="text-sm text-gray-600 dark:text-[#a0a0a0]">Predicted Risk Score</div>
                    <div className="text-4xl font-bold" style={{ color: getRiskColor(explanation.risk_level) }}>
                      {(explanation.predicted_risk_score * 100).toFixed(1)}%
                    </div>
                  </div>
                  <Badge 
                    variant={getRiskBadgeVariant(explanation.risk_level)}
                    className="text-lg px-3 py-1"
                  >
                    {explanation.risk_level}
                  </Badge>
                </div>
                <div className="flex items-center gap-2 text-sm text-gray-600 dark:text-[#a0a0a0]">
                  <MapPin className="w-4 h-4" />
                  <span>Location: {locationId}</span>
                </div>
              </div>

              <div>
                <div className="flex items-center gap-2 mb-2">
                  <Shield className="w-5 h-5 text-blue-600" />
                  <span className="text-sm font-medium">Confidence</span>
                </div>
                <div className="text-3xl font-bold text-blue-600">
                  {(explanation.confidence * 100).toFixed(0)}%
                </div>
                <div className="text-xs text-gray-500 dark:text-[#666] mt-1">
                  Range: {(explanation.confidence_interval.lower * 100).toFixed(0)}% - 
                  {(explanation.confidence_interval.upper * 100).toFixed(0)}%
                </div>
              </div>

              <div>
                <div className="flex items-center gap-2 mb-2">
                  <Activity className="w-5 h-5 text-purple-600" />
                  <span className="text-sm font-medium">Similar Cases</span>
                </div>
                <div className="text-3xl font-bold text-purple-600">
                  {explanation.similar_historical_cases}
                </div>
                <div className="text-xs text-gray-500 dark:text-[#666] mt-1">
                  Historical validations
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Natural Language Explanation */}
      {summary && (
        <Alert className="border-blue-200 dark:border-blue-800 bg-blue-50 dark:bg-blue-900/20">
          <Info className="h-4 w-4 text-blue-600" />
          <AlertDescription>
            <div className="space-y-3">
              <div>
                <h4 className="font-semibold text-blue-900 dark:text-blue-200 mb-1">Summary</h4>
                <p className="text-sm text-blue-800 dark:text-blue-300">{summary.summary}</p>
              </div>
              <div>
                <h4 className="font-semibold text-blue-900 dark:text-blue-200 mb-1">Confidence Explanation</h4>
                <p className="text-sm text-blue-800 dark:text-blue-300">{summary.confidence_explanation}</p>
              </div>
              <div className="flex items-start gap-2">
                <Lightbulb className="w-4 h-4 text-amber-600 mt-0.5" />
                <div>
                  <h4 className="font-semibold text-amber-900 dark:text-amber-200 mb-1">Recommendation</h4>
                  <p className="text-sm text-amber-800 dark:text-amber-300">{summary.recommendation}</p>
                </div>
              </div>
            </div>
          </AlertDescription>
        </Alert>
      )}

      {/* Main Tabs */}
      <Tabs defaultValue="shap" className="w-full">
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="shap">
            <Layers className="w-4 h-4 mr-2" />
            SHAP Values
          </TabsTrigger>
          <TabsTrigger value="confidence">
            <Shield className="w-4 h-4 mr-2" />
            Confidence
          </TabsTrigger>
          <TabsTrigger value="importance">
            <TrendingUp className="w-4 h-4 mr-2" />
            Feature Importance
          </TabsTrigger>
          <TabsTrigger value="timeline">
            <Clock className="w-4 h-4 mr-2" />
            Timeline
          </TabsTrigger>
          <TabsTrigger value="whatif">
            <Lightbulb className="w-4 h-4 mr-2" />
            What-If
          </TabsTrigger>
        </TabsList>

        {/* SHAP Values Tab */}
        <TabsContent value="shap">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Feature Contributions (SHAP-like Analysis)</CardTitle>
              <p className="text-sm text-gray-500 dark:text-[#a0a0a0]">
                How each feature pushes the prediction higher or lower
              </p>
            </CardHeader>
            <CardContent>
              {/* Waterfall Chart */}
              <ResponsiveContainer width="100%" height={400}>
                <BarChart
                  data={waterfallData}
                  layout="vertical"
                  margin={{ left: 200, right: 20 }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis type="number" label={{ value: 'Contribution to Risk Score', position: 'bottom' }} />
                  <YAxis type="category" dataKey="name" width={180} />
                  <Tooltip 
                    formatter={(value, name, props) => [
                      `${value > 0 ? '+' : ''}${(value * 100).toFixed(1)}%`,
                      `Contribution (${props.payload.percentage.toFixed(1)}% of total)`
                    ]}
                  />
                  <ReferenceLine x={0} stroke="#000" />
                  <Bar dataKey="value" name="Contribution">
                    {waterfallData.map((entry, index) => (
                      <Cell 
                        key={`cell-${index}`}
                        fill={entry.impact === 'increases' ? '#ef4444' : '#22c55e'}
                      />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>

              {/* Base Value Reference */}
              <div className="mt-4 p-4 bg-gray-50 dark:bg-[#1a1a1a] rounded-lg">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-600 dark:text-[#a0a0a0]">Base Value (Model Average):</span>
                  <span className="font-semibold">{(explanation.base_value * 100).toFixed(1)}%</span>
                </div>
                <div className="flex items-center justify-between text-sm mt-1">
                  <span className="text-gray-600 dark:text-[#a0a0a0]">Total Feature Contributions:</span>
                  <span className="font-semibold">
                    {((explanation.predicted_risk_score - explanation.base_value) * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="flex items-center justify-between text-sm mt-1 pt-2 border-t border-gray-200 dark:border-[#2a2a2a]">
                  <span className="text-gray-600 dark:text-[#a0a0a0] font-semibold">Final Prediction:</span>
                  <span className="font-bold text-lg" style={{ color: getRiskColor(explanation.risk_level) }}>
                    {(explanation.predicted_risk_score * 100).toFixed(1)}%
                  </span>
                </div>
              </div>

              {/* Top Factors */}
              <div className="mt-4">
                <h4 className="font-semibold text-sm mb-2">Top Contributing Factors</h4>
                <div className="space-y-2">
                  {explanation.top_factors.map((factor, idx) => (
                    <div key={idx} className="flex items-center gap-2">
                      <Badge variant="outline" className="w-6 h-6 flex items-center justify-center p-0">
                        {idx + 1}
                      </Badge>
                      <span className="text-sm">{factor}</span>
                    </div>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Confidence Breakdown Tab */}
        <TabsContent value="confidence">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Confidence Components</CardTitle>
                <p className="text-sm text-gray-500 dark:text-[#a0a0a0]">
                  Factors contributing to prediction confidence
                </p>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={confidenceComponents}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis label={{ value: 'Score (%)', angle: -90, position: 'insideLeft' }} />
                    <Tooltip formatter={(value) => `${value.toFixed(1)}%`} />
                    <Bar dataKey="value" fill="#3b82f6" />
                  </BarChart>
                </ResponsiveContainer>

                <div className="mt-4 space-y-3">
                  {confidenceBreakdown?.factors_affecting_confidence.map((factor, idx) => (
                    <Alert key={idx} className="border-gray-200 dark:border-[#2a2a2a]">
                      <AlertCircle className="h-4 w-4" />
                      <AlertDescription className="text-sm">
                        {factor}
                      </AlertDescription>
                    </Alert>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Confidence Interpretation</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-medium">Overall Confidence</span>
                      <span className="text-2xl font-bold text-blue-600">
                        {(confidenceBreakdown?.overall_confidence * 100).toFixed(0)}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 dark:bg-[#1a1a1a] rounded-full h-3">
                      <div
                        className="bg-blue-600 h-3 rounded-full transition-all"
                        style={{ width: `${confidenceBreakdown?.overall_confidence * 100}%` }}
                      />
                    </div>
                  </div>

                  <div className="space-y-3 pt-4">
                    <div className="flex items-start gap-3">
                      <div className="w-12 h-12 rounded-full bg-green-100 dark:bg-green-900/30 flex items-center justify-center flex-shrink-0">
                        <span className="text-lg font-bold text-green-700 dark:text-green-300">
                          {(confidenceBreakdown?.data_quality_score * 100).toFixed(0)}
                        </span>
                      </div>
                      <div>
                        <div className="font-semibold text-sm">Data Quality Score</div>
                        <p className="text-xs text-gray-600 dark:text-[#a0a0a0]">
                          Completeness and reliability of input data for this location
                        </p>
                      </div>
                    </div>

                    <div className="flex items-start gap-3">
                      <div className="w-12 h-12 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center flex-shrink-0">
                        <span className="text-lg font-bold text-blue-700 dark:text-blue-300">
                          {(confidenceBreakdown?.model_certainty * 100).toFixed(0)}
                        </span>
                      </div>
                      <div>
                        <div className="font-semibold text-sm">Model Certainty</div>
                        <p className="text-xs text-gray-600 dark:text-[#a0a0a0]">
                          How confident the model is based on training data distribution
                        </p>
                      </div>
                    </div>

                    <div className="flex items-start gap-3">
                      <div className="w-12 h-12 rounded-full bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center flex-shrink-0">
                        <span className="text-lg font-bold text-purple-700 dark:text-purple-300">
                          {(confidenceBreakdown?.historical_accuracy * 100).toFixed(0)}
                        </span>
                      </div>
                      <div>
                        <div className="font-semibold text-sm">Historical Accuracy</div>
                        <p className="text-xs text-gray-600 dark:text-[#a0a0a0]">
                          Past prediction accuracy for similar locations and conditions
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Global Feature Importance Tab */}
        <TabsContent value="importance">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Global Feature Importance</CardTitle>
              <p className="text-sm text-gray-500 dark:text-[#a0a0a0]">
                Most influential features across all predictions
              </p>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={400}>
                <BarChart data={globalImportance}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="feature_name" angle={-45} textAnchor="end" height={150} />
                  <YAxis label={{ value: 'Importance Score', angle: -90, position: 'insideLeft' }} />
                  <Tooltip 
                    content={({ active, payload }) => {
                      if (active && payload && payload.length) {
                        const data = payload[0].payload;
                        return (
                          <div className="bg-white dark:bg-[#1a1a1a] p-3 border border-gray-200 dark:border-[#2a2a2a] rounded-lg shadow-lg">
                            <p className="font-semibold mb-1">{data.feature_name}</p>
                            <p className="text-sm text-gray-600 dark:text-[#a0a0a0] mb-2">{data.description}</p>
                            <p className="text-sm">
                              <span className="font-medium">Importance:</span> {(data.importance_score * 100).toFixed(1)}%
                            </p>
                            <p className="text-sm">
                              <span className="font-medium">Rank:</span> #{data.rank}
                            </p>
                            <Badge variant="outline" className="mt-1">
                              {data.category}
                            </Badge>
                          </div>
                        );
                      }
                      return null;
                    }}
                  />
                  <Bar dataKey="importance_score" fill="#8b5cf6" />
                </BarChart>
              </ResponsiveContainer>

              <div className="mt-6 grid grid-cols-2 md:grid-cols-4 gap-3">
                {['temporal', 'spatial', 'contextual', 'historical'].map((category) => {
                  const categoryFeatures = globalImportance.filter(f => f.category === category);
                  const totalImportance = categoryFeatures.reduce((sum, f) => sum + f.importance_score, 0);
                  
                  return (
                    <div key={category} className="p-3 bg-gray-50 dark:bg-[#1a1a1a] rounded-lg">
                      <div className="text-xs text-gray-600 dark:text-[#a0a0a0] capitalize mb-1">{category}</div>
                      <div className="text-2xl font-bold text-purple-600">
                        {(totalImportance * 100).toFixed(0)}%
                      </div>
                      <div className="text-xs text-gray-500 dark:text-[#666]">
                        {categoryFeatures.length} features
                      </div>
                    </div>
                  );
                })}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Timeline Tab */}
        <TabsContent value="timeline">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Prediction History & Accuracy</CardTitle>
              <p className="text-sm text-gray-500 dark:text-[#a0a0a0]">
                How predictions have evolved for this location
              </p>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={400}>
                <LineChart data={timeline?.timeline}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis yAxisId="left" label={{ value: 'Risk Score', angle: -90, position: 'insideLeft' }} />
                  <YAxis yAxisId="right" orientation="right" label={{ value: 'Confidence', angle: 90, position: 'insideRight' }} />
                  <Tooltip />
                  <Legend />
                  <Line 
                    yAxisId="left"
                    type="monotone" 
                    dataKey="predicted_risk" 
                    stroke="#3b82f6" 
                    strokeWidth={2}
                    name="Predicted Risk"
                  />
                  <Line 
                    yAxisId="right"
                    type="monotone" 
                    dataKey="confidence" 
                    stroke="#10b981" 
                    strokeWidth={2}
                    name="Confidence"
                  />
                </LineChart>
              </ResponsiveContainer>

              <div className="mt-4 grid grid-cols-3 gap-4">
                <div className="p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                  <div className="text-sm text-blue-600 dark:text-blue-400 mb-1">Average Accuracy</div>
                  <div className="text-2xl font-bold text-blue-700 dark:text-blue-300">
                    {(timeline?.average_accuracy * 100).toFixed(1)}%
                  </div>
                </div>
                <div className="p-3 bg-green-50 dark:bg-green-900/20 rounded-lg">
                  <div className="text-sm text-green-600 dark:text-green-400 mb-1">Confidence Trend</div>
                  <div className="text-2xl font-bold text-green-700 dark:text-green-300 capitalize">
                    {timeline?.confidence_trend}
                  </div>
                </div>
                <div className="p-3 bg-purple-50 dark:bg-purple-900/20 rounded-lg">
                  <div className="text-sm text-purple-600 dark:text-purple-400 mb-1">Data Points</div>
                  <div className="text-2xl font-bold text-purple-700 dark:text-purple-300">
                    {timeline?.timeline.length}
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* What-If Analysis Tab */}
        <TabsContent value="whatif">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">What-If Scenario Simulator</CardTitle>
                <p className="text-sm text-gray-500 dark:text-[#a0a0a0]">
                  See how changing factors affects prediction
                </p>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <Label className="text-sm">Feature to Modify</Label>
                    <select 
                      className="w-full mt-1 p-2 border border-gray-300 dark:border-[#2a2a2a] bg-white dark:bg-[#1a1a1a] rounded-md text-gray-900 dark:text-[#e5e5e5]"
                      value={whatIfFeature}
                      onChange={(e) => setWhatIfFeature(e.target.value)}
                    >
                      <option>Recent Police Presence</option>
                      <option>Street Lighting Quality</option>
                      <option>Community Events Nearby</option>
                      <option>Historical Crime Rate (30d)</option>
                    </select>
                  </div>

                  <div>
                    <Label className="text-sm">New Value</Label>
                    <Input
                      type="number"
                      step="0.1"
                      value={whatIfValue}
                      onChange={(e) => setWhatIfValue(e.target.value)}
                      className="mt-1"
                    />
                  </div>

                  <Button 
                    className="w-full"
                    onClick={runWhatIfScenario}
                  >
                    Run Simulation
                  </Button>
                </div>

                <div className="mt-6 space-y-3">
                  <Alert className="border-blue-200 dark:border-blue-800 bg-blue-50 dark:bg-blue-900/20">
                    <Info className="h-4 w-4 text-blue-600" />
                    <AlertDescription className="text-sm text-blue-800 dark:text-blue-300">
                      <strong>Tip:</strong> Increase "Recent Police Presence" or 
                      "Street Lighting Quality" to see risk reduction. These are actionable 
                      interventions that law enforcement can implement.
                    </AlertDescription>
                  </Alert>
                </div>
              </CardContent>
            </Card>

            {whatIfScenario && (
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Scenario Results</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between p-4 bg-gray-50 dark:bg-[#1a1a1a] rounded-lg">
                      <div>
                        <div className="text-sm text-gray-600 dark:text-[#a0a0a0]">Original Prediction</div>
                        <div className="text-2xl font-bold">
                          {(whatIfScenario.original_prediction * 100).toFixed(1)}%
                        </div>
                      </div>
                      <div className="text-4xl">→</div>
                      <div>
                        <div className="text-sm text-gray-600 dark:text-[#a0a0a0]">Modified Prediction</div>
                        <div className="text-2xl font-bold text-green-600">
                          {(whatIfScenario.modified_prediction * 100).toFixed(1)}%
                        </div>
                      </div>
                    </div>

                    <div className="p-4 border border-gray-200 dark:border-[#2a2a2a] rounded-lg">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-sm font-medium">Impact</span>
                        <Badge 
                          variant={whatIfScenario.change_percentage < 0 ? 'default' : 'destructive'}
                          className="text-lg px-3"
                        >
                          {whatIfScenario.change_percentage > 0 ? '+' : ''}
                          {whatIfScenario.change_percentage.toFixed(1)}%
                        </Badge>
                      </div>
                      <p className="text-sm text-gray-600 dark:text-[#a0a0a0]">
                        {whatIfScenario.change_percentage < 0 
                          ? `This intervention could reduce crime risk by ${Math.abs(whatIfScenario.change_percentage).toFixed(1)}%`
                          : `This change could increase crime risk by ${whatIfScenario.change_percentage.toFixed(1)}%`
                        }
                      </p>
                    </div>

                    <Alert className="border-green-200 dark:border-green-800 bg-green-50 dark:bg-green-900/20">
                      <Lightbulb className="h-4 w-4 text-green-600" />
                      <AlertDescription className="text-sm text-green-800 dark:text-green-300">
                        <strong>Actionable Insight:</strong> Implementing this change 
                        would likely improve public safety outcomes. Consider resource 
                        allocation to make this intervention possible.
                      </AlertDescription>
                    </Alert>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        </TabsContent>
      </Tabs>

      {/* Caveats */}
      {summary && (
        <Card className="border-orange-200 dark:border-orange-800 bg-orange-50 dark:bg-orange-900/20">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-orange-900 dark:text-orange-200">
              <AlertCircle className="w-5 h-5" />
              Important Caveats
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2">
              {summary.caveats.map((caveat, idx) => (
                <li key={idx} className="flex items-start gap-2 text-sm text-orange-800 dark:text-orange-300">
                  <span className="text-orange-600 dark:text-orange-400 font-bold">•</span>
                  <span>{caveat}</span>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

