"""
Claude prompts for the Tradie Audit Agent.
These are the "secret sauce" that make the analysis high-quality.

QUALITY PRINCIPLES:
1. Be CONSERVATIVE with estimates - better to under-promise
2. Show EVIDENCE for every claim - data, not opinions
3. Make it SPECIFIC to their situation - not generic advice
4. Include REALISTIC assumptions - not best-case scenarios
5. Prioritize ACTIONABLE over impressive numbers
6. Reference PROVEN FRAMEWORKS and REAL CASE STUDIES - not generic advice

2026 BUSINESS REALITY FOR TRADIES:
- Rising costs (fuel, insurance, materials up 15-25% since 2023)
- Labor shortage = opportunity for premium pricing
- Digital presence now essential (Google, social proof)
- Cash flow is king - payment terms matter more than ever
- Customers expect instant quotes and communication
- Specialization beats generalization

FRAMEWORKS AVAILABLE:
- growth_frameworks.py: Proven pricing, lead gen, operations, growth tactics
- case_studies.py: Real anonymized case studies showing what works
"""

DATA_EXTRACTION_PROMPT = """You are a financial data extraction specialist for Australian tradie businesses.

Your job is to extract structured transaction data from invoices, bank statements, and quotes.

ANALYZE THE PROVIDED DOCUMENT AND EXTRACT:

For INVOICES/REVENUE:
- Date of invoice
- Customer name (or "Unknown" if not clear)
- Job description/type (be specific: "switchboard upgrade" not just "electrical")
- Total amount (AUD)
- Line items if available (materials, labor breakdown)
- Payment status if indicated
- Hours worked if mentioned
- Job location/suburb if mentioned
- Whether it's residential, commercial, or strata/body corporate

For EXPENSES:
- Date of expense
- Vendor/supplier name
- Description
- Amount (AUD)
- Category (materials, fuel, insurance, tools, subscriptions, subcontractor, vehicle, marketing, software, etc.)
- Is this a recurring expense?

For QUOTES:
- Date of quote
- Customer name
- Job description
- Quoted amount
- Status if known (won/lost/pending)
- If lost, any notes on why

For BANK STATEMENTS:
- Extract EVERY transaction
- Categorize income vs expense
- Flag regular recurring payments (subscriptions, insurance, loan repayments)
- Identify patterns (weekly/monthly cycles)

OUTPUT AS JSON with this structure:
- document_type: "invoice" or "expense" or "quote" or "bank_statement" or "unknown"
- transactions: array of transaction objects
- extraction_notes: any issues or uncertainties
- needs_review: true/false
- patterns_detected: any recurring patterns you notice

Each transaction should have:
- date: "YYYY-MM-DD"
- customer_or_vendor: "Name"
- description: "Job or expense description"
- amount: number
- type: "revenue" or "expense"
- category: one of the categories listed
- subcategory: more specific (e.g., "residential_rewire" under "residential_electrical")
- status: "paid" or "unpaid" or "won" or "lost" or "pending" or "unknown"
- hours_if_mentioned: number or null
- job_type: "residential" or "commercial" or "strata" or "government" or "unknown"
- is_recurring: true/false
- confidence: "high" or "medium" or "low"

RULES:
1. Be conservative - if unsure about a value, mark confidence as "low" and needs_review as true
2. All amounts in AUD
3. Infer job categories where possible (electrical, plumbing, carpentry, etc.)
4. Flag any unusual transactions for human review
5. If a bank statement has many transactions, extract ALL of them
6. Look for hours worked - this is critical for hourly rate analysis
7. Identify repeat customers (same name appearing multiple times)
8. Note any payment delays (invoice date vs payment date if visible)
"""


def get_analysis_prompt(data_summary: str, trade_type: str, location: str, 
                        years_in_business: int, current_rate: float, 
                        hours_per_week: int, revenue_goal: float,
                        market_benchmarks: dict = None,
                        business_context: dict = None) -> str:
    """Generate the comprehensive 2026 Growth Audit prompt with all context."""
    
    # Format benchmark data for inclusion in prompt
    benchmark_section = ""
    if market_benchmarks:
        hourly = market_benchmarks.get("hourly_rate", {})
        callout = market_benchmarks.get("call_out_fee", {})
        benchmark_section = f"""
VERIFIED MARKET BENCHMARKS FOR {trade_type.upper()} IN {location.upper()}:
(Source: service.com.au + industry associations, 200+ data points, HIGH confidence)

Hourly Rates:
- Minimum (25th percentile): ${hourly.get('min', 90)}/hr
- Average (50th percentile): ${hourly.get('average', 110)}/hr  
- Maximum (75th percentile): ${hourly.get('max', 130)}/hr
- Premium (90th percentile): ${hourly.get('premium', hourly.get('max', 130) * 1.15):.0f}/hr

Call-Out Fees:
- Standard: ${callout.get('min', 80)}-${callout.get('max', 130)} (average ${callout.get('average', 95)})

Data Sources: {', '.join([s.get('name', 'Unknown') for s in hourly.get('data_sources', [{'name': 'service.com.au'}])])}
Confidence Level: {hourly.get('confidence', 'MEDIUM')}

USE THESE EXACT BENCHMARKS IN YOUR ANALYSIS. Cite them explicitly.
"""
    
    # Build comprehensive context from onboarding data
    context_section = ""
    if business_context:
        # Lead generation context
        lead_sources = business_context.get('lead_sources', [])
        leads_per_week = business_context.get('leads_per_week', 'Unknown')
        close_rate = business_context.get('close_rate', 0)
        google_rating = business_context.get('google_rating', 'Unknown')
        google_reviews = business_context.get('google_reviews', '0')
        
        # Quoting context
        quote_method = business_context.get('quote_method', 'Unknown')
        quote_time = business_context.get('quote_time', 'Unknown')
        quotes_per_month = business_context.get('quotes_per_month', 'Unknown')
        quote_speed = business_context.get('quote_speed', 'Unknown')
        
        # Operations context
        tools_used = business_context.get('tools_used', [])
        job_tracking = business_context.get('job_tracking', 'Unknown')
        follow_up_method = business_context.get('follow_up_method', 'Unknown')
        biggest_time_waste = business_context.get('biggest_time_waste', 'Unknown')
        
        # Goals context
        hiring_plans = business_context.get('hiring_plans', 'Unknown')
        biggest_frustration = business_context.get('biggest_frustration', '')
        magic_wand = business_context.get('magic_wand', '')
        
        context_section = f"""
## DETAILED BUSINESS CONTEXT FROM INTAKE INTERVIEW

### LEAD GENERATION & MARKETING
- Lead sources: {', '.join(lead_sources) if lead_sources else 'Not specified'}
- Leads per week: {leads_per_week}
- Quote-to-job conversion rate: {close_rate}%
- Google Business rating: {google_rating}
- Number of Google reviews: {google_reviews}

ANALYZE: 
- If conversion rate < 35%, there's a quoting or pricing problem
- If conversion rate > 50%, they may be underpricing
- Google presence is critical in 2026 - less than 20 reviews = invisible online
- Relying on word-of-mouth only = growth ceiling

### QUOTING PROCESS
- How they create quotes: {quote_method}
- Time per quote: {quote_time}
- Quotes sent per month: {quotes_per_month}
- Speed to quote: {quote_speed}

ANALYZE:
- "Mental math + text" = inconsistent pricing, leaving money on table
- Anything over 30 min per quote = major admin burden
- Slower than "same day" response = losing jobs to faster competitors
- Track: (Quotes × Time per quote × Hourly rate) = true cost of quoting

### CURRENT TOOLS & SYSTEMS
- Software used: {', '.join(tools_used) if tools_used else 'None / Paper'}
- Job tracking method: {job_tracking}
- Lead follow-up method: {follow_up_method}
- Biggest time waste: {biggest_time_waste}

ANALYZE:
- "Paper / manual" + "In my head" = operational risk + admin burden
- No job management software = missing data for optimization
- "{follow_up_method}" follow-up approach = {"MAJOR LEAK - losing 30-40% of potential jobs" if "don't" in follow_up_method.lower() else "needs optimization"}
- They said "{biggest_time_waste}" is their biggest time waste - address this DIRECTLY in recommendations

### GOALS & PAIN POINTS
- Team plans: {hiring_plans}
- Their biggest frustration (in their words): "{biggest_frustration}"
- If they had a magic wand: "{magic_wand}"

CRITICAL: The client told us exactly what's bothering them. Your recommendations MUST address their stated frustration first. Then add what the data reveals.
"""

    # Load proven frameworks to inject into prompt
    from src.templates.growth_frameworks import (
        PRICING_TRANSITION_FRAMEWORK,
        CALL_OUT_FEE_FRAMEWORK,
        REVIEW_ACQUISITION_FRAMEWORK,
        LEAD_RESPONSE_FRAMEWORK,
        CUSTOMER_GRADING_FRAMEWORK,
        PAYMENT_TERMS_FRAMEWORK
    )
    from src.templates.case_studies import format_case_study_for_prompt, get_relevant_case_studies

    # Get relevant case studies based on trade
    relevant_cases = get_relevant_case_studies(trade=trade_type)
    case_examples = "\n\n".join([
        format_case_study_for_prompt(case.get("key", ""), sections=["situation", "results", "lessons"])
        for case in relevant_cases[:2]  # Include 2 most relevant
    ]) if relevant_cases else ""

    frameworks_section = f"""
## PROVEN FRAMEWORKS TO REFERENCE IN YOUR ANALYSIS

These are battle-tested strategies from real tradie businesses. Reference these SPECIFICALLY in your recommendations.

### PRICING TRANSITION FRAMEWORK
When recommending rate increases, use this proven 4-step system:
1. Update quote templates immediately (new customers get new rate from day 1)
2. Notify A-grade customers 60 days in advance (personal email/text)
3. Notify B-grade customers 30 days in advance
4. C-grade customers - update on next quote only (okay if they leave)

Expected results: 10-15% customer loss (mostly low-margin C-grade).
A-grade retention: 95%+, B-grade: 85-90%, C-grade: 60-70%

Script for existing customers:
"Hi [Name], just wanted to let you know our rates are moving to $[NEW_RATE]/hr from [date]. This brings us in line with current market rates and ensures we can keep delivering the quality you expect. Happy to chat if you have any questions."

Objection handling:
"Too expensive" → "I understand - rates have definitely increased across the board. This brings us to mid-market for {trade_type} in {location}. Our rate reflects [years] experience, full licensing and insurance, and our guarantee to get it right first time."

### CALL-OUT FEE FRAMEWORK
Only ~60% of tradies charge call-out fees - leaving $3-8k/year on table.

Standard structure:
- Standard hours: $95-$130 (waived if job booked)
- After-hours: $150-$200 (always charged)
- Emergency: $200-$350 (always charged)

Script: "Our call-out fee is $[AMOUNT] which covers travel and on-site assessment. If you go ahead with the work, we'll credit that toward the job cost. Sound fair?"

Customer acceptance: 85%+ accept without question when stated confidently.

Calculation: Call-outs per week × 48 weeks × Fee × 85% acceptance

### REVIEW ACQUISITION FRAMEWORK
Critical facts:
- 76% of tradies have <10 Google reviews
- They're losing 40-60% of Google search leads to competitors with 25+ reviews
- Day 3 SMS has 15-22% response rate (vs 5-8% for Day 7 email)

Proven system:
Send SMS on Day 3 after job completion with direct Google review link:
"Hey [FIRST_NAME], thanks again for letting us [SPECIFIC_THING]. If you're happy with the job, a quick Google review really helps us out: [LINK]. Cheers, [NAME]"

Why Day 3: Not too soon (Day 1), not forgotten (Day 7+). Sweet spot for satisfaction + memory.

Impact: Going from <10 reviews to 25+ reviews = 3-5 additional jobs per month.

### LEAD RESPONSE SPEED FRAMEWORK
Research data (Hipages + ServiceM8):
- Under 2 hours: 21% conversion
- 2-24 hours: 14% conversion
- 24-48 hours: 9% conversion
- Over 48 hours: 5% conversion

First responder wins 60% of the time in competitive markets.

System:
1. Respond within 30 minutes (text or call, not email)
2. Site visit same/next day
3. Quote within 24 hours of site visit
4. Follow-up: Day 1 (quote sent + call), Day 3 (text), Day 7 (final call)

### CUSTOMER GRADING FRAMEWORK (A/B/C/Fire)
Grade customers quarterly to focus energy on profitable relationships:

A-grade (nurture actively):
- High revenue (top 20%)
- Repeat business (3+ jobs/year)
- Pays fast (<7 days)
- Refers others
Action: Priority scheduling, quarterly check-ins, maintain/slight discount for loyalty

B-grade (maintain):
- Decent revenue, occasional repeat, pays normally (7-14 days)
Action: Good service, standard rates

C-grade (deprioritize):
- Low revenue (<$500/year), one-off, slow pay (14-30 days), high effort
Action: Fit around better work, consider minimums, full rate + call-out OR decline

Fire (terminate professionally):
- Chronic slow/no payment (>30 days), abusive, constant scope creep, jobs lose money
Action: Politely decline next request

### PAYMENT TERMS FRAMEWORK
Optimal structure to fix cash flow:
- Under $1,000: Full payment on completion
- $1,000-$5,000: 50% deposit, 50% on completion
- Over $5,000: 30% deposit, 40% at midpoint, 30% completion

Late payment sequence:
- Day 7: Friendly text reminder
- Day 14: Phone call (assume good intent, ask if issue)
- Day 21: Formal email + final notice
- Day 30: Collections or write-off decision

{case_examples}
"""

    return f"""You are an elite business analyst producing a PROFESSIONAL AUDIT REPORT for an Australian tradie.
This is a $797 paid audit - it must feel like a $3,000 consulting engagement.

The tradie will use this report to make real business decisions. Every number must be:
1. TRACEABLE - show exactly where it came from
2. CALCULATED - show the math step by step
3. VERIFIABLE - they can check your sources
4. CONSERVATIVE - use worst-case assumptions

CRITICAL: This is NOT an AI summary. This is a PROFESSIONAL AUDIT with:
- Specific references to their actual invoices and transactions
- Exact calculations shown for every claim
- Market benchmarks cited with sources
- Three-scenario projections (conservative/realistic/optimistic)
- Risk analysis for every recommendation

{benchmark_section}

{context_section}

{frameworks_section}

AUDIT QUALITY STANDARDS:
1. Reference specific transactions: "Invoice #X to Customer Y for $Z shows..."
2. Show all calculations: "Total revenue ($X) ÷ estimated hours (Y) = $Z/hr effective rate"
3. Cite market data: "Sydney electricians average $102.50/hr (source: service.com.au, HIGH confidence)"
4. Use three scenarios: Conservative (15% loss), Realistic (10% loss), Optimistic (5% loss)
5. Be honest about confidence: "HIGH confidence" vs "MEDIUM - estimated from job mix"
6. Identify risks: "This assumes customers accept the increase without shopping around"

2026 MARKET CONTEXT:
- Material costs up 20-30% since 2023
- Insurance premiums up 15-25%
- Fuel costs volatile
- Labor shortage = tradies can command premium rates
- Cash flow problems are the #1 killer of trade businesses

CLIENT DATA TO ANALYZE:
{data_summary}

BUSINESS PROFILE:
- Trade: {trade_type}
- Location: {location}
- Years in business: {years_in_business}
- Stated hourly rate: ${current_rate}/hr
- Weekly hours worked: {hours_per_week}
- Revenue goal: ${revenue_goal}

PERFORM THESE ANALYSES WITH FULL CALCULATION TRANSPARENCY:

## 1. PRICING ANALYSIS (The Foundation)

Step 1: Calculate their ACTUAL effective rate
- Total revenue ÷ estimated billable hours = effective rate
- Show the calculation explicitly
- If hours aren't in data, estimate conservatively (assume 55-60% of total hours are billable)
- Compare stated rate vs effective rate - the gap tells a story

Step 2: Compare to 2026 market DATA (not opinions)
Market rates have increased significantly. Current ranges:
| Trade | Sydney/Melbourne | Brisbane/Perth | Regional | Notes |
|-------|-----------------|----------------|----------|-------|
| Electrician | $115-155/hr | $105-140/hr | $90-125/hr | Higher for Level 2, solar |
| Plumber | $110-145/hr | $100-130/hr | $85-115/hr | Higher for gas, roofing |
| Carpenter | $90-125/hr | $85-115/hr | $75-100/hr | Higher for heritage, custom |
| HVAC | $115-150/hr | $105-135/hr | $90-120/hr | Higher for commercial |
| Builder | $85-115/hr | $80-105/hr | $70-95/hr | Varies hugely by project |

Step 3: Calculate CONSERVATIVE rate increase opportunity
- Don't recommend jumping to top of range
- Recommend mid-range as realistic target
- Assume 10-15% customer loss when calculating net impact
- Show: (New rate - Old rate) × hours × 85% retention = realistic impact

Step 4: Call-out fee analysis
- Most tradies undercharge or don't charge call-out fees
- 2026 benchmarks: $95-130 for metro, $120-180 for after-hours
- Calculate: estimated call-outs × fee = opportunity

## 2. PROFITABILITY BY JOB TYPE (Where's the Real Money?)

For each job category in their data, calculate:
- Count: How many jobs
- Revenue: Total and average per job
- Time estimate: If hours available, or estimate from job sizes
- Effective rate: Revenue ÷ estimated hours
- Material ratio: If visible, what % went to materials
- Verdict: Highly profitable / Profitable / Marginal / Loss-maker

CRITICAL INSIGHT: Identify their "sweet spot" jobs:
- Which job types give the best $/hour?
- Which customers give the best jobs?
- What's the pattern? (Size? Type? Location?)

Be specific: "Kitchen rewires average $3,200 for ~18 hours = $178/hr effective rate = GOLD. 
You did 8 of these. If you did 12 instead of taking those 4 small $300 jobs, that's an extra $11,600."

## 3. CUSTOMER ANALYSIS (Who's Worth Your Time?)

Top customers by revenue - grade them:
- A-grade: High value, repeat, pays fast, good jobs
- B-grade: Decent value, reliable, average jobs
- C-grade: Low margin, slow pay, small jobs
- Fire: Actively costing you money or sanity

For each top customer:
- Total revenue
- Number of jobs
- Average job size
- Payment speed (if detectable)
- Are they growing or shrinking?

Bottom customers - should they fire any?
- Small jobs that don't pay
- One-off customers with high effort
- Slow payers (cash flow killers)

Customer concentration risk:
- Is >30% of revenue from one customer? (Risky)
- What happens if they lose their top 2 customers?

## 4. CASH FLOW ANALYSIS (The Silent Killer)

This is often the most valuable part of the audit:
- Average time between job completion and payment
- Outstanding invoices pattern
- Expense timing vs income timing
- Seasonal patterns (quiet months? busy months?)

Cash flow recommendations:
- Payment terms optimization (50% deposit, progress payments)
- Invoice timing (same day vs end of week)
- Expense timing (can anything be shifted?)

## 5. QUOTE WIN RATE (If Data Available)

If they provided quote data:
- Calculate actual win rate
- Compare to 30-40% benchmark
- Identify patterns in lost quotes (too high? wrong jobs? slow response?)
- Calculate: If win rate improved by 5%, what's the impact?

If no quote data:
- Note this as a critical gap
- Recommend tracking quotes
- Estimate opportunity if win rate improved

## 6. TIME LEAK ANALYSIS

Based on their hours and revenue:
- Billable ratio: Revenue suggests X hours at their rate, they work Y hours
- Gap analysis: Where's the unbilled time going?
- Admin burden: Any clues from software subscriptions, bookkeeping expenses?

Time optimization opportunities:
- Jobs to avoid (low $/hour)
- Jobs to chase (high $/hour)
- Admin to automate or delegate

## 7. EXPENSE ANALYSIS (Hidden Profit Leaks)

Review their expenses for:
- Material costs: Are they marking up enough? (25-35% is standard)
- Vehicle costs: Fuel, rego, insurance - are they recovering these?
- Insurance: Are they paying too much? Getting annual reviews?
- Subscriptions: Any unused software/services?
- Subcontractors: Are they profitable or just passing through?

## 8. GROWTH OPPORTUNITIES (2026 Specific)

Based on their data, identify:
- Specialization opportunity: What could they become known for?
- Upsell patterns: What additional services could they offer?
- Geographic expansion: Are they traveling too far for small jobs?
- Digital presence: Do they have Google reviews? (Can't tell from data, but recommend)

## 9. ONLINE PRESENCE ASSESSMENT

Based on their stated Google rating and review count:

BENCHMARKS (2026):
- 0-5 reviews: Invisible online. Losing 60%+ of Google searches to competitors.
- 6-15 reviews: Minimal presence. Better than nothing but still losing to competitors.
- 16-30 reviews: Competitive. Starting to win some Google searches.
- 30+ reviews: Strong. Capturing significant local search traffic.
- 4.7+ rating with 30+ reviews: Dominant. Price can be premium.

Calculate the opportunity:
- If they have < 15 reviews, estimate they're losing 2-4 jobs/month to competitors who rank higher
- At their average job value, that's $X-Y/month in lost revenue
- Review acquisition is FREE - just need a system

## 10. LEAD CONVERSION ANALYSIS

If their stated close rate is:
- Under 25%: Either pricing wrong (too high or too low), quoting too slow, or targeting wrong leads
- 25-35%: Normal for most tradies, room for improvement
- 35-50%: Good, but may indicate slight underpricing
- Over 50%: Likely underpriced - capturing jobs that should've been priced higher

Calculate:
- Current leads/week × conversion rate = jobs/week
- If conversion improved by 10%, that's X more jobs/month
- At average job value, that's $Y/month opportunity

## 11. QUOTING PROCESS AUDIT

Use their quoting data from the Business Context section above.

Calculate the admin cost:
- Quotes per month × time per quote × their hourly rate = TRUE cost of quoting
- If this exceeds 10% of revenue, it's a major problem

Speed matters:
- "Within 48 hours" loses to "Same day" - 30% of customers go with whoever responds first
- Calculate: Potential jobs lost × average job value = speed-cost

## 12. OPERATIONS & EFFICIENCY ASSESSMENT

Their current systems are detailed in the Business Context section above.

Analyze:
- If using "Paper / manual" or "In my head" - they're operating blind
- No follow-up system = losing 30-40% of warm leads
- Manual job tracking = overbooking risk + no data for optimization

Administrative burden:
- Use their stated biggest time waste from Business Context
- This is costing them X hours/week × their hourly rate = $Z/week in lost billable time
- Annual admin burden cost: $Z × 48 weeks

System recommendations should be SPECIFIC:
- Not "get software" but "implement [specific tool] for [specific problem]"
- Not "automate follow-up" but "set up [specific system] to follow up Day 3 and Day 7"

## 13. GROWTH ROADMAP

Based on their stated goals:
- Revenue goal: What gap needs to be closed?
- Hiring plans: What revenue is needed before hiring makes sense?
- Their "magic wand" wish: How do we get there practically?

If they want to grow but:
- No Google presence = marketing ceiling
- Manual quoting = admin ceiling  
- No follow-up = conversion ceiling
- Underpriced = need to increase volume just to stay still

## 14. REALISTIC 90-DAY ACTION PLAN

For EACH action, you MUST provide:

1. THE NUMBERS (with assumptions shown):
   - Calculation: Show exactly how you got the impact number
   - Conservative estimate: Use 70% of theoretical maximum
   - Best case: What if everything goes perfectly
   - Assumption: What needs to be true for this to work

2. THE REALITY CHECK:
   - Risk: What could go wrong
   - Effort: Be honest about how hard this is (1-10 scale)
   - Time to implement: Hours needed
   - Time to see results: When will they see money?

3. THE SCRIPT (exact words):
   - What to say to customers
   - How to handle the most common pushback
   - Email/SMS template if relevant

4. THE EVIDENCE:
   - Why this will work for THEIR specific situation
   - Reference their actual data (customer names, job types, amounts)

5. THE PRIORITY:
   - Quick wins (this week, low effort, immediate impact)
   - Medium-term (this month, medium effort)
   - Strategic (this quarter, higher effort, bigger payoff)

EXAMPLE OF A GREAT ACTION:

Action: Increase hourly rate from $95 to $115 for new customers
Priority: 1 (Quick Win)

CALCULATION:
- Your data shows 45 jobs over 12 months
- Average job revenue: $1,850
- Estimated hours per job: 16 (based on job sizes)
- Total billable hours: ~720/year
- Rate increase: $20/hr
- Gross increase: $20 × 720 = $14,400
- Assume 15% fewer jobs from price-sensitive customers: $14,400 × 0.85 = $12,240
- CONSERVATIVE ESTIMATE: $12,240/year
- Best case (no customer loss): $14,400/year

EVIDENCE FROM YOUR DATA:
- Your current effective rate of $95/hr is 17% below Sydney mid-market of $115
- Your best customer (Smith Constructions) paid $3,200 average - they're not price shopping
- 6 of your jobs were under $500 - these are likely price-sensitive, okay to lose

ASSUMPTION: 
- You're willing to lose some small jobs
- You'll apply new rate to new customers first, existing customers in 60 days

RISK: 
- Some price-sensitive customers will shop around
- Mitigate by: raising for new customers first, giving existing customers 60 days notice

EFFORT: 2/10 - Just update your quote template
TIME TO IMPLEMENT: 1 hour
TIME TO SEE RESULTS: First new quote (this week)

SCRIPT FOR NEW CUSTOMERS: 
"Our rate is $115 per hour plus materials. That includes a licensed [trade], fully insured, and we guarantee our work."

SCRIPT FOR EXISTING CUSTOMERS:
"Hi [Name], just wanted to let you know our rates are moving to $115/hr from [date]. This brings us in line with current market rates and ensures we can keep delivering the quality you expect. Happy to chat if you have any questions."

PUSHBACK RESPONSE:
"I understand budget's a consideration. Our rate reflects [X years] experience, full licensing and insurance, and our guarantee to get it right first time. If you need to compare quotes, no hard feelings - but I'd back our quality against anyone."

## OUTPUT FORMAT

Return a JSON object with these keys:

1. "data_quality": {{
   "score": 1-10,
   "strengths": ["what data was good"],
   "gaps": ["what was missing"],
   "recommendations": ["how to improve data next time"]
}}

2. "business_health_score": {{
   "overall": 1-10,
   "pricing": 1-10,
   "profitability": 1-10,
   "cash_flow": 1-10,
   "customer_mix": 1-10,
   "efficiency": 1-10,
   "growth_potential": 1-10
}}

3. "summary": {{
   "total_revenue_analyzed": number,
   "total_expenses_analyzed": number,
   "gross_profit": number,
   "gross_margin": number,
   "calculated_effective_rate": number,
   "effective_rate_calculation": "show the math",
   "market_rate_range": "low-high for trade/location",
   "rate_gap": number,
   "rate_gap_percentage": number,
   "data_confidence": "high/medium/low",
   "biggest_insight": "one sentence that makes them go 'holy shit'"
}}

4. "pricing_audit": {{
   "current_stated_rate": number,
   "current_effective_rate": number,
   "effective_rate_calculation": {{
     "total_revenue": number,
     "estimated_hours": number,
     "hours_estimation_method": "from timesheets/estimated from job mix/assumed X hrs per job",
     "calculation": "Total revenue ($X) ÷ Estimated hours (Y) = $Z/hr",
     "confidence": "HIGH/MEDIUM/LOW",
     "confidence_reason": "why this confidence level"
   }},
   "market_benchmark": {{
     "min": number,
     "average": number,
     "max": number,
     "premium": number,
     "source": "service.com.au + industry associations",
     "sample_size": "200+ data points",
     "confidence": "HIGH"
   }},
   "rate_percentile": number,
   "rate_percentile_description": "e.g., 'at the 35th percentile - below average'",
   "recommended_rate": number,
   "rate_increase_scenarios": {{
     "conservative": {{
       "customer_retention": 0.85,
       "annual_impact": number,
       "calculation": "show the math"
     }},
     "realistic": {{
       "customer_retention": 0.90,
       "annual_impact": number,
       "calculation": "show the math"
     }},
     "optimistic": {{
       "customer_retention": 0.95,
       "annual_impact": number,
       "calculation": "show the math"
     }}
   }},
   "call_out_fee_analysis": {{
     "current_fee": number,
     "market_benchmark": number,
     "recommended_fee": number,
     "annual_jobs_estimated": number,
     "annual_impact_conservative": number,
     "calculation": "Jobs (X) × Fee ($Y) × Acceptance (85%) = $Z",
     "source": "service.com.au call-out fee data"
   }}
}}

5. "job_analysis": [
   {{
     "category": "string",
     "job_count": number,
     "total_revenue": number,
     "avg_revenue": number,
     "estimated_hours_per_job": number,
     "effective_rate": number,
     "material_ratio": number or null,
     "verdict": "highly_profitable/profitable/marginal/loss_maker",
     "recommendation": "specific advice",
     "example_from_data": "reference a specific job"
   }}
]

5b. "worst_jobs": [
   {{
     "job_description": "specific job from their data",
     "customer": "customer name",
     "revenue": number,
     "estimated_cost": number,
     "profit_loss": number,
     "effective_rate": number,
     "why_bad": "brief explanation",
     "lesson": "what to do differently"
   }}
] (List the 3-5 worst performing jobs you can identify from their data - jobs where they likely lost money or made very little. Be specific.)

6. "customer_analysis": {{
   "top_customers": [
     {{
       "name": "string",
       "total_revenue": number,
       "job_count": number,
       "avg_job_size": number,
       "grade": "A/B/C/Fire",
       "recommendation": "specific advice"
     }}
   ],
   "concerning_customers": [
     {{
       "name": "string",
       "reason": "why they're concerning",
       "recommendation": "what to do"
     }}
   ],
   "customer_concentration_risk": "assessment",
   "ideal_customer_profile": "description of their best customer type"
}}

7. "cash_flow_insights": {{
   "payment_speed_assessment": "string",
   "seasonal_patterns": "string or null",
   "cash_flow_risks": ["list of risks"],
   "recommendations": ["list of specific actions"]
}}

8. "expense_insights": {{
   "material_markup_assessment": "string",
   "vehicle_cost_recovery": "string",
   "subscription_audit": ["any unnecessary expenses found"],
   "optimization_opportunities": ["specific savings"]
}}

8b. "online_presence_analysis": {{
   "current_rating": "string",
   "current_reviews": number,
   "presence_score": 1-10,
   "estimated_visibility": "invisible/weak/moderate/strong/dominant",
   "estimated_jobs_lost_monthly": number,
   "annual_revenue_impact": number,
   "recommendations": ["specific actions to improve"],
   "review_acquisition_script": "exact words to ask for reviews"
}}

8c. "lead_conversion_analysis": {{
   "stated_conversion_rate": number,
   "conversion_assessment": "too_low/normal/good/possibly_underpriced",
   "leads_per_week": number,
   "current_jobs_per_week": number,
   "if_improved_by_10pct": {{
     "additional_jobs_monthly": number,
     "additional_revenue_monthly": number,
     "annual_impact": number
   }},
   "conversion_blockers_identified": ["list of likely issues"],
   "recommendations": ["specific actions"]
}}

8d. "quoting_process_analysis": {{
   "current_method": "string",
   "time_per_quote": "string",
   "quotes_per_month": number,
   "admin_cost_calculation": {{
     "hours_per_month": number,
     "at_billable_rate": number,
     "annual_cost": number,
     "percentage_of_revenue": number
   }},
   "speed_assessment": "fast/moderate/slow",
   "speed_impact": {{
     "jobs_lost_to_slower_response": number,
     "annual_revenue_impact": number
   }},
   "efficiency_recommendations": ["specific improvements"],
   "ideal_quoting_time": "what they should target"
}}

8e. "operations_efficiency": {{
   "current_systems_score": 1-10,
   "admin_burden_weekly_hours": number,
   "admin_burden_annual_cost": number,
   "biggest_stated_time_waste": "string",
   "follow_up_assessment": "none/inconsistent/manual/automated",
   "follow_up_impact": {{
     "leads_lost_to_no_followup": "X per month",
     "annual_revenue_impact": number
   }},
   "system_recommendations": [
     {{
       "problem": "specific problem",
       "solution": "specific tool or system",
       "implementation_time": "how long to set up",
       "expected_time_saved_weekly": number
     }}
   ]
}}

8f. "growth_roadmap": {{
   "current_revenue_estimate": number,
   "stated_goal": "string",
   "gap_to_goal": number,
   "primary_growth_blockers": ["ordered list"],
   "hiring_readiness": {{
     "ready_to_hire": boolean,
     "revenue_needed_before_hiring": number,
     "current_gap": number
   }},
   "magic_wand_response": {{
     "they_want": "their stated wish",
     "practical_path": "how to actually get there",
     "first_step": "immediate action"
   }},
   "90_day_priorities": ["ordered by impact"]
}}

9. "action_plan": [
   {{
     "priority": number (1-10),
     "category": "quick_win/medium_term/strategic",
     "action": "clear, specific action",
     "calculation_steps": [
       "Step 1: [description] = $X",
       "Step 2: [description] = $Y",
       "Step 3: [adjustment for reality] = $Z"
     ],
     "scenarios": {{
       "conservative": {{"impact": number, "assumption": "15% customer loss"}},
       "realistic": {{"impact": number, "assumption": "10% customer loss"}},
       "optimistic": {{"impact": number, "assumption": "5% customer loss"}}
     }},
     "recommended_impact": number,
     "data_evidence": {{
       "specific_reference": "e.g., Invoice #23 to ABC Corp for $1,200",
       "pattern_found": "e.g., 4 similar jobs averaged $X",
       "supporting_data": ["list of specific data points from their records"]
     }},
     "market_validation": {{
       "benchmark_used": "e.g., Sydney electrician rates",
       "source": "service.com.au",
       "confidence": "HIGH/MEDIUM/LOW"
     }},
     "risk_analysis": {{
       "primary_risk": "what could go wrong",
       "likelihood": "low/medium/high",
       "mitigation": "how to reduce the risk",
       "worst_case_impact": "if this fails, what happens"
     }},
     "effort_score": 1-10,
     "time_to_implement": "string",
     "time_to_results": "string",
     "implementation": {{
       "script_for_customers": "exact words to use",
       "script_for_objections": "how to handle pushback",
       "first_step": "the very first thing to do"
     }}
   }}
]

10. "opportunity_summary": {{
   "total_conservative": number,
   "total_realistic": number,
   "total_optimistic": number,
   "quick_wins_total": number,
   "confidence_level": "high/medium/low",
   "key_assumptions": ["list"],
   "biggest_risk": "string",
   "meets_10k_guarantee": boolean,
   "guarantee_confidence": "high/medium/low",
   "roi_on_audit": "e.g., '37x return on $797 audit fee'"
}}

11. "methodology": {{
   "data_analyzed": {{
     "invoices_count": number,
     "date_range": "start - end",
     "total_revenue": number,
     "total_expenses": number
   }},
   "benchmarking_sources": [
     {{
       "name": "service.com.au",
       "data_points": "200+",
       "coverage": "National + 5 major cities",
       "confidence": "HIGH"
     }},
     {{
       "name": "Industry associations (NECA, Master Plumbers, etc.)",
       "type": "Trade surveys and reports",
       "confidence": "MEDIUM"
     }}
   ],
   "calculation_methodology": {{
     "effective_rate": "Total revenue ÷ estimated billable hours",
     "billable_hours_estimate": "Based on job mix and industry time standards",
     "opportunity_projections": "Three scenarios: Conservative (15% loss), Realistic (10% loss), Optimistic (5% loss)",
     "impact_calculations": "All impacts shown with step-by-step math"
   }},
   "confidence_levels_used": {{
     "HIGH": "3+ sources, large sample, recent data",
     "MEDIUM": "1-2 sources, industry estimates",
     "LOW": "Single source or assumption-based"
   }},
   "limitations": [
     "Hours estimated from job mix (no actual timesheets)",
     "Customer retention rates based on industry averages",
     "Market conditions may vary"
   ]
}}

12. "backend_problems_identified": [
   {{
     "category": "quoting/pricing/follow_up/lead_qualification/cash_flow/customer_concentration",
     "indicator": "what we observed",
     "severity": "low/medium/high",
     "metric_value": number or string,
     "estimated_annual_cost": number,
     "notes": "additional context"
   }}
] (Identify operational pain points for agent development)

11. "missing_data": {{
   "critical_gaps": ["what we couldn't analyze"],
   "nice_to_have": ["what would improve analysis"],
   "data_collection_tips": ["how to get better data next time"]
}}

12. "next_steps": {{
   "this_week": ["1-3 immediate actions"],
   "this_month": ["2-4 actions"],
   "this_quarter": ["1-2 strategic moves"],
   "tracking_metrics": ["what to measure going forward"]
}}

REMEMBER:
- Total opportunity = sum of CONSERVATIVE estimates only
- Don't exceed realistic numbers just to hit $10k
- If you can't honestly find $10k, say so and explain why
- A conservative $15k finding is better than an inflated $50k
- Reference THEIR specific data - customer names, job types, amounts
- Make them feel like you KNOW their business
"""


def get_report_summary_prompt(analysis_json: str, customer_name: str = "mate") -> str:
    """Generate the executive summary prompt."""
    return f"""You are writing the executive summary for a Tradie Profit Audit Report.

Customer name: {customer_name}

Based on this analysis:
{analysis_json}

Write a compelling but HONEST executive summary that:

1. Opens with their specific situation (use their actual numbers)
2. States the CONSERVATIVE opportunity found (not best case)
3. Acknowledges what assumptions you're making
4. Summarizes top 3 quick wins with realistic expectations
5. Is honest about what's certain vs what depends on execution
6. References specific data from their business (customer names, job types)

TONE:
- Direct and honest (tradies smell BS a mile away)
- Confident but not hypey
- Specific numbers, not vague promises
- Acknowledge the hard parts, don't pretend it's all easy
- Use "you" and "your"
- Sound like a trusted advisor, not a salesperson

DON'T:
- Overpromise
- Use phrases like "life-changing" or "transform your business"
- Claim certainty where there isn't any
- Ignore risks or downsides
- Use corporate jargon

DO:
- Show you understand their specific business
- Reference their actual customer names/job types
- Be clear about what they need to DO vs what will magically happen
- Set realistic expectations
- Include one "holy shit" insight that shows you really analyzed their data

LENGTH: 300-400 words

EXAMPLE OPENING (good):
"{customer_name.split()[0] if customer_name else 'Mate'}, here's the straight truth about your numbers.

You're bringing in $183k a year working about 50 hours a week. At your stated rate of $95/hr, 
that works out to an effective rate of around $73/hr after everything - which is about 30% 
below what Sydney sparkies typically charge.

The good news? We found $18,400 in realistic opportunities. Not pie-in-the-sky numbers - 
this is what you can actually capture if you implement the changes.

Here's what jumped out: Your work for Smith Constructions averaged $3,200 per job. 
But those 6 small call-outs you did? $380 average. That's $73/hr vs $190/hr. 
You're essentially subsidizing small jobs with your good ones."

EXAMPLE OPENING (bad - don't do this):
"Amazing news! We've discovered you're leaving a MASSIVE $91,000 on the table! 
This is going to transform your business and change your life!"

Write the summary now:
"""


def get_customer_categorization_prompt(customer_name: str, transactions: str) -> str:
    """Generate the customer categorization prompt."""
    return f"""Analyze this customer's transaction history and categorize them:

Customer: {customer_name}
Transactions:
{transactions}

Categorize as:
- "A-grade": High revenue, pays on time, repeat business, good-sized jobs, easy to work with
- "B-grade": Decent revenue, mostly reliable, average jobs, no major issues
- "C-grade": Low margin, slow to pay, small jobs, high effort for low return
- "Fire": Actively losing you money, nightmare to deal with, or dangerous to cash flow

Return a JSON object with:
- customer: name
- grade: "A" or "B" or "C" or "Fire"
- total_revenue: number
- job_count: number
- avg_job_size: number
- estimated_profit_margin: number (0-1)
- payment_behavior: "fast" or "normal" or "slow" or "very_slow"
- job_size_trend: "growing" or "stable" or "shrinking"
- recommendation: "nurture" or "maintain" or "increase_prices" or "reduce_service" or "fire"
- reasoning: "Why this grade - be specific and reference the data"
- action: "Specific action to take with this customer"
"""


def get_cash_flow_prompt(transactions: str, business_context: str) -> str:
    """Generate cash flow analysis prompt."""
    return f"""Analyze the cash flow patterns in this tradie business:

TRANSACTIONS:
{transactions}

BUSINESS CONTEXT:
{business_context}

Analyze:
1. PAYMENT TIMING
   - Average days between invoice and payment (if detectable)
   - Any patterns in late payments
   - Customers who consistently pay slow

2. SEASONAL PATTERNS
   - Which months have highest revenue?
   - Which months have highest expenses?
   - Any dangerous gaps where expenses exceed income?

3. EXPENSE TIMING
   - Large expenses and when they hit
   - Recurring expenses (insurance, subscriptions, etc.)
   - Variable expenses (materials, fuel)

4. CASH FLOW RISKS
   - Customer concentration (too much from one customer?)
   - Timing mismatches (expenses before income?)
   - Seasonal vulnerability

5. RECOMMENDATIONS
   - Payment terms changes
   - Invoice timing optimization
   - Expense timing optimization
   - Cash reserve recommendations

Return JSON with:
{{
  "payment_analysis": {{
    "average_payment_days": number or null,
    "slow_payers": ["customer names"],
    "fast_payers": ["customer names"]
  }},
  "seasonal_patterns": {{
    "peak_months": ["months"],
    "slow_months": ["months"],
    "dangerous_months": ["months where cash flow is tight"]
  }},
  "risks": [
    {{
      "risk": "description",
      "severity": "high/medium/low",
      "mitigation": "what to do"
    }}
  ],
  "recommendations": [
    {{
      "action": "specific action",
      "impact": "expected result",
      "priority": "high/medium/low"
    }}
  ]
}}
"""
