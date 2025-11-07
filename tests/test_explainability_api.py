"""
Tests for Explainability API Endpoints (Sprint F4)

Tests cover:
- SHAP-like feature contributions
- Confidence breakdown
- What-if scenarios
- Global feature importance
- Prediction timeline
- Natural language explanations
"""

import pytest
from fastapi.testclient import TestClient
from src.api.main import app
import json

client = TestClient(app)


class TestExplainPrediction:
    """Test /api/explainability/explain-prediction endpoint"""

    def test_explain_prediction_basic(self):
        """Test basic prediction explanation request"""
        response = client.get(
            "/api/explainability/explain-prediction",
            params={"location_id": "grid_5_7"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Check required fields
        assert "prediction_id" in data
        assert "predicted_risk_score" in data
        assert "confidence" in data
        assert "risk_level" in data
        assert "base_value" in data
        assert "feature_contributions" in data
        assert "top_factors" in data
        assert "confidence_interval" in data
        assert "similar_historical_cases" in data

    def test_explain_prediction_risk_score_range(self):
        """Test risk score is between 0 and 1"""
        response = client.get(
            "/api/explainability/explain-prediction",
            params={"location_id": "grid_5_7"}
        )
        
        data = response.json()
        assert 0 <= data["predicted_risk_score"] <= 1

    def test_explain_prediction_confidence_range(self):
        """Test confidence is between 0 and 1"""
        response = client.get(
            "/api/explainability/explain-prediction",
            params={"location_id": "grid_5_7"}
        )
        
        data = response.json()
        assert 0 <= data["confidence"] <= 1

    def test_explain_prediction_risk_levels(self):
        """Test risk level is one of valid values"""
        response = client.get(
            "/api/explainability/explain-prediction",
            params={"location_id": "grid_5_7"}
        )
        
        data = response.json()
        assert data["risk_level"] in ["Critical", "High", "Medium", "Low"]

    def test_explain_prediction_feature_contributions(self):
        """Test feature contributions structure"""
        response = client.get(
            "/api/explainability/explain-prediction",
            params={"location_id": "grid_5_7"}
        )
        
        data = response.json()
        assert len(data["feature_contributions"]) > 0
        
        for fc in data["feature_contributions"]:
            assert "feature_name" in fc
            assert "value" in fc
            assert "contribution" in fc
            assert "contribution_percentage" in fc
            assert "impact" in fc
            assert fc["impact"] in ["increases", "decreases"]

    def test_explain_prediction_top_factors(self):
        """Test top factors are provided"""
        response = client.get(
            "/api/explainability/explain-prediction",
            params={"location_id": "grid_5_7"}
        )
        
        data = response.json()
        assert len(data["top_factors"]) >= 3

    def test_explain_prediction_confidence_interval(self):
        """Test confidence interval structure"""
        response = client.get(
            "/api/explainability/explain-prediction",
            params={"location_id": "grid_5_7"}
        )
        
        data = response.json()
        assert "lower" in data["confidence_interval"]
        assert "upper" in data["confidence_interval"]
        assert 0 <= data["confidence_interval"]["lower"] <= 1
        assert 0 <= data["confidence_interval"]["upper"] <= 1
        assert data["confidence_interval"]["lower"] <= data["confidence_interval"]["upper"]

    def test_explain_prediction_with_time_window(self):
        """Test prediction with custom time window"""
        response = client.get(
            "/api/explainability/explain-prediction",
            params={"location_id": "grid_5_7", "time_window": "48h"}
        )
        
        assert response.status_code == 200

    def test_explain_prediction_missing_location_id(self):
        """Test error handling for missing location_id"""
        response = client.get("/api/explainability/explain-prediction")
        assert response.status_code == 422  # Validation error


class TestConfidenceBreakdown:
    """Test /api/explainability/confidence-breakdown endpoint"""

    def test_confidence_breakdown_basic(self):
        """Test basic confidence breakdown request"""
        # First get a prediction_id
        pred_response = client.get(
            "/api/explainability/explain-prediction",
            params={"location_id": "grid_5_7"}
        )
        prediction_id = pred_response.json()["prediction_id"]
        
        response = client.get(
            "/api/explainability/confidence-breakdown",
            params={"prediction_id": prediction_id}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "overall_confidence" in data
        assert "data_quality_score" in data
        assert "model_certainty" in data
        assert "historical_accuracy" in data
        assert "factors_affecting_confidence" in data

    def test_confidence_breakdown_ranges(self):
        """Test all confidence scores are between 0 and 1"""
        pred_response = client.get(
            "/api/explainability/explain-prediction",
            params={"location_id": "grid_5_7"}
        )
        prediction_id = pred_response.json()["prediction_id"]
        
        response = client.get(
            "/api/explainability/confidence-breakdown",
            params={"prediction_id": prediction_id}
        )
        
        data = response.json()
        assert 0 <= data["overall_confidence"] <= 1
        assert 0 <= data["data_quality_score"] <= 1
        assert 0 <= data["model_certainty"] <= 1
        assert 0 <= data["historical_accuracy"] <= 1

    def test_confidence_breakdown_factors(self):
        """Test factors list is provided"""
        pred_response = client.get(
            "/api/explainability/explain-prediction",
            params={"location_id": "grid_5_7"}
        )
        prediction_id = pred_response.json()["prediction_id"]
        
        response = client.get(
            "/api/explainability/confidence-breakdown",
            params={"prediction_id": prediction_id}
        )
        
        data = response.json()
        assert isinstance(data["factors_affecting_confidence"], list)
        assert len(data["factors_affecting_confidence"]) > 0


class TestWhatIfScenario:
    """Test /api/explainability/what-if endpoint"""

    def test_what_if_basic(self):
        """Test basic what-if scenario"""
        response = client.post(
            "/api/explainability/what-if",
            params={
                "location_id": "grid_5_7",
                "feature_name": "Recent Police Presence",
                "new_value": 0.8
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "scenario_name" in data
        assert "original_prediction" in data
        assert "modified_prediction" in data
        assert "change_percentage" in data
        assert "modified_features" in data

    def test_what_if_prediction_ranges(self):
        """Test prediction values are between 0 and 1"""
        response = client.post(
            "/api/explainability/what-if",
            params={
                "location_id": "grid_5_7",
                "feature_name": "Recent Police Presence",
                "new_value": 0.8
            }
        )
        
        data = response.json()
        assert 0 <= data["original_prediction"] <= 1
        assert 0 <= data["modified_prediction"] <= 1

    def test_what_if_different_features(self):
        """Test what-if with different features"""
        features = [
            "Recent Police Presence",
            "Street Lighting Quality",
            "Community Events Nearby"
        ]
        
        for feature in features:
            response = client.post(
                "/api/explainability/what-if",
                params={
                    "location_id": "grid_5_7",
                    "feature_name": feature,
                    "new_value": 0.9
                }
            )
            assert response.status_code == 200

    def test_what_if_negative_value(self):
        """Test what-if handles negative values"""
        response = client.post(
            "/api/explainability/what-if",
            params={
                "location_id": "grid_5_7",
                "feature_name": "Recent Police Presence",
                "new_value": -0.5
            }
        )
        # Should still work, but prediction clamped to [0,1]
        assert response.status_code == 200


class TestGlobalFeatureImportance:
    """Test /api/explainability/global-importance endpoint"""

    def test_global_importance_basic(self):
        """Test basic global importance request"""
        response = client.get("/api/explainability/global-importance")
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        assert len(data) > 0

    def test_global_importance_structure(self):
        """Test feature importance structure"""
        response = client.get("/api/explainability/global-importance")
        data = response.json()
        
        for feature in data:
            assert "feature_name" in feature
            assert "importance_score" in feature
            assert "rank" in feature
            assert "category" in feature
            assert "description" in feature

    def test_global_importance_categories(self):
        """Test feature categories are valid"""
        response = client.get("/api/explainability/global-importance")
        data = response.json()
        
        valid_categories = ["temporal", "spatial", "contextual", "historical"]
        for feature in data:
            assert feature["category"] in valid_categories

    def test_global_importance_scores(self):
        """Test importance scores are valid"""
        response = client.get("/api/explainability/global-importance")
        data = response.json()
        
        for feature in data:
            assert 0 <= feature["importance_score"] <= 1
            assert feature["rank"] > 0

    def test_global_importance_ranking(self):
        """Test features are ranked correctly"""
        response = client.get("/api/explainability/global-importance")
        data = response.json()
        
        # Check ranks are sequential
        ranks = [f["rank"] for f in data]
        assert ranks == sorted(ranks)
        assert ranks[0] == 1  # First rank should be 1


class TestPredictionTimeline:
    """Test /api/explainability/prediction-timeline endpoint"""

    def test_prediction_timeline_basic(self):
        """Test basic timeline request"""
        response = client.get(
            "/api/explainability/prediction-timeline",
            params={"location_id": "grid_5_7"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "location_id" in data
        assert "timeline" in data
        assert "average_accuracy" in data
        assert "confidence_trend" in data

    def test_prediction_timeline_structure(self):
        """Test timeline entry structure"""
        response = client.get(
            "/api/explainability/prediction-timeline",
            params={"location_id": "grid_5_7"}
        )
        
        data = response.json()
        assert len(data["timeline"]) > 0
        
        for entry in data["timeline"]:
            assert "date" in entry
            assert "predicted_risk" in entry
            assert "confidence" in entry
            assert "actual_incidents" in entry
            assert "accuracy" in entry

    def test_prediction_timeline_ranges(self):
        """Test timeline values are valid"""
        response = client.get(
            "/api/explainability/prediction-timeline",
            params={"location_id": "grid_5_7"}
        )
        
        data = response.json()
        for entry in data["timeline"]:
            assert 0 <= entry["predicted_risk"] <= 1
            assert 0 <= entry["confidence"] <= 1
            assert entry["actual_incidents"] >= 0

    def test_prediction_timeline_custom_days(self):
        """Test timeline with custom days_back"""
        response = client.get(
            "/api/explainability/prediction-timeline",
            params={"location_id": "grid_5_7", "days_back": 14}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["timeline"]) == 14

    def test_prediction_timeline_trend(self):
        """Test confidence trend is valid"""
        response = client.get(
            "/api/explainability/prediction-timeline",
            params={"location_id": "grid_5_7"}
        )
        
        data = response.json()
        assert data["confidence_trend"] in ["improving", "stable", "decreasing"]


class TestExplanationSummary:
    """Test /api/explainability/explanation-summary endpoint"""

    def test_explanation_summary_basic(self):
        """Test basic explanation summary request"""
        pred_response = client.get(
            "/api/explainability/explain-prediction",
            params={"location_id": "grid_5_7"}
        )
        prediction_id = pred_response.json()["prediction_id"]
        
        response = client.get(
            "/api/explainability/explanation-summary",
            params={"prediction_id": prediction_id}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "prediction_id" in data
        assert "summary" in data
        assert "confidence_explanation" in data
        assert "recommendation" in data
        assert "caveats" in data

    def test_explanation_summary_content(self):
        """Test explanation summary has meaningful content"""
        pred_response = client.get(
            "/api/explainability/explain-prediction",
            params={"location_id": "grid_5_7"}
        )
        prediction_id = pred_response.json()["prediction_id"]
        
        response = client.get(
            "/api/explainability/explanation-summary",
            params={"prediction_id": prediction_id}
        )
        
        data = response.json()
        assert len(data["summary"]) > 50  # Should be substantial
        assert len(data["confidence_explanation"]) > 50
        assert len(data["recommendation"]) > 50
        assert isinstance(data["caveats"], list)
        assert len(data["caveats"]) > 0


class TestIntegration:
    """Integration tests for explainability workflow"""

    def test_full_explanation_workflow(self):
        """Test complete explanation workflow"""
        # 1. Get prediction explanation
        explain_response = client.get(
            "/api/explainability/explain-prediction",
            params={"location_id": "grid_5_7"}
        )
        explain_data = explain_response.json()
        prediction_id = explain_data["prediction_id"]
        
        # 2. Get confidence breakdown
        confidence_response = client.get(
            "/api/explainability/confidence-breakdown",
            params={"prediction_id": prediction_id}
        )
        assert confidence_response.status_code == 200
        
        # 3. Get explanation summary
        summary_response = client.get(
            "/api/explainability/explanation-summary",
            params={"prediction_id": prediction_id}
        )
        assert summary_response.status_code == 200
        
        # 4. Run what-if scenario
        whatif_response = client.post(
            "/api/explainability/what-if",
            params={
                "location_id": "grid_5_7",
                "feature_name": "Recent Police Presence",
                "new_value": 0.9
            }
        )
        assert whatif_response.status_code == 200
        
        # 5. Get timeline
        timeline_response = client.get(
            "/api/explainability/prediction-timeline",
            params={"location_id": "grid_5_7"}
        )
        assert timeline_response.status_code == 200

    def test_feature_contributions_sum_to_prediction(self):
        """Test feature contributions logically sum to prediction"""
        response = client.get(
            "/api/explainability/explain-prediction",
            params={"location_id": "grid_5_7"}
        )
        
        data = response.json()
        base_value = data["base_value"]
        
        # Sum contributions
        total_contribution = sum([fc["contribution"] for fc in data["feature_contributions"]])
        
        # Prediction should be approximately base + contributions
        expected = base_value + total_contribution
        actual = data["predicted_risk_score"]
        
        # Allow small floating point differences
        assert abs(expected - actual) < 0.01

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

