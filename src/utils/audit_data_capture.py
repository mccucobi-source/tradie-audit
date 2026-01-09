"""
Audit Data Capture - Captures structured data from each audit for agent development.

Every audit tells you:
1. What backend problems tradies actually have
2. Which pain points are most common
3. What agents to build (and in what order)

After 50 audits, you'll know EXACTLY what product to build.
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
import uuid


class AuditDataCapture:
    """
    Captures and stores structured data from each audit.
    Used to identify patterns and inform agent development.
    """
    
    def __init__(self, storage_path: str = "./data/audit_insights"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.insights_file = self.storage_path / "aggregated_insights.json"
    
    def capture_audit(
        self,
        audit_id: str,
        business_profile: Dict[str, Any],
        analysis_result: Any,  # AnalysisResult
        context: Any  # BusinessContext
    ) -> Dict[str, Any]:
        """
        Capture structured data from a completed audit.
        
        Returns the captured data object.
        """
        # Generate unique ID if not provided
        if not audit_id:
            audit_id = f"BRC-{context.location[:3].upper()}-{context.trade_type[:4].upper()}-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        
        # Extract pain points from the audit
        pain_points = self._identify_pain_points(analysis_result, context)
        
        # Score agent opportunities
        agent_opportunities = self._score_agent_opportunities(pain_points, analysis_result)
        
        # Extract financial metrics
        financial_metrics = self._extract_financial_metrics(analysis_result, context)
        
        # Compile the captured data
        captured_data = {
            "audit_id": audit_id,
            "captured_at": datetime.now().isoformat(),
            "business_profile": {
                "trade": context.trade_type,
                "location": context.location,
                "years_in_business": context.years_in_business,
                "stated_rate": context.current_rate,
                "hours_per_week": context.hours_per_week,
                "revenue_goal": context.revenue_goal
            },
            "financial_metrics": financial_metrics,
            "pain_points": pain_points,
            "agent_opportunities": agent_opportunities,
            "backend_problems": analysis_result.backend_problems if hasattr(analysis_result, 'backend_problems') else [],
            "data_quality_score": analysis_result.data_quality.get('score', 5) if analysis_result.data_quality else 5
        }
        
        # Save individual audit data
        self._save_audit_data(audit_id, captured_data)
        
        # Update aggregated insights
        self._update_aggregated_insights(captured_data)
        
        return captured_data
    
    def _identify_pain_points(self, analysis: Any, context: Any) -> List[Dict[str, Any]]:
        """Identify operational pain points from the audit."""
        pain_points = []
        
        # 1. Quoting volume
        summary = analysis.summary or {}
        total_jobs = summary.get('total_jobs', summary.get('total_transactions', 0))
        if total_jobs and total_jobs > 50:
            pain_points.append({
                "category": "quoting",
                "indicator": "high_quote_volume",
                "metric_value": total_jobs,
                "threshold": 50,
                "severity": "high" if total_jobs > 100 else "medium",
                "estimated_time_cost_hours": total_jobs * 0.5,  # 30 min per quote
                "estimated_dollar_cost": total_jobs * 0.5 * 150,  # at $150/hr
                "notes": f"Generating {total_jobs} quotes/year manually"
            })
        
        # 2. No call-out fee
        pricing = analysis.pricing_audit or {}
        callout_current = pricing.get('call_out_fee_current', 0)
        if not callout_current or callout_current == 0:
            callout_impact = pricing.get('call_out_impact', 5000)
            pain_points.append({
                "category": "pricing",
                "indicator": "no_callout_fee",
                "metric_value": 0,
                "severity": "high",
                "estimated_dollar_cost": callout_impact,
                "notes": "Missing call-out fee revenue"
            })
        
        # 3. Underpricing
        effective_rate = summary.get('calculated_effective_rate', context.current_rate)
        market_mid = pricing.get('market_mid', context.current_rate + 20)
        rate_gap_pct = ((market_mid - effective_rate) / market_mid * 100) if market_mid > 0 else 0
        if rate_gap_pct > 10:
            pain_points.append({
                "category": "pricing",
                "indicator": "underpricing",
                "metric_value": rate_gap_pct,
                "threshold": 10,
                "severity": "high" if rate_gap_pct > 20 else "medium",
                "notes": f"Rate is {rate_gap_pct:.1f}% below market average"
            })
        
        # 4. Customer concentration
        customer_analysis = analysis.customer_analysis or {}
        top_customers = customer_analysis.get('top_customers', [])
        if top_customers:
            total_revenue = summary.get('total_revenue_analyzed', 1)
            top_4_revenue = sum(c.get('total_revenue', 0) for c in top_customers[:4])
            top_4_pct = (top_4_revenue / total_revenue * 100) if total_revenue > 0 else 0
            if top_4_pct > 40:
                pain_points.append({
                    "category": "customer_concentration",
                    "indicator": "high_concentration",
                    "metric_value": top_4_pct,
                    "threshold": 40,
                    "severity": "high" if top_4_pct > 60 else "medium",
                    "notes": f"Top 4 customers = {top_4_pct:.0f}% of revenue"
                })
        
        # 5. Cash flow issues
        cash_flow = analysis.cash_flow_insights or {}
        if cash_flow.get('cash_flow_risks'):
            pain_points.append({
                "category": "cash_flow",
                "indicator": "cash_flow_risks",
                "severity": "medium",
                "notes": "; ".join(cash_flow.get('cash_flow_risks', [])[:3])
            })
        
        # 6. Too many job types
        profitability = analysis.profitability or {}
        job_types = profitability.get('by_job_type', [])
        if len(job_types) > 10:
            pain_points.append({
                "category": "operations",
                "indicator": "job_type_sprawl",
                "metric_value": len(job_types),
                "threshold": 10,
                "severity": "medium",
                "notes": f"Doing {len(job_types)} different job types - consider specializing"
            })
        
        return pain_points
    
    def _score_agent_opportunities(
        self, 
        pain_points: List[Dict], 
        analysis: Any
    ) -> List[Dict[str, Any]]:
        """Score potential agent opportunities based on pain points."""
        opportunities = []
        
        # Map pain points to agent types
        agent_mapping = {
            "quoting": {
                "agent_type": "quoting_agent",
                "description": "Auto-generates quotes from job details",
                "implementation_difficulty": "medium"
            },
            "pricing": {
                "agent_type": "pricing_optimizer_agent",
                "description": "Optimizes pricing based on market data",
                "implementation_difficulty": "low"
            },
            "customer_concentration": {
                "agent_type": "customer_diversification_agent",
                "description": "Automated customer acquisition outreach",
                "implementation_difficulty": "high"
            },
            "cash_flow": {
                "agent_type": "follow_up_agent",
                "description": "Automated payment reminders and follow-ups",
                "implementation_difficulty": "medium"
            },
            "operations": {
                "agent_type": "job_recommendation_agent",
                "description": "Recommends which jobs to take/avoid",
                "implementation_difficulty": "medium"
            }
        }
        
        for pain in pain_points:
            category = pain.get("category", "")
            if category in agent_mapping:
                mapping = agent_mapping[category]
                
                # Calculate priority score (1-10)
                severity_score = {"high": 9, "medium": 6, "low": 3}.get(pain.get("severity", "medium"), 5)
                
                # Estimate value
                estimated_value = pain.get("estimated_dollar_cost", 5000)
                if not estimated_value:
                    estimated_value = 5000  # Default
                
                opportunities.append({
                    "agent_type": mapping["agent_type"],
                    "description": mapping["description"],
                    "priority_score": severity_score,
                    "estimated_value": estimated_value,
                    "implementation_difficulty": mapping["implementation_difficulty"],
                    "triggered_by": pain.get("indicator", ""),
                    "willingness_to_pay_score": min(10, int(estimated_value / 1000))
                })
        
        # Sort by priority score
        opportunities.sort(key=lambda x: -x["priority_score"])
        
        return opportunities
    
    def _extract_financial_metrics(self, analysis: Any, context: Any) -> Dict[str, Any]:
        """Extract key financial metrics for benchmarking."""
        summary = analysis.summary or {}
        pricing = analysis.pricing_audit or {}
        guarantee = analysis.guarantee_check or {}
        
        return {
            "total_revenue_analyzed": summary.get("total_revenue_analyzed", 0),
            "total_expenses_analyzed": summary.get("total_expenses_analyzed", 0),
            "gross_profit": summary.get("gross_profit", 0),
            "gross_margin": summary.get("gross_margin", 0),
            "effective_rate": summary.get("calculated_effective_rate", context.current_rate),
            "stated_rate": context.current_rate,
            "rate_gap_pct": summary.get("rate_gap_percentage", 0),
            "market_rate_mid": pricing.get("market_mid", 0),
            "total_opportunity_found": guarantee.get("total_opportunity", guarantee.get("total_conservative", 0)),
            "meets_guarantee": guarantee.get("meets_10k_guarantee", False)
        }
    
    def _save_audit_data(self, audit_id: str, data: Dict) -> None:
        """Save individual audit data to file."""
        audit_file = self.storage_path / f"{audit_id}.json"
        with open(audit_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def _update_aggregated_insights(self, new_data: Dict) -> None:
        """Update aggregated insights with new audit data."""
        # Load existing insights
        insights = self._load_aggregated_insights()
        
        # Update counts
        insights["total_audits"] += 1
        insights["last_updated"] = datetime.now().isoformat()
        
        # Track by trade
        trade = new_data["business_profile"]["trade"]
        if trade not in insights["by_trade"]:
            insights["by_trade"][trade] = {"count": 0, "total_opportunity": 0}
        insights["by_trade"][trade]["count"] += 1
        insights["by_trade"][trade]["total_opportunity"] += new_data["financial_metrics"].get("total_opportunity_found", 0)
        
        # Track pain point frequency
        for pain in new_data.get("pain_points", []):
            indicator = pain.get("indicator", "unknown")
            if indicator not in insights["pain_point_frequency"]:
                insights["pain_point_frequency"][indicator] = 0
            insights["pain_point_frequency"][indicator] += 1
        
        # Track agent opportunity scores
        for opp in new_data.get("agent_opportunities", []):
            agent_type = opp.get("agent_type", "unknown")
            if agent_type not in insights["agent_opportunity_scores"]:
                insights["agent_opportunity_scores"][agent_type] = {
                    "count": 0,
                    "total_value": 0,
                    "total_priority": 0
                }
            insights["agent_opportunity_scores"][agent_type]["count"] += 1
            insights["agent_opportunity_scores"][agent_type]["total_value"] += opp.get("estimated_value", 0)
            insights["agent_opportunity_scores"][agent_type]["total_priority"] += opp.get("priority_score", 0)
        
        # Save updated insights
        with open(self.insights_file, 'w') as f:
            json.dump(insights, f, indent=2)
    
    def _load_aggregated_insights(self) -> Dict:
        """Load aggregated insights from file."""
        if self.insights_file.exists():
            with open(self.insights_file, 'r') as f:
                return json.load(f)
        
        return {
            "total_audits": 0,
            "last_updated": None,
            "by_trade": {},
            "by_location": {},
            "pain_point_frequency": {},
            "agent_opportunity_scores": {},
            "financial_benchmarks": {
                "effective_rates": [],
                "opportunity_amounts": []
            }
        }
    
    def get_insights_summary(self) -> Dict[str, Any]:
        """Get a summary of all captured insights."""
        insights = self._load_aggregated_insights()
        
        if insights["total_audits"] == 0:
            return {"message": "No audits captured yet. Run some audits to build insights."}
        
        # Calculate top pain points
        sorted_pains = sorted(
            insights["pain_point_frequency"].items(),
            key=lambda x: -x[1]
        )
        
        # Calculate agent priorities
        agent_priorities = []
        for agent_type, data in insights["agent_opportunity_scores"].items():
            if data["count"] > 0:
                agent_priorities.append({
                    "agent_type": agent_type,
                    "occurrence_rate": data["count"] / insights["total_audits"] * 100,
                    "avg_value": data["total_value"] / data["count"],
                    "avg_priority": data["total_priority"] / data["count"]
                })
        agent_priorities.sort(key=lambda x: -x["occurrence_rate"])
        
        return {
            "total_audits": insights["total_audits"],
            "last_updated": insights["last_updated"],
            "top_pain_points": [
                {
                    "indicator": p[0],
                    "count": p[1],
                    "occurrence_rate": p[1] / insights["total_audits"] * 100
                }
                for p in sorted_pains[:5]
            ],
            "agent_build_priority": agent_priorities[:5],
            "by_trade": insights["by_trade"],
            "recommendation": self._get_build_recommendation(agent_priorities)
        }
    
    def _get_build_recommendation(self, agent_priorities: List[Dict]) -> str:
        """Get recommendation for which agent to build first."""
        if not agent_priorities:
            return "Need more audits to make a recommendation. Target: 10+ audits."
        
        if len(agent_priorities) < 3:
            return f"Consider building {agent_priorities[0]['agent_type']} first (found in {agent_priorities[0]['occurrence_rate']:.0f}% of audits)."
        
        top = agent_priorities[0]
        return (
            f"BUILD FIRST: {top['agent_type']} - "
            f"Found in {top['occurrence_rate']:.0f}% of audits, "
            f"avg value ${top['avg_value']:,.0f}/year"
        )


# Singleton instance
_capture = None

def get_data_capture() -> AuditDataCapture:
    """Get or create the data capture singleton."""
    global _capture
    if _capture is None:
        _capture = AuditDataCapture()
    return _capture


def capture_audit_data(
    audit_id: str,
    analysis_result: Any,
    context: Any
) -> Dict[str, Any]:
    """Convenience function to capture audit data."""
    return get_data_capture().capture_audit(
        audit_id=audit_id,
        business_profile={},  # Will be populated from context
        analysis_result=analysis_result,
        context=context
    )
