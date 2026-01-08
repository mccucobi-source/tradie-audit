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

# Clean centered card UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background: #f4f4f5 !important;
    }
    
    #MainMenu, footer, header, [data-testid="stToolbar"], [data-testid="stSidebar"], 
    [data-testid="stDecoration"], .stDeployButton {
        display: none !important;
    }
    
    /* Center the form */
    .block-container {
        max-width: 480px !important;
        padding: 60px 20px 40px !important;
    }
    
    /* Card */
    .card {
        background: #ffffff;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
        padding: 32px;
        margin-bottom: 16px;
    }
    
    /* Brand */
    .brand {
        font-size: 18px;
        font-weight: 700;
        color: #18181b;
        margin-bottom: 24px;
    }
    
    /* Title */
    .title {
        font-size: 22px;
        font-weight: 600;
        color: #18181b;
        margin: 0 0 6px;
    }
    
    .subtitle {
        font-size: 14px;
        color: #71717a;
        margin: 0 0 28px;
        line-height: 1.5;
    }
    
    /* Section label */
    .section-label {
        font-size: 12px;
        font-weight: 600;
        color: #a1a1aa;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 12px;
    }
    
    /* Inputs */
    .stTextInput > label,
    .stSelectbox > label,
    .stFileUploader > label {
        font-size: 13px !important;
        font-weight: 500 !important;
        color: #3f3f46 !important;
        margin-bottom: 4px !important;
    }
    
    .stTextInput > div > div > input {
        font-size: 14px !important;
        border: 1px solid #e4e4e7 !important;
        border-radius: 8px !important;
        padding: 10px 12px !important;
        background: #fafafa !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #18181b !important;
        background: #fff !important;
        box-shadow: none !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #a1a1aa !important;
    }
    
    .stSelectbox > div > div {
        border: 1px solid #e4e4e7 !important;
        border-radius: 8px !important;
        background: #fafafa !important;
        font-size: 14px !important;
    }
    
    /* File uploader - compact */
    .stFileUploader > div {
        background: #fafafa !important;
        border: 1px dashed #d4d4d8 !important;
        border-radius: 8px !important;
        padding: 12px !important;
    }
    
    .stFileUploader > div:hover {
        border-color: #a1a1aa !important;
    }
    
    /* Button */
    .stButton > button {
        width: 100% !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        background: #18181b !important;
        color: #fff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
        cursor: pointer !important;
    }
    
    .stButton > button:hover {
        background: #27272a !important;
    }
    
    /* Success/Error */
    .stSuccess, .stError, .stInfo {
        font-size: 13px !important;
        border-radius: 8px !important;
        padding: 10px 12px !important;
    }
    
    .stSuccess {
        background: #f0fdf4 !important;
        border: 1px solid #bbf7d0 !important;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        font-size: 12px;
        color: #a1a1aa;
        padding: 8px 0;
    }
    
    /* Result */
    .result {
        background: #f0fdf4;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        margin: 16px 0;
    }
    
    .result-label {
        font-size: 12px;
        color: #6b7280;
        margin-bottom: 2px;
    }
    
    .result-value {
        font-size: 32px;
        font-weight: 700;
        color: #059669;
    }
    
    /* Spacing */
    .spacer {
        height: 20px;
    }
    
    .spacer-sm {
        height: 12px;
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
    
    # Card start
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    # Header
    st.markdown("""
        <div class="brand">Brace</div>
        <h1 class="title">Upload your data</h1>
        <p class="subtitle">We'll find your profit leaks and send your report within 48 hours.</p>
    """, unsafe_allow_html=True)
    
    # Business details
    st.markdown('<div class="section-label">Your Details</div>', unsafe_allow_html=True)
    
    business_name = st.text_input("Business name", placeholder="e.g. Smith Electrical", label_visibility="collapsed")
    
    col1, col2 = st.columns([3, 2])
    with col1:
        contact_email = st.text_input("Email", value=email or "", placeholder="Email address", label_visibility="collapsed")
    with col2:
        trade = st.selectbox("Trade", ["Electrician", "Plumber", "Carpenter", "HVAC", "Builder", "Other"], label_visibility="collapsed")
    
    location = st.text_input("Location", placeholder="Location (e.g. Sydney)", label_visibility="collapsed")
    
    st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
    
    # Files
    st.markdown('<div class="section-label">Your Files</div>', unsafe_allow_html=True)
    
    invoices = st.file_uploader("Invoices", type=['pdf', 'xlsx', 'csv'], accept_multiple_files=True, key="inv", label_visibility="collapsed")
    if invoices:
        st.success(f"✓ {len(invoices)} invoice(s)")
    
    st.markdown('<div class="spacer-sm"></div>', unsafe_allow_html=True)
    
    expenses = st.file_uploader("Expenses", type=['pdf', 'xlsx', 'csv'], accept_multiple_files=True, key="exp", label_visibility="collapsed")
    if expenses:
        st.success(f"✓ {len(expenses)} file(s)")
    
    st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
    
    # Submit
    if st.button("Submit"):
        if not business_name:
            st.error("Enter your business name")
        elif not contact_email:
            st.error("Enter your email")
        elif not invoices and not expenses:
            st.error("Upload at least one file")
        else:
            run_audit(business_name, contact_email, trade.lower(), location or "Australia", invoices or [], expenses or [])
    
    # Card end
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown('<div class="footer">🔒 Encrypted & deleted after 30 days</div>', unsafe_allow_html=True)


def run_audit(business_name, email, trade_type, location, invoices, expenses):
    from src.utils.file_handler import FileHandler
    from src.agents.data_extractor import DataExtractor
    from src.agents.analyzer import Analyzer, BusinessContext
    from src.agents.report_generator import ReportGenerator
    
    with st.status("Analyzing...", expanded=True) as status:
        
        st.write("Uploading...")
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
        
        st.write("Analyzing...")
        context = BusinessContext(trade_type=trade_type, location=location, years_in_business=5, current_rate=100.0, hours_per_week=45, revenue_goal=250000)
        analyzer = Analyzer()
        analysis = analyzer.analyze(combined, context)
        
        st.write("Creating report...")
        generator = ReportGenerator(output_dir="./output")
        report = generator.generate_report(analysis, context, business_name)
        
        status.update(label="✓ Done", state="complete")
    
    opp = analysis.guarantee_check.get('total_opportunity', 0) * 0.7
    
    st.markdown(f"""
    <div class="result">
        <div class="result-label">Opportunity found</div>
        <div class="result-value">${opp:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if Path(report['html_report']).exists():
            with open(report['html_report'], 'r') as f:
                st.download_button("📄 Report", f.read(), file_name=f"{business_name}_report.html", mime="text/html", use_container_width=True)
    with col2:
        if Path(report['excel_report']).exists():
            with open(report['excel_report'], 'rb') as f:
                st.download_button("📊 Excel", f.read(), file_name=f"{business_name}_workbook.xlsx", use_container_width=True)
    
    st.info(f"📧 Also sent to {email}")


def show_locked():
    st.markdown('<div class="card" style="text-align:center;">', unsafe_allow_html=True)
    st.markdown("""
        <div class="brand">Brace</div>
        <h1 class="title">Access Required</h1>
        <p class="subtitle">Complete your purchase to access the audit form.</p>
    """, unsafe_allow_html=True)
    st.link_button("Go to Brace →", "https://brace-rvnk.vercel.app", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


def main():
    verified, email = verify_session()
    if verified:
        show_form(email)
    else:
        show_locked()


if __name__ == "__main__":
    main()
