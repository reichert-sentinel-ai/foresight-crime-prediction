from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import numpy as np

router = APIRouter(prefix="/api/bias", tags=["bias-analysis"])

class DemographicMetrics(BaseModel):
    demographic_group: str
    population_percentage: float
    prediction_percentage: float
    false_positive_rate: float
    false_negative_rate: float
    accuracy: float
    precision: float
    recall: float
    parity_ratio: float  # Closer to 1.0 is better

class BiasMetric(BaseModel):
    metric_name: str
    value: float
    threshold: float
    status: str  # "pass", "warning", "fail"
    description: str

class HistoricalBiasTrend(BaseModel):
    date: str
    demographic_group: str
    parity_ratio: float
    false_positive_rate: float

class BiasAnalysisReport(BaseModel):
    analysis_date: str
    model_version: str
    overall_fairness_score: float  # 0-100 scale
    demographic_metrics: List[DemographicMetrics]
    fairness_metrics: List[BiasMetric]
    historical_trends: List[HistoricalBiasTrend]
    recommendations: List[str]
    audit_status: str
    next_audit_date: str

class InterventionImpact(BaseModel):
    intervention_type: str
    implemented_date: str
    before_parity: float
    after_parity: float
    improvement_percentage: float
    affected_groups: List[str]

@router.get("/analysis", response_model=BiasAnalysisReport)
async def get_bias_analysis(
    model_version: str = Query("v2.3.1", description="Model version to analyze"),
    include_historical: bool = Query(True, description="Include trend data")
):
    """
    Comprehensive bias and fairness analysis for crime prediction model.
    """
    
    # Define demographic groups for analysis
    demographics = [
        {"group": "White", "pop_pct": 45.0},
        {"group": "Black", "pop_pct": 30.0},
        {"group": "Hispanic", "pop_pct": 20.0},
        {"group": "Asian", "pop_pct": 5.0}
    ]
    
    # Generate demographic metrics
    demographic_metrics = []
    for demo in demographics:
        # Simulate fairness metrics (in production, calculate from actual data)
        base_accuracy = 0.85
        variation = np.random.uniform(-0.05, 0.05)
        
        accuracy = base_accuracy + variation
        fpr = np.random.uniform(0.08, 0.15)  # False positive rate
        fnr = np.random.uniform(0.10, 0.18)  # False negative rate
        precision = accuracy * np.random.uniform(0.90, 0.98)
        recall = accuracy * np.random.uniform(0.88, 0.96)
        
        # Prediction percentage should be close to population percentage for fairness
        pred_pct = demo["pop_pct"] * np.random.uniform(0.85, 1.15)
        
        # Calculate parity ratio (closer to 1.0 is better)
        parity_ratio = min(pred_pct, demo["pop_pct"]) / max(pred_pct, demo["pop_pct"])
        
        demographic_metrics.append(DemographicMetrics(
            demographic_group=demo["group"],
            population_percentage=demo["pop_pct"],
            prediction_percentage=round(pred_pct, 2),
            false_positive_rate=round(fpr, 3),
            false_negative_rate=round(fnr, 3),
            accuracy=round(accuracy, 3),
            precision=round(precision, 3),
            recall=round(recall, 3),
            parity_ratio=round(parity_ratio, 3)
        ))
    
    # Calculate fairness metrics
    fairness_metrics = []
    
    # 1. Demographic Parity
    avg_parity = np.mean([dm.parity_ratio for dm in demographic_metrics])
    fairness_metrics.append(BiasMetric(
        metric_name="Demographic Parity",
        value=round(avg_parity, 3),
        threshold=0.80,
        status="pass" if avg_parity >= 0.80 else "warning" if avg_parity >= 0.70 else "fail",
        description="Measures if predictions are distributed proportionally across groups"
    ))
    
    # 2. Equal Opportunity (FNR parity)
    fnr_values = [dm.false_negative_rate for dm in demographic_metrics]
    fnr_disparity = max(fnr_values) - min(fnr_values)
    fairness_metrics.append(BiasMetric(
        metric_name="Equal Opportunity",
        value=round(1 - fnr_disparity, 3),
        threshold=0.85,
        status="pass" if fnr_disparity < 0.10 else "warning" if fnr_disparity < 0.15 else "fail",
        description="Ensures false negative rates are similar across groups"
    ))
    
    # 3. Equalized Odds (FPR and FNR parity)
    fpr_values = [dm.false_positive_rate for dm in demographic_metrics]
    fpr_disparity = max(fpr_values) - min(fpr_values)
    combined_disparity = (fpr_disparity + fnr_disparity) / 2
    fairness_metrics.append(BiasMetric(
        metric_name="Equalized Odds",
        value=round(1 - combined_disparity, 3),
        threshold=0.85,
        status="pass" if combined_disparity < 0.10 else "warning" if combined_disparity < 0.15 else "fail",
        description="Both FPR and FNR are similar across groups"
    ))
    
    # 4. Predictive Parity (Precision equality)
    precision_values = [dm.precision for dm in demographic_metrics]
    precision_disparity = max(precision_values) - min(precision_values)
    fairness_metrics.append(BiasMetric(
        metric_name="Predictive Parity",
        value=round(1 - precision_disparity, 3),
        threshold=0.85,
        status="pass" if precision_disparity < 0.08 else "warning" if precision_disparity < 0.12 else "fail",
        description="Precision is consistent across demographic groups"
    ))
    
    # 5. Calibration Score
    calibration = np.random.uniform(0.88, 0.95)
    fairness_metrics.append(BiasMetric(
        metric_name="Calibration",
        value=round(calibration, 3),
        threshold=0.85,
        status="pass" if calibration >= 0.85 else "warning" if calibration >= 0.75 else "fail",
        description="Predicted probabilities match actual outcomes across groups"
    ))
    
    # Generate historical trends (if requested)
    historical_trends = []
    if include_historical:
        base_date = datetime.now()
        
        for days_back in range(90, 0, -10):  # Last 90 days, every 10 days
            date = (base_date - timedelta(days=days_back)).strftime("%Y-%m-%d")
            
            for demo in demographics:
                # Simulate improving trend over time
                trend_improvement = (90 - days_back) / 90 * 0.15  # Gradual improvement
                base_parity = 0.75
                parity = min(0.95, base_parity + trend_improvement + np.random.uniform(-0.05, 0.05))
                fpr = 0.15 - (trend_improvement * 0.5)  # Decreasing FPR over time
                
                historical_trends.append(HistoricalBiasTrend(
                    date=date,
                    demographic_group=demo["group"],
                    parity_ratio=round(parity, 3),
                    false_positive_rate=round(max(0.05, fpr), 3)
                ))
    
    # Calculate overall fairness score (0-100)
    passing_metrics = sum(1 for m in fairness_metrics if m.status == "pass")
    overall_fairness_score = (passing_metrics / len(fairness_metrics)) * 100
    
    # Generate recommendations
    recommendations = []
    for metric in fairness_metrics:
        if metric.status == "fail":
            recommendations.append(
                f"CRITICAL: {metric.metric_name} below threshold. "
                f"Implement bias mitigation strategies immediately."
            )
        elif metric.status == "warning":
            recommendations.append(
                f"WARNING: {metric.metric_name} needs improvement. "
                f"Monitor closely and consider retraining with balanced data."
            )
    
    if not recommendations:
        recommendations.append("All fairness metrics within acceptable thresholds.")
        recommendations.append("Continue quarterly bias audits to maintain standards.")
    
    recommendations.extend([
        "Ensure diverse training data representation across all demographics",
        "Implement regular community feedback sessions on model predictions",
        "Conduct quarterly external bias audits by independent reviewers"
    ])
    
    # Determine audit status
    if overall_fairness_score >= 80:
        audit_status = "PASSED"
    elif overall_fairness_score >= 60:
        audit_status = "CONDITIONAL PASS"
    else:
        audit_status = "FAILED"
    
    return BiasAnalysisReport(
        analysis_date=datetime.now().isoformat(),
        model_version=model_version,
        overall_fairness_score=round(overall_fairness_score, 1),
        demographic_metrics=demographic_metrics,
        fairness_metrics=fairness_metrics,
        historical_trends=historical_trends,
        recommendations=recommendations,
        audit_status=audit_status,
        next_audit_date=(datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d")
    )


@router.get("/interventions", response_model=List[InterventionImpact])
async def get_bias_interventions():
    """
    Track impact of bias mitigation interventions over time.
    """
    
    interventions = [
        {
            "type": "Data Rebalancing",
            "date": "2024-08-15",
            "before": 0.72,
            "after": 0.88,
            "groups": ["Black", "Hispanic"]
        },
        {
            "type": "Feature Engineering Review",
            "date": "2024-09-01",
            "before": 0.78,
            "after": 0.91,
            "groups": ["Asian"]
        },
        {
            "type": "Threshold Calibration",
            "date": "2024-10-10",
            "before": 0.81,
            "after": 0.93,
            "groups": ["White", "Black", "Hispanic", "Asian"]
        }
    ]
    
    return [
        InterventionImpact(
            intervention_type=i["type"],
            implemented_date=i["date"],
            before_parity=i["before"],
            after_parity=i["after"],
            improvement_percentage=round(((i["after"] - i["before"]) / i["before"]) * 100, 1),
            affected_groups=i["groups"]
        )
        for i in interventions
    ]


@router.get("/disparity-report")
async def get_disparity_report(
    metric_type: str = Query("false_positive_rate", description="Metric to analyze for disparity")
):
    """
    Detailed disparity analysis for a specific metric across demographics.
    """
    
    demographics = ["White", "Black", "Hispanic", "Asian"]
    
    # Generate disparity data
    if metric_type == "false_positive_rate":
        base_rate = 0.12
        rates = {
            "White": round(base_rate * np.random.uniform(0.85, 1.00), 3),
            "Black": round(base_rate * np.random.uniform(1.05, 1.25), 3),
            "Hispanic": round(base_rate * np.random.uniform(0.95, 1.15), 3),
            "Asian": round(base_rate * np.random.uniform(0.80, 0.95), 3)
        }
    elif metric_type == "false_negative_rate":
        base_rate = 0.14
        rates = {
            "White": round(base_rate * np.random.uniform(0.90, 1.05), 3),
            "Black": round(base_rate * np.random.uniform(1.00, 1.20), 3),
            "Hispanic": round(base_rate * np.random.uniform(0.95, 1.10), 3),
            "Asian": round(base_rate * np.random.uniform(0.85, 1.00), 3)
        }
    else:  # accuracy
        base_rate = 0.85
        rates = {
            "White": round(base_rate * np.random.uniform(0.98, 1.02), 3),
            "Black": round(base_rate * np.random.uniform(0.95, 1.00), 3),
            "Hispanic": round(base_rate * np.random.uniform(0.96, 1.01), 3),
            "Asian": round(base_rate * np.random.uniform(0.97, 1.02), 3)
        }
    
    max_rate = max(rates.values())
    min_rate = min(rates.values())
    disparity_ratio = max_rate / min_rate if min_rate > 0 else 0
    
    return {
        "metric_type": metric_type,
        "analysis_date": datetime.now().isoformat(),
        "rates_by_demographic": rates,
        "max_rate": max_rate,
        "min_rate": min_rate,
        "disparity_ratio": round(disparity_ratio, 3),
        "disparity_percentage": round((disparity_ratio - 1) * 100, 1),
        "fairness_threshold": 1.25,  # 80/20 rule (1.25 = 125%)
        "status": "pass" if disparity_ratio <= 1.25 else "fail",
        "interpretation": (
            f"The {metric_type} varies by {round((disparity_ratio - 1) * 100, 1)}% "
            f"across demographic groups. "
            f"{'This is within acceptable fairness bounds.' if disparity_ratio <= 1.25 else 'This exceeds fairness thresholds and requires intervention.'}"
        )
    }


@router.post("/simulate-mitigation")
async def simulate_mitigation(
    strategy: str = Query(..., description="Mitigation strategy to simulate"),
    target_demographic: str = Query(..., description="Demographic group to target")
):
    """
    Simulate the impact of different bias mitigation strategies.
    """
    
    strategies = {
        "rebalance_training_data": {
            "parity_improvement": 0.15,
            "accuracy_impact": -0.02,
            "implementation_time": "2-3 weeks"
        },
        "threshold_adjustment": {
            "parity_improvement": 0.10,
            "accuracy_impact": -0.01,
            "implementation_time": "1 week"
        },
        "feature_engineering": {
            "parity_improvement": 0.12,
            "accuracy_impact": 0.01,
            "implementation_time": "3-4 weeks"
        },
        "adversarial_debiasing": {
            "parity_improvement": 0.18,
            "accuracy_impact": -0.03,
            "implementation_time": "4-5 weeks"
        }
    }
    
    if strategy not in strategies:
        raise HTTPException(status_code=400, detail="Invalid mitigation strategy")
    
    strategy_data = strategies[strategy]
    
    # Current metrics (simulated)
    current_parity = 0.75
    current_accuracy = 0.85
    
    # Projected metrics after intervention
    projected_parity = min(0.98, current_parity + strategy_data["parity_improvement"])
    projected_accuracy = max(0.70, current_accuracy + strategy_data["accuracy_impact"])
    
    return {
        "strategy": strategy,
        "target_demographic": target_demographic,
        "current_metrics": {
            "parity_ratio": current_parity,
            "accuracy": current_accuracy
        },
        "projected_metrics": {
            "parity_ratio": round(projected_parity, 3),
            "accuracy": round(projected_accuracy, 3)
        },
        "improvements": {
            "parity_gain": round(projected_parity - current_parity, 3),
            "accuracy_change": round(projected_accuracy - current_accuracy, 3)
        },
        "implementation_time": strategy_data["implementation_time"],
        "recommendation": (
            f"Implementing {strategy} is expected to improve fairness by "
            f"{round((projected_parity - current_parity) * 100, 1)}% "
            f"with minimal impact on overall accuracy."
        ),
        "risk_level": "low" if abs(strategy_data["accuracy_impact"]) < 0.02 else "medium"
    }

