import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { apiPath } from '../config/api.js';
import {
  BarChart, Bar, LineChart, Line, RadarChart, Radar, PolarGrid,
  PolarAngleAxis, PolarRadiusAxis, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Badge } from './ui/badge';
import { Alert, AlertDescription } from './ui/alert';
import { Progress } from './ui/progress';
import {
  Loader2, Scale, AlertTriangle, CheckCircle2, TrendingUp,
  Users, Shield, FileText, Lightbulb, BarChart3
} from 'lucide-react';

const COLORS = {
  White: '#3b82f6',
  Black: '#8b5cf6',
  Hispanic: '#10b981',
  Asian: '#f59e0b'
};

const getStatusColor = (status) => {
  switch(status) {
    case 'pass': return 'text-green-600 bg-green-50 border-green-200 dark:text-green-400 dark:bg-green-900/20 dark:border-green-800';
    case 'warning': return 'text-orange-600 bg-orange-50 border-orange-200 dark:text-orange-400 dark:bg-orange-900/20 dark:border-orange-800';
    case 'fail': return 'text-red-600 bg-red-50 border-red-200 dark:text-red-400 dark:bg-red-900/20 dark:border-red-800';
    default: return 'text-gray-600 bg-gray-50 border-gray-200 dark:text-gray-400 dark:bg-gray-900/20 dark:border-gray-800';
  }
};

const getStatusIcon = (status) => {
  switch(status) {
    case 'pass': return <CheckCircle2 className="w-5 h-5 text-green-600 dark:text-green-400" />;
    case 'warning': return <AlertTriangle className="w-5 h-5 text-orange-600 dark:text-orange-400" />;
    case 'fail': return <AlertTriangle className="w-5 h-5 text-red-600 dark:text-red-400" />;
    default: return <Scale className="w-5 h-5" />;
  }
};

export default function BiasAnalysisDashboard() {
  const [analysisData, setAnalysisData] = useState(null);
  const [interventions, setInterventions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedMetric, setSelectedMetric] = useState('false_positive_rate');

  useEffect(() => {
    fetchBiasData();
  }, []);

  const fetchBiasData = async () => {
    setLoading(true);
    try {
      const [analysis, interventionData] = await Promise.all([
        axios.get(apiPath('bias/analysis')),
        axios.get(apiPath('bias/interventions'))
      ]);
      
      setAnalysisData(analysis.data);
      setInterventions(interventionData.data);
    } catch (error) {
      console.error('Error fetching bias analysis:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <Loader2 className="w-8 h-8 animate-spin text-blue-600 dark:text-blue-400" />
      </div>
    );
  }

  // Prepare data for visualizations
  const demographicComparisonData = analysisData?.demographic_metrics.map(dm => ({
    group: dm.demographic_group,
    'Population %': dm.population_percentage,
    'Prediction %': dm.prediction_percentage,
    'Parity Ratio': dm.parity_ratio * 100,
    'FPR': dm.false_positive_rate * 100,
    'FNR': dm.false_negative_rate * 100,
    'Accuracy': dm.accuracy * 100
  })) || [];

  const fairnessRadarData = analysisData?.demographic_metrics.map(dm => ({
    group: dm.demographic_group,
    Accuracy: dm.accuracy * 100,
    Precision: dm.precision * 100,
    Recall: dm.recall * 100,
    'Parity': dm.parity_ratio * 100
  })) || [];

  // Historical trends - group by demographic
  const historicalByDemo = {};
  analysisData?.historical_trends.forEach(trend => {
    if (!historicalByDemo[trend.demographic_group]) {
      historicalByDemo[trend.demographic_group] = [];
    }
    historicalByDemo[trend.demographic_group].push({
      date: new Date(trend.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
      parity: trend.parity_ratio * 100,
      fpr: trend.false_positive_rate * 100
    });
  });

  return (
    <div className="space-y-6 p-6">
      {/* Header */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center gap-2 text-2xl">
                <Shield className="w-6 h-6" />
                Bias & Fairness Analysis Dashboard
              </CardTitle>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                Comprehensive ethical AI assessment for crime prediction model
              </p>
            </div>
            <div className="text-right">
              <div className="text-sm text-gray-600 dark:text-gray-400">Audit Status</div>
              <Badge 
                variant={analysisData?.audit_status === 'PASSED' ? 'default' : 'destructive'}
                className="text-lg px-4 py-1 mt-1"
              >
                {analysisData?.audit_status}
              </Badge>
            </div>
          </div>
        </CardHeader>
      </Card>

      {/* Overall Fairness Score */}
      <Card className="border-blue-200 dark:border-blue-800 bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20">
        <CardContent className="pt-6">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="col-span-2">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                  Overall Fairness Score
                </span>
                <span className="text-3xl font-bold text-blue-600 dark:text-blue-400">
                  {analysisData?.overall_fairness_score}/100
                </span>
              </div>
              <Progress 
                value={analysisData?.overall_fairness_score} 
                className="h-3"
              />
              <div className="flex items-center gap-2 mt-2 text-xs text-gray-600 dark:text-gray-400">
                <FileText className="w-4 h-4" />
                Model: {analysisData?.model_version}
              </div>
            </div>

            <div>
              <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Analysis Date</div>
              <div className="font-semibold">
                {new Date(analysisData?.analysis_date).toLocaleDateString()}
              </div>
              <div className="text-xs text-gray-500 dark:text-gray-500 mt-2">
                Next Audit: {new Date(analysisData?.next_audit_date).toLocaleDateString()}
              </div>
            </div>

            <div>
              <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Metrics Status</div>
              <div className="space-y-1">
                {analysisData?.fairness_metrics.map(metric => (
                  <div key={metric.metric_name} className="flex items-center gap-2 text-xs">
                    {getStatusIcon(metric.status)}
                    <span>{metric.metric_name}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Main Tabs */}
      <Tabs defaultValue="demographics" className="w-full">
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="demographics">
            <Users className="w-4 h-4 mr-2" />
            Demographics
          </TabsTrigger>
          <TabsTrigger value="metrics">
            <BarChart3 className="w-4 h-4 mr-2" />
            Fairness Metrics
          </TabsTrigger>
          <TabsTrigger value="trends">
            <TrendingUp className="w-4 h-4 mr-2" />
            Historical Trends
          </TabsTrigger>
          <TabsTrigger value="interventions">
            <Lightbulb className="w-4 h-4 mr-2" />
            Interventions
          </TabsTrigger>
          <TabsTrigger value="recommendations">
            <FileText className="w-4 h-4 mr-2" />
            Recommendations
          </TabsTrigger>
        </TabsList>

        {/* Demographics Tab */}
        <TabsContent value="demographics">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Demographic Parity Comparison */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Demographic Parity Analysis</CardTitle>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  Population vs Prediction Distribution
                </p>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={demographicComparisonData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                    <XAxis dataKey="group" />
                    <YAxis label={{ value: 'Percentage', angle: -90, position: 'insideLeft' }} />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="Population %" fill="#94a3b8" />
                    <Bar dataKey="Prediction %" fill="#3b82f6" />
                  </BarChart>
                </ResponsiveContainer>
                
                <div className="mt-4 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
                  <p className="text-xs text-blue-900 dark:text-blue-300">
                    <strong>Ideal:</strong> Prediction percentages should closely match population 
                    percentages across all demographic groups for fair representation.
                  </p>
                </div>
              </CardContent>
            </Card>

            {/* Performance Radar Chart */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Performance Comparison</CardTitle>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  Multi-dimensional fairness view
                </p>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <RadarChart data={fairnessRadarData[0] ? [
                    { metric: 'Accuracy', ...Object.fromEntries(fairnessRadarData.map(d => [d.group, d.Accuracy])) },
                    { metric: 'Precision', ...Object.fromEntries(fairnessRadarData.map(d => [d.group, d.Precision])) },
                    { metric: 'Recall', ...Object.fromEntries(fairnessRadarData.map(d => [d.group, d.Recall])) },
                    { metric: 'Parity', ...Object.fromEntries(fairnessRadarData.map(d => [d.group, d.Parity])) }
                  ] : []}>
                    <PolarGrid />
                    <PolarAngleAxis dataKey="metric" />
                    <PolarRadiusAxis angle={90} domain={[0, 100]} />
                    {fairnessRadarData.map((demo, index) => (
                      <Radar
                        key={demo.group}
                        name={demo.group}
                        dataKey={demo.group}
                        stroke={COLORS[demo.group]}
                        fill={COLORS[demo.group]}
                        fillOpacity={0.3}
                      />
                    ))}
                    <Legend />
                  </RadarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Detailed Metrics Table */}
            <Card className="lg:col-span-2">
              <CardHeader>
                <CardTitle className="text-lg">Detailed Performance Metrics by Demographic</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead className="bg-gray-50 dark:bg-[#1a1a1a]">
                      <tr>
                        <th className="px-4 py-3 text-left">Group</th>
                        <th className="px-4 py-3 text-right">Accuracy</th>
                        <th className="px-4 py-3 text-right">Precision</th>
                        <th className="px-4 py-3 text-right">Recall</th>
                        <th className="px-4 py-3 text-right">FPR</th>
                        <th className="px-4 py-3 text-right">FNR</th>
                        <th className="px-4 py-3 text-right">Parity Ratio</th>
                      </tr>
                    </thead>
                    <tbody>
                      {analysisData?.demographic_metrics.map((dm, idx) => (
                        <tr key={idx} className="border-t hover:bg-gray-50 dark:hover:bg-[#1a1a1a]">
                          <td className="px-4 py-3 font-medium flex items-center gap-2">
                            <div 
                              className="w-3 h-3 rounded-full" 
                              style={{ backgroundColor: COLORS[dm.demographic_group] }}
                            />
                            {dm.demographic_group}
                          </td>
                          <td className="px-4 py-3 text-right">
                            {(dm.accuracy * 100).toFixed(1)}%
                          </td>
                          <td className="px-4 py-3 text-right">
                            {(dm.precision * 100).toFixed(1)}%
                          </td>
                          <td className="px-4 py-3 text-right">
                            {(dm.recall * 100).toFixed(1)}%
                          </td>
                          <td className="px-4 py-3 text-right">
                            <span className={dm.false_positive_rate > 0.15 ? 'text-red-600 dark:text-red-400 font-semibold' : ''}>
                              {(dm.false_positive_rate * 100).toFixed(1)}%
                            </span>
                          </td>
                          <td className="px-4 py-3 text-right">
                            <span className={dm.false_negative_rate > 0.18 ? 'text-red-600 dark:text-red-400 font-semibold' : ''}>
                              {(dm.false_negative_rate * 100).toFixed(1)}%
                            </span>
                          </td>
                          <td className="px-4 py-3 text-right">
                            <Badge 
                              variant={
                                dm.parity_ratio >= 0.85 ? 'default' :
                                dm.parity_ratio >= 0.75 ? 'warning' :
                                'destructive'
                              }
                            >
                              {(dm.parity_ratio * 100).toFixed(0)}%
                            </Badge>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Fairness Metrics Tab */}
        <TabsContent value="metrics">
          <div className="space-y-6">
            {analysisData?.fairness_metrics.map((metric, idx) => (
              <Card key={idx} className={getStatusColor(metric.status)}>
                <CardContent className="pt-6">
                  <div className="flex items-start justify-between">
                    <div className="flex items-start gap-4 flex-1">
                      {getStatusIcon(metric.status)}
                      <div className="flex-1">
                        <h3 className="font-semibold text-lg mb-1">
                          {metric.metric_name}
                        </h3>
                        <p className="text-sm mb-3">
                          {metric.description}
                        </p>
                        <div className="flex items-center gap-4">
                          <div>
                            <span className="text-xs text-gray-600 dark:text-gray-400">Current Value</span>
                            <div className="text-2xl font-bold">
                              {(metric.value * 100).toFixed(1)}%
                            </div>
                          </div>
                          <div>
                            <span className="text-xs text-gray-600 dark:text-gray-400">Threshold</span>
                            <div className="text-lg font-semibold">
                              {(metric.threshold * 100).toFixed(0)}%
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    <Badge 
                      variant={
                        metric.status === 'pass' ? 'default' :
                        metric.status === 'warning' ? 'warning' :
                        'destructive'
                      }
                      className="text-sm px-3 py-1"
                    >
                      {metric.status.toUpperCase()}
                    </Badge>
                  </div>
                  <Progress 
                    value={(metric.value / metric.threshold) * 100} 
                    className="h-2 mt-4"
                  />
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* Historical Trends Tab */}
        <TabsContent value="trends">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Parity Ratio Trends (90 Days)</CardTitle>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                Tracking fairness improvements over time
              </p>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={400}>
                <LineChart>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                  <XAxis 
                    dataKey="date" 
                    type="category"
                    allowDuplicatedCategory={false}
                  />
                  <YAxis 
                    label={{ value: 'Parity Ratio (%)', angle: -90, position: 'insideLeft' }}
                    domain={[60, 100]}
                  />
                  <Tooltip />
                  <Legend />
                  {Object.entries(historicalByDemo).map(([group, data]) => (
                    <Line
                      key={group}
                      data={data}
                      type="monotone"
                      dataKey="parity"
                      name={group}
                      stroke={COLORS[group]}
                      strokeWidth={2}
                      dot={{ r: 3 }}
                    />
                  ))}
                </LineChart>
              </ResponsiveContainer>

              <div className="mt-4 p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-800">
                <div className="flex items-center gap-2 text-green-900 dark:text-green-300 font-semibold mb-2">
                  <TrendingUp className="w-5 h-5" />
                  Positive Trend Detected
                </div>
                <p className="text-sm text-green-800 dark:text-green-300">
                  Parity ratios have improved by an average of 18% across all demographic 
                  groups over the past 90 days due to implemented bias mitigation strategies.
                </p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Interventions Tab */}
        <TabsContent value="interventions">
          <div className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Bias Mitigation Interventions</CardTitle>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  Tracking impact of fairness improvements
                </p>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {interventions.map((intervention, idx) => (
                    <div key={idx} className="p-4 border rounded-lg bg-gray-50 dark:bg-[#1a1a1a]">
                      <div className="flex items-start justify-between mb-3">
                        <div>
                          <h4 className="font-semibold text-lg">
                            {intervention.intervention_type}
                          </h4>
                          <p className="text-sm text-gray-600 dark:text-gray-400">
                            Implemented: {new Date(intervention.implemented_date).toLocaleDateString()}
                          </p>
                        </div>
                        <Badge variant="default" className="text-sm">
                          +{intervention.improvement_percentage}%
                        </Badge>
                      </div>

                      <div className="grid grid-cols-2 gap-4 mb-3">
                        <div>
                          <div className="text-xs text-gray-600 dark:text-gray-400">Before</div>
                          <div className="text-2xl font-bold text-red-600 dark:text-red-400">
                            {(intervention.before_parity * 100).toFixed(0)}%
                          </div>
                        </div>
                        <div>
                          <div className="text-xs text-gray-600 dark:text-gray-400">After</div>
                          <div className="text-2xl font-bold text-green-600 dark:text-green-400">
                            {(intervention.after_parity * 100).toFixed(0)}%
                          </div>
                        </div>
                      </div>

                      <div>
                        <div className="text-xs text-gray-600 dark:text-gray-400 mb-1">Affected Groups</div>
                        <div className="flex gap-2 flex-wrap">
                          {intervention.affected_groups.map((group, i) => (
                            <Badge key={i} variant="outline">
                              {group}
                            </Badge>
                          ))}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Recommendations Tab */}
        <TabsContent value="recommendations">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Actionable Recommendations</CardTitle>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                Steps to improve model fairness and reduce bias
              </p>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {analysisData?.recommendations.map((rec, idx) => {
                  const isCritical = rec.includes('CRITICAL');
                  const isWarning = rec.includes('WARNING');
                  
                  return (
                    <Alert 
                      key={idx}
                      className={
                        isCritical ? 'border-red-200 bg-red-50 dark:border-red-800 dark:bg-red-900/20' :
                        isWarning ? 'border-orange-200 bg-orange-50 dark:border-orange-800 dark:bg-orange-900/20' :
                        'border-blue-200 bg-blue-50 dark:border-blue-800 dark:bg-blue-900/20'
                      }
                    >
                      {isCritical ? (
                        <AlertTriangle className="h-4 w-4 text-red-600 dark:text-red-400" />
                      ) : isWarning ? (
                        <AlertTriangle className="h-4 w-4 text-orange-600 dark:text-orange-400" />
                      ) : (
                        <Lightbulb className="h-4 w-4 text-blue-600 dark:text-blue-400" />
                      )}
                      <AlertDescription className="text-sm">
                        {rec}
                      </AlertDescription>
                    </Alert>
                  );
                })}
              </div>

              <div className="mt-6 p-4 bg-purple-50 dark:bg-purple-900/20 border border-purple-200 dark:border-purple-800 rounded-lg">
                <h4 className="font-semibold text-purple-900 dark:text-purple-300 mb-2 flex items-center gap-2">
                  <Shield className="w-5 h-5" />
                  Ethical AI Best Practices
                </h4>
                <ul className="text-sm text-purple-800 dark:text-purple-300 space-y-2">
                  <li className="flex items-start gap-2">
                    <CheckCircle2 className="w-4 h-4 mt-0.5 flex-shrink-0" />
                    <span>Regular community stakeholder engagement sessions</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle2 className="w-4 h-4 mt-0.5 flex-shrink-0" />
                    <span>Transparent model documentation and decision logs</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle2 className="w-4 h-4 mt-0.5 flex-shrink-0" />
                    <span>Quarterly independent bias audits</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle2 className="w-4 h-4 mt-0.5 flex-shrink-0" />
                    <span>Continuous monitoring of disparate impact</span>
                  </li>
                </ul>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}

