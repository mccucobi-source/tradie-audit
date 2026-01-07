"""
Customer Portal - The intake form customers fill out after payment.
Run with: streamlit run src/customer_portal.py
"""

import os
import sys
from pathlib import Path
import json
from datetime import datetime
import tempfile

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def load_css(file_path):
    """Load a CSS file and return its content."""
    with open(file_path) as f:
        return f.read()

css_file = Path(__file__).parent.parent / "styles" / "main.css"
st.markdown(f'<style>{load_css(css_file)}</style>', unsafe_allow_html=True)



def show_header():
    st.markdown("""
    <div class="section">
        <h1>🔧 Profit Leak Audit - Data Collection</h1>
        <p>Complete this form to start your audit. Takes about 15 minutes.</p>
    </div>
    """, unsafe_allow_html=True)


def step_business_info():
    """Step 1: Collect business information."""
    with st.container():
        st.markdown("## Step 1: Your Business Details")
        st.markdown("Tell us about your business so we can benchmark against similar tradies.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            business_name = st.text_input(
                "Business Name *",
                placeholder="e.g., Dave's Electrical Services",
                help="Your registered business name or trading name"
            )
            
            owner_name = st.text_input(
                "Your Name *",
                placeholder="e.g., Dave Smith",
                help="We'll use this to personalize your report"
            )
            
            email = st.text_input(
                "Email Address *",
                placeholder="dave@example.com",
                help="We'll send your report here"
            )
            
            phone = st.text_input(
                "Phone Number",
                placeholder="0412 345 678",
                help="In case we need to clarify anything"
            )
        
        with col2:
            trade_type = st.selectbox(
                "Your Trade *",
                options=[
                    "Select your trade...",
                    "Electrician",
                    "Plumber", 
                    "Carpenter / Joiner",
                    "HVAC / Air Conditioning",
                    "Builder",
                    "Painter",
                    "Roofer",
                    "Landscaper",
                    "Other"
                ],
                help="This helps us compare you to the right benchmarks"
            )
            
            if trade_type == "Other":
                trade_other = st.text_input("Please specify your trade:")
            
            location = st.text_input(
                "Primary Service Area *",
                placeholder="e.g., Sydney, Melbourne, Brisbane",
                help="City or region where you do most of your work"
            )
            
            years_in_business = st.selectbox(
                "Years in Business *",
                options=[
                    "Select...",
                    "1-2 years",
                    "3-5 years", 
                    "6-10 years",
                    "10+ years"
                ]
            )
            
            business_structure = st.selectbox(
                "Business Structure",
                options=[
                    "Sole trader",
                    "Partnership",
                    "Pty Ltd company",
                    "Trust"
                ]
            )
    
    return {
        'business_name': business_name,
        'owner_name': owner_name,
        'email': email,
        'phone': phone,
        'trade_type': trade_type if trade_type != "Select your trade..." else "",
        'location': location,
        'years_in_business': years_in_business if years_in_business != "Select..." else "",
        'business_structure': business_structure
    }


def step_current_numbers():
    """Step 2: Current business numbers."""
    with st.container():
        st.markdown("## Step 2: Your Current Numbers")
        st.markdown("Rough estimates are fine. This helps us understand your baseline.")
        st.info("💡 **Don't worry if you don't know exact numbers.** Your best guess is fine - we'll calculate the real numbers from your data.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💰 Revenue & Pricing")
            
            annual_revenue = st.selectbox(
                "Approximate Annual Revenue *",
                options=[
                    "Select...",
                    "Under $100k",
                    "$100k - $150k",
                    "$150k - $200k",
                    "$200k - $300k",
                    "$300k - $500k",
                    "$500k+"
                ],
                help="Your total invoiced amount for the last 12 months"
            )
            
            hourly_rate = st.number_input(
                "Your Standard Hourly Rate ($) *",
                min_value=0,
                max_value=500,
                value=0,
                step=5,
                help="What you typically charge per hour for labor"
            )
            
            call_out_fee = st.number_input(
                "Call-out / Service Fee ($)",
                min_value=0,
                max_value=300,
                value=0,
                step=5,
                help="If you charge one. Enter 0 if you don't."
            )
            
            material_markup = st.selectbox(
                "Material Markup",
                options=[
                    "I don't know",
                    "Cost price (0%)",
                    "5-10%",
                    "10-20%",
                    "20-30%",
                    "30%+"
                ],
                help="How much you add to materials when billing customers"
            )
        
        with col2:
            st.subheader("⏰ Time & Capacity")
            
            hours_per_week = st.slider(
                "Hours Worked Per Week *",
                min_value=20,
                max_value=80,
                value=50,
                help="Total hours including admin, travel, everything"
            )
            
            billable_percentage = st.slider(
                "Estimate: % Time on Actual Jobs",
                min_value=20,
                max_value=100,
                value=60,
                help="vs admin, quoting, travel, etc."
            )
            
            jobs_per_week = st.number_input(
                "Average Jobs Per Week",
                min_value=1,
                max_value=50,
                value=10,
                help="Roughly how many separate jobs you do"
            )
            
            employees = st.selectbox(
                "Team Size",
                options=[
                    "Just me",
                    "Me + 1 employee/apprentice",
                    "Me + 2-3 employees",
                    "4+ employees"
                ]
            )
    
    return {
        'annual_revenue': annual_revenue if annual_revenue != "Select..." else "",
        'hourly_rate': hourly_rate,
        'call_out_fee': call_out_fee,
        'material_markup': material_markup,
        'hours_per_week': hours_per_week,
        'billable_percentage': billable_percentage,
        'jobs_per_week': jobs_per_week,
        'employees': employees
    }


def step_goals_challenges():
    """Step 3: Goals and challenges."""
    with st.container():
        st.markdown("## Step 3: Your Goals & Challenges")
        st.markdown("This helps us focus on what matters most to you.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 Goals")
            
            revenue_goal = st.number_input(
                "Revenue Goal (next 12 months) $",
                min_value=0,
                max_value=2000000,
                value=250000,
                step=10000,
                help="What you'd like to hit"
            )
            
            ideal_hours = st.slider(
                "Ideal Hours Per Week",
                min_value=20,
                max_value=60,
                value=40,
                help="How much you'd LIKE to work"
            )
            
            main_goal = st.selectbox(
                "Primary Goal",
                options=[
                    "Increase profit (keep same hours)",
                    "Same profit, work fewer hours",
                    "Grow the business significantly",
                    "Prepare to hire first employee",
                    "Reduce stress / better work-life balance",
                    "Other"
                ]
            )
        
        with col2:
            st.subheader("😤 Biggest Frustrations")
            
            frustrations = st.multiselect(
                "What's frustrating you most? (select all that apply)",
                options=[
                    "Working too many hours",
                    "Not enough profit for the effort",
                    "Too much time on admin/paperwork",
                    "Chasing payments",
                    "Winning enough quotes",
                    "Finding good staff",
                    "Unreliable customers",
                    "Material costs eating into margins",
                    "Competition on price",
                    "Not sure where money goes"
                ]
            )
            
            biggest_question = st.text_area(
                "What's the #1 question you want answered?",
                placeholder="e.g., 'Am I charging enough?' or 'Which jobs should I stop doing?'",
                help="We'll make sure to address this in your report"
            )
    
    return {
        'revenue_goal': revenue_goal,
        'ideal_hours': ideal_hours,
        'main_goal': main_goal,
        'frustrations': frustrations,
        'biggest_question': biggest_question
    }


def step_file_upload():
    """Step 4: Upload financial documents."""
    with st.container():
        st.markdown("## Step 4: Upload Your Documents")
        st.markdown("This is where the magic happens. The more data, the better your audit.")
        st.warning("🔒 **Your data is secure and confidential.** We only use it for your audit and never share it. You can anonymize customer names if you prefer.")
        
        # Invoices
        st.subheader("📄 Invoices (Required)")
        st.markdown("""
        Upload your invoices from the last 12 months. Accepted formats: PDF, Excel, CSV
        
        **Where to get them:**
        - Export from Xero, MYOB, QuickBooks, or your invoicing app
        - PDF copies of invoices you've sent
        - Excel/CSV export if you use a spreadsheet
        """)
        
        invoices = st.file_uploader(
            "Drop invoice files here",
            type=['pdf', 'xlsx', 'xls', 'csv'],
            accept_multiple_files=True,
            key="invoices",
            help="The more invoices, the better the analysis"
        )
        
        if invoices:
            st.success(f"✓ {len(invoices)} invoice file(s) uploaded")
        
        st.divider()
        
        # Expenses
        st.subheader("💳 Expenses (Required)")
        st.markdown("""
        Upload your business expenses. Can be:
        - Bank statement exports (most accounting software can do this)
        - Credit card statements
        - Expense reports from your accounting software
        """)
        
        expenses = st.file_uploader(
            "Drop expense files here",
            type=['pdf', 'xlsx', 'xls', 'csv'],
            accept_multiple_files=True,
            key="expenses"
        )
        
        if expenses:
            st.success(f"✓ {len(expenses)} expense file(s) uploaded")
        
        st.divider()
        
        # Bank statements
        st.subheader("🏦 Bank Statements (Recommended)")
        st.markdown("""
        Your business bank statements help us see actual cash flow vs invoiced amounts.
        - Shows payment timing
        - Catches expenses not in your accounting software
        - Most accurate picture of profitability
        """)
        
        statements = st.file_uploader(
            "Drop bank statement files here",
            type=['pdf', 'xlsx', 'xls', 'csv'],
            accept_multiple_files=True,
            key="statements"
        )
        
        if statements:
            st.success(f"✓ {len(statements)} statement file(s) uploaded")
        
        st.divider()
        
        # Quotes
        st.subheader("📋 Quotes (If Available)")
        st.markdown("""
        If you track your quotes, upload them here. Include won AND lost quotes.
        This helps us analyze your win rate and pricing strategy.
        """)
        
        quotes = st.file_uploader(
            "Drop quote files here",
            type=['pdf', 'xlsx', 'xls', 'csv'],
            accept_multiple_files=True,
            key="quotes"
        )
        
        if quotes:
            st.success(f"✓ {len(quotes)} quote file(s) uploaded")
    
    return {
        'invoices': invoices or [],
        'expenses': expenses or [],
        'statements': statements or [],
        'quotes': quotes or []
    }


def step_final_details():
    """Step 5: Final details and submission."""
    with st.container():
        st.markdown("## Step 5: Final Details")
        st.markdown("Almost done! Just a few more questions.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            accounting_software = st.selectbox(
                "What accounting software do you use?",
                options=[
                    "Xero",
                    "MYOB",
                    "QuickBooks",
                    "FreshBooks",
                    "Wave",
                    "Spreadsheet / Excel",
                    "Paper / Manual",
                    "Other"
                ]
            )
            
            invoicing_software = st.selectbox(
                "What do you use for quotes/invoices?",
                options=[
                    "Same as accounting",
                    "ServiceM8",
                    "Tradify",
                    "Fergus",
                    "simPRO",
                    "AroFlo",
                    "Word/PDF templates",
                    "Other"
                ]
            )
        
        with col2:
            preferred_contact = st.selectbox(
                "Preferred contact method",
                options=["Email", "Phone", "Text/SMS"]
            )
            
            best_time = st.selectbox(
                "Best time for strategy call",
                options=[
                    "Morning (before 10am)",
                    "Mid-morning (10am-12pm)",
                    "Afternoon (12pm-3pm)",
                    "Late afternoon (3pm-5pm)",
                    "Evening (after 5pm)"
                ]
            )
        
        anything_else = st.text_area(
            "Anything else we should know?",
            placeholder="Any context about your business that would help us...",
            help="Seasonal patterns, recent changes, special circumstances, etc."
        )
        
        st.divider()
        
        # Agreement
        agree = st.checkbox(
            "I confirm this information is accurate to the best of my knowledge, and I agree to the audit terms.",
            help="We use this data only for your audit"
        )
    
    return {
        'accounting_software': accounting_software,
        'invoicing_software': invoicing_software,
        'preferred_contact': preferred_contact,
        'best_time': best_time,
        'anything_else': anything_else,
        'agreed': agree
    }


def save_submission(all_data: dict, files: dict) -> str:
    """Save the submission to disk and return the folder path."""
    from src.utils.file_handler import FileHandler
    
    handler = FileHandler(base_dir="./data")
    customer_folder = handler.create_customer_folder(all_data['business_info']['business_name'])
    
    # Save form data as JSON
    form_data_path = customer_folder / "intake_form.json"
    with open(form_data_path, 'w') as f:
        # Remove file objects before saving
        saveable_data = {k: v for k, v in all_data.items() if k != 'files'}
        json.dump(saveable_data, f, indent=2, default=str)
    
    # Save uploaded files
    file_categories = [
        ('invoices', 'invoices'),
        ('expenses', 'expenses'),
        ('statements', 'statements'),
        ('quotes', 'quotes')
    ]
    
    for key, folder_name in file_categories:
        for f in files.get(key, []):
            file_path = customer_folder / folder_name / f.name
            file_path.parent.mkdir(exist_ok=True)
            with open(file_path, 'wb') as out_file:
                out_file.write(f.read())
    
    return str(customer_folder)


def run_audit_from_submission(folder_path: str, business_info: dict, numbers: dict):
    """Run the actual audit on submitted data."""
    from src.agents.data_extractor import DataExtractor
    from src.agents.analyzer import Analyzer, BusinessContext
    from src.agents.report_generator import ReportGenerator
    
    # Parse hourly rate
    hourly_rate = numbers.get('hourly_rate', 95)
    if hourly_rate == 0:
        hourly_rate = 95  # Default
    
    # Parse years in business
    years_map = {
        "1-2 years": 2,
        "3-5 years": 4,
        "6-10 years": 8,
        "10+ years": 15
    }
    years = years_map.get(business_info.get('years_in_business', ''), 5)
    
    # Parse trade type
    trade = business_info.get('trade_type', 'electrician').lower()
    if 'electric' in trade:
        trade = 'electrician'
    elif 'plumb' in trade:
        trade = 'plumber'
    elif 'carp' in trade or 'join' in trade:
        trade = 'carpenter'
    elif 'hvac' in trade or 'air' in trade:
        trade = 'hvac'
    elif 'build' in trade:
        trade = 'builder'
    else:
        trade = 'other'
    
    # Build context
    context = BusinessContext(
        trade_type=trade,
        location=business_info.get('location', 'Sydney'),
        years_in_business=years,
        current_rate=hourly_rate,
        hours_per_week=numbers.get('hours_per_week', 50),
        revenue_goal=250000  # Default
    )
    
    # Run extraction
    extractor = DataExtractor()
    results = extractor.extract_from_folder(folder_path)
    combined = extractor.combine_results(results)
    
    # Run analysis
    analyzer = Analyzer()
    analysis = analyzer.analyze(combined, context)
    
    # Generate report
    generator = ReportGenerator(output_dir="./output")
    report = generator.generate_report(
        analysis, 
        context, 
        business_info.get('business_name', 'Customer')
    )
    
    return {
        'analysis': analysis,
        'report': report,
        'combined_data': combined
    }


def customer_portal_page():
    show_header()
    
    # Progress tracking
    if 'step' not in st.session_state:
        st.session_state.step = 1
    
    # Collect all data
    st.session_state.setdefault('business_info', {})
    st.session_state.setdefault('numbers', {})
    st.session_state.setdefault('goals', {})
    st.session_state.setdefault('files', {})
    st.session_state.setdefault('final', {})
    
    # Show progress
    progress = (st.session_state.step - 1) / 5
    st.markdown(f"""
    <div class="progress-bar">
        <div class="progress-fill" style="width: {progress * 100}%"></div>
    </div>
    <p style="text-align: center; color: #64748b; margin-bottom: 2rem;">
        Step {st.session_state.step} of 5
    </p>
    """, unsafe_allow_html=True)
    
    # Show current step
    if st.session_state.step == 1:
        st.session_state.business_info = step_business_info()
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Continue to Step 2 →", use_container_width=True):
                if (st.session_state.business_info.get('business_name') and 
                    st.session_state.business_info.get('trade_type') and
                    st.session_state.business_info.get('email')):
                    st.session_state.step = 2
                    st.rerun()
                else:
                    st.error("Please fill in required fields: Business Name, Trade, and Email")
    
    elif st.session_state.step == 2:
        st.session_state.numbers = step_current_numbers()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("← Back"):
                st.session_state.step = 1
                st.rerun()
        with col3:
            if st.button("Continue to Step 3 →", use_container_width=True):
                if st.session_state.numbers.get('hourly_rate', 0) > 0:
                    st.session_state.step = 3
                    st.rerun()
                else:
                    st.error("Please enter your hourly rate")
    
    elif st.session_state.step == 3:
        st.session_state.goals = step_goals_challenges()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("← Back"):
                st.session_state.step = 2
                st.rerun()
        with col3:
            if st.button("Continue to Step 4 →", use_container_width=True):
                st.session_state.step = 4
                st.rerun()
    
    elif st.session_state.step == 4:
        st.session_state.files = step_file_upload()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("← Back"):
                st.session_state.step = 3
                st.rerun()
        with col3:
            total_files = (len(st.session_state.files.get('invoices', [])) + 
                          len(st.session_state.files.get('expenses', [])))
            if st.button("Continue to Step 5 →", use_container_width=True):
                if total_files > 0:
                    st.session_state.step = 5
                    st.rerun()
                else:
                    st.error("Please upload at least your invoices OR expenses")
    
    elif st.session_state.step == 5:
        st.session_state.final = step_final_details()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("← Back"):
                st.session_state.step = 4
                st.rerun()
        with col3:
            if st.button("🚀 Submit & Start Audit", use_container_width=True, type="primary"):
                if st.session_state.final.get('agreed'):
                    # Save everything
                    all_data = {
                        'business_info': st.session_state.business_info,
                        'numbers': st.session_state.numbers,
                        'goals': st.session_state.goals,
                        'final': st.session_state.final,
                        'submitted_at': datetime.now().isoformat()
                    }
                    
                    with st.status("🔍 Processing your audit...", expanded=True) as status:
                        st.write("📁 Saving your files...")
                        folder_path = save_submission(all_data, st.session_state.files)
                        st.write(f"✓ Files saved to {folder_path}")
                        
                        st.write("🔬 Running audit analysis...")
                        try:
                            result = run_audit_from_submission(
                                folder_path,
                                st.session_state.business_info,
                                st.session_state.numbers
                            )
                            st.write("✓ Analysis complete!")
                            st.session_state.audit_result = result
                            status.update(label="✅ Audit Complete!", state="complete")
                        except Exception as e:
                            st.error(f"Error running audit: {e}")
                            status.update(label="⚠️ Error occurred", state="error")
                    
                    if 'audit_result' in st.session_state:
                        st.balloons()
                        st.success("""
                        ## 🎉 Your Audit is Complete!
                        
                        We've analyzed your data and generated your report. 
                        You'll receive an email shortly with:
                        - Your full Profit Leak Audit Report (PDF)
                        - Action Plan Workbook (Excel)
                        - Link to book your strategy call
                        
                        **What we found:**
                        """)
                        
                        result = st.session_state.audit_result
                        opp = result['analysis'].guarantee_check.get('total_opportunity', 0)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Total Opportunity Identified", f"${opp:,.0f}")
                        with col2:
                            actions = len(result['analysis'].action_plan)
                            st.metric("Quick Wins Identified", f"{actions} actions")
                        
                        # Download links
                        report = result['report']
                        if Path(report['html_report']).exists():
                            with open(report['html_report'], 'r') as f:
                                st.download_button(
                                    "📄 Download Your Report",
                                    f.read(),
                                    file_name="profit_leak_audit_report.html",
                                    mime="text/html"
                                )
                else:
                    st.error("Please agree to the terms to submit")


if __name__ == "__main__":
    customer_portal_page()

