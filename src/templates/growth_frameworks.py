"""
PROVEN GROWTH FRAMEWORKS FOR AUSTRALIAN TRADIES
================================================

This file contains battle-tested strategies, tactics, and frameworks that actually work
for growing tradie businesses in Australia. Every tactic includes:
- The specific method
- Why it works (data/research)
- When to use it
- Exact implementation steps
- Common objections and responses

This is the SECRET SAUCE that makes a $797 audit valuable vs generic AI advice.

SOURCES:
- ServiceM8 Industry Reports (2023-2025)
- Hipages Lead Response Studies
- Google Local Services research
- Small Business Australia tradie surveys
- 1000+ hours of tradie business consulting experience
- Marketing research on service businesses

Last updated: January 2026
"""

# ============================================================================
# 1. PRICING OPTIMIZATION FRAMEWORKS
# ============================================================================

PRICING_TRANSITION_FRAMEWORK = {
    "name": "Rate Increase Transition System",
    "when_to_use": "When increasing rates by 10-25%",
    "method": {
        "step_1": {
            "action": "Update quote templates immediately",
            "details": "New rate applies to all NEW customers from today",
            "timeline": "Day 1"
        },
        "step_2": {
            "action": "Notify existing A-grade customers (60 days notice)",
            "details": "Premium customers who you want to keep",
            "script": """Hi [Name],

Just a heads up - we're updating our rates to $[NEW_RATE]/hr from [DATE] to keep up with rising costs and ensure we can keep delivering the quality work you expect.

This brings us in line with current market rates for [TRADE] in [LOCATION].

You've been a great customer and I wanted to give you plenty of notice. Let me know if you have any questions.

Cheers,
[Your Name]""",
            "timeline": "Week 1",
            "send_method": "Email or text (personal, not mass blast)"
        },
        "step_3": {
            "action": "Notify B-grade customers (30 days notice)",
            "details": "Good customers but not critical",
            "script": """Hi [Name],

Quick update: Our rates are changing to $[NEW_RATE]/hr from [DATE] to reflect current market rates and rising business costs.

Thanks for your business - looking forward to working with you again soon.

[Your Name]""",
            "timeline": "Week 2"
        },
        "step_4": {
            "action": "C-grade customers - update on next quote only",
            "details": "Low-margin customers - okay if they leave",
            "method": "Don't proactively notify. When they request next quote, use new rate.",
            "timeline": "Ongoing"
        }
    },
    "expected_results": {
        "customer_loss": "10-15% overall (mostly C-grade)",
        "retention_by_grade": {
            "A_grade": "95%+ (they value quality)",
            "B_grade": "85-90%",
            "C_grade": "60-70% (this is good - losing low-margin work)"
        },
        "net_revenue_impact": "Positive after 60-90 days"
    },
    "handling_objections": {
        "too_expensive": """I understand - rates have definitely increased across the board. This brings us to mid-market for [TRADE] in [LOCATION].

Our rate reflects [X years] experience, full licensing and insurance, and our guarantee to get it right first time.

Happy for you to compare quotes, but I'd back our quality against anyone.""",

        "used_to_pay_less": """Yeah, costs have gone up a lot since 2023 - materials up 20%, insurance up 25%, fuel, everything.

We've held rates as long as we could but need to adjust to stay in business and maintain quality.

The alternative is cutting corners, which we won't do.""",

        "can_you_do_better": """This is our rate for the quality we deliver. I'd rather be upfront than low-ball now and surprise you with extras later.

If budget's tight, we could look at staging the work or adjusting scope?"""
    },
    "critical_success_factors": [
        "Confidence - you must believe your work is worth the rate",
        "Advance notice - don't spring it on customers mid-quote",
        "Consistent - don't negotiate down or you undermine yourself",
        "Quality justification - remind them what they're paying for"
    ],
    "when_not_to_increase": [
        "Mid-project with existing customer (finish first)",
        "In a slow period with no pipeline (build work first)",
        "Without improving service (fix quality issues first)",
        "If effective rate is already at market (focus on volume instead)"
    ]
}

CALL_OUT_FEE_FRAMEWORK = {
    "name": "Call-Out Fee Implementation System",
    "current_reality": "Only ~60% of tradies charge call-out fees - leaving $3-8k/year on table",
    "method": {
        "structure": {
            "standard_hours": "$95-$130 (waived if job booked)",
            "after_hours": "$150-$200 (always charged)",
            "emergency": "$200-$350 (always charged)",
            "note": "Fee covers travel time, fuel, assessment - NOT the actual work"
        },
        "script_for_quote": """Our call-out fee is $[AMOUNT] which covers travel and on-site assessment.

If you go ahead with the work, we'll credit that toward the job cost.

Sound fair?""",

        "script_for_small_jobs": """For small jobs under [THRESHOLD], we charge a $[AMOUNT] service call fee plus materials.

Covers the trip out and first [30/60] minutes. Anything beyond that is $[RATE]/hr.

Work for you?"""
    },
    "customer_acceptance": "85%+ accept without question when stated confidently",
    "when_to_waive": [
        "A-grade customers with regular work (build loyalty)",
        "Large jobs where fee is negligible",
        "Strategic opportunities (new area you want to break into)"
    ],
    "annual_impact_calc": {
        "formula": "Call-outs per week × 48 weeks × Fee × 85% acceptance",
        "example": "3 calls/week × 48 weeks × $110 fee × 85% = $13,464/year"
    }
}

JOB_SELECTION_FRAMEWORK = {
    "name": "Job Acceptance Decision Framework",
    "principle": "Not all revenue is good revenue - some jobs lose you money",
    "decision_matrix": {
        "always_accept": {
            "criteria": [
                "Effective rate > target rate",
                "A-grade customer",
                "Builds portfolio/reputation in target niche",
                "Easy job in dead time"
            ]
        },
        "negotiate_or_decline": {
            "criteria": [
                "Effective rate < 70% of target rate",
                "Customer has history of slow payment",
                "Scope creep risk high",
                "Requires skills/tools you don't have"
            ],
            "action": "Increase quote 50% or politely decline"
        },
        "strategic_accept": {
            "criteria": [
                "New area/niche you want to enter",
                "Referral from A-grade customer",
                "Portfolio building opportunity",
                "Fills gap in slow period"
            ],
            "note": "Accept at lower margin but set boundaries"
        }
    },
    "small_job_threshold": {
        "rule": "Minimum job size = 3 hours at your rate OR charge premium",
        "example": "If rate is $120/hr, minimum job is $360 OR charge $180/hr for 1-2hr jobs",
        "reasoning": "Small jobs have proportionally higher overhead (travel, quotes, invoicing)"
    },
    "scripts": {
        "declining_small_job": """Thanks for thinking of us. Our minimum job size is [AMOUNT] to make it viable with travel and setup.

For smaller work, I'd recommend [LOCAL HANDYMAN / NEWER TRADIE] - they might be a better fit.

But if you have anything bigger down the track, definitely give us a call.""",

        "declining_bad_fit": """I appreciate the inquiry, but [REASON - outside our area / not our specialty / booked solid].

I'd hate to take it on and not do it justice. Try [RECOMMENDATION] - they'd be perfect for this.

Cheers and good luck with the project!"""
    }
}

# ============================================================================
# 2. LEAD GENERATION & CONVERSION FRAMEWORKS
# ============================================================================

REVIEW_ACQUISITION_FRAMEWORK = {
    "name": "Systematic Review Generation System",
    "current_reality": {
        "problem": "76% of tradies have <10 Google reviews",
        "impact": "Losing 40-60% of Google search leads to competitors with 25+ reviews",
        "opportunity": "3-5 additional jobs per month by going from 8 to 25+ reviews"
    },
    "proven_system": {
        "timing": "Day 3 after job completion (CRITICAL - highest response rate)",
        "method": "SMS with direct Google review link (79% open rate vs 21% email)",
        "optimal_script": """Hey [FIRST_NAME], thanks again for letting us [SPECIFIC_THING - e.g., "fix the switchboard"].

Hope everything's working great!

If you're happy with the job, a quick Google review really helps us out: [DIRECT_LINK]

Cheers,
[YOUR_NAME]""",

        "why_day_3": "Day 1: Too soon, job fresh. Day 3: Used the work, satisfaction confirmed, easy yes. Day 7+: Forgotten, response rate drops 60%",

        "direct_link": "Get from: google.com/business → Your profile → Get more reviews → Copy link",

        "response_rate": {
            "day_3_sms": "15-22%",
            "day_7_email": "5-8%",
            "random_asking": "2-4%"
        }
    },
    "for_unhappy_customers": {
        "timing": "Day 1 follow-up call",
        "goal": "Fix issue BEFORE they review",
        "script": """Hey [NAME], just wanted to check everything's all good with the [JOB]?

[If issue] → Fix immediately, over-deliver
[If happy] → Day 3 review request"""
    },
    "responding_to_reviews": {
        "all_reviews": "Respond within 24 hours",
        "positive_reviews": """Thanks [NAME]! Really appreciate you taking the time to leave a review.

Glad we could [SPECIFIC_THING]. Looking forward to working with you again!""",

        "negative_reviews": """Thanks for the feedback [NAME]. We're disappointed we didn't meet expectations.

[If fixable] We'd like to make this right - I'll call you today to discuss.
[If unfixable] We've taken your feedback on board to improve our service.

Please reach out if there's anything we can do."""
    },
    "goal": "25+ reviews with 4.6+ rating within 6 months"
}

LEAD_RESPONSE_FRAMEWORK = {
    "name": "Speed-to-Quote System",
    "research_data": {
        "source": "Hipages Lead Response Study + ServiceM8 data",
        "findings": {
            "under_2hrs": "21% quote-to-job conversion",
            "2_24hrs": "14% conversion",
            "24_48hrs": "9% conversion",
            "over_48hrs": "5% conversion"
        },
        "key_insight": "First responder wins 60% of the time in competitive markets"
    },
    "optimal_system": {
        "immediate_response": {
            "within": "30 minutes of inquiry",
            "method": "Text or call (not email)",
            "message": """Hi [NAME], got your inquiry about [JOB].

I can take a look [TODAY/TOMORROW] around [TIME] and give you a price on the spot.

Work for you?

[YOUR NAME] - [PHONE]"""
        },
        "quote_delivery": {
            "timing": "Within 24 hours of site visit",
            "method": "Text with PDF (easy to forward/save) + follow-up call",
            "format": "Clean, professional, itemized, single page"
        },
        "follow_up_sequence": {
            "day_1": "Quote sent via text/email + immediate call",
            "day_3": "Follow-up text: 'Hey [NAME], just checking if you had any questions about the quote?'",
            "day_7": "Final call: 'Hi [NAME], following up on the [JOB] quote. Still interested or have you gone another direction?'",
            "after_day_7": "Mark lost, ask why if willing to share"
        }
    },
    "quote_format_best_practices": {
        "include": [
            "Itemized breakdown (transparency builds trust)",
            "Start date and estimated duration",
            "Payment terms (deposit + final)",
            "Warranty/guarantee details",
            "What's included vs excluded (scope clarity)",
            "Licensing/insurance mentions",
            "Expiry date (creates urgency)"
        ],
        "avoid": [
            "Vague 'supply and install' lumps",
            "No timeline",
            "Unclear payment terms",
            "Spelling/formatting errors (looks amateur)"
        ]
    }
}

GOOGLE_BUSINESS_OPTIMIZATION = {
    "name": "Google Business Profile Optimization",
    "impact": "60-70% of local service searches happen on Google",
    "critical_elements": {
        "photos": {
            "upload_frequency": "Weekly",
            "types": "Before/after, team, truck/van with branding, completed projects",
            "quantity_target": "30+ photos",
            "impact": "Profiles with 30+ photos get 42% more direction requests"
        },
        "posts": {
            "frequency": "2-3x per week",
            "content": "Completed projects, tips, seasonal reminders (e.g., 'Get your AC serviced before summer')",
            "include": "Photo + 100-150 words + call-to-action",
            "impact": "Active profiles rank higher in local search"
        },
        "business_description": {
            "include": [
                "Trade + location (SEO keywords)",
                "Years in business",
                "Specific services",
                "Service area",
                "Licensing/certifications",
                "What makes you different"
            ],
            "example": """Licensed electrician servicing Sydney's Northern Beaches since 2018.

Specializing in: Switchboard upgrades, EV charger installations, solar connections, rewires, and all residential electrical work.

Family-owned, fully insured, guaranteed quality. Available 7 days - call [PHONE]."""
        },
        "questions_and_answers": {
            "action": "Seed with 5-10 common questions YOU answer",
            "examples": [
                "Do you charge a call-out fee?",
                "What areas do you service?",
                "Are you licensed and insured?",
                "Do you offer emergency services?",
                "What payment methods do you accept?"
            ],
            "benefit": "Controls narrative before customers ask"
        }
    }
}

# ============================================================================
# 3. OPERATIONS & EFFICIENCY FRAMEWORKS
# ============================================================================

TIME_AUDIT_FRAMEWORK = {
    "name": "Weekly Time Allocation Analysis",
    "benchmark_comparison": {
        "excellent_operator": {
            "billable_work": 65,
            "quoting": 10,
            "admin": 8,
            "travel": 10,
            "business_dev": 5,
            "training": 2
        },
        "typical_tradie": {
            "billable_work": 52,
            "quoting": 15,
            "admin": 15,
            "travel": 13,
            "business_dev": 3,
            "training": 2
        },
        "struggling_tradie": {
            "billable_work": 40,
            "quoting": 18,
            "admin": 20,
            "travel": 15,
            "business_dev": 5,
            "training": 2
        }
    },
    "efficiency_levers": {
        "increase_billable": {
            "tactic": "Job clustering by location",
            "method": "Book jobs in same suburb on same day",
            "impact": "Save 5-8 hours/week travel time",
            "implementation": "Use map pins on calendar/scheduling software"
        },
        "reduce_admin": {
            "tactic": "Same-day invoicing automation",
            "method": "Invoice on-site before leaving (phone/tablet)",
            "impact": "Save 3-5 hours/week",
            "tools": "Tradify, ServiceM8, Simpro (all have mobile invoicing)"
        },
        "reduce_quoting_time": {
            "tactic": "Template-based quoting",
            "method": "Pre-built quotes for common jobs with variable fields",
            "impact": "Quote time from 45min → 10min",
            "example": "Switchboard upgrade template: Fill in [PANEL_TYPE], [CIRCUIT_COUNT], [SURGE_PROTECTION] → Generate"
        }
    },
    "automation_opportunities": [
        "Job confirmation texts (automated via ServiceM8/Tradify)",
        "Invoice reminders (auto-send Day 7, 14, 21)",
        "Review requests (auto-send Day 3 post-job)",
        "Quote follow-ups (auto-schedule in CRM)"
    ]
}

CUSTOMER_GRADING_FRAMEWORK = {
    "name": "A/B/C/Fire Customer Classification",
    "purpose": "Focus energy on profitable relationships, minimize time on draining ones",
    "grading_criteria": {
        "A_grade": {
            "characteristics": [
                "High revenue (top 20% of customers)",
                "Repeat business (3+ jobs per year)",
                "Pays on time (<7 days)",
                "Refers others",
                "Easy to work with",
                "Good job margins"
            ],
            "action": "Nurture actively - call quarterly, priority scheduling, special treatment",
            "pricing": "Maintain or slight discount for loyalty"
        },
        "B_grade": {
            "characteristics": [
                "Decent revenue",
                "Occasional repeat business",
                "Pays normally (7-14 days)",
                "No major issues"
            ],
            "action": "Maintain relationship - occasional check-ins, good service",
            "pricing": "Standard rates"
        },
        "C_grade": {
            "characteristics": [
                "Low revenue (<$500/year)",
                "One-off jobs",
                "Slow payment (14-30 days)",
                "High effort for low return",
                "Price sensitive"
            ],
            "action": "Deprioritize - fit around better work, consider minimum job sizes",
            "pricing": "Full rate + call-out, or decline"
        },
        "Fire": {
            "characteristics": [
                "Chronic slow/no payment (>30 days)",
                "Abusive or unreasonable",
                "Constant scope creep/complaints",
                "Jobs consistently lose money",
                "Damage to reputation risk"
            ],
            "action": "Terminate relationship professionally",
            "script": """Thanks for thinking of us, but I don't think we're the right fit for this project.

I'd recommend [ALTERNATIVE] - they might be better suited to your needs.

All the best!"""
        }
    },
    "annual_review_process": {
        "frequency": "Quarterly",
        "action": "Review all customers, reclassify, adjust approach",
        "impact": "Spend 80% of time on A+B grade (Pareto principle)"
    }
}

# ============================================================================
# 4. CASH FLOW OPTIMIZATION FRAMEWORKS
# ============================================================================

PAYMENT_TERMS_FRAMEWORK = {
    "name": "Cash Flow Optimization Through Payment Structure",
    "problem": "Most tradies have 30-60 day cash flow gaps",
    "optimal_structure": {
        "small_jobs": {
            "under_1000": "Full payment on completion",
            "method": "Bank transfer, card, or cash on the day",
            "script": "Payment's due on completion - bank transfer or card work for you?"
        },
        "medium_jobs": {
            "1000_5000": "50% deposit, 50% on completion",
            "reasoning": "Covers materials + locks in commitment",
            "script": "We take a 50% deposit to secure the booking and cover materials, balance due when we're done."
        },
        "large_jobs": {
            "over_5000": "Deposit + progress payments",
            "structure": "30% deposit, 40% at midpoint, 30% completion",
            "script": "For larger projects we work on a progress payment structure: [BREAKDOWN]. Keeps everything fair for both sides."
        }
    },
    "late_payment_sequence": {
        "day_7": {
            "action": "Friendly text reminder",
            "message": "Hi [NAME], just a reminder the invoice for [JOB] was due [DATE]. Can you let me know when you'll be settling up? Cheers!"
        },
        "day_14": {
            "action": "Phone call",
            "approach": "Assume good intent, ask if there's an issue",
            "script": "Hey [NAME], following up on the invoice. Is everything okay with the work? Just want to make sure there's no issues."
        },
        "day_21": {
            "action": "Formal email + final notice",
            "tone": "Professional but firm",
            "include": "Late fees (if terms allow), next steps"
        },
        "day_30": {
            "action": "Collections process or write-off",
            "decision": "Is it worth pursuing? Or cut losses and fire customer?"
        }
    },
    "preventing_late_payment": {
        "clear_terms": "Put payment terms on quote AND invoice",
        "quality_work": "Problems with work = excuse for delayed payment",
        "invoice_timing": "Invoice same day as completion while top-of-mind",
        "payment_convenience": "Accept card/online payment (removes 'need to go to bank' excuse)"
    }
}

# ============================================================================
# 5. GROWTH & SCALING FRAMEWORKS
# ============================================================================

HIRING_READINESS_FRAMEWORK = {
    "name": "When to Hire Your First Employee/Apprentice",
    "critical_metrics": {
        "revenue": {
            "minimum": "1.8x your desired salary",
            "explanation": "If you want $100k, need $180k revenue before hiring",
            "reasoning": "Employee costs ~$60-80k (wages + super + insurance + tools), you need buffer"
        },
        "work_pipeline": {
            "minimum": "8+ weeks of confirmed work",
            "explanation": "Can't hire based on 'hopeful' work",
            "test": "Would you be comfortable with this workload yourself for 6 months?"
        },
        "systems": {
            "requirements": [
                "Job management software in place",
                "Standard operating procedures written",
                "Quote/invoice templates ready",
                "Safety systems documented",
                "Insurance updated for employees"
            ]
        }
    },
    "apprentice_vs_licensed_tradie": {
        "apprentice": {
            "cost": "$25-35k/year all-in",
            "pros": "Cheap, moldable, loyal if treated well",
            "cons": "Can't work unsupervised, training overhead, 4-year commitment",
            "when": "Revenue $150k+, consistent work, can supervise daily"
        },
        "licensed_tradie": {
            "cost": "$70-90k/year all-in",
            "pros": "Productive immediately, can work independently, handles complex jobs",
            "cons": "Expensive, might leave after training, expectations higher",
            "when": "Revenue $250k+, more work than you can handle, need immediate capacity"
        }
    },
    "revenue_model": {
        "solo": "You = 100% capacity, income = your billable hours × rate",
        "with_employee": "You = 60% billable (managing + working), Employee = 80% billable",
        "required_rate": "Must charge enough that employee's 80% covers their cost + profit"
    }
}

SPECIALIZATION_FRAMEWORK = {
    "name": "Niche Specialization Strategy",
    "principle": "Riches in niches - specialists charge 20-40% more than generalists",
    "examples_by_trade": {
        "electrician": [
            "Solar + battery specialist",
            "EV charger installations",
            "Data/communications cabling",
            "Level 2 ASP (overhead/underground)",
            "Smart home automation",
            "Commercial fit-outs"
        ],
        "plumber": [
            "Gas fitting specialist",
            "Bathroom renovations",
            "Backflow prevention",
            "Hot water system expert",
            "Roof plumbing",
            "Fire services maintenance"
        ],
        "carpenter": [
            "Heritage restoration",
            "Custom cabinetry",
            "Deck/outdoor structures",
            "Shopfitting",
            "Structural work"
        ]
    },
    "benefits": {
        "premium_pricing": "Specialists charge 20-40% more",
        "less_competition": "Fewer people doing the exact thing",
        "better_customers": "People seeking specialists are less price-sensitive",
        "referrability": "Easy to remember and refer ('the EV charger guy')",
        "efficiency": "Repeat similar jobs = faster = higher effective rate"
    },
    "how_to_transition": {
        "step_1": "Identify your highest-margin job types from data",
        "step_2": "Pick ONE to focus on (don't dilute)",
        "step_3": "Still accept general work, but market the specialty",
        "step_4": "Build portfolio of specialty work",
        "step_5": "Increase specialty pricing as reputation grows",
        "timeline": "12-18 months to transition fully"
    }
}

# ============================================================================
# 6. TRADIE-SPECIFIC GROWTH TACTICS
# ============================================================================

TRADIE_GROWTH_TACTICS = {
    "partnership_referrals": {
        "principle": "Tradies refer tradies - build a referral network",
        "method": {
            "identify_complementary": "Electrician → Plumber, Carpenter, HVAC",
            "build_relationship": "Coffee catch-up, refer work first (give before receive)",
            "formalize": "10% referral fee or reciprocal agreement",
            "maintain": "Quarterly check-in, keep them updated on projects"
        },
        "script": """Hey [NAME], I often have customers asking for a good [TRADE].

Mind if I pass your name along? Happy to do the same if you ever need a [YOUR TRADE].

Want to grab a coffee sometime and chat?"""
    },

    "builder_relationships": {
        "principle": "Builders = consistent work pipeline",
        "target": "Small-medium builders (2-10 projects/year)",
        "pitch": "Reliability + quality + speed",
        "how_to_break_in": [
            "Offer to help on a small job (prove yourself)",
            "Be available when their usual tradie isn't",
            "Never ghost them or delay timeline",
            "Transparent pricing (no surprises)"
        ],
        "value": "One good builder = $50-150k/year consistent work"
    },

    "property_manager_pipeline": {
        "principle": "Property managers = recurring maintenance work",
        "target": "Local agencies managing 50+ properties",
        "pitch": "Fast response + tenant-friendly + detailed reporting",
        "requirements": [
            "Respond within 2 hours",
            "Can invoice directly to agency (not tenant)",
            "Provide photo evidence of work",
            "Quotes upfront (tenants don't approve big expenses)"
        ],
        "value": "One agency = 10-20 call-outs/month"
    },

    "real_estate_agent_staging": {
        "principle": "Agents need fast cosmetic fixes for auctions",
        "services": "Pre-sale repairs, safety certs, cosmetic upgrades",
        "pitch": "Fast turnaround + reliable + neat work (presentation matters)",
        "how_to_approach": [
            "Target agents selling in your area",
            "Offer free property assessment for upcoming sales",
            "Provide 'pre-sale checklist' (positions you as expert)",
            "Fast quotes + 48hr turnaround commitment"
        ]
    },

    "strata_management": {
        "principle": "Strata = regular contract work for complexes",
        "target": "Complexes with 20-50+ units",
        "services": "Maintenance contracts, emergency call-outs, annual inspections",
        "pitch": "One point of contact + preventative maintenance + bulk pricing",
        "value": "One complex = $20-80k/year contract"
    },

    "local_business_maintenance": {
        "principle": "Businesses need regular maintenance (they have budgets)",
        "target": "Retail, cafes, gyms, offices, medical centers",
        "pitch": "After-hours service + preventative maintenance + fast response",
        "script": """Hi [BUSINESS], I'm [NAME], a local [TRADE].

I work with a few businesses in [AREA] on regular maintenance and emergency call-outs.

Mind if I drop by with my card? Happy to do a free safety check while I'm there.

Cheers!"""
    }
}

# ============================================================================
# IMPLEMENTATION TEMPLATES
# ============================================================================

WEEKLY_BUSINESS_ROUTINE = {
    "monday_morning": [
        "Review week's jobs (confirm times with customers)",
        "Check materials needed (order anything missing)",
        "Review cashflow (who owes money? chase if needed)"
    ],
    "wednesday_check": [
        "Mid-week pipeline check (enough work for next 2 weeks?)",
        "Follow up pending quotes",
        "Update Google Business Profile with this week's work photos"
    ],
    "friday_admin": [
        "Send all outstanding invoices",
        "Review week's completed jobs (any issues? send review requests)",
        "Schedule next week's jobs",
        "Review quote win rate (are you winning enough?)"
    ],
    "monthly_reviews": [
        "Calculate effective rate for month",
        "Grade customers (any new A's? any to Fire?)",
        "Review expenses (any surprises? unnecessary subscriptions?)",
        "Check progress toward revenue goal"
    ]
}

# ============================================================================
# EXPORT FOR USE IN PROMPTS
# ============================================================================

def get_framework(framework_name: str) -> dict:
    """Retrieve a specific framework by name."""
    frameworks = {
        "pricing_transition": PRICING_TRANSITION_FRAMEWORK,
        "call_out_fee": CALL_OUT_FEE_FRAMEWORK,
        "job_selection": JOB_SELECTION_FRAMEWORK,
        "review_acquisition": REVIEW_ACQUISITION_FRAMEWORK,
        "lead_response": LEAD_RESPONSE_FRAMEWORK,
        "google_optimization": GOOGLE_BUSINESS_OPTIMIZATION,
        "time_audit": TIME_AUDIT_FRAMEWORK,
        "customer_grading": CUSTOMER_GRADING_FRAMEWORK,
        "payment_terms": PAYMENT_TERMS_FRAMEWORK,
        "hiring_readiness": HIRING_READINESS_FRAMEWORK,
        "specialization": SPECIALIZATION_FRAMEWORK,
        "growth_tactics": TRADIE_GROWTH_TACTICS,
        "weekly_routine": WEEKLY_BUSINESS_ROUTINE
    }
    return frameworks.get(framework_name, {})


def get_all_frameworks() -> dict:
    """Get all frameworks for embedding in prompts."""
    return {
        "pricing": {
            "transition": PRICING_TRANSITION_FRAMEWORK,
            "call_out_fee": CALL_OUT_FEE_FRAMEWORK,
            "job_selection": JOB_SELECTION_FRAMEWORK
        },
        "lead_gen": {
            "reviews": REVIEW_ACQUISITION_FRAMEWORK,
            "response": LEAD_RESPONSE_FRAMEWORK,
            "google": GOOGLE_BUSINESS_OPTIMIZATION
        },
        "operations": {
            "time": TIME_AUDIT_FRAMEWORK,
            "customers": CUSTOMER_GRADING_FRAMEWORK,
            "payments": PAYMENT_TERMS_FRAMEWORK
        },
        "growth": {
            "hiring": HIRING_READINESS_FRAMEWORK,
            "specialization": SPECIALIZATION_FRAMEWORK,
            "tactics": TRADIE_GROWTH_TACTICS
        },
        "implementation": {
            "weekly_routine": WEEKLY_BUSINESS_ROUTINE
        }
    }


if __name__ == "__main__":
    # Test framework retrieval
    pricing = get_framework("pricing_transition")
    print(f"Pricing Transition Framework: {pricing['name']}")
    print(f"Expected customer loss: {pricing['expected_results']['customer_loss']}")
