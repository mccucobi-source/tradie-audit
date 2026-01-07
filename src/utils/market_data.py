"""
Market benchmark data for Australian tradies.
Updated for 2026 market conditions.

SOURCES:
- NECA (National Electrical Contractors Association)
- Master Plumbers Association
- HIA (Housing Industry Association)
- AIRAH (Australian Institute of Refrigeration, Air Conditioning and Heating)
- MBA (Master Builders Association)
- ServiceM8 industry reports
- Hipages market data
- Trade industry surveys 2025-2026

NOTES:
- Rates have increased 15-25% since 2023 due to:
  - Labor shortage (fewer apprentices, aging workforce)
  - Material cost increases
  - Insurance premium increases
  - Fuel cost volatility
  - Inflation catch-up
"""

# Hourly rate benchmarks by trade and location (AUD, 2026)
# These are CHARGED rates, not effective rates (which are typically 15-25% lower)
HOURLY_RATES = {
    "electrician": {
        "sydney": {"min": 115, "mid": 135, "max": 165, "premium": 200},
        "melbourne": {"min": 110, "mid": 130, "max": 155, "premium": 190},
        "brisbane": {"min": 105, "mid": 125, "max": 150, "premium": 180},
        "perth": {"min": 110, "mid": 130, "max": 155, "premium": 185},
        "adelaide": {"min": 100, "mid": 120, "max": 145, "premium": 175},
        "gold_coast": {"min": 105, "mid": 125, "max": 150, "premium": 180},
        "newcastle": {"min": 100, "mid": 120, "max": 145, "premium": 170},
        "regional_nsw": {"min": 95, "mid": 115, "max": 140, "premium": 165},
        "regional_vic": {"min": 95, "mid": 115, "max": 140, "premium": 165},
        "regional_qld": {"min": 90, "mid": 110, "max": 135, "premium": 160},
        "regional": {"min": 95, "mid": 115, "max": 140, "premium": 165},
        "default": {"min": 105, "mid": 125, "max": 150, "premium": 180}
    },
    "plumber": {
        "sydney": {"min": 110, "mid": 130, "max": 160, "premium": 195},
        "melbourne": {"min": 105, "mid": 125, "max": 150, "premium": 185},
        "brisbane": {"min": 100, "mid": 120, "max": 145, "premium": 175},
        "perth": {"min": 105, "mid": 125, "max": 150, "premium": 180},
        "adelaide": {"min": 95, "mid": 115, "max": 140, "premium": 170},
        "gold_coast": {"min": 100, "mid": 120, "max": 145, "premium": 175},
        "regional": {"min": 90, "mid": 110, "max": 135, "premium": 160},
        "default": {"min": 100, "mid": 120, "max": 145, "premium": 175}
    },
    "carpenter": {
        "sydney": {"min": 95, "mid": 115, "max": 140, "premium": 170},
        "melbourne": {"min": 90, "mid": 110, "max": 135, "premium": 165},
        "brisbane": {"min": 85, "mid": 105, "max": 130, "premium": 155},
        "perth": {"min": 90, "mid": 110, "max": 135, "premium": 160},
        "adelaide": {"min": 80, "mid": 100, "max": 125, "premium": 150},
        "regional": {"min": 75, "mid": 95, "max": 120, "premium": 145},
        "default": {"min": 85, "mid": 105, "max": 130, "premium": 155}
    },
    "hvac": {
        "sydney": {"min": 120, "mid": 140, "max": 170, "premium": 210},
        "melbourne": {"min": 115, "mid": 135, "max": 165, "premium": 200},
        "brisbane": {"min": 110, "mid": 130, "max": 155, "premium": 190},
        "perth": {"min": 115, "mid": 135, "max": 160, "premium": 195},
        "adelaide": {"min": 105, "mid": 125, "max": 150, "premium": 180},
        "regional": {"min": 100, "mid": 120, "max": 145, "premium": 175},
        "default": {"min": 110, "mid": 130, "max": 155, "premium": 190}
    },
    "builder": {
        "sydney": {"min": 90, "mid": 110, "max": 135, "premium": 165},
        "melbourne": {"min": 85, "mid": 105, "max": 130, "premium": 160},
        "brisbane": {"min": 80, "mid": 100, "max": 125, "premium": 150},
        "perth": {"min": 85, "mid": 105, "max": 130, "premium": 155},
        "adelaide": {"min": 75, "mid": 95, "max": 120, "premium": 145},
        "regional": {"min": 70, "mid": 90, "max": 115, "premium": 140},
        "default": {"min": 80, "mid": 100, "max": 125, "premium": 150}
    },
    "other": {
        "default": {"min": 85, "mid": 105, "max": 130, "premium": 160}
    }
}

# Specialization premiums (% above standard rate)
SPECIALIZATION_PREMIUMS = {
    "electrician": {
        "level_2_asp": 0.25,  # Level 2 Accredited Service Provider
        "solar_installer": 0.20,
        "ev_charger": 0.25,
        "data_cabling": 0.15,
        "industrial": 0.20,
        "hazardous_areas": 0.35,
        "emergency_24hr": 0.50
    },
    "plumber": {
        "gas_fitter": 0.20,
        "roof_plumber": 0.15,
        "backflow_prevention": 0.20,
        "fire_services": 0.25,
        "commercial": 0.15,
        "emergency_24hr": 0.50
    },
    "carpenter": {
        "heritage_restoration": 0.30,
        "custom_cabinetry": 0.25,
        "structural": 0.20,
        "formwork": 0.15,
        "shopfitting": 0.20
    },
    "hvac": {
        "commercial": 0.20,
        "refrigeration": 0.25,
        "clean_room": 0.35,
        "hospital_grade": 0.30,
        "emergency_24hr": 0.50
    }
}

# Material markup benchmarks (2026)
# Note: These have increased due to supply chain costs
MATERIAL_MARKUP = {
    "electrician": {"min": 0.25, "standard": 0.35, "premium": 0.45},
    "plumber": {"min": 0.25, "standard": 0.35, "premium": 0.45},
    "carpenter": {"min": 0.20, "standard": 0.30, "premium": 0.40},
    "hvac": {"min": 0.30, "standard": 0.40, "premium": 0.50},
    "builder": {"min": 0.15, "standard": 0.25, "premium": 0.35},
    "other": {"min": 0.20, "standard": 0.30, "premium": 0.40}
}

# Call-out fee benchmarks (2026)
CALL_OUT_FEES = {
    "electrician": {
        "standard": {"min": 95, "standard": 120, "premium": 150},
        "after_hours": {"min": 150, "standard": 180, "premium": 250},
        "emergency": {"min": 200, "standard": 250, "premium": 350}
    },
    "plumber": {
        "standard": {"min": 90, "standard": 115, "premium": 145},
        "after_hours": {"min": 145, "standard": 175, "premium": 240},
        "emergency": {"min": 195, "standard": 240, "premium": 340}
    },
    "carpenter": {
        "standard": {"min": 75, "standard": 95, "premium": 120},
        "after_hours": {"min": 120, "standard": 150, "premium": 200}
    },
    "hvac": {
        "standard": {"min": 100, "standard": 125, "premium": 160},
        "after_hours": {"min": 160, "standard": 200, "premium": 280},
        "emergency": {"min": 220, "standard": 280, "premium": 400}
    },
    "builder": {
        "standard": {"min": 65, "standard": 85, "premium": 110}
    },
    "other": {
        "standard": {"min": 75, "standard": 95, "premium": 120}
    }
}

# Quote win rate benchmarks
WIN_RATES = {
    "residential": {"poor": 0.20, "average": 0.35, "good": 0.45, "excellent": 0.55},
    "commercial": {"poor": 0.15, "average": 0.25, "good": 0.35, "excellent": 0.45},
    "government": {"poor": 0.10, "average": 0.20, "good": 0.30, "excellent": 0.40},
    "strata": {"poor": 0.25, "average": 0.40, "good": 0.50, "excellent": 0.60}
}

# Profit margin benchmarks (2026)
# Note: Margins have compressed slightly due to cost increases
PROFIT_MARGINS = {
    "excellent": 0.45,    # Top performers
    "healthy": 0.35,      # Target for solo tradie
    "acceptable": 0.25,   # Minimum acceptable
    "concerning": 0.18,   # Needs attention
    "critical": 0.10      # Urgent action needed
}

# Time allocation benchmarks (% of work week)
TIME_ALLOCATION = {
    "ideal": {
        "billable_work": 0.65,
        "quoting": 0.10,
        "admin": 0.08,
        "travel": 0.10,
        "business_development": 0.05,
        "training": 0.02
    },
    "typical": {
        "billable_work": 0.52,
        "quoting": 0.15,
        "admin": 0.15,
        "travel": 0.13,
        "business_development": 0.03,
        "training": 0.02
    },
    "struggling": {
        "billable_work": 0.40,
        "quoting": 0.18,
        "admin": 0.20,
        "travel": 0.15,
        "business_development": 0.05,
        "training": 0.02
    }
}

# Average job sizes by type (2026, AUD)
AVERAGE_JOB_SIZES = {
    "electrician": {
        "small_repair": {"min": 180, "avg": 350, "max": 600},
        "power_point_install": {"min": 150, "avg": 280, "max": 450},
        "switchboard_upgrade": {"min": 1800, "avg": 2800, "max": 4500},
        "full_rewire": {"min": 8000, "avg": 15000, "max": 35000},
        "solar_install": {"min": 6000, "avg": 12000, "max": 25000},
        "ev_charger": {"min": 1200, "avg": 2200, "max": 4000},
        "commercial_fit_out": {"min": 15000, "avg": 45000, "max": 150000}
    },
    "plumber": {
        "small_repair": {"min": 150, "avg": 320, "max": 550},
        "tap_replacement": {"min": 200, "avg": 380, "max": 600},
        "hot_water_system": {"min": 1500, "avg": 2500, "max": 4500},
        "bathroom_rough_in": {"min": 3500, "avg": 6500, "max": 12000},
        "full_bathroom": {"min": 8000, "avg": 18000, "max": 40000},
        "blocked_drain": {"min": 200, "avg": 450, "max": 1200},
        "gas_fitting": {"min": 400, "avg": 850, "max": 2000}
    }
}

# Operating cost benchmarks (annual, solo tradie)
OPERATING_COSTS = {
    "vehicle": {
        "fuel": {"min": 6000, "avg": 9500, "max": 15000},
        "insurance": {"min": 1800, "avg": 2800, "max": 4500},
        "rego_maintenance": {"min": 2500, "avg": 4000, "max": 6500},
        "finance": {"min": 0, "avg": 8000, "max": 18000}
    },
    "insurance": {
        "public_liability": {"min": 800, "avg": 1400, "max": 2500},
        "professional_indemnity": {"min": 600, "avg": 1100, "max": 2000},
        "tools_equipment": {"min": 400, "avg": 800, "max": 1500},
        "income_protection": {"min": 1500, "avg": 3000, "max": 5500}
    },
    "tools_equipment": {
        "replacement_upgrade": {"min": 2000, "avg": 5000, "max": 12000}
    },
    "software_subscriptions": {
        "accounting": {"min": 300, "avg": 600, "max": 1200},
        "job_management": {"min": 0, "avg": 800, "max": 2400},
        "other": {"min": 200, "avg": 600, "max": 1500}
    },
    "professional": {
        "accountant": {"min": 1200, "avg": 2500, "max": 5000},
        "licenses_memberships": {"min": 500, "avg": 1200, "max": 2500}
    }
}


def get_rate_benchmark(trade: str, location: str) -> dict:
    """Get hourly rate benchmark for trade and location."""
    trade = trade.lower().strip()
    location = location.lower().strip()
    
    # Normalize location names
    location_map = {
        "sydney": "sydney",
        "melbourne": "melbourne", 
        "brisbane": "brisbane",
        "perth": "perth",
        "adelaide": "adelaide",
        "gold coast": "gold_coast",
        "goldcoast": "gold_coast",
        "newcastle": "newcastle",
        "wollongong": "regional_nsw",
        "geelong": "regional_vic",
        "sunshine coast": "regional_qld",
        "canberra": "regional_nsw",
        "hobart": "regional",
        "darwin": "regional"
    }
    
    location = location_map.get(location, location)
    
    if trade not in HOURLY_RATES:
        trade = "other"
    
    trade_rates = HOURLY_RATES[trade]
    
    # Try to find location, fall back to regional, then default
    for loc in [location, "regional", "default"]:
        if loc in trade_rates:
            return trade_rates[loc]
    
    return trade_rates.get("default", {"min": 85, "mid": 105, "max": 130, "premium": 160})


def get_markup_benchmark(trade: str) -> dict:
    """Get material markup benchmark for trade."""
    trade = trade.lower().strip()
    return MATERIAL_MARKUP.get(trade, MATERIAL_MARKUP["other"])


def get_callout_benchmark(trade: str, call_type: str = "standard") -> dict:
    """Get call-out fee benchmark for trade."""
    trade = trade.lower().strip()
    call_type = call_type.lower().strip()
    
    trade_fees = CALL_OUT_FEES.get(trade, CALL_OUT_FEES["other"])
    return trade_fees.get(call_type, trade_fees.get("standard", {"min": 75, "standard": 95, "premium": 120}))


def calculate_rate_gap(current_rate: float, trade: str, location: str) -> dict:
    """
    Calculate the gap between current rate and market benchmark.
    
    Returns:
        dict with gap_amount, gap_percentage, and recommendation
    """
    benchmark = get_rate_benchmark(trade, location)
    mid_rate = benchmark["mid"]
    
    gap = mid_rate - current_rate
    gap_pct = (gap / mid_rate) * 100 if mid_rate > 0 else 0
    
    if current_rate >= benchmark.get("premium", benchmark["max"] * 1.2):
        recommendation = "premium_pricing"
        status = "premium"
        urgency = "none"
    elif current_rate >= benchmark["max"]:
        recommendation = "at_premium"
        status = "above_market"
        urgency = "none"
    elif current_rate >= benchmark["mid"]:
        recommendation = "competitive"
        status = "at_market"
        urgency = "low"
    elif current_rate >= benchmark["min"]:
        recommendation = "increase_recommended"
        status = "below_market"
        urgency = "medium"
    else:
        recommendation = "urgent_increase"
        status = "significantly_below_market"
        urgency = "high"
    
    return {
        "current_rate": current_rate,
        "benchmark_min": benchmark["min"],
        "benchmark_mid": benchmark["mid"],
        "benchmark_max": benchmark["max"],
        "benchmark_premium": benchmark.get("premium", benchmark["max"] * 1.2),
        "gap_amount": gap,
        "gap_percentage": gap_pct,
        "status": status,
        "recommendation": recommendation,
        "urgency": urgency,
        "suggested_rate": max(current_rate, benchmark["mid"]),
        "stretch_target": benchmark["max"]
    }


def estimate_annual_impact(
    current_rate: float,
    suggested_rate: float,
    billable_hours_per_week: float = 28,
    weeks_per_year: int = 48,
    customer_retention: float = 0.85
) -> dict:
    """
    Estimate annual revenue impact from rate increase.
    
    Args:
        current_rate: Current hourly rate
        suggested_rate: New target rate
        billable_hours_per_week: Actual billable hours (not total hours worked)
        weeks_per_year: Working weeks (typically 48)
        customer_retention: Expected retention after price increase (0.85 = 15% loss)
    
    Returns:
        dict with gross_impact, conservative_impact, best_case_impact
    """
    annual_hours = billable_hours_per_week * weeks_per_year
    rate_increase = suggested_rate - current_rate
    
    gross_impact = rate_increase * annual_hours
    conservative_impact = gross_impact * customer_retention * 0.85  # Extra 15% buffer
    best_case_impact = gross_impact * 0.95  # 5% loss only
    
    return {
        "rate_increase": rate_increase,
        "annual_billable_hours": annual_hours,
        "gross_impact": gross_impact,
        "conservative_impact": conservative_impact,
        "best_case_impact": best_case_impact,
        "assumed_retention": customer_retention,
        "calculation": f"${rate_increase:.0f}/hr × {annual_hours:.0f} hours × {customer_retention:.0%} retention = ${conservative_impact:,.0f}"
    }


def get_efficiency_benchmark(trade: str) -> dict:
    """Get billable efficiency benchmarks."""
    return {
        "excellent": 0.68,
        "good": 0.60,
        "average": 0.52,
        "poor": 0.40,
        "note": "Billable hours as % of total hours worked"
    }


def calculate_effective_rate(total_revenue: float, total_hours_worked: float, billable_ratio: float = 0.55) -> dict:
    """
    Calculate effective hourly rate from revenue and hours.
    
    Args:
        total_revenue: Total revenue for period
        total_hours_worked: Total hours worked (including non-billable)
        billable_ratio: Estimated billable ratio (default 55%)
    
    Returns:
        dict with effective_rate, billable_hours, analysis
    """
    estimated_billable_hours = total_hours_worked * billable_ratio
    effective_rate = total_revenue / estimated_billable_hours if estimated_billable_hours > 0 else 0
    
    return {
        "total_revenue": total_revenue,
        "total_hours_worked": total_hours_worked,
        "estimated_billable_hours": estimated_billable_hours,
        "billable_ratio_used": billable_ratio,
        "effective_rate": effective_rate,
        "calculation": f"${total_revenue:,.0f} ÷ {estimated_billable_hours:,.0f} billable hours = ${effective_rate:.0f}/hr"
    }


# Example usage
if __name__ == "__main__":
    # Test the functions
    print("=== 2026 Market Benchmarks ===\n")
    
    result = calculate_rate_gap(95, "electrician", "sydney")
    print("Rate Gap Analysis (Electrician, Sydney, $95/hr):")
    for k, v in result.items():
        print(f"  {k}: {v}")
    
    print("\n")
    
    impact = estimate_annual_impact(95, result["suggested_rate"])
    print("Impact of Rate Increase:")
    for k, v in impact.items():
        print(f"  {k}: {v}")
    
    print("\n")
    
    effective = calculate_effective_rate(180000, 2400)
    print("Effective Rate Calculation:")
    for k, v in effective.items():
        print(f"  {k}: {v}")
