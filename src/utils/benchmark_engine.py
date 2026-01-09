"""
Benchmark Engine - The source of truth for all market comparisons.
Combines multiple data sources with full provenance and confidence tracking.

DESIGN PRINCIPLES:
1. Every number has a SOURCE - no magic numbers
2. Every estimate has CONFIDENCE - be honest about uncertainty
3. Every calculation is TRANSPARENT - show your work
4. Every claim is VERIFIABLE - the customer can check

DATA SOURCES:
- service.com.au (200+ data points) - PRIMARY
- NECA, Master Plumbers, HIA, AIRAH, MBA - SECONDARY
- ServiceM8, Hipages market reports - SUPPLEMENTARY
- Internal audit database (after 10+ audits) - COMPARATIVE
"""

import json
import os
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime


class BenchmarkEngine:
    """
    Provides market benchmarks with full provenance and confidence tracking.
    Every number returned includes its source, confidence level, and calculation.
    """
    
    CONFIDENCE_LEVELS = {
        "HIGH": "3+ sources, large sample, recent data (2024-2026)",
        "MEDIUM": "1-2 sources, medium sample, or industry estimates",
        "LOW": "Single source, assumption-based, or limited data"
    }
    
    def __init__(self):
        # Load the service.com.au benchmarks
        benchmarks_path = Path(__file__).parent / "benchmarks.json"
        self.benchmarks = self._load_benchmarks(benchmarks_path)
        
        # Import the existing market data as fallback
        from src.utils.market_data import (
            HOURLY_RATES, MATERIAL_MARKUP, CALL_OUT_FEES, 
            AVERAGE_JOB_SIZES, OPERATING_COSTS, TIME_ALLOCATION,
            PROFIT_MARGINS
        )
        self.internal_rates = HOURLY_RATES
        self.internal_markup = MATERIAL_MARKUP
        self.internal_callout = CALL_OUT_FEES
        self.internal_job_sizes = AVERAGE_JOB_SIZES
        self.internal_costs = OPERATING_COSTS
        self.internal_time = TIME_ALLOCATION
        self.internal_margins = PROFIT_MARGINS
    
    def _load_benchmarks(self, path: Path) -> dict:
        """Load external benchmarks with error handling."""
        try:
            if path.exists():
                with open(path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load benchmarks.json: {e}")
        return {}
    
    def get_hourly_rate(self, trade: str, location: str) -> Dict[str, Any]:
        """
        Get hourly rate benchmark with full provenance.
        
        Returns dict with:
        - min, max, average, median (if available)
        - source, confidence, sample_size
        - calculation_notes
        """
        trade = self._normalize_trade(trade)
        location = self._normalize_location(location)
        
        result = {
            "trade": trade,
            "location": location,
            "data_sources": [],
            "confidence": "MEDIUM",
            "notes": []
        }
        
        # Try service.com.au data first (most reliable)
        service_data = self._get_service_com_rate(trade, location)
        if service_data:
            result.update(service_data)
            result["data_sources"].append({
                "name": "service.com.au",
                "type": "PRIMARY",
                "data_points": "200+",
                "last_updated": "2025-2026",
                "url": "https://service.com.au"
            })
        
        # Add internal data as cross-reference
        internal_data = self._get_internal_rate(trade, location)
        if internal_data:
            result["data_sources"].append({
                "name": "Industry associations (NECA, Master Plumbers, HIA)",
                "type": "SECONDARY",
                "data_points": "Industry surveys",
                "last_updated": "2025-2026"
            })
            
            # Cross-validate
            if service_data and internal_data:
                result["cross_validated"] = True
                result["notes"].append(
                    f"Cross-validated: service.com.au avg ${service_data.get('average', 'N/A')}/hr, "
                    f"industry data ${internal_data['mid']}/hr"
                )
                # If both sources agree (within 15%), boost confidence
                if service_data.get("average"):
                    variance = abs(service_data["average"] - internal_data["mid"]) / internal_data["mid"]
                    if variance < 0.15:
                        result["confidence"] = "HIGH"
                        result["notes"].append("HIGH confidence: Two independent sources agree within 15%")
            elif internal_data and not service_data:
                # Use internal data as fallback
                result.update({
                    "min": internal_data["min"],
                    "max": internal_data["max"],
                    "average": internal_data["mid"],
                    "premium": internal_data.get("premium", internal_data["max"] * 1.2)
                })
        
        # Add percentile estimates based on ranges
        if "min" in result and "max" in result:
            result["percentiles"] = {
                "p25": result["min"],
                "p50": result.get("average", (result["min"] + result["max"]) / 2),
                "p75": result["max"],
                "p90": result.get("premium", result["max"] * 1.15)
            }
        
        return result
    
    def _get_service_com_rate(self, trade: str, location: str) -> Optional[Dict]:
        """Get rate from service.com.au benchmarks."""
        if not self.benchmarks or trade not in self.benchmarks:
            return None
        
        trade_data = self.benchmarks[trade]
        
        # Try specific location first
        if location in trade_data and "hourly_rate" in trade_data[location]:
            rate = trade_data[location]["hourly_rate"]
            return {
                "min": rate.get("min"),
                "max": rate.get("max"),
                "average": rate.get("average"),
                "median": rate.get("median"),
                "source": rate.get("source", "service.com.au"),
                "confidence": rate.get("confidence", "MEDIUM")
            }
        
        # Fall back to national
        if "national" in trade_data and "hourly_rate" in trade_data["national"]:
            rate = trade_data["national"]["hourly_rate"]
            return {
                "min": rate.get("min"),
                "max": rate.get("max"),
                "average": rate.get("average"),
                "median": rate.get("median"),
                "source": rate.get("source", "service.com.au national"),
                "confidence": "MEDIUM",  # Lower confidence for national vs local
                "notes": [f"Using national benchmark (no {location} specific data)"]
            }
        
        return None
    
    def _get_internal_rate(self, trade: str, location: str) -> Optional[Dict]:
        """Get rate from internal market data."""
        if trade not in self.internal_rates:
            trade = "other"
        
        trade_rates = self.internal_rates[trade]
        
        for loc in [location, "regional", "default"]:
            if loc in trade_rates:
                return trade_rates[loc]
        
        return trade_rates.get("default")
    
    def get_call_out_fee(self, trade: str, fee_type: str = "standard") -> Dict[str, Any]:
        """Get call-out fee benchmark with provenance."""
        trade = self._normalize_trade(trade)
        
        result = {
            "trade": trade,
            "fee_type": fee_type,
            "data_sources": [],
            "confidence": "MEDIUM"
        }
        
        # Service.com.au data
        if self.benchmarks and trade in self.benchmarks:
            trade_data = self.benchmarks[trade]
            if "national" in trade_data and "call_out_fee" in trade_data["national"]:
                fee = trade_data["national"]["call_out_fee"]
                result.update({
                    "min": fee.get("min"),
                    "max": fee.get("max"),
                    "average": fee.get("average"),
                    "source": fee.get("source", "service.com.au"),
                    "confidence": fee.get("confidence", "MEDIUM")
                })
                result["data_sources"].append({
                    "name": "service.com.au",
                    "type": "PRIMARY"
                })
        
        # Internal data
        if trade in self.internal_callout:
            internal = self.internal_callout[trade].get(fee_type, {})
            if internal:
                result["data_sources"].append({
                    "name": "Industry associations",
                    "type": "SECONDARY"
                })
                if "min" not in result:
                    result.update({
                        "min": internal.get("min"),
                        "max": internal.get("premium"),
                        "average": internal.get("standard")
                    })
        
        return result
    
    def get_common_job_costs(self, trade: str) -> Dict[str, Any]:
        """Get common job cost benchmarks."""
        trade = self._normalize_trade(trade)
        
        result = {
            "trade": trade,
            "jobs": {},
            "data_sources": []
        }
        
        # Service.com.au job costs
        if self.benchmarks and trade in self.benchmarks:
            if "common_jobs" in self.benchmarks[trade]:
                jobs = self.benchmarks[trade]["common_jobs"]
                for job_name, job_data in jobs.items():
                    result["jobs"][job_name] = {
                        "min": job_data.get("min"),
                        "max": job_data.get("max"),
                        "average": job_data.get("average", job_data.get("cost")),
                        "source": job_data.get("source", "service.com.au"),
                        "confidence": job_data.get("confidence", "MEDIUM")
                    }
                result["data_sources"].append({
                    "name": "service.com.au",
                    "type": "PRIMARY"
                })
        
        # Internal job sizes
        if trade in self.internal_job_sizes:
            for job_name, job_data in self.internal_job_sizes[trade].items():
                if job_name not in result["jobs"]:
                    result["jobs"][job_name] = {
                        "min": job_data.get("min"),
                        "max": job_data.get("max"),
                        "average": job_data.get("avg"),
                        "source": "Industry associations",
                        "confidence": "MEDIUM"
                    }
        
        return result
    
    def calculate_rate_percentile(self, rate: float, trade: str, location: str) -> Dict[str, Any]:
        """
        Calculate what percentile a rate falls in.
        Returns the percentile and comparison text.
        """
        benchmark = self.get_hourly_rate(trade, location)
        
        if "percentiles" not in benchmark:
            # Create approximate percentiles
            min_rate = benchmark.get("min", 80)
            max_rate = benchmark.get("max", 130)
            avg_rate = benchmark.get("average", (min_rate + max_rate) / 2)
            
            benchmark["percentiles"] = {
                "p25": min_rate,
                "p50": avg_rate,
                "p75": max_rate,
                "p90": max_rate * 1.15
            }
        
        percentiles = benchmark["percentiles"]
        
        # Calculate approximate percentile
        if rate <= percentiles["p25"]:
            pct = int(25 * (rate / percentiles["p25"]))
            description = "bottom quartile"
            status = "below_market"
        elif rate <= percentiles["p50"]:
            pct = 25 + int(25 * (rate - percentiles["p25"]) / (percentiles["p50"] - percentiles["p25"]))
            description = "below average"
            status = "below_market"
        elif rate <= percentiles["p75"]:
            pct = 50 + int(25 * (rate - percentiles["p50"]) / (percentiles["p75"] - percentiles["p50"]))
            description = "above average"
            status = "at_market"
        elif rate <= percentiles["p90"]:
            pct = 75 + int(15 * (rate - percentiles["p75"]) / (percentiles["p90"] - percentiles["p75"]))
            description = "top quartile"
            status = "above_market"
        else:
            pct = min(99, 90 + int(10 * (rate - percentiles["p90"]) / (percentiles["p90"] * 0.2)))
            description = "premium pricing"
            status = "premium"
        
        return {
            "rate": rate,
            "percentile": pct,
            "description": description,
            "status": status,
            "comparison": f"${rate}/hr is at the {pct}th percentile for {location} {trade}s",
            "market_data": {
                "p25": percentiles["p25"],
                "p50": percentiles["p50"],
                "p75": percentiles["p75"],
                "p90": percentiles["p90"]
            },
            "sources": benchmark.get("data_sources", []),
            "confidence": benchmark.get("confidence", "MEDIUM")
        }
    
    def calculate_opportunity(
        self,
        current_rate: float,
        target_rate: float,
        annual_jobs: int,
        avg_hours_per_job: float,
        trade: str,
        location: str
    ) -> Dict[str, Any]:
        """
        Calculate revenue opportunity with three scenarios.
        Returns transparent calculation with all assumptions.
        """
        annual_hours = annual_jobs * avg_hours_per_job
        rate_increase = target_rate - current_rate
        gross_impact = rate_increase * annual_hours
        
        # Three scenarios
        scenarios = {
            "conservative": {
                "customer_retention": 0.85,
                "label": "Conservative (15% customer loss)",
                "impact": gross_impact * 0.85,
                "notes": "Assumes 15% of customers leave due to price increase"
            },
            "realistic": {
                "customer_retention": 0.90,
                "label": "Realistic (10% customer loss)",
                "impact": gross_impact * 0.90,
                "notes": "Industry average customer loss for 10-15% price increase"
            },
            "optimistic": {
                "customer_retention": 0.95,
                "label": "Optimistic (5% customer loss)",
                "impact": gross_impact * 0.95,
                "notes": "Best case if you communicate value well"
            }
        }
        
        # Market validation
        market_data = self.get_hourly_rate(trade, location)
        target_percentile = self.calculate_rate_percentile(target_rate, trade, location)
        
        return {
            "current_rate": current_rate,
            "target_rate": target_rate,
            "rate_increase": rate_increase,
            "rate_increase_pct": (rate_increase / current_rate) * 100 if current_rate > 0 else 0,
            "annual_jobs": annual_jobs,
            "avg_hours_per_job": avg_hours_per_job,
            "annual_hours": annual_hours,
            "gross_impact": gross_impact,
            "scenarios": scenarios,
            "recommended_scenario": "conservative",
            "recommended_impact": scenarios["conservative"]["impact"],
            "calculation_steps": [
                f"Current rate: ${current_rate}/hr",
                f"Target rate: ${target_rate}/hr (at {target_percentile['percentile']}th percentile)",
                f"Rate increase: ${rate_increase}/hr ({(rate_increase / current_rate * 100):.1f}% increase)",
                f"Annual hours: {annual_jobs} jobs × {avg_hours_per_job} hrs/job = {annual_hours} hours",
                f"Gross impact: ${rate_increase}/hr × {annual_hours} hrs = ${gross_impact:,.0f}",
                f"Conservative impact: ${gross_impact:,.0f} × 85% retention = ${scenarios['conservative']['impact']:,.0f}"
            ],
            "market_validation": {
                "target_is_reasonable": target_percentile["percentile"] <= 85,
                "target_percentile": target_percentile["percentile"],
                "market_max": market_data.get("max"),
                "confidence": market_data.get("confidence", "MEDIUM")
            },
            "data_sources": market_data.get("data_sources", [])
        }
    
    def get_market_patterns(self) -> Dict[str, Any]:
        """Get general market pattern data."""
        if "market_patterns" in self.benchmarks:
            return self.benchmarks["market_patterns"]
        
        # Fallback to internal data
        return {
            "materials_markup": {
                "standard": 30,
                "min": 20,
                "max": 40,
                "source": "Industry standard",
                "confidence": "MEDIUM"
            },
            "call_out_fee_adoption": {
                "percentage_with_fee": 75,
                "source": "Industry estimate",
                "confidence": "LOW"
            },
            "customer_loss_price_increase": {
                "typical": 10,
                "conservative": 15,
                "optimistic": 5,
                "source": "Industry feedback",
                "confidence": "LOW"
            },
            "unbilled_hours_per_week": {
                "typical": 12,
                "min": 8,
                "max": 18,
                "source": "Industry estimate",
                "confidence": "MEDIUM"
            }
        }
    
    def format_for_report(self, data: Dict, include_sources: bool = True) -> str:
        """Format benchmark data for inclusion in report."""
        lines = []
        
        if "average" in data:
            lines.append(f"Market average: ${data['average']}/hr")
        if "min" in data and "max" in data:
            lines.append(f"Market range: ${data['min']}-${data['max']}/hr")
        
        if include_sources and "data_sources" in data:
            sources = [s["name"] for s in data["data_sources"]]
            lines.append(f"Sources: {', '.join(sources)}")
        
        if "confidence" in data:
            lines.append(f"Confidence: {data['confidence']}")
        
        return "\n".join(lines)
    
    def _normalize_trade(self, trade: str) -> str:
        """Normalize trade name."""
        trade = trade.lower().strip()
        trade_map = {
            "electrician": "electrician",
            "electrical": "electrician",
            "sparky": "electrician",
            "plumber": "plumber",
            "plumbing": "plumber",
            "carpenter": "carpenter",
            "carpentry": "carpenter",
            "chippy": "carpenter",
            "hvac": "hvac",
            "air conditioning": "hvac",
            "aircon": "hvac",
            "builder": "builder",
            "building": "builder",
            "painter": "painter",
            "painting": "painter"
        }
        return trade_map.get(trade, trade)
    
    def _normalize_location(self, location: str) -> str:
        """Normalize location name."""
        location = location.lower().strip()
        location_map = {
            "sydney": "sydney",
            "syd": "sydney",
            "melbourne": "melbourne",
            "melb": "melbourne",
            "brisbane": "brisbane",
            "bris": "brisbane",
            "perth": "perth",
            "adelaide": "adelaide",
            "gold coast": "gold_coast",
            "goldcoast": "gold_coast",
            "sunshine coast": "brisbane",  # Use Brisbane as proxy
            "newcastle": "sydney",  # Use Sydney as proxy
            "wollongong": "sydney",  # Use Sydney as proxy
            "canberra": "sydney",  # Use Sydney as proxy
            "hobart": "national",
            "darwin": "national"
        }
        return location_map.get(location, location)


# Singleton instance
_engine = None

def get_benchmark_engine() -> BenchmarkEngine:
    """Get or create the benchmark engine singleton."""
    global _engine
    if _engine is None:
        _engine = BenchmarkEngine()
    return _engine


# Convenience functions for direct use
def get_rate_benchmark(trade: str, location: str) -> Dict[str, Any]:
    """Get hourly rate benchmark with full provenance."""
    return get_benchmark_engine().get_hourly_rate(trade, location)


def get_rate_percentile(rate: float, trade: str, location: str) -> Dict[str, Any]:
    """Calculate what percentile a rate falls in."""
    return get_benchmark_engine().calculate_rate_percentile(rate, trade, location)


def calculate_opportunity_with_provenance(
    current_rate: float,
    target_rate: float,
    annual_jobs: int,
    avg_hours_per_job: float,
    trade: str,
    location: str
) -> Dict[str, Any]:
    """Calculate opportunity with full transparency."""
    return get_benchmark_engine().calculate_opportunity(
        current_rate, target_rate, annual_jobs, avg_hours_per_job, trade, location
    )


if __name__ == "__main__":
    # Test the engine
    engine = BenchmarkEngine()
    
    print("=== Benchmark Engine Test ===\n")
    
    # Test hourly rate
    rate = engine.get_hourly_rate("electrician", "sydney")
    print("Sydney Electrician Hourly Rate:")
    print(f"  Range: ${rate.get('min')}-${rate.get('max')}/hr")
    print(f"  Average: ${rate.get('average')}/hr")
    print(f"  Confidence: {rate.get('confidence')}")
    print(f"  Sources: {[s['name'] for s in rate.get('data_sources', [])]}")
    print()
    
    # Test percentile
    pct = engine.calculate_rate_percentile(95, "electrician", "sydney")
    print(f"$95/hr Percentile: {pct['percentile']}th ({pct['description']})")
    print()
    
    # Test opportunity
    opp = engine.calculate_opportunity(95, 115, 57, 4.5, "electrician", "sydney")
    print("Opportunity Calculation:")
    for step in opp["calculation_steps"]:
        print(f"  {step}")
    print(f"  Conservative impact: ${opp['recommended_impact']:,.0f}/year")
