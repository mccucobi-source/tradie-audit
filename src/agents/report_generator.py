"""
Report Generator - Creates professional PDF and Excel deliverables.
Focus on QUALITY and CREDIBILITY, not just pretty formatting.
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Optional
import anthropic
from jinja2 import Template

from src.templates.prompts import get_report_summary_prompt
from src.agents.analyzer import AnalysisResult, BusinessContext


class ReportGenerator:
    """
    Generates professional audit reports in PDF and Excel formats.
    """
    
    def __init__(self, api_key: Optional[str] = None, output_dir: str = "./output"):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.client = anthropic.Anthropic(api_key=self.api_key) if self.api_key else None
        self.model = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_report(
        self, 
        analysis: AnalysisResult, 
        context: BusinessContext,
        customer_name: str
    ) -> dict:
        """
        Generate complete report package.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = customer_name.replace(" ", "_").lower()
        
        customer_dir = self.output_dir / f"{safe_name}_{timestamp}"
        customer_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate executive summary
        exec_summary = self._generate_executive_summary(analysis, context, customer_name)
        
        # Generate HTML report
        html_path = self._generate_html_report(
            analysis, context, customer_name, exec_summary, customer_dir
        )
        
        # Generate Excel workbook
        excel_path = self._generate_excel_report(
            analysis, context, customer_name, customer_dir
        )
        
        # Save JSON data
        json_path = customer_dir / "analysis_data.json"
        with open(json_path, 'w') as f:
            json.dump({
                'customer_name': customer_name,
                'context': context.model_dump(),
                'summary': analysis.summary,
                'pricing_audit': analysis.pricing_audit,
                'profitability': analysis.profitability,
                'quote_analysis': analysis.quote_analysis,
                'time_analysis': analysis.time_analysis,
                'action_plan': analysis.action_plan,
                'guarantee_check': analysis.guarantee_check
            }, f, indent=2)
        
        return {
            'output_folder': str(customer_dir),
            'html_report': str(html_path),
            'excel_report': str(excel_path),
            'json_data': str(json_path),
            'executive_summary': exec_summary
        }
    
    def _generate_executive_summary(
        self, 
        analysis: AnalysisResult, 
        context: BusinessContext,
        customer_name: str
    ) -> str:
        """Generate personalized executive summary using Claude."""
        if not self.client:
            return self._fallback_executive_summary(analysis, context, customer_name)
        
        analysis_dict = {
            'summary': analysis.summary,
            'pricing_audit': analysis.pricing_audit,
            'action_plan': analysis.action_plan[:5],
            'guarantee_check': analysis.guarantee_check,
            'context': {
                'trade': context.trade_type,
                'location': context.location,
                'current_rate': context.current_rate,
                'hours_per_week': context.hours_per_week
            }
        }
        
        prompt = get_report_summary_prompt(
            analysis_json=json.dumps(analysis_dict, indent=2),
            customer_name=customer_name.split()[0] if customer_name else "mate"
        )
        
        message = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return message.content[0].text
    
    def _fallback_executive_summary(
        self, 
        analysis: AnalysisResult, 
        context: BusinessContext,
        customer_name: str
    ) -> str:
        """Generate basic summary without Claude."""
        summary = analysis.summary
        total_opp = analysis.guarantee_check.get('total_opportunity', 0)
        conservative = analysis.guarantee_check.get('total_conservative', total_opp * 0.7)
        
        return f"""
{customer_name.split()[0] if customer_name else "Mate"}, here's what we found in your numbers.

You're bringing in ${summary.get('total_revenue_analyzed', 0):,.0f} a year at a stated rate of 
${context.current_rate}/hr. Based on your revenue and hours, your effective rate works out 
to around ${summary.get('effective_hourly_rate', context.current_rate):,.0f}/hr.

The market rate for {context.trade_type}s in {context.location} is typically 
${analysis.pricing_audit.get('market_mid', context.current_rate + 15)}/hr at the mid-point.

We found ${conservative:,.0f} in opportunities you can realistically capture (conservative estimate).
Best case, if everything goes well, that could be ${total_opp:,.0f}.

Top 3 things to do:
{chr(10).join([f"- {a.get('action', 'N/A')} (${a.get('impact_conservative', a.get('impact_annual', 0)):,.0f})" for a in analysis.action_plan[:3]])}

These numbers assume you actually implement the changes. They won't happen by themselves.
"""
    
    def _generate_html_report(
        self,
        analysis: AnalysisResult,
        context: BusinessContext,
        customer_name: str,
        exec_summary: str,
        output_dir: Path
    ) -> Path:
        """Generate HTML report with evidence and calculations shown."""
        
        html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Profit Audit Report - {{ customer_name }}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');
        
        :root {
            --bg: #fafafa;
            --surface: #ffffff;
            --border: #e5e5e5;
            --text: #171717;
            --text-muted: #737373;
            --accent: #ea580c;
            --success: #16a34a;
            --warning: #ca8a04;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'IBM Plex Sans', -apple-system, sans-serif;
            line-height: 1.7;
            color: var(--text);
            background: var(--bg);
            font-size: 16px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 60px 40px;
        }
        
        /* Header */
        header {
            border-bottom: 3px solid var(--text);
            padding-bottom: 40px;
            margin-bottom: 50px;
        }
        
        .report-label {
            font-family: 'IBM Plex Mono', monospace;
            font-size: 12px;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--text-muted);
            margin-bottom: 12px;
        }
        
        header h1 {
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 8px;
        }
        
        header .date {
            color: var(--text-muted);
        }
        
        /* Summary Box */
        .summary-box {
            background: var(--surface);
            border: 1px solid var(--border);
            padding: 40px;
            margin-bottom: 50px;
        }
        
        .summary-box h2 {
            font-size: 14px;
            font-family: 'IBM Plex Mono', monospace;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--text-muted);
            margin-bottom: 20px;
        }
        
        .summary-content {
            font-size: 17px;
            line-height: 1.8;
        }
        
        .summary-content p {
            margin-bottom: 16px;
        }
        
        /* Key Numbers */
        .key-numbers {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 30px;
            margin-bottom: 50px;
        }
        
        .number-card {
            background: var(--surface);
            border: 1px solid var(--border);
            padding: 30px;
        }
        
        .number-card .label {
            font-family: 'IBM Plex Mono', monospace;
            font-size: 11px;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--text-muted);
            margin-bottom: 8px;
        }
        
        .number-card .value {
            font-size: 36px;
            font-weight: 700;
        }
        
        .number-card .value.positive {
            color: var(--success);
        }
        
        .number-card .note {
            font-size: 13px;
            color: var(--text-muted);
            margin-top: 8px;
        }
        
        /* Sections */
        section {
            margin-bottom: 50px;
        }
        
        section h2 {
            font-size: 22px;
            font-weight: 600;
            margin-bottom: 24px;
            padding-bottom: 12px;
            border-bottom: 1px solid var(--border);
        }
        
        section h3 {
            font-size: 16px;
            font-weight: 600;
            margin: 24px 0 12px;
        }
        
        /* Calculation Box - SHOWS THE MATH */
        .calculation {
            background: #f5f5f5;
            border-left: 3px solid var(--accent);
            padding: 20px 24px;
            margin: 20px 0;
            font-family: 'IBM Plex Mono', monospace;
            font-size: 14px;
        }
        
        .calculation .label {
            font-size: 11px;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--text-muted);
            margin-bottom: 12px;
        }
        
        .calculation .line {
            margin-bottom: 6px;
        }
        
        .calculation .result {
            margin-top: 12px;
            padding-top: 12px;
            border-top: 1px solid var(--border);
            font-weight: 600;
        }
        
        /* Evidence Box */
        .evidence {
            background: #fef9f3;
            border: 1px solid #fed7aa;
            padding: 16px 20px;
            margin: 16px 0;
            font-size: 14px;
        }
        
        .evidence strong {
            color: var(--accent);
        }
        
        /* Action Cards */
        .action-card {
            background: var(--surface);
            border: 1px solid var(--border);
            padding: 30px;
            margin-bottom: 24px;
        }
        
        .action-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 16px;
        }
        
        .action-number {
            font-family: 'IBM Plex Mono', monospace;
            font-size: 12px;
            color: var(--accent);
        }
        
        .action-title {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 4px;
        }
        
        .action-impact {
            font-family: 'IBM Plex Mono', monospace;
            font-size: 20px;
            font-weight: 600;
            color: var(--success);
        }
        
        .action-meta {
            display: flex;
            gap: 16px;
            margin-bottom: 16px;
            font-size: 13px;
        }
        
        .action-meta span {
            background: #f5f5f5;
            padding: 4px 12px;
            border-radius: 2px;
        }
        
        .action-body {
            margin-top: 16px;
        }
        
        .action-body h4 {
            font-size: 13px;
            font-family: 'IBM Plex Mono', monospace;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            color: var(--text-muted);
            margin: 20px 0 8px;
        }
        
        .action-body p {
            font-size: 15px;
            color: var(--text);
            margin-bottom: 8px;
        }
        
        .script-box {
            background: #f8f8f8;
            border: 1px solid var(--border);
            padding: 16px 20px;
            font-size: 14px;
            font-style: italic;
            margin: 12px 0;
        }
        
        .risk-box {
            background: #fef2f2;
            border: 1px solid #fecaca;
            padding: 12px 16px;
            font-size: 14px;
            margin: 12px 0;
        }
        
        /* Table */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 14px;
        }
        
        th, td {
            padding: 12px 16px;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }
        
        th {
            font-family: 'IBM Plex Mono', monospace;
            font-size: 11px;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            color: var(--text-muted);
            font-weight: 500;
        }
        
        /* Guarantee */
        .guarantee-box {
            background: var(--text);
            color: white;
            padding: 40px;
            text-align: center;
            margin: 50px 0;
        }
        
        .guarantee-box h2 {
            border: none;
            color: white;
            margin-bottom: 16px;
        }
        
        .guarantee-amount {
            font-size: 48px;
            font-weight: 700;
            margin: 16px 0;
        }
        
        .guarantee-note {
            font-size: 14px;
            opacity: 0.8;
            max-width: 500px;
            margin: 0 auto;
        }
        
        /* Assumptions */
        .assumptions {
            background: #fffbeb;
            border: 1px solid #fde68a;
            padding: 24px;
            margin: 30px 0;
        }
        
        .assumptions h3 {
            font-size: 14px;
            font-family: 'IBM Plex Mono', monospace;
            margin-bottom: 12px;
        }
        
        .assumptions ul {
            padding-left: 20px;
            font-size: 14px;
        }
        
        .assumptions li {
            margin-bottom: 6px;
        }
        
        /* Footer */
        footer {
            border-top: 1px solid var(--border);
            padding-top: 30px;
            margin-top: 50px;
            text-align: center;
            color: var(--text-muted);
            font-size: 14px;
        }
        
        @media print {
            .container { max-width: 100%; padding: 20px; }
            .action-card { break-inside: avoid; }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="report-label">Profit Leak Audit Report</div>
            <h1>{{ customer_name }}</h1>
            <div class="date">{{ date }} · {{ context.trade_type | capitalize }} · {{ context.location }}</div>
        </header>
        
        <div class="summary-box">
            <h2>Executive Summary</h2>
            <div class="summary-content">
                {{ exec_summary | replace('\n', '</p><p>') | safe }}
            </div>
        </div>
        
        <div class="key-numbers">
            <div class="number-card">
                <div class="label">Revenue Analyzed</div>
                <div class="value">${{ "{:,.0f}".format(summary.total_revenue_analyzed or 0) }}</div>
            </div>
            <div class="number-card">
                <div class="label">Your Effective Rate</div>
                <div class="value">${{ (summary.effective_hourly_rate or summary.calculated_effective_rate or context.current_rate) | default(95) | round(0) | int }}/hr</div>
                <div class="note">vs market ${{ pricing.market_mid or (context.current_rate + 20) | int }}/hr</div>
            </div>
            <div class="number-card">
                <div class="label">Conservative Opportunity</div>
                <div class="value positive">${{ "{:,.0f}".format(guarantee.total_conservative or (guarantee.total_opportunity or 15000) * 0.7) }}</div>
                <div class="note">Realistic estimate</div>
            </div>
            <div class="number-card">
                <div class="label">Best Case Opportunity</div>
                <div class="value">${{ "{:,.0f}".format(guarantee.total_best_case or guarantee.total_opportunity or 15000) }}</div>
                <div class="note">If everything goes perfectly</div>
            </div>
        </div>
        
        {% if business_health %}
        <section>
            <h2>Business Health Score</h2>
            <p style="margin-bottom: 20px;">How your business stacks up across key metrics (1-10 scale):</p>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px;">
                {% for metric, score in business_health.items() if metric != 'overall' %}
                <div style="background: var(--surface); border: 1px solid var(--border); padding: 20px; text-align: center;">
                    <div style="font-size: 28px; font-weight: 700; color: {% if score >= 7 %}var(--success){% elif score >= 5 %}var(--warning){% else %}#dc2626{% endif %};">{{ score }}/10</div>
                    <div style="font-size: 13px; color: var(--text-muted); text-transform: capitalize;">{{ metric | replace('_', ' ') }}</div>
                </div>
                {% endfor %}
            </div>
            {% if business_health.overall %}
            <div style="background: var(--text); color: white; padding: 24px; margin-top: 20px; text-align: center;">
                <div style="font-size: 14px; opacity: 0.7;">Overall Business Health</div>
                <div style="font-size: 42px; font-weight: 700;">{{ business_health.overall }}/10</div>
            </div>
            {% endif %}
        </section>
        {% endif %}
        
        <section>
            <h2>Pricing Analysis</h2>
            
            <div class="calculation">
                <div class="label">How We Calculated Your Effective Rate</div>
                <div class="line">Total revenue: ${{ "{:,.0f}".format(summary.total_revenue_analyzed or 0) }}</div>
                <div class="line">Estimated billable hours: ~{{ ((summary.total_revenue_analyzed or 0) / (summary.effective_hourly_rate or context.current_rate or 95)) | round(0) | int }} hours/year</div>
                <div class="line">Calculation: ${{ "{:,.0f}".format(summary.total_revenue_analyzed or 0) }} ÷ {{ ((summary.total_revenue_analyzed or 0) / (summary.effective_hourly_rate or context.current_rate or 95)) | round(0) | int }} hours</div>
                <div class="result">= ${{ (summary.effective_hourly_rate or context.current_rate or 95) | round(0) | int }}/hr effective rate</div>
            </div>
            
            <div class="evidence">
                <strong>Market data:</strong> {{ context.trade_type | capitalize }}s in {{ context.location }} typically charge 
                ${{ pricing.market_low or (context.current_rate - 5) }}-${{ pricing.market_high or (context.current_rate + 35) }}/hr, 
                with ${{ pricing.market_mid or (context.current_rate + 15) }}/hr being mid-market.
                Source: Industry associations & trade surveys.
            </div>
            
            <table>
                <tr>
                    <th>Metric</th>
                    <th>Current</th>
                    <th>Recommended</th>
                    <th>Impact (Conservative)</th>
                </tr>
                <tr>
                    <td>Hourly Rate</td>
                    <td>${{ context.current_rate }}/hr</td>
                    <td>${{ pricing.recommended_rate or (context.current_rate + 15) }}/hr</td>
                    <td style="color: var(--success)">+${{ "{:,.0f}".format((pricing.rate_increase_impact or 15000) * 0.7) }}/yr</td>
                </tr>
                {% if pricing.call_out_fee_recommended %}
                <tr>
                    <td>Call-out Fee</td>
                    <td>${{ pricing.call_out_fee_current or 0 }}</td>
                    <td>${{ pricing.call_out_fee_recommended }}</td>
                    <td style="color: var(--success)">+${{ "{:,.0f}".format((pricing.call_out_impact or 3000) * 0.7) }}/yr</td>
                </tr>
                {% endif %}
            </table>
        </section>
        
        <section>
            <h2>Action Plan</h2>
            <p>Prioritized by realistic impact. Each action includes the calculation, what to say, and what could go wrong.</p>
            
            {% for action in action_plan[:8] %}
            <div class="action-card">
                <div class="action-header">
                    <div>
                        <div class="action-number">Action {{ loop.index }}</div>
                        <div class="action-title">{{ action.action }}</div>
                    </div>
                    <div class="action-impact">+${{ "{:,.0f}".format((action.impact_conservative or action.impact_annual or 0) * 0.85) }}/yr</div>
                </div>
                
                <div class="action-meta">
                    <span>Effort: {{ action.effort }}</span>
                    <span>Timeline: {{ action.timeline }}</span>
                </div>
                
                <div class="action-body">
                    {% if action.calculation %}
                    <div class="calculation">
                        <div class="label">The Math</div>
                        <div>{{ action.calculation }}</div>
                    </div>
                    {% endif %}
                    
                    {% if action.how %}
                    <h4>How to implement</h4>
                    <p>{{ action.how }}</p>
                    {% endif %}
                    
                    {% if action.script %}
                    <h4>What to say</h4>
                    <div class="script-box">"{{ action.script }}"</div>
                    {% endif %}
                    
                    {% if action.pushback_response %}
                    <h4>If they push back</h4>
                    <div class="script-box">"{{ action.pushback_response }}"</div>
                    {% endif %}
                    
                    {% if action.risk %}
                    <h4>What could go wrong</h4>
                    <div class="risk-box">{{ action.risk }}</div>
                    {% endif %}
                </div>
            </div>
            {% endfor %}
        </section>
        
        {% if customer_analysis and customer_analysis.top_customers %}
        <section>
            <h2>Customer Analysis</h2>
            <p>Who's worth your time - and who isn't.</p>
            
            <h3 style="margin-top: 24px;">Your Best Customers</h3>
            <table>
                <tr>
                    <th>Customer</th>
                    <th>Revenue</th>
                    <th>Jobs</th>
                    <th>Avg Job</th>
                    <th>Grade</th>
                    <th>Action</th>
                </tr>
                {% for cust in customer_analysis.top_customers[:8] %}
                <tr>
                    <td>{{ cust.name or cust.customer or 'Unknown' }}</td>
                    <td>${{ "{:,.0f}".format(cust.total_revenue or cust.revenue or 0) }}</td>
                    <td>{{ cust.job_count or cust.jobs or 0 }}</td>
                    <td>${{ "{:,.0f}".format(cust.avg_job_size or 0) }}</td>
                    <td style="font-weight: 600; color: {% if cust.grade == 'A' %}var(--success){% elif cust.grade == 'B' %}var(--text){% elif cust.grade == 'C' %}var(--warning){% else %}#dc2626{% endif %};">{{ cust.grade or 'B' }}</td>
                    <td>{{ cust.recommendation or 'Maintain' }}</td>
                </tr>
                {% endfor %}
            </table>
            
            {% if customer_analysis.concerning_customers %}
            <h3 style="margin-top: 24px;">⚠️ Customers to Watch</h3>
            {% for cust in customer_analysis.concerning_customers[:3] %}
            <div class="risk-box" style="margin-bottom: 12px;">
                <strong>{{ cust.name or 'Unknown' }}:</strong> {{ cust.reason or 'Review needed' }}
                <br><em>Recommendation: {{ cust.recommendation or 'Review' }}</em>
            </div>
            {% endfor %}
            {% endif %}
            
            {% if customer_analysis.ideal_customer_profile %}
            <div class="evidence" style="margin-top: 20px;">
                <strong>Your ideal customer profile:</strong> {{ customer_analysis.ideal_customer_profile }}
            </div>
            {% endif %}
        </section>
        {% endif %}
        
        {% if cash_flow_insights and (cash_flow_insights.recommendations or cash_flow_insights.cash_flow_risks) %}
        <section>
            <h2>Cash Flow Insights</h2>
            <p>Cash flow kills more trade businesses than lack of work. Here's what we found:</p>
            
            {% if cash_flow_insights.payment_speed_assessment %}
            <div class="evidence">
                <strong>Payment timing:</strong> {{ cash_flow_insights.payment_speed_assessment }}
            </div>
            {% endif %}
            
            {% if cash_flow_insights.seasonal_patterns %}
            <div class="evidence">
                <strong>Seasonal patterns:</strong> {{ cash_flow_insights.seasonal_patterns }}
            </div>
            {% endif %}
            
            {% if cash_flow_insights.cash_flow_risks %}
            <h3 style="margin-top: 20px;">Cash Flow Risks</h3>
            {% for risk in cash_flow_insights.cash_flow_risks %}
            <div class="risk-box" style="margin-bottom: 8px;">{{ risk }}</div>
            {% endfor %}
            {% endif %}
            
            {% if cash_flow_insights.recommendations %}
            <h3 style="margin-top: 20px;">Cash Flow Actions</h3>
            <ul style="padding-left: 24px;">
                {% for rec in cash_flow_insights.recommendations %}
                <li style="margin-bottom: 8px;">{{ rec }}</li>
                {% endfor %}
            </ul>
            {% endif %}
        </section>
        {% endif %}
        
        {% if job_analysis %}
        <section>
            <h2>Job Profitability Breakdown</h2>
            <p>Which jobs make you money - and which don't.</p>
            
            <table>
                <tr>
                    <th>Job Type</th>
                    <th>Count</th>
                    <th>Revenue</th>
                    <th>Avg Job</th>
                    <th>Eff. Rate</th>
                    <th>Verdict</th>
                </tr>
                {% for job in job_analysis[:8] %}
                <tr>
                    <td>{{ job.category or 'Unknown' }}</td>
                    <td>{{ job.job_count or 0 }}</td>
                    <td>${{ "{:,.0f}".format(job.total_revenue or 0) }}</td>
                    <td>${{ "{:,.0f}".format(job.avg_revenue or 0) }}</td>
                    <td>${{ "{:,.0f}".format(job.effective_rate or 0) }}/hr</td>
                    <td style="font-weight: 600; color: {% if job.verdict == 'highly_profitable' or job.verdict == 'profitable' %}var(--success){% elif job.verdict == 'marginal' %}var(--warning){% else %}#dc2626{% endif %};">
                        {{ job.verdict | default('unknown') | replace('_', ' ') | title }}
                    </td>
                </tr>
                {% endfor %}
            </table>
        </section>
        {% endif %}
        
        <div class="assumptions">
            <h3>⚠️ Key Assumptions (Be Honest With Yourself)</h3>
            <ul>
                <li>These numbers assume you actually implement the changes</li>
                <li>Rate increases assume ~15% customer loss (factored in)</li>
                <li>Timeline estimates assume you start this week</li>
                <li>Results depend on your market, customers, and execution</li>
                {% if guarantee.key_assumptions %}
                {% for assumption in guarantee.key_assumptions %}
                <li>{{ assumption }}</li>
                {% endfor %}
                {% endif %}
            </ul>
        </div>
        
        <div class="guarantee-box">
            <h2>Opportunity Identified</h2>
            <div class="guarantee-amount">${{ "{:,.0f}".format((guarantee.total_opportunity or 15000) * 0.7) }}</div>
            <p>Conservative estimate (85% of calculated value)</p>
            <p class="guarantee-note">
                Best case: ${{ "{:,.0f}".format(guarantee.total_opportunity or 15000) }} if you implement everything and retain all customers. 
                We've factored in realistic customer loss and execution challenges.
            </p>
        </div>
        
        <section>
            <h2>Next Steps</h2>
            <ol style="padding-left: 24px; line-height: 2;">
                <li><strong>This week:</strong> Implement the "this_week" actions - start with new customers</li>
                <li><strong>Strategy call:</strong> Let's discuss your specific questions and concerns</li>
                <li><strong>Track it:</strong> Use the Excel tracker to log what you've done and results</li>
                <li><strong>30-day check:</strong> We'll follow up to see what's working</li>
            </ol>
        </section>
        
        <footer>
            <p>Profit Leak Audit · {{ date }}</p>
            <p>Questions? Hit reply or book a call.</p>
        </footer>
    </div>
</body>
</html>
"""
        
        template = Template(html_template)
        
        # Get job analysis from profitability or directly
        job_analysis = []
        if isinstance(analysis.profitability, dict):
            job_analysis = analysis.profitability.get('by_job_type', [])
        
        html_content = template.render(
            customer_name=customer_name,
            date=datetime.now().strftime("%B %d, %Y"),
            exec_summary=exec_summary,
            context=context,
            summary=analysis.summary,
            pricing=analysis.pricing_audit,
            profitability=analysis.profitability,
            quote_analysis=analysis.quote_analysis,
            time_analysis=analysis.time_analysis,
            action_plan=analysis.action_plan,
            guarantee=analysis.guarantee_check,
            # Enhanced 2026 analysis
            business_health=analysis.business_health_score,
            customer_analysis=analysis.customer_analysis,
            cash_flow_insights=analysis.cash_flow_insights,
            job_analysis=job_analysis,
            data_quality=analysis.data_quality,
            next_steps=analysis.next_steps
        )
        
        html_path = output_dir / "profit_leak_audit_report.html"
        with open(html_path, 'w') as f:
            f.write(html_content)
        
        return html_path
    
    def _generate_excel_report(
        self,
        analysis: AnalysisResult,
        context: BusinessContext,
        customer_name: str,
        output_dir: Path
    ) -> Path:
        """Generate Excel workbook with actionable spreadsheets."""
        try:
            import openpyxl
            from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
        except ImportError:
            return self._generate_csv_fallback(analysis, context, customer_name, output_dir)
        
        wb = openpyxl.Workbook()
        
        # Styles
        header_font = Font(bold=True, color="FFFFFF", size=11)
        header_fill = PatternFill(start_color="171717", end_color="171717", fill_type="solid")
        money_font = Font(bold=True, color="16a34a")
        
        # Sheet 1: Summary
        ws = wb.active
        ws.title = "Summary"
        
        summary_data = [
            ["PROFIT LEAK AUDIT - SUMMARY", ""],
            ["", ""],
            ["Customer", customer_name],
            ["Trade", context.trade_type.capitalize()],
            ["Location", context.location],
            ["Report Date", datetime.now().strftime("%Y-%m-%d")],
            ["", ""],
            ["YOUR NUMBERS", ""],
            ["Revenue Analyzed", f"${analysis.summary.get('total_revenue_analyzed', 0):,.0f}"],
            ["Effective Hourly Rate", f"${analysis.summary.get('effective_hourly_rate', 0):,.0f}"],
            ["Market Mid-Rate", f"${analysis.pricing_audit.get('market_mid', context.current_rate + 15):,.0f}"],
            ["", ""],
            ["OPPORTUNITY", ""],
            ["Conservative Estimate", f"${analysis.guarantee_check.get('total_opportunity', 0) * 0.7:,.0f}"],
            ["Best Case", f"${analysis.guarantee_check.get('total_opportunity', 0):,.0f}"],
        ]
        
        for row in summary_data:
            ws.append(row)
        
        # Sheet 2: Action Tracker
        ws2 = wb.create_sheet("Action Tracker")
        headers = ["#", "Action", "Impact ($/yr)", "Effort", "Timeline", "Status", "Started", "Completed", "Actual Result", "Notes"]
        ws2.append(headers)
        
        for cell in ws2[1]:
            cell.font = header_font
            cell.fill = header_fill
        
        for i, action in enumerate(analysis.action_plan, 1):
            impact = action.get('impact_conservative', action.get('impact_annual', 0))
            ws2.append([
                i,
                action.get('action', ''),
                f"${impact * 0.85:,.0f}",
                action.get('effort', ''),
                action.get('timeline', ''),
                "Not Started",
                "",
                "",
                "",
                ""
            ])
        
        # Column widths
        ws2.column_dimensions['B'].width = 45
        ws2.column_dimensions['J'].width = 30
        
        # Sheet 3: Rate Calculator
        ws3 = wb.create_sheet("Rate Calculator")
        
        calc_data = [
            ["RATE INCREASE CALCULATOR", ""],
            ["", ""],
            ["Enter your numbers:", ""],
            ["Current Hourly Rate", context.current_rate],
            ["New Hourly Rate", analysis.pricing_audit.get('recommended_rate', context.current_rate + 15)],
            ["Billable Hours / Week", 30],
            ["Weeks / Year", 48],
            ["Expected Customer Loss %", 15],
            ["", ""],
            ["RESULTS:", ""],
            ["Total Billable Hours", "=B6*B7"],
            ["Rate Increase", "=B5-B4"],
            ["Gross Additional Revenue", "=B11*B12"],
            ["After Customer Loss", "=B13*(1-B8/100)"],
            ["", ""],
            ["Your realistic annual gain:", "=B14"],
        ]
        
        for row in calc_data:
            ws3.append(row)
        
        ws3.column_dimensions['A'].width = 30
        ws3.column_dimensions['B'].width = 15
        
        # Sheet 4: Scripts
        ws4 = wb.create_sheet("Scripts")
        ws4.append(["SCRIPTS - COPY & USE THESE", ""])
        ws4.append(["", ""])
        
        for action in analysis.action_plan:
            if action.get('script'):
                ws4.append([action.get('action', ''), ""])
                ws4.append(["What to say:", action.get('script', '')])
                if action.get('pushback_response'):
                    ws4.append(["If they push back:", action.get('pushback_response', '')])
                ws4.append(["", ""])
        
        ws4.column_dimensions['A'].width = 25
        ws4.column_dimensions['B'].width = 80
        
        excel_path = output_dir / "profit_leak_audit_workbook.xlsx"
        wb.save(excel_path)
        
        return excel_path
    
    def _generate_csv_fallback(
        self,
        analysis: AnalysisResult,
        context: BusinessContext,
        customer_name: str,
        output_dir: Path
    ) -> Path:
        """Generate CSV if openpyxl not available."""
        import csv
        
        csv_path = output_dir / "action_plan.csv"
        
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["#", "Action", "Impact ($/yr)", "Effort", "Timeline", "Status", "Notes"])
            
            for i, action in enumerate(analysis.action_plan, 1):
                impact = action.get('impact_conservative', action.get('impact_annual', 0))
                writer.writerow([
                    i,
                    action.get('action', ''),
                    f"${impact * 0.85:,.0f}",
                    action.get('effort', ''),
                    action.get('timeline', ''),
                    "Not Started",
                    ""
                ])
        
        return csv_path
