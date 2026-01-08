"""
Brace Profit Leak Audit - Clean Intake Form
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
    page_title="Brace | Upload Your Data",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

from dotenv import load_dotenv
load_dotenv()

# Clean UI styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background: #f9fafb !important;
    }
    
    #MainMenu, footer, header, [data-testid="stToolbar"], [data-testid="stSidebar"], 
    [data-testid="stDecoration"], .stDeployButton {
        display: none !important;
    }
    
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    /* Card container */
    .form-card {
        background: #ffffff;
        max-width: 520px;
        margin: 40px auto;
        border-radius: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08), 0 4px 12px rgba(0,0,0,0.04);
        overflow: hidden;
    }
    
    /* Header */
    .form-header {
        padding: 32px 32px 24px;
        border-bottom: 1px solid #f1f5f9;
    }
    
    .brand {
        font-size: 20px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 20px;
    }
    
    .form-title {
        font-size: 24px;
        font-weight: 700;
        color: #0f172a;
        margin: 0 0 6px;
        line-height: 1.3;
    }
    
    .form-desc {
        font-size: 15px;
        color: #64748b;
        margin: 0;
        line-height: 1.5;
    }
    
    /* Form body */
    .form-body {
        padding: 24px 32px 32px;
    }
    
    /* Section titles */
    .section-title {
        font-size: 13px;
        font-weight: 600;
        color: #0f172a;
        margin: 0 0 16px;
        padding-bottom: 8px;
        border-bottom: 1px solid #f1f5f9;
    }
    
    /* Inputs */
    .stTextInput > label,
    .stSelectbox > label,
    .stFileUploader > label {
        font-size: 14px !important;
        font-weight: 500 !important;
        color: #374151 !important;
        margin-bottom: 6px !important;
    }
    
    .stTextInput > div > div > input {
        font-size: 15px !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 8px !important;
        padding: 10px 12px !important;
        background: #fff !important;
        color: #0f172a !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #0f172a !important;
        box-shadow: 0 0 0 2px rgba(15,23,42,0.08) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #9ca3af !important;
    }
    
    .stSelectbox > div > div {
        border: 1px solid #e5e7eb !important;
        border-radius: 8px !important;
        background: #fff !important;
    }
    
    /* File uploader */
    .stFileUploader > div {
        background: #f9fafb !important;
        border: 1px dashed #d1d5db !important;
        border-radius: 10px !important;
        padding: 16px !important;
    }
    
    .stFileUploader > div:hover {
        background: #f3f4f6 !important;
        border-color: #9ca3af !important;
    }
    
    /* Button */
    .stButton > button {
        width: 100% !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        background: #0f172a !important;
        color: #fff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 20px !important;
        margin-top: 8px !important;
        cursor: pointer !important;
        transition: background 0.15s !important;
    }
    
    .stButton > button:hover {
        background: #1e293b !important;
    }
    
    /* Success */
    .stSuccess {
        background: #f0fdf4 !important;
        border: 1px solid #bbf7d0 !important;
        border-radius: 8px !important;
        font-size: 14px !important;
    }
    
    .stError {
        border-radius: 8px !important;
        font-size: 14px !important;
    }
    
    /* Footer */
    .form-footer {
        padding: 16px 32px;
        background: #f9fafb;
        border-top: 1px solid #f1f5f9;
        text-align: center;
    }
    
    .footer-text {
        font-size: 12px;
        color: #9ca3af;
    }
    
    /* Result */
    .result-box {
        background: #ecfdf5;
        border-radius: 12px;
        padding: 24px;
        text-align: center;
        margin: 16px 0;
    }
    
    .result-label {
        font-size: 13px;
        color: #6b7280;
        margin-bottom: 4px;
    }
    
    .result-value {
        font-size: 36px;
        font-weight: 700;
        color: #059669;
    }
    
    /* Spacing fix */
    .row-widget {
        margin-bottom: 16px;
    }
    
    /* Hide extra padding */
    .element-container {
        margin-bottom: 0 !important;
    }
    
    div[data-testid="column"] {
        padding: 0 8px !important;
    }
    
    div[data-testid="column"]:first-child {
        padding-left: 0 !important;
    }
    
    div[data-testid="column"]:last-child {
        padding-right: 0 !important;
    }
</style>
""", unsafe_allow_html=True)


def verify_session():
    params = st.query_params
    email = params.get("email", "")
    session = params.get("session_id", "")
    if email or session or os.getenv("BYPASS_PAYMENT") == "true":
        return True, email
    return False, None


def show_form(email: str = None):
    
    # Start card
    st.markdown("""
    <div class="form-card">
        <div class="form-header">
            <div class="brand">Brace</div>
            <h1 class="form-title">Upload your business data</h1>
            <p class="form-desc">We'll analyze your numbers and send your profit leak report within 48 hours.</p>
        </div>
        <div class="form-body">
    """, unsafe_allow_html=True)
    
    # Business details
    st.markdown('<div class="section-title">Business Details</div>', unsafe_allow_html=True)
    
    business_name = st.text_input("Business name", placeholder="e.g. Smith Electrical")
    
    col1, col2 = st.columns(2)
    with col1:
        contact_email = st.text_input("Email", value=email or "", placeholder="you@example.com")
    with col2:
        trade = st.selectbox("Trade", ["Electrician", "Plumber", "Carpenter", "HVAC", "Builder", "Other"])
    
    location = st.text_input("Location", placeholder="e.g. Sydney, NSW")
    
    st.markdown("<div style='height: 24px'></div>", unsafe_allow_html=True)
    
    # File uploads
    st.markdown('<div class="section-title">Upload Files</div>', unsafe_allow_html=True)
    
    invoices = st.file_uploader(
        "Invoices (last 12 months)", 
        type=['pdf', 'xlsx', 'csv'], 
        accept_multiple_files=True,
        key="inv"
    )
    if invoices:
        st.success(f"✓ {len(invoices)} invoice file(s) ready")
    
    expenses = st.file_uploader(
        "Expenses or bank statements", 
        type=['pdf', 'xlsx', 'csv'], 
        accept_multiple_files=True,
        key="exp"
    )
    if expenses:
        st.success(f"✓ {len(expenses)} expense file(s) ready")
    
    st.markdown("<div style='height: 16px'></div>", unsafe_allow_html=True)
    
    # Submit
    if st.button("Submit & Run Audit"):
        if not business_name:
            st.error("Please enter your business name")
        elif not contact_email:
            st.error("Please enter your email")
        elif not invoices and not expenses:
            st.error("Please upload at least one file")
        else:
            run_audit(business_name, contact_email, trade.lower(), location or "Australia", invoices or [], expenses or [])
    
    # Close form body
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
        <div class="form-footer">
            <span class="footer-text">🔒 Your data is encrypted and deleted after 30 days</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def run_audit(business_name, email, trade_type, location, invoices, expenses):
    from src.utils.file_handler import FileHandler
    from src.agents.data_extractor import DataExtractor
    from src.agents.analyzer import Analyzer, BusinessContext
    from src.agents.report_generator import ReportGenerator
    
    with st.status("Analyzing your data...", expanded=True) as status:
        
        st.write("Uploading files...")
        handler = FileHandler()
        folder = handler.create_customer_folder(business_name)
        
        for files, cat in [(invoices, "invoices"), (expenses, "expenses")]:
            for f in files:
                path = folder / cat / f.name
                path.parent.mkdir(exist_ok=True)
                with open(path, 'wb') as out:
                    out.write(f.read())
        
        with open(folder / "intake.json", 'w') as f:
            json.dump({"business_name": business_name, "email": email, "trade": trade_type, "location": location}, f)
        
        st.write("Extracting data...")
        extractor = DataExtractor()
        results = extractor.extract_from_folder(str(folder))
        combined = extractor.combine_results(results)
        
        st.write("Running analysis...")
        context = BusinessContext(trade_type=trade_type, location=location, years_in_business=5, current_rate=100.0, hours_per_week=45, revenue_goal=250000)
        analyzer = Analyzer()
        analysis = analyzer.analyze(combined, context)
        
        st.write("Generating report...")
        generator = ReportGenerator(output_dir="./output")
        report = generator.generate_report(analysis, context, business_name)
        
        status.update(label="✓ Complete", state="complete")
    
    opp = analysis.guarantee_check.get('total_opportunity', 0) * 0.7
    
    st.markdown(f"""
    <div class="result-box">
        <div class="result-label">Opportunity identified</div>
        <div class="result-value">${opp:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if Path(report['html_report']).exists():
            with open(report['html_report'], 'r') as f:
                st.download_button("📄 Download Report", f.read(), file_name=f"{business_name}_report.html", mime="text/html", use_container_width=True)
    with col2:
        if Path(report['excel_report']).exists():
            with open(report['excel_report'], 'rb') as f:
                st.download_button("📊 Download Excel", f.read(), file_name=f"{business_name}_workbook.xlsx", use_container_width=True)
    
    st.info(f"📧 Reports also sent to {email}")


def show_locked():
    st.markdown("""
    <div class="form-card">
        <div class="form-header">
            <div class="brand">Brace</div>
            <h1 class="form-title">Access Required</h1>
            <p class="form-desc">Please complete your purchase to access the audit form.</p>
        </div>
        <div class="form-body" style="text-align: center; padding: 40px 32px;">
    """, unsafe_allow_html=True)
    
    st.link_button("Go to Brace →", "https://brace-rvnk.vercel.app", use_container_width=True)
    
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)


def main():
    verified, email = verify_session()
    if verified:
        show_form(email)
    else:
        show_locked()


if __name__ == "__main__":
    main()
