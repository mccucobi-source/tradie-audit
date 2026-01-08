"""
Brace Profit Leak Audit - Simple Upload Form
Clean, minimal design that doesn't overwhelm tradies.
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
    page_title="Upload Your Data | Brace",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

from dotenv import load_dotenv
load_dotenv()

# Clean, minimal styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Reset */
    .stApp {
        background: #ffffff !important;
    }
    
    #MainMenu, footer, header, [data-testid="stToolbar"], [data-testid="stSidebar"], 
    [data-testid="stDecoration"], .stDeployButton {
        display: none !important;
    }
    
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    /* Main container */
    .main-wrapper {
        max-width: 480px;
        margin: 0 auto;
        padding: 40px 24px 60px;
    }
    
    /* Logo */
    .logo {
        text-align: center;
        margin-bottom: 48px;
    }
    
    .logo-text {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 24px;
        color: #0f172a;
        display: inline-flex;
        align-items: center;
        gap: 10px;
    }
    
    .logo-icon {
        width: 36px;
        height: 36px;
        background: #fbbf24;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
    }
    
    /* Title */
    .page-title {
        font-family: 'Inter', sans-serif;
        font-size: 28px;
        font-weight: 700;
        color: #0f172a;
        text-align: center;
        margin: 0 0 8px;
    }
    
    .page-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 15px;
        color: #64748b;
        text-align: center;
        margin: 0 0 40px;
    }
    
    /* Section headers */
    .section-label {
        font-family: 'Inter', sans-serif;
        font-size: 11px;
        font-weight: 600;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 16px;
    }
    
    /* Form styling */
    .stTextInput > label,
    .stSelectbox > label,
    .stFileUploader > label {
        font-family: 'Inter', sans-serif !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        color: #374151 !important;
        margin-bottom: 4px !important;
    }
    
    .stTextInput > div > div > input,
    .stSelectbox > div > div {
        font-family: 'Inter', sans-serif !important;
        font-size: 15px !important;
        border: 1.5px solid #e5e7eb !important;
        border-radius: 10px !important;
        padding: 12px 14px !important;
        background: #ffffff !important;
        transition: border-color 0.15s !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #0f172a !important;
        box-shadow: none !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #9ca3af !important;
    }
    
    /* File uploader */
    .stFileUploader {
        margin-top: 8px;
    }
    
    .stFileUploader > div {
        border: 1.5px dashed #d1d5db !important;
        border-radius: 12px !important;
        background: #fafafa !important;
        padding: 24px !important;
    }
    
    .stFileUploader > div:hover {
        border-color: #9ca3af !important;
        background: #f5f5f5 !important;
    }
    
    /* Upload helper text */
    .upload-help {
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        color: #6b7280;
        margin-top: 8px;
    }
    
    /* Button */
    .stButton > button {
        font-family: 'Inter', sans-serif !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        background: #0f172a !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 14px 24px !important;
        width: 100% !important;
        margin-top: 8px !important;
        transition: all 0.15s !important;
    }
    
    .stButton > button:hover {
        background: #1e293b !important;
        transform: translateY(-1px) !important;
    }
    
    /* Divider */
    .divider {
        height: 1px;
        background: #f1f5f9;
        margin: 32px 0;
    }
    
    /* Trust note */
    .trust-note {
        font-family: 'Inter', sans-serif;
        font-size: 12px;
        color: #9ca3af;
        text-align: center;
        margin-top: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
    }
    
    /* Success state */
    .stSuccess {
        background: #f0fdf4 !important;
        border: 1px solid #bbf7d0 !important;
        border-radius: 8px !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Results */
    .result-box {
        background: #f0fdf4;
        border: 2px solid #10b981;
        border-radius: 16px;
        padding: 32px;
        text-align: center;
        margin: 24px 0;
    }
    
    .result-label {
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        color: #6b7280;
        margin-bottom: 4px;
    }
    
    .result-amount {
        font-family: 'Inter', sans-serif;
        font-size: 42px;
        font-weight: 700;
        color: #059669;
    }
    
    /* Info box */
    .info-box {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 16px;
        margin-top: 20px;
    }
    
    .info-box p {
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        color: #475569;
        margin: 0;
        line-height: 1.5;
    }
    
    /* Hide streamlit elements */
    div[data-testid="stStatusWidget"] {
        font-family: 'Inter', sans-serif !important;
    }
</style>
""", unsafe_allow_html=True)


def verify_session():
    """Check if user has a valid payment session."""
    params = st.query_params
    email = params.get("email", "")
    session = params.get("session_id", "")
    
    if email or session or os.getenv("BYPASS_PAYMENT") == "true":
        return True, email
    return False, None


def show_upload_form(email: str = None):
    """Simple, clean upload form."""
    
    st.markdown('<div class="main-wrapper">', unsafe_allow_html=True)
    
    # Logo
    st.markdown("""
    <div class="logo">
        <div class="logo-text">
            <div class="logo-icon">⚡</div>
            Brace
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Title
    st.markdown("""
    <h1 class="page-title">Upload your data</h1>
    <p class="page-subtitle">Takes about 5 minutes. Report ready in 48 hours.</p>
    """, unsafe_allow_html=True)
    
    # Section 1: Basic Info
    st.markdown('<div class="section-label">Your details</div>', unsafe_allow_html=True)
    
    business_name = st.text_input("Business name", placeholder="e.g. Dave's Electrical", label_visibility="visible")
    
    col1, col2 = st.columns(2)
    with col1:
        contact_email = st.text_input("Email", value=email or "", placeholder="dave@example.com")
    with col2:
        trade_type = st.selectbox("Trade", ["Electrician", "Plumber", "Carpenter", "HVAC", "Builder", "Other"], label_visibility="visible")
    
    location = st.text_input("Location", placeholder="e.g. Sydney")
    
    # Divider
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Section 2: Files
    st.markdown('<div class="section-label">Your files</div>', unsafe_allow_html=True)
    
    invoices = st.file_uploader(
        "Invoices", 
        type=['pdf', 'xlsx', 'csv'], 
        accept_multiple_files=True,
        key="inv"
    )
    if invoices:
        st.success(f"✓ {len(invoices)} file(s) uploaded")
    
    expenses = st.file_uploader(
        "Expenses or bank statements", 
        type=['pdf', 'xlsx', 'csv'], 
        accept_multiple_files=True,
        key="exp"
    )
    if expenses:
        st.success(f"✓ {len(expenses)} file(s) uploaded")
    
    st.markdown('<p class="upload-help">PDF, Excel, or CSV files from the last 12 months</p>', unsafe_allow_html=True)
    
    # Divider
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Submit
    if st.button("Run my audit →"):
        if not business_name:
            st.error("Please enter your business name")
        elif not contact_email:
            st.error("Please enter your email")
        elif not invoices and not expenses:
            st.error("Please upload at least one file")
        else:
            run_audit(
                business_name=business_name,
                email=contact_email,
                trade_type=trade_type.lower() if trade_type != "Other" else "trade",
                location=location or "Australia",
                invoices=invoices or [],
                expenses=expenses or []
            )
    
    # Trust note
    st.markdown("""
    <div class="trust-note">
        🔒 Your data is encrypted and deleted after 30 days
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


def run_audit(business_name, email, trade_type, location, invoices, expenses):
    """Run the audit."""
    from src.utils.file_handler import FileHandler
    from src.agents.data_extractor import DataExtractor
    from src.agents.analyzer import Analyzer, BusinessContext
    from src.agents.report_generator import ReportGenerator
    
    with st.status("Analyzing your data...", expanded=True) as status:
        
        st.write("Saving files...")
        handler = FileHandler()
        folder = handler.create_customer_folder(business_name)
        
        for files, category in [(invoices, "invoices"), (expenses, "expenses")]:
            for f in files:
                path = folder / category / f.name
                path.parent.mkdir(exist_ok=True)
                with open(path, 'wb') as out:
                    out.write(f.read())
        
        with open(folder / "intake_form.json", 'w') as f:
            json.dump({
                "business_name": business_name,
                "email": email,
                "trade_type": trade_type,
                "location": location,
                "submitted_at": datetime.now().isoformat()
            }, f, indent=2)
        
        st.write("Extracting data...")
        extractor = DataExtractor()
        results = extractor.extract_from_folder(str(folder))
        combined = extractor.combine_results(results)
        
        st.write("Running analysis...")
        context = BusinessContext(
            trade_type=trade_type,
            location=location,
            years_in_business=5,
            current_rate=100.0,
            hours_per_week=45,
            revenue_goal=250000
        )
        
        analyzer = Analyzer()
        analysis = analyzer.analyze(combined, context)
        
        st.write("Creating reports...")
        generator = ReportGenerator(output_dir="./output")
        report = generator.generate_report(analysis, context, business_name)
        
        status.update(label="✓ Done!", state="complete")
    
    # Results
    opportunity = analysis.guarantee_check.get('total_opportunity', 0)
    conservative = opportunity * 0.7
    
    st.markdown(f"""
    <div class="result-box">
        <div class="result-label">Opportunity found</div>
        <div class="result-amount">${conservative:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Downloads
    col1, col2 = st.columns(2)
    with col1:
        if Path(report['html_report']).exists():
            with open(report['html_report'], 'r') as f:
                st.download_button("📄 HTML Report", f.read(), 
                    file_name=f"{business_name.replace(' ', '_')}_report.html",
                    mime="text/html", use_container_width=True)
    with col2:
        if Path(report['excel_report']).exists():
            with open(report['excel_report'], 'rb') as f:
                st.download_button("📊 Excel Workbook", f.read(),
                    file_name=f"{business_name.replace(' ', '_')}_workbook.xlsx",
                    use_container_width=True)
    
    st.markdown(f"""
    <div class="info-box">
        <p>📧 We've also sent these to <strong>{email}</strong></p>
    </div>
    """, unsafe_allow_html=True)


def show_access_denied():
    """Access denied page."""
    st.markdown('<div class="main-wrapper">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="logo">
        <div class="logo-text">
            <div class="logo-icon">⚡</div>
            Brace
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; padding: 40px 0;">
        <div style="font-size: 48px; margin-bottom: 16px;">🔒</div>
        <h1 class="page-title">Access required</h1>
        <p class="page-subtitle">Complete your purchase to access the audit form.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.link_button("Go to Brace →", "https://brace-rvnk.vercel.app", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


def main():
    verified, email = verify_session()
    if verified:
        show_upload_form(email)
    else:
        show_access_denied()


if __name__ == "__main__":
    main()
