import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  LineChart, Line, BarChart, Bar, AreaChart, Area, ComposedChart,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Badge } from './ui/badge';
import { Alert, AlertDescription } from './ui/alert';
import { 
  Loader2, Clock, Calendar, TrendingUp, AlertTriangle, 
  Activity, BarChart3, Info 
} from 'lucide-react';

export default function TemporalPatterns() {
  const [analysisData, setAnalysisData] = useState(null);
  const [forecastData, setForecastData] = useState(null);
  const [anomalyData, setAnomalyData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [crimeType, setCrimeType] = useState('all');
  const [location, setLocation] = useState('downtown');

  useEffect(() => {
    fetchAllData();
  }, [crimeType, location]);

  const fetchAllData = async () => {
    setLoading(true);
    try {
      const [analysis, forecast, anomalies] = await Promise.all([
        axios.get('http://localhost:8000/api/temporal/analysis', {
          params: { crime_type: crimeType, location }
        }),
        axios.get('http://localhost:8000/api/temporal/forecast', {
          params: { crime_type: crimeType, location, forecast_days: 7 }
        }),
        axios.get('http://localhost:8000/api/temporal/anomalies')
      ]);
      
      setAnalysisData(analysis.data);
      setForecastData(forecast.data);
      setAnomalyData(anomalies.data);
    } catch (error) {
      console.error('Error fetching temporal data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
      </div>
    );
  }

  return (
    <div className="space-y-6 px-4 py-6">
      {/* Header with Controls */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Activity className="w-5 h-5" />
            Temporal Crime Pattern Analysis
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="text-sm font-medium mb-2 block">Crime Type</label>
              <Select value={crimeType} onValueChange={setCrimeType}>
                <SelectTrigger>
                  <SelectValue>
                    {crimeType === 'all' ? 'All Crimes' : 
                     crimeType === 'theft' ? 'Theft' :
                     crimeType === 'assault' ? 'Assault' :
                     crimeType === 'burglary' ? 'Burglary' :
                     crimeType === 'robbery' ? 'Robbery' : 'All Crimes'}
                  </SelectValue>
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Crimes</SelectItem>
                  <SelectItem value="theft">Theft</SelectItem>
                  <SelectItem value="assault">Assault</SelectItem>
                  <SelectItem value="burglary">Burglary</SelectItem>
                  <SelectItem value="robbery">Robbery</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div>
              <label className="text-sm font-medium mb-2 block">Location</label>
              <Select value={location} onValueChange={setLocation}>
                <SelectTrigger>
                  <SelectValue>
                    {location === 'downtown' ? 'Downtown' :
                     location === 'northside' ? 'North Side' :
                     location === 'southside' ? 'South Side' :
                     location === 'westside' ? 'West Side' : 'Downtown'}
                  </SelectValue>
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="downtown">Downtown</SelectItem>
                  <SelectItem value="northside">North Side</SelectItem>
                  <SelectItem value="southside">South Side</SelectItem>
                  <SelectItem value="westside">West Side</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Key Insights */}
      {analysisData && (
        <Card className="border-blue-200 bg-blue-50 dark:bg-blue-900/20 dark:border-blue-800">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-blue-900 dark:text-blue-200">
              <Info className="w-5 h-5" />
              Key Insights
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {analysisData.insights.map((insight, idx) => (
                <div key={idx} className="flex items-start gap-2 text-sm">
                  <div className="w-2 h-2 bg-blue-600 rounded-full mt-1.5" />
                  <span className="text-gray-700 dark:text-gray-300">{insight}</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Tabbed Visualizations */}
      <Tabs defaultValue="hourly" className="w-full">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="hourly">
            <Clock className="w-4 h-4 mr-2" />
            Hourly
          </TabsTrigger>
          <TabsTrigger value="weekly">
            <Calendar className="w-4 h-4 mr-2" />
            Weekly
          </TabsTrigger>
          <TabsTrigger value="forecast">
            <TrendingUp className="w-4 h-4 mr-2" />
            Forecast
          </TabsTrigger>
          <TabsTrigger value="anomalies">
            <AlertTriangle className="w-4 h-4 mr-2" />
            Anomalies
          </TabsTrigger>
        </TabsList>

        {/* Hourly Patterns */}
        <TabsContent value="hourly">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">24-Hour Crime Pattern</CardTitle>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                Incident distribution and severity across hours of the day
              </p>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={400}>
                <ComposedChart data={analysisData?.hourly_patterns}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="hour" 
                    tickFormatter={(hour) => `${hour}:00`}
                  />
                  <YAxis yAxisId="left" label={{ value: 'Incidents', angle: -90, position: 'insideLeft' }} />
                  <YAxis yAxisId="right" orientation="right" label={{ value: 'Severity', angle: 90, position: 'insideRight' }} />
                  <Tooltip 
                    formatter={(value, name) => [
                      value,
                      name === 'incidents' ? 'Incidents' : 
                      name === 'severity_score' ? 'Severity' : 
                      'Response Time (min)'
                    ]}
                    labelFormatter={(hour) => `Hour: ${hour}:00`}
                  />
                  <Legend />
                  <Bar yAxisId="left" dataKey="incidents" fill="#3b82f6" name="Incidents" />
                  <Line 
                    yAxisId="right" 
                    type="monotone" 
                    dataKey="severity_score" 
                    stroke="#ef4444" 
                    name="Severity"
                    strokeWidth={2}
                  />
                </ComposedChart>
              </ResponsiveContainer>
              
              {/* Peak Hours Summary */}
              <div className="mt-4 p-4 bg-gray-50 dark:bg-[#1f1f1f] rounded-lg">
                <h4 className="font-semibold text-sm mb-2">Peak Crime Hours</h4>
                <div className="flex gap-2 flex-wrap">
                  {analysisData?.peak_times.hours.map((hour) => (
                    <Badge key={hour} variant="destructive">
                      {hour}:00 - {hour + 1}:00
                    </Badge>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Day of Week Patterns */}
        <TabsContent value="weekly">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Day of Week Pattern</CardTitle>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                Crime incidents by day with trend indicators
              </p>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={400}>
                <BarChart data={analysisData?.day_of_week_patterns}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="day" />
                  <YAxis label={{ value: 'Incidents', angle: -90, position: 'insideLeft' }} />
                  <Tooltip />
                  <Legend />
                  <Bar 
                    dataKey="incidents" 
                    fill="#8b5cf6"
                    name="Incidents"
                  />
                </BarChart>
              </ResponsiveContainer>

              {/* Weekly Summary */}
              <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-4">
                {analysisData?.day_of_week_patterns.map((day) => (
                  <div key={day.day} className="p-3 bg-gray-50 dark:bg-[#1f1f1f] rounded-lg">
                    <div className="text-xs text-gray-600 dark:text-gray-400">{day.day}</div>
                    <div className="text-lg font-bold">{day.incidents}</div>
                    <Badge 
                      variant={
                        day.trend === 'increasing' ? 'destructive' : 
                        day.trend === 'decreasing' ? 'default' : 
                        'secondary'
                      }
                      className="text-xs mt-1"
                    >
                      {day.trend}
                    </Badge>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Time Series Forecast */}
        <TabsContent value="forecast">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">7-Day Crime Forecast</CardTitle>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                Predicted vs actual incidents with confidence intervals
              </p>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={400}>
                <AreaChart data={analysisData?.time_series.slice(-14)}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="timestamp" 
                    tickFormatter={(date) => new Date(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                  />
                  <YAxis label={{ value: 'Incidents', angle: -90, position: 'insideLeft' }} />
                  <Tooltip 
                    labelFormatter={(date) => new Date(date).toLocaleDateString()}
                  />
                  <Legend />
                  <Area 
                    type="monotone" 
                    dataKey="confidence_upper" 
                    stackId="1"
                    stroke="#cbd5e1" 
                    fill="#e2e8f0" 
                    name="Upper Confidence"
                  />
                  <Area 
                    type="monotone" 
                    dataKey="confidence_lower" 
                    stackId="1"
                    stroke="#cbd5e1" 
                    fill="#ffffff" 
                    name="Lower Confidence"
                  />
                  <Line 
                    type="monotone" 
                    dataKey="actual_incidents" 
                    stroke="#3b82f6" 
                    strokeWidth={2}
                    name="Actual"
                    dot={{ r: 4 }}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="predicted_incidents" 
                    stroke="#10b981" 
                    strokeWidth={2}
                    strokeDasharray="5 5"
                    name="Predicted"
                  />
                </AreaChart>
              </ResponsiveContainer>

              {/* Forecast Table */}
              {forecastData && (
                <div className="mt-4">
                  <h4 className="font-semibold text-sm mb-3">Next 7 Days Forecast</h4>
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead className="bg-gray-50 dark:bg-[#1f1f1f]">
                        <tr>
                          <th className="px-4 py-2 text-left">Date</th>
                          <th className="px-4 py-2 text-left">Day</th>
                          <th className="px-4 py-2 text-right">Predicted</th>
                          <th className="px-4 py-2 text-center">Risk</th>
                          <th className="px-4 py-2 text-right">Patrol Units</th>
                        </tr>
                      </thead>
                      <tbody>
                        {forecastData.forecasts.map((forecast, idx) => (
                          <tr key={idx} className="border-t border-gray-200 dark:border-[#2a2a2a]">
                            <td className="px-4 py-2">{new Date(forecast.date).toLocaleDateString()}</td>
                            <td className="px-4 py-2">{forecast.day_of_week}</td>
                            <td className="px-4 py-2 text-right font-semibold">
                              {forecast.predicted_incidents}
                            </td>
                            <td className="px-4 py-2 text-center">
                              <Badge 
                                variant={
                                  forecast.risk_level === 'high' ? 'destructive' :
                                  forecast.risk_level === 'medium' ? 'warning' :
                                  'secondary'
                                }
                              >
                                {forecast.risk_level}
                              </Badge>
                            </td>
                            <td className="px-4 py-2 text-right">
                              {forecast.recommended_patrol_units}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* Anomaly Detection */}
        <TabsContent value="anomalies">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Detected Anomalies</CardTitle>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                Unusual crime spikes requiring investigation
              </p>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {anomalyData?.anomalies.map((anomaly, idx) => (
                  <Alert key={idx} className="border-orange-200 bg-orange-50 dark:bg-orange-900/20 dark:border-orange-800" variant="warning">
                    <AlertTriangle className="h-4 w-4 text-orange-600 dark:text-orange-400" />
                    <AlertDescription>
                      <div className="space-y-2">
                        <div className="flex items-center justify-between">
                          <span className="font-semibold text-gray-900 dark:text-gray-100">
                            {new Date(anomaly.date).toLocaleDateString('en-US', { 
                              weekday: 'long', 
                              year: 'numeric', 
                              month: 'long', 
                              day: 'numeric' 
                            })}
                          </span>
                          <Badge variant="destructive">{anomaly.severity.toUpperCase()}</Badge>
                        </div>
                        
                        <div className="grid grid-cols-3 gap-4 text-sm">
                          <div>
                            <div className="text-gray-600 dark:text-gray-400">Expected</div>
                            <div className="font-semibold">{anomaly.expected_incidents}</div>
                          </div>
                          <div>
                            <div className="text-gray-600 dark:text-gray-400">Actual</div>
                            <div className="font-semibold text-orange-600 dark:text-orange-400">{anomaly.actual_incidents}</div>
                          </div>
                          <div>
                            <div className="text-gray-600 dark:text-gray-400">Deviation</div>
                            <div className="font-semibold">{anomaly.deviation}σ</div>
                          </div>
                        </div>

                        <div>
                          <div className="text-xs text-gray-600 dark:text-gray-400 mb-1">Possible Causes:</div>
                          <div className="flex gap-2 flex-wrap">
                            {anomaly.possible_causes.map((cause, i) => (
                              <Badge key={i} variant="secondary" className="text-xs">
                                {cause}
                              </Badge>
                            ))}
                          </div>
                        </div>
                      </div>
                    </AlertDescription>
                  </Alert>
                ))}
              </div>

              {anomalyData && (
                <div className="mt-4 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                  <p className="text-sm text-blue-900 dark:text-blue-200">
                    <strong>Recommendation:</strong> {anomalyData.recommendation}
                  </p>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}

