"""
Analysis Agent - Performs financial analysis and generates insights.
The brain of the audit system.
"""

import os
import json
from typing import Optional
from datetime import datetime
import anthropic
from pydantic import BaseModel

from src.templates.prompts import get_analysis_prompt, get_customer_categorization_prompt


class BusinessContext(BaseModel):
    """Customer's business context for analysis."""
    trade_type: str = "electrician"
    location: str = "Sydney"
    years_in_business: int = 5
    current_rate: float = 95.0
    hours_per_week: int = 50
    revenue_goal: float = 300000.0


class AnalysisResult(BaseModel):
    """Complete analysis output - comprehensive 2026 audit."""
    # Core metrics
    summary: dict
    pricing_audit: dict
    profitability: dict
    quote_analysis: dict
    time_analysis: dict
    action_plan: list
    guarantee_check: dict
    raw_data_summary: str
    api_cost: float = 0.0
    
    # Enhanced 2026 analysis
    data_quality: dict = {}
    business_health_score: dict = {}
    customer_analysis: dict = {}
    cash_flow_insights: dict = {}
    expense_insights: dict = {}
    missing_data: dict = {}
    next_steps: dict = {}


class Analyzer:
    """
    Analyzes extracted financial data and generates actionable insights.
    
    Performs:
    - Pricing audit (vs market benchmarks)
    - Profitability breakdown (by job type, customer)
    - Quote win rate analysis
    - Time efficiency analysis
    - Action plan generation
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY required")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")
        
        # Cost tracking
        self.input_cost_per_1m = 3.00
        self.output_cost_per_1m = 15.00
    
    def analyze(self, extracted_data: dict, context: BusinessContext) -> AnalysisResult:
        """
        Perform full analysis on extracted data.
        
        Args:
            extracted_data: Output from DataExtractor.combine_results()
            context: Business context (trade, location, rates, etc.)
            
        Returns:
            AnalysisResult with all insights and recommendations
        """
        # Prepare data summary for Claude
        data_summary = self._prepare_data_summary(extracted_data)
        
        # Build the analysis prompt
        prompt = get_analysis_prompt(
            data_summary=data_summary,
            trade_type=context.trade_type,
            location=context.location,
            years_in_business=context.years_in_business,
            current_rate=context.current_rate,
            hours_per_week=context.hours_per_week,
            revenue_goal=context.revenue_goal
        )
        
        # Call Claude for analysis
        print("Running analysis with Claude...")
        message = self.client.messages.create(
            model=self.model,
            max_tokens=8192,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        # Track costs
        input_tokens = message.usage.input_tokens
        output_tokens = message.usage.output_tokens
        cost = (input_tokens / 1_000_000 * self.input_cost_per_1m + 
                output_tokens / 1_000_000 * self.output_cost_per_1m)
        
        print(f"Analysis complete. API cost: ${cost:.2f}")
        
        # Parse response
        response_text = message.content[0].text
        
        # Extract JSON from response
        json_str = response_text
        if "```json" in response_text:
            json_str = response_text.split("```json")[1].split("```")[0]
        elif "```" in response_text:
            parts = response_text.split("```")
            if len(parts) >= 2:
                json_str = parts[1]
        
        try:
            analysis = json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"Warning: Failed to parse analysis JSON: {e}")
            print("Response text:", response_text[:1000])
            # Return a partial result
            analysis = self._create_fallback_analysis(extracted_data, context)
        
        # Handle both old and new JSON structures
        guarantee = analysis.get("guarantee_check", {})
        opportunity = analysis.get("opportunity_summary", {})
        
        # Merge opportunity_summary into guarantee_check format
        if opportunity and not guarantee:
            guarantee = {
                'total_opportunity': opportunity.get('total_conservative', opportunity.get('total_best_case', 0)),
                'total_conservative': opportunity.get('total_conservative', 0),
                'total_best_case': opportunity.get('total_best_case', 0),
                'meets_10k_guarantee': opportunity.get('meets_10k_guarantee', False),
                'confidence': opportunity.get('confidence_level', 'medium'),
                'key_assumptions': opportunity.get('key_assumptions', [])
            }
        
        # If still empty, calculate from action plan
        if not guarantee.get('total_opportunity'):
            action_plan = analysis.get("action_plan", [])
            total = sum(
                a.get('impact_conservative', a.get('impact_annual', 0)) 
                for a in action_plan
            )
            guarantee = {
                'total_opportunity': total,
                'meets_10k_guarantee': total >= 10000,
                'confidence': 'medium'
            }
        
        return AnalysisResult(
            # Core analysis
            summary=analysis.get("summary", {}),
            pricing_audit=analysis.get("pricing_audit", {}),
            profitability=self._normalize_profitability(analysis),
            quote_analysis=analysis.get("quote_analysis", {}),
            time_analysis=analysis.get("time_analysis", {}),
            action_plan=analysis.get("action_plan", []),
            guarantee_check=guarantee,
            raw_data_summary=data_summary,
            api_cost=cost,
            
            # Enhanced 2026 analysis
            data_quality=analysis.get("data_quality", {}),
            business_health_score=analysis.get("business_health_score", {}),
            customer_analysis=analysis.get("customer_analysis", {}),
            cash_flow_insights=analysis.get("cash_flow_insights", {}),
            expense_insights=analysis.get("expense_insights", {}),
            missing_data=analysis.get("missing_data", {}),
            next_steps=analysis.get("next_steps", {})
        )
    
    def _normalize_profitability(self, analysis: dict) -> dict:
        """Convert job_analysis array to profitability dict format."""
        profitability = analysis.get("profitability", {})
        
        # If it's already a dict with the right structure, return it
        if isinstance(profitability, dict) and profitability:
            return profitability
        
        # If job_analysis is an array, convert it
        job_analysis = analysis.get("job_analysis", [])
        if isinstance(job_analysis, list):
            return {
                "by_job_type": job_analysis,
                "by_customer": analysis.get("customer_analysis", {}).get("top_customers", []),
                "loss_makers": [],
                "high_margin_opportunities": []
            }
        
        # Fallback
        return {"by_job_type": [], "by_customer": [], "loss_makers": [], "high_margin_opportunities": []}
    
    def _prepare_data_summary(self, data: dict) -> str:
        """
        Prepare a text summary of the extracted data for Claude.
        """
        summary_parts = []
        
        # Basic stats
        s = data['summary']
        summary_parts.append(f"""
## DATA SUMMARY
- Files processed: {s['total_files_processed']}
- Total transactions: {s['total_transactions']}
- Total revenue: ${s['total_revenue']:,.2f}
- Total expenses: ${s['total_expenses']:,.2f}
- Gross profit: ${s['gross_profit']:,.2f}
- Gross margin: {(s['gross_profit'] / s['total_revenue'] * 100) if s['total_revenue'] > 0 else 0:.1f}%
""")
        
        # Revenue breakdown
        revenue = data['revenue_transactions']
        if revenue:
            summary_parts.append("\n## REVENUE TRANSACTIONS (sample of up to 50)")
            # Group by category
            by_category = {}
            for t in revenue:
                cat = t.get('category', 'other')
                if cat not in by_category:
                    by_category[cat] = {'count': 0, 'total': 0, 'transactions': []}
                by_category[cat]['count'] += 1
                by_category[cat]['total'] += t['amount']
                if len(by_category[cat]['transactions']) < 10:
                    by_category[cat]['transactions'].append(t)
            
            for cat, info in sorted(by_category.items(), key=lambda x: -x[1]['total']):
                summary_parts.append(f"\n### {cat.upper()}: {info['count']} jobs, ${info['total']:,.2f}")
                for t in info['transactions'][:5]:
                    summary_parts.append(f"  - {t['date']}: {t['description'][:50]} - ${t['amount']:,.2f}")
        
        # Expense breakdown
        expenses = data['expense_transactions']
        if expenses:
            summary_parts.append("\n## EXPENSE TRANSACTIONS (by category)")
            by_category = {}
            for t in expenses:
                cat = t.get('category', 'other')
                if cat not in by_category:
                    by_category[cat] = {'count': 0, 'total': 0}
                by_category[cat]['count'] += 1
                by_category[cat]['total'] += t['amount']
            
            for cat, info in sorted(by_category.items(), key=lambda x: -x[1]['total']):
                summary_parts.append(f"  - {cat}: {info['count']} items, ${info['total']:,.2f}")
        
        # Customer analysis
        if revenue:
            summary_parts.append("\n## TOP CUSTOMERS (by revenue)")
            by_customer = {}
            for t in revenue:
                cust = t.get('customer_or_vendor', 'Unknown')
                if cust not in by_customer:
                    by_customer[cust] = {'count': 0, 'total': 0}
                by_customer[cust]['count'] += 1
                by_customer[cust]['total'] += t['amount']
            
            for cust, info in sorted(by_customer.items(), key=lambda x: -x[1]['total'])[:20]:
                summary_parts.append(f"  - {cust}: {info['count']} jobs, ${info['total']:,.2f}")
        
        return "\n".join(summary_parts)
    
    def _create_fallback_analysis(self, data: dict, context: BusinessContext) -> dict:
        """
        Create a basic analysis if Claude response parsing fails.
        """
        s = data['summary']
        
        # Basic calculations
        estimated_hours = context.hours_per_week * 48  # 48 working weeks
        billable_ratio = 0.6  # Assume 60% billable
        billable_hours = estimated_hours * billable_ratio
        
        effective_rate = s['total_revenue'] / billable_hours if billable_hours > 0 else 0
        profit_margin = s['gross_profit'] / s['total_revenue'] if s['total_revenue'] > 0 else 0
        
        # Market rate comparison (simplified)
        market_rates = {
            'electrician': 115,
            'plumber': 110,
            'carpenter': 95,
            'hvac': 110,
            'builder': 90
        }
        market_rate = market_rates.get(context.trade_type.lower(), 100)
        
        rate_gap = market_rate - context.current_rate
        rate_increase_impact = rate_gap * billable_hours
        
        return {
            "summary": {
                "total_revenue_analyzed": s['total_revenue'],
                "total_expenses_analyzed": s['total_expenses'],
                "effective_hourly_rate": effective_rate,
                "market_rate_comparison": f"{(context.current_rate / market_rate - 1) * 100:+.1f}% vs ${market_rate}/hr benchmark",
                "profit_margin": profit_margin,
                "biggest_profit_leak": "Rate appears below market benchmark" if rate_gap > 0 else "Unknown - manual review needed",
                "total_opportunity_identified": max(rate_increase_impact, 10000)
            },
            "pricing_audit": {
                "current_rate": context.current_rate,
                "recommended_rate": market_rate,
                "rate_increase_impact": rate_increase_impact
            },
            "profitability": {
                "by_job_type": [],
                "by_customer": [],
                "note": "Detailed breakdown requires manual review"
            },
            "quote_analysis": {
                "note": "Quote data not detected - requires manual review"
            },
            "time_analysis": {
                "billable_percentage": billable_ratio * 100,
                "estimated_billable_hours": billable_hours
            },
            "action_plan": [
                {
                    "priority": 1,
                    "action": f"Increase hourly rate from ${context.current_rate} to ${market_rate}",
                    "effort": "low",
                    "impact_annual": rate_increase_impact,
                    "timeline": "this_week",
                    "how": "Update quote templates, apply to new customers immediately, phase in with existing customers over 60 days"
                },
                {
                    "priority": 2,
                    "action": "Add/increase call-out fee to $95",
                    "effort": "low",
                    "impact_annual": 95 * 150,  # Assume 150 call-outs per year
                    "timeline": "this_week",
                    "how": "Add to all quotes: 'Call-out fee: $95 (includes first 30 mins)'"
                },
                {
                    "priority": 3,
                    "action": "Review material markup - should be 25-35%",
                    "effort": "medium",
                    "impact_annual": s['total_revenue'] * 0.05,  # Assume 5% improvement possible
                    "timeline": "this_month",
                    "how": "Audit last 10 jobs for actual material costs vs charged"
                }
            ],
            "guarantee_check": {
                "total_opportunity": max(rate_increase_impact, 10000),
                "meets_10k_guarantee": True,
                "confidence": "medium",
                "note": "Fallback analysis used - recommend manual review"
            }
        }
    
    def categorize_customers(self, extracted_data: dict) -> list[dict]:
        """
        Categorize customers into A/B/C/Fire grades.
        
        Returns list of customer grades with recommendations.
        """
        revenue = extracted_data['revenue_transactions']
        
        # Group by customer
        by_customer = {}
        for t in revenue:
            cust = t.get('customer_or_vendor', 'Unknown')
            if cust not in by_customer:
                by_customer[cust] = []
            by_customer[cust].append(t)
        
        results = []
        
        for customer, transactions in by_customer.items():
            if customer == 'Unknown' or len(transactions) < 2:
                continue
            
            # Use Claude to categorize
            trans_summary = "\n".join([
                f"- {t['date']}: {t['description'][:40]} - ${t['amount']:.2f} ({t['status']})"
                for t in transactions[:20]
            ])
            
            prompt = get_customer_categorization_prompt(
                customer_name=customer,
                transactions=trans_summary
            )
            
            message = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = message.content[0].text
            
            # Parse response
            try:
                if "```json" in response_text:
                    json_str = response_text.split("```json")[1].split("```")[0]
                elif "```" in response_text:
                    json_str = response_text.split("```")[1].split("```")[0]
                else:
                    json_str = response_text
                
                grade_info = json.loads(json_str)
                results.append(grade_info)
            except (json.JSONDecodeError, IndexError):
                # Simple fallback grading
                total = sum(t['amount'] for t in transactions)
                avg = total / len(transactions)
                
                grade = 'B'
                if total > 10000 or avg > 2000:
                    grade = 'A'
                elif total < 2000 or avg < 500:
                    grade = 'C'
                
                results.append({
                    'customer': customer,
                    'grade': grade,
                    'total_revenue': total,
                    'job_count': len(transactions),
                    'recommendation': 'keep' if grade in ['A', 'B'] else 'review'
                })
        
        return sorted(results, key=lambda x: {'A': 0, 'B': 1, 'C': 2, 'Fire': 3}.get(x.get('grade', 'C'), 2))


# CLI for testing
if __name__ == "__main__":
    import sys
    
    # Test with sample data
    sample_data = {
        'all_transactions': [],
        'revenue_transactions': [
            {'date': '2024-01-15', 'customer_or_vendor': 'Smith Residence', 
             'description': 'Kitchen rewire', 'amount': 2850, 'type': 'revenue', 
             'category': 'residential_electrical', 'status': 'paid'},
            {'date': '2024-01-20', 'customer_or_vendor': 'Jones Property', 
             'description': 'Commercial switchboard upgrade', 'amount': 5200, 'type': 'revenue', 
             'category': 'commercial_electrical', 'status': 'paid'},
        ],
        'expense_transactions': [
            {'date': '2024-01-10', 'customer_or_vendor': 'Electrical Supplies', 
             'description': 'Materials', 'amount': 1200, 'type': 'expense', 
             'category': 'materials', 'status': 'paid'},
        ],
        'summary': {
            'total_files_processed': 3,
            'total_transactions': 50,
            'revenue_count': 35,
            'expense_count': 15,
            'total_revenue': 180000,
            'total_expenses': 95000,
            'gross_profit': 85000,
            'files_needing_review': [],
            'total_extraction_cost': 2.50
        }
    }
    
    context = BusinessContext(
        trade_type="electrician",
        location="Sydney",
        years_in_business=5,
        current_rate=95,
        hours_per_week=50,
        revenue_goal=250000
    )
    
    analyzer = Analyzer()
    result = analyzer.analyze(sample_data, context)
    
    print("\n" + "="*50)
    print("ANALYSIS RESULTS")
    print("="*50)
    print(f"\nTotal opportunity identified: ${result.guarantee_check.get('total_opportunity', 0):,.2f}")
    print(f"Meets $10k guarantee: {result.guarantee_check.get('meets_10k_guarantee', False)}")
    
    print("\n--- TOP ACTIONS ---")
    for i, action in enumerate(result.action_plan[:5], 1):
        print(f"\n{i}. {action.get('action', 'N/A')}")
        print(f"   Impact: ${action.get('impact_annual', 0):,.2f}/year")
        print(f"   Effort: {action.get('effort', 'N/A')}")
        print(f"   Timeline: {action.get('timeline', 'N/A')}")

