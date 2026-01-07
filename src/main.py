#!/usr/bin/env python3
"""
Tradie Audit Agent - Main CLI
Run audits from the command line.
"""

import os
import sys
import argparse
import json
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv()

from src.agents.data_extractor import DataExtractor
from src.agents.analyzer import Analyzer, BusinessContext
from src.agents.report_generator import ReportGenerator


def run_audit(
    customer_name: str,
    data_folder: str,
    trade_type: str = "electrician",
    location: str = "Sydney",
    current_rate: float = 95.0,
    hours_per_week: int = 50,
    years_in_business: int = 5,
    revenue_goal: float = 250000.0,
    output_dir: str = "./output"
) -> dict:
    """
    Run a complete audit for a customer.
    
    Args:
        customer_name: Customer's business name
        data_folder: Path to folder containing invoices/expenses/quotes
        trade_type: Type of trade (electrician, plumber, etc.)
        location: City/region
        current_rate: Current hourly rate
        hours_per_week: Hours worked per week
        years_in_business: Years in business
        revenue_goal: Annual revenue goal
        output_dir: Where to save reports
    
    Returns:
        Dict with report paths and summary
    """
    print("\n" + "="*60)
    print(f"🔍 TRADIE PROFIT LEAK AUDIT")
    print(f"   Customer: {customer_name}")
    print("="*60)
    
    total_cost = 0.0
    
    # Step 1: Extract data
    print("\n📄 Step 1/3: Extracting data from documents...")
    extractor = DataExtractor()
    extraction_results = extractor.extract_from_folder(data_folder)
    combined_data = extractor.combine_results(extraction_results)
    total_cost += combined_data['summary']['total_extraction_cost']
    
    print(f"   ✓ Extracted {combined_data['summary']['total_transactions']} transactions")
    print(f"   ✓ Revenue: ${combined_data['summary']['total_revenue']:,.2f}")
    print(f"   ✓ Expenses: ${combined_data['summary']['total_expenses']:,.2f}")
    
    # Step 2: Analyze
    print("\n📊 Step 2/3: Analyzing profitability and finding opportunities...")
    context = BusinessContext(
        trade_type=trade_type,
        location=location,
        years_in_business=years_in_business,
        current_rate=current_rate,
        hours_per_week=hours_per_week,
        revenue_goal=revenue_goal
    )
    
    analyzer = Analyzer()
    analysis = analyzer.analyze(combined_data, context)
    total_cost += analysis.api_cost
    
    print(f"   ✓ Effective hourly rate: ${analysis.summary.get('effective_hourly_rate', 0):,.2f}")
    print(f"   ✓ Total opportunity found: ${analysis.guarantee_check.get('total_opportunity', 0):,.2f}")
    print(f"   ✓ Top actions identified: {len(analysis.action_plan)}")
    
    # Step 3: Generate reports
    print("\n📑 Step 3/3: Generating reports...")
    generator = ReportGenerator(output_dir=output_dir)
    report_result = generator.generate_report(analysis, context, customer_name)
    
    print(f"   ✓ HTML report: {report_result['html_report']}")
    print(f"   ✓ Excel workbook: {report_result['excel_report']}")
    
    # Summary
    print("\n" + "="*60)
    print("✅ AUDIT COMPLETE")
    print("="*60)
    print(f"\n💰 Total API cost: ${total_cost:.2f}")
    print(f"📁 Output folder: {report_result['output_folder']}")
    
    opportunity = analysis.guarantee_check.get('total_opportunity', 0)
    print(f"\n🎯 Opportunity identified: ${opportunity:,.2f}")
    
    if opportunity >= 10000:
        print("   ✓ Meets $10k guarantee!")
    else:
        print("   ⚠️  Below $10k - may need manual review")
    
    print("\n📋 Top 3 Quick Wins:")
    for i, action in enumerate(analysis.action_plan[:3], 1):
        print(f"   {i}. {action.get('action', 'N/A')}")
        print(f"      Impact: ${action.get('impact_annual', 0):,.2f}/year | Effort: {action.get('effort', 'N/A')}")
    
    return {
        'customer_name': customer_name,
        'output_folder': report_result['output_folder'],
        'html_report': report_result['html_report'],
        'excel_report': report_result['excel_report'],
        'total_opportunity': opportunity,
        'meets_guarantee': opportunity >= 10000,
        'api_cost': total_cost,
        'action_count': len(analysis.action_plan)
    }


def main():
    parser = argparse.ArgumentParser(
        description="Run a Tradie Profit Leak Audit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python src/main.py --customer "Dave's Electrical" --data ./data/dave
  python src/main.py --customer "Smith Plumbing" --data ./data/smith --trade plumber --location Melbourne
  python src/main.py --customer "Jones Carpentry" --data ./data/jones --rate 85 --hours 55
        """
    )
    
    parser.add_argument(
        "--customer", "-c",
        required=True,
        help="Customer/business name"
    )
    
    parser.add_argument(
        "--data", "-d",
        required=True,
        help="Path to folder containing customer's documents (invoices, expenses, quotes)"
    )
    
    parser.add_argument(
        "--trade", "-t",
        default="electrician",
        choices=["electrician", "plumber", "carpenter", "hvac", "builder", "other"],
        help="Type of trade (default: electrician)"
    )
    
    parser.add_argument(
        "--location", "-l",
        default="Sydney",
        help="City/region (default: Sydney)"
    )
    
    parser.add_argument(
        "--rate", "-r",
        type=float,
        default=95.0,
        help="Current hourly rate in AUD (default: 95)"
    )
    
    parser.add_argument(
        "--hours",
        type=int,
        default=50,
        help="Hours worked per week (default: 50)"
    )
    
    parser.add_argument(
        "--years",
        type=int,
        default=5,
        help="Years in business (default: 5)"
    )
    
    parser.add_argument(
        "--goal",
        type=float,
        default=250000,
        help="Revenue goal (default: 250000)"
    )
    
    parser.add_argument(
        "--output", "-o",
        default="./output",
        help="Output directory (default: ./output)"
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    
    args = parser.parse_args()
    
    # Check API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Error: ANTHROPIC_API_KEY not set")
        print("   Set it in your environment or .env file")
        sys.exit(1)
    
    # Check data folder exists
    if not Path(args.data).exists():
        print(f"❌ Error: Data folder not found: {args.data}")
        sys.exit(1)
    
    # Run audit
    try:
        result = run_audit(
            customer_name=args.customer,
            data_folder=args.data,
            trade_type=args.trade,
            location=args.location,
            current_rate=args.rate,
            hours_per_week=args.hours,
            years_in_business=args.years,
            revenue_goal=args.goal,
            output_dir=args.output
        )
        
        if args.json:
            print("\n" + json.dumps(result, indent=2))
        
        sys.exit(0)
        
    except Exception as e:
        print(f"\n❌ Error running audit: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

