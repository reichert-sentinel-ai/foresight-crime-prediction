# Sprint F4: Prediction Confidence Explainer - Testing Checklist

## Prerequisites

1. **Start Backend Server:**
   ```bash
   cd project/repo-foresight/src/api
   uvicorn main:app --reload --port 8000
   ```

2. **Start Frontend Server (in separate terminal):**
   ```bash
   cd project/repo-foresight/frontend
   npm run dev
   ```

## Backend API Tests

### Test Script: `test_f4_explainability.py`

Run backend tests:
```bash
cd project/repo-foresight
python test_f4_explainability.py
```

### Expected Results:

✅ **Test 1: Explain Prediction**
- Endpoint: `/api/explainability/explain-prediction`
- Validates: risk_score, confidence, risk_level, feature_contributions
- Checks: values in valid ranges [0,1], risk_level in ["Critical", "High", "Medium", "Low"]

✅ **Test 2: Confidence Breakdown**
- Endpoint: `/api/explainability/confidence-breakdown`
- Validates: overall_confidence, data_quality_score, model_certainty, historical_accuracy
- Checks: all scores between 0-1, factors list provided

✅ **Test 3: What-If Scenario**
- Endpoint: `/api/explainability/what-if` (POST)
- Validates: original_prediction, modified_prediction, change_percentage
- Checks: predictions clamped to [0,1], change percentage calculated correctly

✅ **Test 4: Global Feature Importance**
- Endpoint: `/api/explainability/global-importance`
- Validates: feature_name, importance_score, rank, category, description
- Checks: categories in ["temporal", "spatial", "contextual", "historical"]

✅ **Test 5: Prediction Timeline**
- Endpoint: `/api/explainability/prediction-timeline`
- Validates: timeline entries, average_accuracy, confidence_trend
- Checks: timeline entries match days_back parameter

✅ **Test 6: Explanation Summary**
- Endpoint: `/api/explainability/explanation-summary`
- Validates: summary, confidence_explanation, recommendation, caveats
- Checks: all text fields have meaningful content (>50 chars)

## Frontend Component Tests

### Test File: `frontend/src/__tests__/PredictionExplainer.test.jsx`

Run frontend tests:
```bash
cd project/repo-foresight/frontend
npm test PredictionExplainer.test.jsx
```

### Test Coverage:

✅ **SHAP Waterfall Chart**
- Displays feature contributions correctly
- Positive contributions shown in red (#ef4444)
- Negative contributions shown in green (#22c55e)
- Base value and total contributions displayed
- Top factors list rendered

✅ **Confidence Breakdown**
- Shows all three components (Data Quality, Model Certainty, Historical Accuracy)
- Overall confidence score displayed
- Progress bars render correctly
- Factors affecting confidence listed

✅ **Natural Language Summary**
- Summary text displays
- Confidence explanation shown
- Recommendation displayed
- All text is clear and actionable

✅ **Timeline Tab**
- Historical predictions displayed
- Average accuracy calculated
- Confidence trend shown
- Chart renders with correct data

✅ **What-If Simulator**
- Feature selector dropdown works
- Value input accepts numeric values
- Run Simulation button triggers API call
- Results display original vs modified prediction
- Impact percentage calculated correctly

✅ **Global Feature Importance**
- Chart displays all features
- Features ranked correctly
- Category breakdown shown
- Tooltips provide helpful context

✅ **Risk Levels and Badges**
- Risk level displays correctly ("Critical", "High", "Medium", "Low")
- Badge colors match risk level
- Confidence interval displayed

✅ **Caveats Section**
- Warning section displayed
- All caveats listed
- Proper styling applied

## Manual Testing Checklist

### Navigate to Dashboard
1. Open browser: `http://localhost:5173/explainability`
2. Verify page loads without errors
3. Check loading spinner appears initially

### SHAP Values Tab
- [ ] Waterfall chart displays feature contributions
- [ ] Positive contributions colored red
- [ ] Negative contributions colored green
- [ ] Base value shown (around 45%)
- [ ] Total contributions calculated correctly
- [ ] Top 3 factors displayed
- [ ] Tooltips show contribution percentages

### Confidence Tab
- [ ] Bar chart shows 3 components
- [ ] Data Quality score displayed
- [ ] Model Certainty score displayed
- [ ] Historical Accuracy score displayed
- [ ] Overall confidence progress bar works
- [ ] Factors affecting confidence listed

### Feature Importance Tab
- [ ] Bar chart displays all features
- [ ] Features ranked by importance
- [ ] Category breakdown shows temporal/spatial/contextual/historical
- [ ] Tooltips show feature descriptions
- [ ] Categories sum to 100%

### Timeline Tab
- [ ] Line chart shows predicted risk over time
- [ ] Confidence line displayed on secondary axis
- [ ] Average accuracy calculated
- [ ] Confidence trend shown ("improving" or "stable")
- [ ] Data points match days_back parameter

### What-If Tab
- [ ] Feature dropdown populated
- [ ] Value input accepts numbers
- [ ] Run Simulation button works
- [ ] Original prediction displayed
- [ ] Modified prediction displayed
- [ ] Change percentage calculated
- [ ] Impact message appropriate

### Summary & Caveats
- [ ] Natural language summary displayed
- [ ] Confidence explanation shown
- [ ] Recommendation displayed
- [ ] Caveats section warns of limitations

### Location ID Input
- [ ] Input field accepts location IDs
- [ ] Analyze button triggers new API calls
- [ ] Data updates when location changes

## Integration Tests

### Full Workflow Test
1. Get prediction explanation
2. Get confidence breakdown
3. Get explanation summary
4. Run what-if scenario
5. Get prediction timeline
6. Get global feature importance

All endpoints should work together without errors.

## Performance Tests

- [ ] API responses complete in < 500ms
- [ ] Dashboard loads in < 2 seconds
- [ ] Charts render smoothly
- [ ] No memory leaks when switching tabs

## Browser Compatibility

- [ ] Chrome/Edge (Chromium)
- [ ] Firefox
- [ ] Safari (if available)

## Accessibility Tests

- [ ] Keyboard navigation works
- [ ] Screen reader compatible
- [ ] Color contrast meets WCAG AA
- [ ] Focus indicators visible

## Test Results Summary

Run all tests and mark completed:

- [ ] Backend API tests: `python test_f4_explainability.py`
- [ ] Frontend unit tests: `npm test PredictionExplainer.test.jsx`
- [ ] Manual visual testing completed
- [ ] All checklist items verified

## Issues Found

Document any issues discovered during testing:

1. 
2. 
3. 

## Test Completion Status

- **Backend Tests**: ⬜ Not Started / ⬜ In Progress / ⬜ Complete
- **Frontend Tests**: ⬜ Not Started / ⬜ In Progress / ⬜ Complete
- **Manual Testing**: ⬜ Not Started / ⬜ In Progress / ⬜ Complete
- **Integration Tests**: ⬜ Not Started / ⬜ In Progress / ⬜ Complete

---

**Last Updated**: {{ datetime.now().strftime('%Y-%m-%d %H:%M:%S') }}

