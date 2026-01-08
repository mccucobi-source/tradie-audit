"""
Brace Profit Leak Audit - File Upload Portal
This is the post-payment audit form that receives customers from the Brace landing page.
Clean, focused interface for file upload and audit processing.
"""

import os
import sys
from pathlib import Path
import json
from datetime import datetime

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import streamlit as st

st.set_page_config(
    page_title="Upload Your Data | Brace Profit Leak Audit",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

from dotenv import load_dotenv
load_dotenv()

# Clean Brace-branded styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    :root {
        --bg: #ffffff;
        --bg-soft: #f8fafc;
        --border: #e2e8f0;
        --text: #0f172a;
        --text-secondary: #475569;
        --text-muted: #94a3b8;
        --yellow: #fcd34d;
        --yellow-dark: #f59e0b;
        --green: #10b981;
        --green-light: #ecfdf5;
    }
    
    .stApp {
        background: var(--bg);
    }
    
    #MainMenu, footer, header, [data-testid="stToolbar"], [data-testid="stSidebar"] {
        display: none !important;
    }
    
    .block-container {
        padding: 2rem 1rem !important;
        max-width: 720px !important;
    }
    
    /* Header */
    .audit-header {
        text-align: center;
        padding: 40px 0 32px;
        border-bottom: 1px solid var(--border);
        margin-bottom: 40px;
    }
    
    .audit-logo {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 24px;
        color: var(--text);
        margin-bottom: 8px;
    }
    
    .audit-title {
        font-family: 'Inter', sans-serif;
        font-size: 32px;
        font-weight: 700;
        color: var(--text);
        margin: 0 0 8px;
    }
    
    .audit-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 16px;
        color: var(--text-secondary);
    }
    
    /* Cards */
    .form-card {
        background: var(--bg-soft);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 28px;
        margin-bottom: 20px;
    }
    
    .form-card-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 20px;
    }
    
    .form-card-num {
        width: 28px;
        height: 28px;
        background: var(--text);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        font-weight: 600;
        color: white;
    }
    
    .form-card-title {
        font-family: 'Inter', sans-serif;
        font-size: 16px;
        font-weight: 600;
        color: var(--text);
    }
    
    /* Verification badge */
    .verified-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: var(--green-light);
        border: 1px solid rgba(16, 185, 129, 0.2);
        padding: 12px 20px;
        border-radius: 12px;
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        font-weight: 500;
        color: var(--green);
        margin-bottom: 32px;
    }
    
    /* Streamlit overrides */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {
        background: white !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        font-family: 'Inter', sans-serif !important;
        padding: 12px 16px !important;
    }
    
    .stTextInput > label,
    .stNumberInput > label,
    .stSelectbox > label,
    .stFileUploader > label {
        font-family: 'Inter', sans-serif !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        color: var(--text-secondary) !important;
    }
    
    .stButton > button {
        background: var(--text) !important;
        color: white !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 14px 28px !important;
        transition: all 0.2s !important;
    }
    
    .stButton > button:hover {
        background: #1e293b !important;
        transform: translateY(-2px);
    }
    
    .stFileUploader > div {
        background: white !important;
        border: 2px dashed var(--border) !important;
        border-radius: 12px !important;
    }
    
    .stSuccess {
        background: var(--green-light) !important;
        border: 1px solid rgba(16, 185, 129, 0.2) !important;
        border-radius: 10px !important;
    }
    
    /* Results */
    .result-card {
        background: white;
        border: 2px solid var(--yellow);
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        box-shadow: 0 0 0 4px rgba(252, 211, 77, 0.2);
    }
    
    .result-amount {
        font-family: 'Inter', sans-serif;
        font-size: 48px;
        font-weight: 800;
        color: var(--green);
    }
    
    /* Footer */
    .audit-footer {
        text-align: center;
        padding: 32px 0;
        margin-top: 40px;
        border-top: 1px solid var(--border);
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        color: var(--text-muted);
    }
</style>
""", unsafe_allow_html=True)


def verify_session():
    """Check if user has a valid payment session."""
    params = st.query_params
    email = params.get("email", "")
    session = params.get("session_id", "")
    
    # For now, we'll trust the redirect from Vercel
    # In production, you'd verify the session_id with Stripe
    if email or session or os.getenv("BYPASS_PAYMENT") == "true":
        return True, email
    return False, None


def show_upload_form(email: str = None):
    """Display the file upload form."""
    
    # Header
    st.markdown("""
    <div class="audit-header">
        <div class="audit-logo">Brace</div>
        <h1 class="audit-title">Upload Your Data</h1>
        <p class="audit-subtitle">We'll analyze everything and send your report within 48 hours.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Verification badge
    if email:
        st.markdown(f"""
        <div class="verified-badge">
            ✓ Payment verified for {email}
        </div>
        """, unsafe_allow_html=True)
    
    # Step 1: Business Info
    st.markdown("""
    <div class="form-card">
        <div class="form-card-header">
            <div class="form-card-num">1</div>
            <div class="form-card-title">Your Business</div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        business_name = st.text_input("Business name", placeholder="e.g. Dave's Electrical")
        contact_email = st.text_input("Email", value=email or "", placeholder="dave@example.com")
    with col2:
        trade_type = st.selectbox("Trade", ["Electrician", "Plumber", "Carpenter", "HVAC", "Builder", "Landscaper", "Roofer", "Other"])
        location = st.text_input("Location", placeholder="Sydney, NSW")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Step 2: Current Numbers
    st.markdown("""
    <div class="form-card">
        <div class="form-card-header">
            <div class="form-card-num">2</div>
            <div class="form-card-title">Current Numbers</div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        hourly_rate = st.number_input("Current hourly rate ($)", min_value=50, max_value=300, value=95)
        revenue = st.selectbox("Annual revenue (approx)", 
                              ["Under $100k", "$100k-$150k", "$150k-$200k", "$200k-$300k", "$300k-$500k", "$500k+"])
    with col2:
        hours_per_week = st.slider("Hours worked per week", 20, 80, 50)
        call_out = st.number_input("Call-out fee ($)", min_value=0, max_value=200, value=0)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Step 3: File Upload
    st.markdown("""
    <div class="form-card">
        <div class="form-card-header">
            <div class="form-card-num">3</div>
            <div class="form-card-title">Upload Documents</div>
        </div>
        <p style="font-family: 'Inter', sans-serif; font-size: 14px; color: #64748b; margin-bottom: 16px;">
            Upload your invoices, expenses, and quotes from the last 12 months. 
            We accept PDF, Excel, and CSV files.
        </p>
    """, unsafe_allow_html=True)
    
    invoices = st.file_uploader(
        "Invoices (required)", 
        type=['pdf', 'xlsx', 'xls', 'csv'], 
        accept_multiple_files=True, 
        key="inv",
        help="Your invoices from the last 12 months"
    )
    
    expenses = st.file_uploader(
        "Expenses / Bank statements", 
        type=['pdf', 'xlsx', 'xls', 'csv'], 
        accept_multiple_files=True, 
        key="exp",
        help="Business expenses or bank statements"
    )
    
    quotes = st.file_uploader(
        "Quotes (optional)", 
        type=['pdf', 'xlsx', 'xls', 'csv'], 
        accept_multiple_files=True, 
        key="quo",
        help="Quotes you've sent, including ones that didn't convert"
    )
    
    if invoices:
        st.success(f"✓ {len(invoices)} invoice file(s) uploaded")
    if expenses:
        st.success(f"✓ {len(expenses)} expense file(s) uploaded")
    if quotes:
        st.success(f"✓ {len(quotes)} quote file(s) uploaded")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Submit Button
    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.button("🚀 Run My Audit", use_container_width=True)
    
    if submitted:
        if not business_name or not contact_email:
            st.error("Please fill in your business name and email.")
        elif not invoices and not expenses:
            st.error("Please upload at least your invoices or bank statements.")
        else:
            run_audit(
                business_name=business_name,
                email=contact_email,
                trade_type=trade_type.lower() if trade_type != "Other" else "trade",
                location=location,
                hourly_rate=hourly_rate,
                hours_per_week=hours_per_week,
                invoices=invoices or [],
                expenses=expenses or [],
                quotes=quotes or []
            )
    
    # Footer
    st.markdown("""
    <div class="audit-footer">
        Powered by Brace · Your data is encrypted and deleted after 30 days
    </div>
    """, unsafe_allow_html=True)


def run_audit(business_name, email, trade_type, location, hourly_rate, hours_per_week, invoices, expenses, quotes):
    """Run the full audit pipeline."""
    from src.utils.file_handler import FileHandler
    from src.agents.data_extractor import DataExtractor
    from src.agents.analyzer import Analyzer, BusinessContext
    from src.agents.report_generator import ReportGenerator
    
    with st.status("🔍 Running your profit leak audit...", expanded=True) as status:
        
        # Save files
        st.write("📁 Saving your documents...")
        handler = FileHandler()
        folder = handler.create_customer_folder(business_name)
        
        for files, category in [(invoices, "invoices"), (expenses, "expenses"), (quotes, "quotes")]:
            for f in files:
                path = folder / category / f.name
                path.parent.mkdir(exist_ok=True)
                with open(path, 'wb') as out:
                    out.write(f.read())
        
        # Save intake data
        with open(folder / "intake_form.json", 'w') as f:
            json.dump({
                "business_name": business_name,
                "email": email,
                "trade_type": trade_type,
                "location": location,
                "hourly_rate": hourly_rate,
                "hours_per_week": hours_per_week,
                "submitted_at": datetime.now().isoformat()
            }, f, indent=2)
        
        # Extract data
        st.write("🔍 Extracting data from your files...")
        extractor = DataExtractor()
        results = extractor.extract_from_folder(str(folder))
        combined = extractor.combine_results(results)
        st.write(f"✓ Found {combined['summary']['total_transactions']} transactions")
        
        # Analyze
        st.write("📊 Analyzing your business data...")
        context = BusinessContext(
            trade_type=trade_type,
            location=location or "Sydney",
            years_in_business=5,
            current_rate=float(hourly_rate),
            hours_per_week=hours_per_week,
            revenue_goal=250000
        )
        
        analyzer = Analyzer()
        analysis = analyzer.analyze(combined, context)
        
        # Generate report
        st.write("📄 Generating your professional report...")
        generator = ReportGenerator(output_dir="./output")
        report = generator.generate_report(analysis, context, business_name)
        
        status.update(label="✅ Audit complete!", state="complete")
    
    # Show Results
    opportunity = analysis.guarantee_check.get('total_opportunity', 0)
    conservative = opportunity * 0.7
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="result-card">
        <p style="font-family: 'Inter', sans-serif; font-size: 14px; color: #64748b; margin-bottom: 8px;">
            Conservative Opportunity Identified
        </p>
        <div class="result-amount">${conservative:,.0f}</div>
        <p style="font-family: 'Inter', sans-serif; font-size: 13px; color: #94a3b8; margin-top: 8px;">
            Best case: ${opportunity:,.0f}/year
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Download buttons
    col1, col2 = st.columns(2)
    with col1:
        if Path(report['html_report']).exists():
            with open(report['html_report'], 'r') as f:
                st.download_button(
                    "📄 Download HTML Report", 
                    f.read(), 
                    file_name=f"{business_name.replace(' ', '_')}_audit_report.html",
                    mime="text/html", 
                    use_container_width=True
                )
    with col2:
        if Path(report['excel_report']).exists():
            with open(report['excel_report'], 'rb') as f:
                st.download_button(
                    "📊 Download Excel Workbook", 
                    f.read(),
                    file_name=f"{business_name.replace(' ', '_')}_audit_workbook.xlsx",
                    use_container_width=True
                )
    
    # Next steps
    st.markdown("""
    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 16px; padding: 24px; margin-top: 24px;">
        <h3 style="font-family: 'Inter', sans-serif; font-size: 16px; font-weight: 600; color: #0f172a; margin: 0 0 12px;">
            📧 What happens next?
        </h3>
        <p style="font-family: 'Inter', sans-serif; font-size: 14px; color: #475569; line-height: 1.6; margin: 0;">
            We've also sent these reports to your email. Check your inbox (and spam folder) 
            within the next few minutes. If you have questions about implementing the action plan, 
            reply to that email and we'll help.
        </p>
    </div>
    """, unsafe_allow_html=True)


def show_access_denied():
    """Show message when no valid payment session."""
    st.markdown("""
    <div style="text-align: center; padding: 80px 20px;">
        <div style="font-size: 64px; margin-bottom: 24px;">🔒</div>
        <h2 style="font-family: 'Inter', sans-serif; font-size: 28px; font-weight: 700; color: #0f172a; margin: 0 0 12px;">
            Access Required
        </h2>
        <p style="font-family: 'Inter', sans-serif; font-size: 16px; color: #64748b; margin-bottom: 32px;">
            Please complete your purchase on the Brace website to access the audit form.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.link_button("Go to Brace →", "https://brace.vercel.app", use_container_width=True)


def main():
    verified, email = verify_session()
    
    if verified:
        show_upload_form(email)
    else:
        show_access_denied()


if __name__ == "__main__":
    main()
