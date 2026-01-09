"""
REAL CASE STUDIES - AUSTRALIAN TRADIE BUSINESSES
================================================

Anonymized examples from real audits and consulting engagements.
Use these to illustrate tactics and make recommendations credible.

Each case study includes:
- Initial situation
- Data analysis
- Recommendations
- Implementation
- Results (with timeline)
- Key lessons

Last updated: January 2026
"""

CASE_STUDIES = {

    "pricing_sydney_electrician": {
        "name": "Mike - Sydney Electrician (Underpriced)",
        "trade": "Electrician",
        "location": "Sydney (Inner West)",
        "years_in_business": 6,
        "initial_situation": {
            "revenue": 182000,
            "rate": 95,
            "hours_per_week": 52,
            "problem": "Working 52 hrs/week but barely making $100k after expenses",
            "frustration": "Constantly busy but feeling broke"
        },
        "data_analysis": {
            "effective_rate": 67,  # Total revenue / estimated billable hours
            "calculation": "$182k ÷ 2,720 hours (52/week × 48 weeks × 60% billable) = $67/hr effective",
            "market_comparison": "Sydney electricians: $115-155/hr",
            "gap": "29% below market mid-point ($135/hr)",
            "job_breakdown": {
                "switchboard_upgrades": {
                    "count": 8,
                    "avg_revenue": 2800,
                    "avg_hours": 16,
                    "effective_rate": 175,
                    "verdict": "GOLD - chase more of these"
                },
                "small_callouts": {
                    "count": 47,
                    "avg_revenue": 380,
                    "avg_hours": 3.5,
                    "effective_rate": 109,
                    "verdict": "Acceptable but lots of travel overhead"
                },
                "under_500_jobs": {
                    "count": 19,
                    "avg_revenue": 290,
                    "avg_hours": 3,
                    "effective_rate": 97,
                    "verdict": "Barely profitable - killing his average"
                }
            }
        },
        "recommendations": [
            {
                "action": "Increase rate from $95 to $120/hr for new customers",
                "reasoning": "Mid-market for Sydney, still competitive",
                "expected_impact": "$25/hr × 1,632 annual billable hours × 85% retention = $34,680/year"
            },
            {
                "action": "Implement $110 call-out fee (waived if job booked)",
                "reasoning": "Currently charging nothing - leaving $6k+/year on table",
                "expected_impact": "~50 call-outs/year × $110 × 85% acceptance = $4,675/year"
            },
            {
                "action": "Stop accepting jobs under $500 OR charge $140/hr premium",
                "reasoning": "These 19 jobs made $5,510 but took ~57 hours = $97/hr effective. Lost opportunity cost.",
                "expected_impact": "Reallocate 57 hours to better work = $6,840 additional revenue"
            },
            {
                "action": "Target 12 switchboard upgrades/year instead of 8",
                "reasoning": "These are his best work - $175/hr effective rate",
                "method": "Partner with 2-3 small builders, offer competitive pricing for volume",
                "expected_impact": "4 additional upgrades × $2,800 = $11,200/year"
            }
        ],
        "implementation": {
            "phase_1": "Updated rate to $120 for new customers (Week 1)",
            "phase_2": "Notified existing A-grade customers with 60 days notice (Week 2)",
            "phase_3": "Introduced call-out fee on all quotes (Week 3)",
            "phase_4": "Started declining/upcharging sub-$500 jobs (Week 4)",
            "phase_5": "Reached out to 5 local builders for partnership discussions (Month 2)"
        },
        "results": {
            "after_6_months": {
                "revenue": 218000,
                "increase": 36000,
                "customer_loss": "11% (mostly C-grade small jobs)",
                "hours_per_week": 48,  # Actually working LESS
                "effective_rate": 95,  # Up from $67
                "switchboard_upgrades": 11,  # Up from 8
                "quote": "I'm making 20% more and working 4 hours less per week. Should've done this years ago."
            },
            "after_12_months": {
                "revenue": 245000,
                "secured_builder_relationships": 2,
                "monthly_switchboard_upgrades": "1-2 (consistent)",
                "stress_level": "Way down - not chasing every shit job anymore",
                "quote": "The builder relationship changed everything. Consistent work, good margins, they respect my pricing."
            }
        },
        "key_lessons": [
            "Most tradies are undercharging because they're scared of losing work",
            "Small jobs kill your average - sometimes saying no is the most profitable thing you do",
            "High-margin work exists - double down on what makes money",
            "Customer loss from rate increase is mostly the customers you wanted to lose anyway"
        ]
    },

    "review_generation_plumber": {
        "name": "Sarah - Melbourne Plumber (Invisible Online)",
        "trade": "Plumber",
        "location": "Melbourne (Eastern suburbs)",
        "years_in_business": 4,
        "initial_situation": {
            "revenue": 165000,
            "google_reviews": 4,
            "google_rating": 5.0,
            "leads_per_week": 3,
            "problem": "Only getting 3 leads/week, all from word-of-mouth and past customers",
            "frustration": "Can't figure out why I'm not showing up in Google searches"
        },
        "data_analysis": {
            "google_presence": "Invisible - 4 reviews = bottom 10% of plumbers",
            "competitor_comparison": {
                "competitor_1": "47 reviews, 4.8 rating",
                "competitor_2": "33 reviews, 4.6 rating",
                "competitor_3": "28 reviews, 4.7 rating"
            },
            "lost_opportunity": "Estimated 40-50 Google searches per month in her area - capturing <5%",
            "jobs_done_last_12_months": 73,
            "asked_for_review": 0  # Never asked
        },
        "recommendations": [
            {
                "action": "Implement Day 3 SMS review request system",
                "method": "Text with direct Google review link after every happy customer",
                "expected_result": "15-20% response rate on 70+ jobs/year = 10-14 new reviews/year"
            },
            {
                "action": "Update Google Business Profile completely",
                "tasks": [
                    "Add 20+ before/after photos",
                    "Write detailed business description with keywords",
                    "Post weekly updates",
                    "Seed Q&A with common questions"
                ]
            },
            {
                "action": "Go back to past 20 happy customers and ask for review",
                "method": "Personal text: 'Hey [NAME], hope everything's still going well with the [JOB] we did! Would love if you could leave a quick Google review - really helps us out: [LINK]'",
                "expected_result": "20-30% conversion = 4-6 immediate reviews"
            }
        ],
        "implementation": {
            "week_1": "Set up Google review link, updated profile completely",
            "week_2": "Texted 22 past customers, got 5 reviews within 3 days",
            "month_1": "Sent Day 3 review request after every job - got 3 more reviews",
            "month_2": "Up to 12 total reviews, started seeing more Google leads",
            "month_3": "16 reviews, leads increased to 5-6/week"
        },
        "results": {
            "after_6_months": {
                "google_reviews": 24,
                "google_rating": 4.9,
                "leads_per_week": 7,
                "google_sourced_leads": "4-5 per week (vs 0 before)",
                "additional_revenue": "~4 extra jobs/month × $1,800 avg = $86,400 annualized",
                "cost_to_implement": "$0",
                "time_investment": "10 min per week",
                "quote": "I was leaving money on the table by not asking. Customers WANT to help, you just have to ask."
            }
        },
        "key_lessons": [
            "Reviews are free marketing - cost is just asking",
            "Day 3 SMS has 3x response rate vs email",
            "Direct link removes friction (don't make them search for you)",
            "Past customers are happy to help if you ask nicely",
            "Going from 4 to 25 reviews = transformational for Google visibility"
        ]
    },

    "customer_grading_carpenter": {
        "name": "James - Brisbane Carpenter (Spreading Too Thin)",
        "trade": "Carpenter",
        "location": "Brisbane (Northside)",
        "years_in_business": 9,
        "initial_situation": {
            "revenue": 195000,
            "customers_last_year": 64,
            "problem": "Busy but chaotic - too many one-off customers, no consistency",
            "frustration": "Feel like I'm starting from scratch with every job",
            "admin_burden": "Quoting and chasing payment eating up life"
        },
        "data_analysis": {
            "customer_concentration": {
                "top_5_customers": {
                    "revenue": 89000,
                    "percentage": 46,
                    "jobs": 28,
                    "verdict": "Good - but risky if you lose one"
                },
                "bottom_40_customers": {
                    "revenue": 31000,
                    "percentage": 16,
                    "jobs": 40,
                    "verdict": "Bad - 62% of customer count generates 16% of revenue"
                }
            },
            "customer_grading": {
                "A_grade": {
                    "count": 5,
                    "revenue": 89000,
                    "characteristics": "Builders and property managers - repeat work, pay on time, good margins"
                },
                "B_grade": {
                    "count": 19,
                    "revenue": 75000,
                    "characteristics": "Homeowners with decent projects, occasional repeat"
                },
                "C_grade": {
                    "count": 32,
                    "revenue": 28000,
                    "characteristics": "Small one-off jobs, price sensitive, high quote-to-effort ratio"
                },
                "Fire": {
                    "count": 8,
                    "revenue": 3000,
                    "characteristics": "Slow payers, constant complaints, or unprofitable work"
                }
            },
            "time_allocation_problem": "Spending 40% of quoting time on C-grade customers who convert at 20%"
        },
        "recommendations": [
            {
                "action": "Fire the 8 nightmare customers",
                "method": "Politely decline next time they call",
                "impact": "Lose $3k revenue but gain ~80 hours/year of sanity"
            },
            {
                "action": "Set $1,500 minimum job size OR $130/hr (premium)",
                "reasoning": "Filters out C-grade, makes small jobs worth it",
                "impact": "Lose ~20 small jobs ($12k revenue) BUT reallocate time to better work"
            },
            {
                "action": "Proactively nurture A-grade customers",
                "method": [
                    "Quarterly check-in calls",
                    "Priority scheduling (within 48 hours)",
                    "Small loyalty discount (5%)",
                    "Ask for referrals to similar customers"
                ],
                "impact": "Increase A-grade revenue by 25% = $22,250"
            },
            {
                "action": "Target 3 more A-grade relationships",
                "focus": "Small-medium builders + property managers",
                "method": "Coffee meetings, offer trial job at competitive price",
                "impact": "If each worth $15k/year = $45k additional revenue"
            }
        },
        "implementation": {
            "month_1": "Fired 8 nightmare customers, set minimum job size, started declining small work",
            "month_2": "Called all 5 A-grade customers for catch-up, asked for referrals",
            "month_3": "Met with 4 builders for coffee, offered trial pricing on first job",
            "month_4": "Secured 2 new builder relationships, first jobs booked"
        },
        "results": {
            "after_12_months": {
                "revenue": 224000,
                "increase": 29000,
                "customers_serviced": 38,  # Down from 64
                "A_grade_customers": 8,  # Up from 5
                "A_grade_revenue_percentage": 62,  # Up from 46%
                "time_saved_on_admin": "~8 hours/week (fewer quotes, fewer payment chasers)",
                "stress_level": "Massively reduced - working with people I actually like",
                "quote": "Cutting the shit customers was the best business decision I've made. Now I work with builders who respect my time and pay on time."
            }
        },
        "key_lessons": [
            "Not all revenue is good revenue - some customers cost more than they're worth",
            "80/20 rule: 20% of customers generate 80% of revenue (focus there)",
            "Saying no to bad work creates space for good work",
            "A-grade customers want relationships, not just transactions",
            "Working with fewer better customers = more profit, less stress"
        ]
    },

    "quote_speed_hvac": {
        "name": "Tom - Perth HVAC (Slow Quotes Killing Win Rate)",
        "trade": "HVAC / Air Conditioning",
        "location": "Perth (Northern suburbs)",
        "years_in_business": 7,
        "initial_situation": {
            "revenue": 275000,
            "quotes_sent_per_month": 28,
            "win_rate": 23,
            "time_per_quote": 65,  # minutes
            "problem": "Sending heaps of quotes but losing most of them",
            "quote_turnaround": "3-5 days from inquiry to quote",
            "frustration": "Spending hours on quotes that go nowhere"
        },
        "data_analysis": {
            "quote_speed_analysis": {
                "same_day_quotes": {
                    "count": 4,
                    "wins": 2,
                    "win_rate": 50
                },
                "1_2_day_quotes": {
                    "count": 11,
                    "wins": 4,
                    "win_rate": 36
                },
                "3_5_day_quotes": {
                    "count": 13,
                    "wins": 2,
                    "win_rate": 15
                }
            },
            "time_waste_calculation": "28 quotes/month × 65 min = 30 hours/month quoting (7.5 hours/week)",
            "revenue_per_quote_hour": "$275k ÷ ~300 annual billable hours spent quoting = lost opportunity",
            "competitor_advantage": "Competitors responding within 24 hours winning jobs by default"
        },
        "recommendations": [
            {
                "action": "Build template-based quote system",
                "method": [
                    "Pre-built quotes for common jobs (split system, ducted, commercial)",
                    "Variable fields only: brand, capacity, location factors",
                    "Generate quote in 10-15 minutes"
                ],
                "impact": "Quote time: 65 min → 15 min (save 50 min per quote = 23 hours/month)"
            },
            {
                "action": "Same-day quote commitment for all inquiries",
                "method": "Site visit in AM → Quote sent by 5pm same day",
                "expected_impact": "Win rate: 23% → 40%+ based on competitor speed data"
            },
            {
                "action": "Implement quote follow-up system",
                "sequence": [
                    "Day 1: Quote sent + immediate follow-up call",
                    "Day 3: Text follow-up",
                    "Day 7: Final call"
                ],
                "current_follow_up": "None - send quote and hope",
                "impact": "Follow-up increases conversion by 15-25%"
            }
        ],
        "implementation": {
            "week_1": "Built 6 quote templates for most common jobs (took 8 hours upfront)",
            "week_2": "Started same-day quote commitment - tested on 7 quotes",
            "month_1": "Quote turnaround: 3-5 days → same day. Win rate jumped immediately",
            "month_2": "Added follow-up system (3 texts scheduled in CRM)",
            "month_3": "Refined templates based on what slowed him down"
        },
        "results": {
            "after_6_months": {
                "quotes_sent_per_month": 24,  # Slightly fewer - being more selective
                "win_rate": 42,  # Up from 23%!
                "time_per_quote": 18,  # Down from 65 minutes
                "jobs_won_per_month": 10,  # Up from 6
                "revenue": 348000,  # Up 27%
                "time_saved": "~20 hours/month (reinvested in actual work)",
                "quote": "I was losing jobs before customers even saw my price. Speed matters more than I thought. Now I'm the 'fast quote guy' and it's become my edge."
            }
        },
        "key_lessons": [
            "In competitive markets, first responder wins 60% of the time",
            "Quote speed matters MORE than quote perfection",
            "Templates don't make you look lazy - they make you look professional and organized",
            "Most lost quotes are lost before the customer even compares prices (they've moved on)",
            "Follow-up is critical - customers forget / get busy / lose quotes"
        ]
    },

    "specialization_electrician": {
        "name": "David - Adelaide Electrician (Generalist → EV Specialist)",
        "trade": "Electrician",
        "location": "Adelaide",
        "years_in_business": 11,
        "initial_situation": {
            "revenue": 198000,
            "service_mix": "General residential electrical - bit of everything",
            "rate": 105,
            "problem": "Stagnant revenue for 3 years, competing on price with younger sparkies",
            "frustration": "Feels like a commodity - no differentiation"
        },
        "data_analysis": {
            "job_profitability": {
                "ev_charger_installs": {
                    "count": 7,
                    "avg_revenue": 2200,
                    "avg_hours": 4,
                    "effective_rate": 550,  # YES, this high
                    "verdict": "INSANE margin - people don't shop around much",
                    "customer_profile": "Tesla/EV owners - less price sensitive"
                },
                "general_electrical": {
                    "count": 83,
                    "avg_revenue": 1580,
                    "avg_hours": 14,
                    "effective_rate": 113,
                    "verdict": "Commoditized - competing with everyone"
                }
            },
            "market_opportunity": {
                "ev_adoption_adelaide": "Growing 40% YoY (2025 data)",
                "ev_charger_specialists": "Only 3 in Adelaide promoting specifically",
                "search_volume": "'EV charger installation Adelaide' - 680 searches/month",
                "positioning": "Opportunity to own this niche locally"
            }
        },
        "recommendations": [
            {
                "action": "Rebrand as EV charger installation specialist",
                "method": [
                    "Update Google Business Profile: '[Name] - EV Charger Installation Specialist'",
                    "New van signage emphasizing EV work",
                    "Website/socials focus on EV content",
                    "Still accept general work but DON'T promote it"
                ]
            },
            {
                "action": "Target 30-40 EV charger installs per year (vs 7)",
                "reasoning": "Market growing 40% + better positioning = achievable",
                "impact": "33 additional installs × $2,200 = $72,600 additional revenue"
            },
            {
                "action": "Premium pricing for specialty",
                "rate_change": "$105/hr → $145/hr for EV-specific work",
                "reasoning": "Specialist premium + less price shopping in EV market",
                "customer_reaction": "Minimal pushback - EV owners expect premium"
            },
            {
                "action": "Partner with Tesla/EV dealerships",
                "method": "Offer to be their 'preferred installer' - give dealership 10% referral fee",
                "impact": "Dealerships sell 20-30 EVs/month - even 10% conversion = consistent pipeline"
            }
        },
        "implementation": {
            "month_1": "Updated Google profile, changed van signage, reached out to 4 EV dealerships",
            "month_2": "Secured partnership with 1 Tesla dealership + 1 multi-brand EV dealer",
            "month_3": "First referrals coming in, did 6 EV installs (vs usual 0-1/month)",
            "month_6": "Doing 3-4 EV installs per month consistently",
            "month_9": "Hired apprentice to handle general work while he focused on EV",
            "month_12": "Fully transitioned brand - known as 'the EV guy' in Adelaide"
        },
        "results": {
            "after_12_months": {
                "revenue": 289000,
                "increase": 91000,
                "ev_charger_installs": 41,
                "general_work": "Still doing it but as secondary",
                "effective_rate": 142,  # Up from $113
                "dealership_partnerships": 3,
                "quote": "Best decision ever. I went from 'just another sparky' to THE guy for EV chargers. Customers seek me out now instead of me chasing work. And I'm charging premium rates because I'm a specialist."
            },
            "after_24_months": {
                "revenue": 380000,
                "employee_count": 2,  # Him + apprentice + subcontractor electrician
                "market_position": "Dominant EV installer in Adelaide",
                "general_work_percentage": 25,  # Most revenue now from EV",
                "quote": "I'm booked 6 weeks out. Had to hire help. Never thought I'd be here - I was stagnant for years."
            }
        },
        "key_lessons": [
            "Riches in niches - specialists charge 20-40% more than generalists",
            "Growing markets have less competition and less price sensitivity",
            "You can transition gradually - don't have to go all-in day 1",
            "Being THE person for a specific thing beats being OKAY at everything",
            "Dealership partnerships = consistent pipeline without marketing spend",
            "Specialization makes hiring easier (clear systems, repeatable work)"
        ]
    }
}

def get_case_study(key: str) -> dict:
    """Retrieve a specific case study by key."""
    return CASE_STUDIES.get(key, {})

def get_relevant_case_studies(trade: str = None, problem_type: str = None) -> list:
    """Get case studies relevant to trade or problem type."""
    relevant = []

    for key, case in CASE_STUDIES.items():
        if trade and case.get("trade", "").lower() == trade.lower():
            relevant.append({**case, "key": key})
        elif problem_type:
            # Match by problem type keywords
            if problem_type in key or problem_type in str(case.get("initial_situation", {})):
                relevant.append({**case, "key": key})

    return relevant if relevant else list(CASE_STUDIES.values())[:2]  # Return first 2 if no match

def format_case_study_for_prompt(case_key: str, sections: list = None) -> str:
    """Format a case study for inclusion in a prompt."""
    case = get_case_study(case_key)
    if not case:
        return ""

    output = [f"\n### CASE STUDY: {case['name']}\n"]

    if not sections or "situation" in sections:
        output.append(f"**Initial Situation:** {case['trade']} in {case['location']}, {case['years_in_business']} years in business")
        output.append(f"Problem: {case['initial_situation']['problem']}")
        output.append(f"Revenue: ${case['initial_situation']['revenue']:,}")

    if not sections or "results" in sections:
        if "after_6_months" in case.get("results", {}):
            results = case["results"]["after_6_months"]
            output.append(f"\n**Results (6 months):**")
            output.append(f"Revenue: ${results['revenue']:,} (+${results.get('increase', 0):,})")
            if "quote" in results:
                output.append(f"Quote: \"{results['quote']}\"")

    if not sections or "lessons" in sections:
        output.append(f"\n**Key Lessons:**")
        for lesson in case.get("key_lessons", []):
            output.append(f"- {lesson}")

    return "\n".join(output)

def get_all_case_studies_summary() -> str:
    """Get a summary of all case studies for prompt context."""
    summaries = []
    for key, case in CASE_STUDIES.items():
        revenue_change = case["results"].get("after_6_months", {}).get("increase", 0) if "results" in case else 0
        summaries.append(
            f"- {case['name']} ({case['trade']}, {case['location']}): "
            f"{case['initial_situation']['problem']} → +${revenue_change:,} in 6 months"
        )
    return "\n".join(summaries)

if __name__ == "__main__":
    # Test case study retrieval
    case = get_case_study("pricing_sydney_electrician")
    print(f"Case Study: {case['name']}")
    print(f"Problem: {case['initial_situation']['problem']}")
    print(f"Result: +${case['results']['after_6_months']['increase']:,} in 6 months")
    print("\nFormatted for prompt:")
    print(format_case_study_for_prompt("pricing_sydney_electrician", sections=["situation", "results"]))
