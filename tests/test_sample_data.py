"""
Test with sample data to verify the pipeline works.
Run this after setting up your ANTHROPIC_API_KEY.
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv()


def create_sample_invoice_csv():
    """Create a sample invoice CSV for testing."""
    sample_dir = project_root / "data" / "sample_test"
    sample_dir.mkdir(parents=True, exist_ok=True)
    
    # Sample invoice data
    invoice_csv = """Invoice Number,Date,Customer,Description,Amount,Status
INV-001,2024-01-15,Smith Residence,Kitchen rewire - complete,2850,Paid
INV-002,2024-01-22,Jones Commercial,Switchboard upgrade,5200,Paid
INV-003,2024-02-01,Brown Family,Smoke alarm installation,450,Paid
INV-004,2024-02-08,Wilson Office,LED lighting retrofit,3800,Paid
INV-005,2024-02-15,Taylor Property,Power point installations x8,1200,Paid
INV-006,2024-02-20,Anderson Home,Ceiling fan installation x3,650,Paid
INV-007,2024-03-01,Garcia Industrial,3-phase installation,8500,Paid
INV-008,2024-03-10,Martinez Shop,Shop fitout - electrical,4200,Paid
INV-009,2024-03-18,Robinson House,Hot water system wiring,380,Paid
INV-010,2024-03-25,Lee Apartment,Full unit rewire,6200,Paid
INV-011,2024-04-02,Nguyen Property,Security lighting,1850,Paid
INV-012,2024-04-10,Thompson Cafe,Kitchen equipment wiring,2400,Unpaid
INV-013,2024-04-18,Davis Warehouse,Industrial power upgrade,12500,Paid
INV-014,2024-04-25,Miller Home,EV charger installation,1800,Paid
INV-015,2024-05-02,Wilson Office,Additional GPOs x12,950,Paid
INV-016,2024-05-10,Clark Residence,Garden lighting,2200,Paid
INV-017,2024-05-18,White Factory,Motor circuit installation,4800,Paid
INV-018,2024-05-25,Hall Property,Safety switch upgrade,380,Paid
INV-019,2024-06-01,Young Building,Fire alarm testing,1200,Paid
INV-020,2024-06-10,King Commercial,Office partition wiring,3500,Paid
"""
    
    with open(sample_dir / "invoices_2024.csv", 'w') as f:
        f.write(invoice_csv)
    
    # Sample expense data
    expense_csv = """Date,Vendor,Description,Amount,Category
2024-01-10,Electrical Wholesale,Cable and conduit,1250,Materials
2024-01-15,BP Fuel,Fuel - January,420,Fuel
2024-01-20,Bunnings,Tools and accessories,380,Tools
2024-02-01,NECA,Insurance premium - Q1,1800,Insurance
2024-02-10,Electrical Wholesale,Switchboards and breakers,2200,Materials
2024-02-15,Ampol,Fuel - February,450,Fuel
2024-02-20,Officeworks,Printer and stationery,280,Admin
2024-03-01,Electrical Wholesale,LED fittings,1800,Materials
2024-03-10,Shell,Fuel - March,480,Fuel
2024-03-15,NECA,Training course,450,Training
2024-04-01,Insurance Australia,Vehicle insurance,1200,Insurance
2024-04-10,Electrical Wholesale,General stock,1650,Materials
2024-04-15,BP Fuel,Fuel - April,440,Fuel
2024-05-01,Xero,Accounting software,60,Software
2024-05-10,Electrical Wholesale,Cable and fittings,1400,Materials
2024-05-15,Caltex,Fuel - May,460,Fuel
2024-05-20,Tool King,Drill replacement,850,Tools
2024-06-01,Electrical Wholesale,Smoke detectors,600,Materials
2024-06-10,BP Fuel,Fuel - June,430,Fuel
"""
    
    with open(sample_dir / "expenses_2024.csv", 'w') as f:
        f.write(expense_csv)
    
    # Sample quote data
    quote_csv = """Quote Number,Date,Customer,Description,Amount,Status,Notes
Q-001,2024-01-05,Brown Family,Kitchen rewire,3200,Lost,Customer went cheaper
Q-002,2024-01-12,Smith Residence,Kitchen rewire,2850,Won,
Q-003,2024-01-18,Chen Property,Full house rewire,18000,Lost,Too expensive apparently
Q-004,2024-02-01,Jones Commercial,Switchboard upgrade,5200,Won,
Q-005,2024-02-08,Park Building,Office fitout,8500,Lost,Went with bigger company
Q-006,2024-02-15,Taylor Property,Power points,1200,Won,
Q-007,2024-02-22,Anderson Home,Ceiling fans,650,Won,
Q-008,2024-03-01,Garcia Industrial,3-phase,8500,Won,
Q-009,2024-03-10,Various,Small jobs x5,2400,Won,Multiple small quotes
Q-010,2024-03-20,Lee Apartment,Unit rewire,6200,Won,
Q-011,2024-04-01,Roberts Home,Solar install,15000,Lost,Not our specialty
Q-012,2024-04-10,Davis Warehouse,Power upgrade,12500,Won,
Q-013,2024-04-20,Miller Home,EV charger,1800,Won,
Q-014,2024-05-01,Thompson Cafe,Kitchen wiring,2400,Won,
Q-015,2024-05-10,Clark Residence,Garden lights,2200,Won,
Q-016,2024-05-20,White Factory,Motor circuit,4800,Won,
Q-017,2024-06-01,Young Building,Fire alarm,1200,Won,
Q-018,2024-06-05,Patel Office,Full fitout,22000,Pending,Waiting on response
"""
    
    with open(sample_dir / "quotes_2024.csv", 'w') as f:
        f.write(quote_csv)
    
    print(f"✓ Created sample data in: {sample_dir}")
    return sample_dir


def run_test_audit():
    """Run a test audit with sample data."""
    from src.agents.data_extractor import DataExtractor
    from src.agents.analyzer import Analyzer, BusinessContext
    from src.agents.report_generator import ReportGenerator
    
    # Check API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ANTHROPIC_API_KEY not set!")
        print("   Set it in your .env file or environment")
        return False
    
    print("\n" + "="*60)
    print("🧪 RUNNING TEST AUDIT")
    print("="*60)
    
    # Create sample data
    sample_dir = create_sample_invoice_csv()
    
    # Step 1: Extract
    print("\n📄 Step 1: Extracting data...")
    extractor = DataExtractor()
    results = extractor.extract_from_folder(str(sample_dir))
    combined = extractor.combine_results(results)
    
    print(f"   ✓ Transactions: {combined['summary']['total_transactions']}")
    print(f"   ✓ Revenue: ${combined['summary']['total_revenue']:,.2f}")
    print(f"   ✓ Expenses: ${combined['summary']['total_expenses']:,.2f}")
    
    # Step 2: Analyze
    print("\n📊 Step 2: Analyzing...")
    context = BusinessContext(
        trade_type="electrician",
        location="Sydney",
        years_in_business=5,
        current_rate=95,
        hours_per_week=50,
        revenue_goal=250000
    )
    
    analyzer = Analyzer()
    analysis = analyzer.analyze(combined, context)
    
    print(f"   ✓ Opportunity: ${analysis.guarantee_check.get('total_opportunity', 0):,.2f}")
    print(f"   ✓ Actions: {len(analysis.action_plan)}")
    
    # Step 3: Generate report
    print("\n📑 Step 3: Generating report...")
    generator = ReportGenerator(output_dir="./output")
    report = generator.generate_report(analysis, context, "Test Electrical")
    
    print(f"   ✓ HTML: {report['html_report']}")
    print(f"   ✓ Excel: {report['excel_report']}")
    
    # Summary
    print("\n" + "="*60)
    print("✅ TEST COMPLETE")
    print("="*60)
    
    total_cost = combined['summary']['total_extraction_cost'] + analysis.api_cost
    print(f"\n💰 Total API cost: ${total_cost:.2f}")
    print(f"📁 Output: {report['output_folder']}")
    
    opportunity = analysis.guarantee_check.get('total_opportunity', 0)
    print(f"\n🎯 Opportunity found: ${opportunity:,.2f}")
    print(f"   Meets $10k guarantee: {'✓ Yes' if opportunity >= 10000 else '✗ No'}")
    
    return True


if __name__ == "__main__":
    success = run_test_audit()
    sys.exit(0 if success else 1)

