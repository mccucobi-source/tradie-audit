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
    page_title="Brace | Start Your Audit",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

from dotenv import load_dotenv
load_dotenv()

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * { font-family: 'Inter', -apple-system, sans-serif; }
    
    .stApp { background: #f8f9fa !important; }
    
    #MainMenu, footer, header, [data-testid="stToolbar"], [data-testid="stSidebar"], 
    [data-testid="stDecoration"], .stDeployButton { display: none !important; }
    
    .block-container {
        max-width: 480px !important;
        padding: 40px 20px !important;
    }
    
    /* Card */
    .card {
        background: #ffffff;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        border: 1px solid #e5e7eb;
    }
    
    /* Header */
    .card-header {
        padding: 24px 24px 20px;
        border-bottom: 1px solid #f3f4f6;
    }
    
    .brand {
        font-size: 16px;
        font-weight: 700;
        color: #111827;
        margin-bottom: 16px;
    }
    
    .title {
        font-size: 20px;
        font-weight: 600;
        color: #111827;
        margin: 0 0 4px;
    }
    
    .subtitle {
        font-size: 14px;
        color: #6b7280;
        margin: 0;
    }
    
    /* Body */
    .card-body { padding: 20px 24px 24px; }
    
    /* Section */
    .section { margin-bottom: 20px; }
    .section:last-child { margin-bottom: 0; }
    
    .section-label {
        font-size: 11px;
        font-weight: 600;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 10px;
    }
    
    /* Inputs */
    .stTextInput > label, .stSelectbox > label, .stFileUploader > label, .stTextArea > label, .stNumberInput > label {
        font-size: 13px !important;
        font-weight: 500 !important;
        color: #374151 !important;
    }
    
    .stTextInput > div > div > input, .stNumberInput > div > div > input {
        font-size: 14px !important;
        border: 1px solid #d1d5db !important;
        border-radius: 8px !important;
        padding: 10px 12px !important;
        background: #fff !important;
        color: #111827 !important;
    }
    
    .stTextInput > div > div > input:focus, .stNumberInput > div > div > input:focus {
        border-color: #111827 !important;
        box-shadow: none !important;
    }
    
    .stTextInput > div > div > input::placeholder { color: #9ca3af !important; }
    
    .stSelectbox > div > div {
        border: 1px solid #d1d5db !important;
        border-radius: 8px !important;
        background: #fff !important;
    }
    
    .stTextArea > div > div > textarea {
        font-size: 14px !important;
        border: 1px solid #d1d5db !important;
        border-radius: 8px !important;
        padding: 10px 12px !important;
        background: #fff !important;
        color: #111827 !important;
        min-height: 70px !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #111827 !important;
        box-shadow: none !important;
    }
    
    /* Radio - simple pills */
    .stRadio > label { display: none !important; }
    .stRadio > div { flex-direction: row !important; gap: 6px !important; flex-wrap: wrap !important; }
    
    .stRadio > div > label {
        background: #f3f4f6 !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 6px !important;
        padding: 6px 10px !important;
        font-size: 12px !important;
        font-weight: 500 !important;
        color: #374151 !important;
        margin: 0 !important;
    }
    
    .stRadio > div > label[data-checked="true"] {
        background: #111827 !important;
        border-color: #111827 !important;
        color: #fff !important;
    }
    
    /* File uploader */
    .stFileUploader > div {
        background: #f9fafb !important;
        border: 1px dashed #d1d5db !important;
        border-radius: 8px !important;
        padding: 12px !important;
    }
    
    /* Button */
    .stButton > button {
        width: 100% !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        background: #111827 !important;
        color: #fff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
    }
    
    .stButton > button:hover { background: #1f2937 !important; }
    
    /* Success/Error */
    .stSuccess {
        background: #f0fdf4 !important;
        border: 1px solid #bbf7d0 !important;
        border-radius: 6px !important;
        font-size: 13px !important;
    }
    
    .stError { border-radius: 6px !important; font-size: 13px !important; }
    
    /* Footer */
    .card-footer {
        padding: 12px 24px;
        background: #f9fafb;
        border-top: 1px solid #f3f4f6;
        text-align: center;
        font-size: 11px;
        color: #9ca3af;
        border-radius: 0 0 12px 12px;
    }
    
    /* Result */
    .result {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        margin: 16px 0;
    }
    
    .result-label { font-size: 12px; color: #6b7280; }
    .result-value { font-size: 32px; font-weight: 700; color: #059669; }
    
    .info-box {
        background: #f3f4f6;
        border-radius: 8px;
        padding: 12px;
        font-size: 13px;
        color: #374151;
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
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="card-header">
        <div class="brand">Brace</div>
        <h1 class="title">Start your audit</h1>
        <p class="subtitle">Takes 3 minutes. Report delivered within 48 hours.</p>
    </div>
    <div class="card-body">
    """, unsafe_allow_html=True)
    
    # Business Details
    st.markdown('<div class="section"><div class="section-label">About Your Business</div>', unsafe_allow_html=True)
    
    business_name = st.text_input("Business name", placeholder="e.g. Smith Electrical")
    
    col1, col2 = st.columns(2)
    with col1:
        contact_email = st.text_input("Email", value=email or "", placeholder="you@example.com")
    with col2:
        trade = st.selectbox("Trade", ["Electrician", "Plumber", "Carpenter", "HVAC", "Builder", "Other"])
    
    col1, col2 = st.columns(2)
    with col1:
        location = st.text_input("Location", placeholder="e.g. Sydney")
    with col2:
        team_size = st.selectbox("Team size", ["Just me", "2-3", "4-6", "7+"])
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Numbers
    st.markdown('<div class="section"><div class="section-label">Your Numbers</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        hourly_rate = st.number_input("Hourly rate ($)", min_value=50, max_value=300, value=95)
    with col2:
        jobs_per_week = st.selectbox("Jobs per week", ["1-5", "5-10", "10-20", "20+"])
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Challenge
    st.markdown('<div class="section"><div class="section-label">Biggest Challenge</div>', unsafe_allow_html=True)
    
    frustration = st.radio(
        "challenge",
        ["Not charging enough", "Chasing payments", "Quoting takes too long", "Too much admin", "Not enough work"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Files
    st.markdown('<div class="section"><div class="section-label">Your Files</div>', unsafe_allow_html=True)
    
    invoices = st.file_uploader("Invoices (last 12 months)", type=['pdf', 'xlsx', 'csv'], accept_multiple_files=True, key="inv")
    if invoices:
        st.success(f"✓ {len(invoices)} file(s)")
    
    expenses = st.file_uploader("Expenses or bank statements", type=['pdf', 'xlsx', 'csv'], accept_multiple_files=True, key="exp")
    if expenses:
        st.success(f"✓ {len(expenses)} file(s)")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Notes
    st.markdown('<div class="section"><div class="section-label">Anything Specific? (Optional)</div>', unsafe_allow_html=True)
    
    notes = st.text_area("notes", placeholder="e.g. I think I'm undercharging for emergency call-outs", label_visibility="collapsed")
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # Button
    st.markdown('<div style="padding: 0 24px 20px;">', unsafe_allow_html=True)
    if st.button("Submit"):
        if not business_name:
            st.error("Enter your business name")
        elif not contact_email:
            st.error("Enter your email")
        elif not invoices and not expenses:
            st.error("Upload at least one file")
        else:
            run_audit(business_name, contact_email, trade.lower(), location or "Australia", team_size, hourly_rate, jobs_per_week, frustration, notes, invoices or [], expenses or [])
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown('<div class="card-footer">🔒 Encrypted · Deleted after 30 days</div></div>', unsafe_allow_html=True)


def run_audit(business_name, email, trade, location, team_size, hourly_rate, jobs_per_week, frustration, notes, invoices, expenses):
    from src.utils.file_handler import FileHandler
    from src.agents.data_extractor import DataExtractor
    from src.agents.analyzer import Analyzer, BusinessContext
    from src.agents.report_generator import ReportGenerator
    
    with st.status("Analyzing...", expanded=True) as status:
        
        st.write("Saving files...")
        handler = FileHandler()
        folder = handler.create_customer_folder(business_name)
        
        for files, cat in [(invoices, "invoices"), (expenses, "expenses")]:
            for f in files:
                path = folder / cat / f.name
                path.parent.mkdir(exist_ok=True)
                with open(path, 'wb') as out:
                    out.write(f.read())
        
        with open(folder / "intake.json", 'w') as f:
            json.dump({
                "business_name": business_name, "email": email, "trade": trade, "location": location,
                "team_size": team_size, "hourly_rate": hourly_rate, "jobs_per_week": jobs_per_week,
                "biggest_frustration": frustration, "specific_concerns": notes,
                "submitted_at": datetime.now().isoformat()
            }, f, indent=2)
        
        st.write("Extracting data...")
        extractor = DataExtractor()
        results = extractor.extract_from_folder(str(folder))
        combined = extractor.combine_results(results)
        
        st.write("Analyzing...")
        context = BusinessContext(trade_type=trade, location=location, years_in_business=5, current_rate=float(hourly_rate), hours_per_week=45, revenue_goal=250000)
        analyzer = Analyzer()
        analysis = analyzer.analyze(combined, context)
        
        st.write("Creating report...")
        generator = ReportGenerator(output_dir="./output")
        report = generator.generate_report(analysis, context, business_name)
        
        status.update(label="✓ Done", state="complete")
    
    opp = analysis.guarantee_check.get('total_opportunity', 0) * 0.7
    
    st.markdown(f'<div class="result"><div class="result-label">Opportunity found</div><div class="result-value">${opp:,.0f}</div></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if Path(report['html_report']).exists():
            with open(report['html_report'], 'r') as f:
                st.download_button("📄 Report", f.read(), file_name=f"{business_name}_report.html", mime="text/html", use_container_width=True)
    with col2:
        if Path(report['excel_report']).exists():
            with open(report['excel_report'], 'rb') as f:
                st.download_button("📊 Excel", f.read(), file_name=f"{business_name}_workbook.xlsx", use_container_width=True)
    
    st.markdown(f'<div class="info-box">📧 Also sent to {email}</div>', unsafe_allow_html=True)


def show_locked():
    st.markdown('<div class="card"><div class="card-header" style="text-align:center;"><div class="brand">Brace</div><h1 class="title">Access Required</h1><p class="subtitle">Complete your purchase to start.</p></div><div class="card-body" style="text-align:center;">', unsafe_allow_html=True)
    st.link_button("Go to Brace →", "https://brace-rvnk.vercel.app", use_container_width=True)
    st.markdown('</div></div>', unsafe_allow_html=True)


def main():
    verified, email = verify_session()
    if verified:
        show_form(email)
    else:
        show_locked()


if __name__ == "__main__":
    main()
