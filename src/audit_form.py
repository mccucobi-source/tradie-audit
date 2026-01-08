"""
Brace Profit Leak Audit - Premium Intake Form
Matches landing page design. Collects key context for better AI analysis.
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

# Brace brand colors matching landing page
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    :root {
        --bg: #fafafa;
        --card: #ffffff;
        --slate-900: #0f172a;
        --slate-700: #334155;
        --slate-500: #64748b;
        --slate-400: #94a3b8;
        --slate-200: #e2e8f0;
        --slate-100: #f1f5f9;
        --yellow-400: #facc15;
        --yellow-300: #fde047;
        --yellow-100: #fef9c3;
        --green-500: #22c55e;
        --green-100: #dcfce7;
    }
    
    * { font-family: 'Inter', -apple-system, sans-serif; }
    
    .stApp { background: var(--bg) !important; }
    
    #MainMenu, footer, header, [data-testid="stToolbar"], [data-testid="stSidebar"], 
    [data-testid="stDecoration"], .stDeployButton { display: none !important; }
    
    .block-container {
        max-width: 500px !important;
        padding: 48px 20px 32px !important;
    }
    
    /* Card */
    .card {
        background: var(--card);
        border-radius: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05), 0 4px 20px rgba(0,0,0,0.03);
        border: 1px solid var(--slate-100);
        overflow: hidden;
    }
    
    /* Header with yellow accent */
    .card-header {
        background: linear-gradient(135deg, var(--yellow-100) 0%, var(--card) 100%);
        padding: 28px 28px 24px;
        border-bottom: 1px solid var(--slate-100);
    }
    
    .brand {
        font-size: 17px;
        font-weight: 700;
        color: var(--slate-900);
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .brand-dot {
        width: 8px;
        height: 8px;
        background: var(--yellow-400);
        border-radius: 50%;
    }
    
    .title {
        font-size: 22px;
        font-weight: 700;
        color: var(--slate-900);
        margin: 0 0 6px;
        line-height: 1.3;
    }
    
    .subtitle {
        font-size: 14px;
        color: var(--slate-500);
        margin: 0;
        line-height: 1.5;
    }
    
    /* Body */
    .card-body {
        padding: 24px 28px 28px;
    }
    
    /* Section */
    .section {
        margin-bottom: 24px;
    }
    
    .section:last-child {
        margin-bottom: 0;
    }
    
    .section-label {
        font-size: 11px;
        font-weight: 600;
        color: var(--slate-400);
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 12px;
    }
    
    /* Inputs */
    .stTextInput > label, .stSelectbox > label, .stFileUploader > label, .stTextArea > label, .stNumberInput > label {
        font-size: 13px !important;
        font-weight: 500 !important;
        color: var(--slate-700) !important;
        margin-bottom: 4px !important;
    }
    
    .stTextInput > div > div > input, .stNumberInput > div > div > input {
        font-size: 14px !important;
        border: 1px solid var(--slate-200) !important;
        border-radius: 10px !important;
        padding: 11px 14px !important;
        background: var(--card) !important;
        color: var(--slate-900) !important;
        transition: all 0.15s !important;
    }
    
    .stTextInput > div > div > input:focus, .stNumberInput > div > div > input:focus {
        border-color: var(--slate-900) !important;
        box-shadow: 0 0 0 3px rgba(15,23,42,0.06) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: var(--slate-400) !important;
    }
    
    .stSelectbox > div > div {
        border: 1px solid var(--slate-200) !important;
        border-radius: 10px !important;
        background: var(--card) !important;
    }
    
    .stTextArea > div > div > textarea {
        font-size: 14px !important;
        border: 1px solid var(--slate-200) !important;
        border-radius: 10px !important;
        padding: 11px 14px !important;
        background: var(--card) !important;
        min-height: 80px !important;
        resize: none !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: var(--slate-900) !important;
        box-shadow: 0 0 0 3px rgba(15,23,42,0.06) !important;
    }
    
    /* Radio buttons styled as pills */
    .stRadio > div {
        flex-direction: row !important;
        gap: 8px !important;
        flex-wrap: wrap !important;
    }
    
    .stRadio > div > label {
        background: var(--slate-100) !important;
        border: 1px solid var(--slate-200) !important;
        border-radius: 8px !important;
        padding: 8px 14px !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        color: var(--slate-700) !important;
        cursor: pointer !important;
        transition: all 0.15s !important;
        margin: 0 !important;
    }
    
    .stRadio > div > label:hover {
        border-color: var(--slate-400) !important;
    }
    
    .stRadio > div > label[data-checked="true"] {
        background: var(--slate-900) !important;
        border-color: var(--slate-900) !important;
        color: white !important;
    }
    
    /* File uploader */
    .stFileUploader > div {
        background: var(--slate-100) !important;
        border: 1px dashed var(--slate-200) !important;
        border-radius: 10px !important;
        padding: 16px !important;
    }
    
    .stFileUploader > div:hover {
        border-color: var(--slate-400) !important;
        background: var(--card) !important;
    }
    
    /* Yellow submit button */
    .stButton > button {
        width: 100% !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        background: var(--yellow-400) !important;
        color: var(--slate-900) !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 14px 20px !important;
        cursor: pointer !important;
        transition: all 0.15s !important;
        box-shadow: 0 2px 8px rgba(250, 204, 21, 0.3) !important;
    }
    
    .stButton > button:hover {
        background: var(--yellow-300) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(250, 204, 21, 0.4) !important;
    }
    
    /* Success */
    .stSuccess {
        background: var(--green-100) !important;
        border: none !important;
        border-radius: 8px !important;
        font-size: 13px !important;
        color: #166534 !important;
    }
    
    .stError {
        border-radius: 8px !important;
        font-size: 13px !important;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 20px 28px;
        background: var(--slate-100);
        border-top: 1px solid var(--slate-200);
    }
    
    .footer-text {
        font-size: 12px;
        color: var(--slate-400);
    }
    
    /* Result */
    .result {
        background: linear-gradient(135deg, var(--green-100) 0%, #f0fdf4 100%);
        border: 1px solid #bbf7d0;
        border-radius: 12px;
        padding: 24px;
        text-align: center;
        margin: 20px 0;
    }
    
    .result-label {
        font-size: 12px;
        font-weight: 500;
        color: var(--slate-500);
        margin-bottom: 4px;
    }
    
    .result-value {
        font-size: 36px;
        font-weight: 700;
        color: #16a34a;
    }
    
    /* Info box */
    .info-box {
        background: var(--slate-100);
        border-radius: 10px;
        padding: 14px 16px;
        font-size: 13px;
        color: var(--slate-600);
    }
    
    /* Hide radio label */
    .stRadio > label { display: none !important; }
    
    /* Column spacing */
    div[data-testid="column"] { padding: 0 6px !important; }
    div[data-testid="column"]:first-child { padding-left: 0 !important; }
    div[data-testid="column"]:last-child { padding-right: 0 !important; }
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
        <div class="brand"><span class="brand-dot"></span> Brace</div>
        <h1 class="title">Let's find your profit leaks</h1>
        <p class="subtitle">Takes 3 minutes. Report delivered within 48 hours.</p>
    </div>
    <div class="card-body">
    """, unsafe_allow_html=True)
    
    # === SECTION 1: Business Details ===
    st.markdown('<div class="section"><div class="section-label">About Your Business</div>', unsafe_allow_html=True)
    
    business_name = st.text_input("Business name", placeholder="e.g. Smith Electrical")
    
    col1, col2 = st.columns(2)
    with col1:
        contact_email = st.text_input("Email", value=email or "", placeholder="you@example.com")
    with col2:
        trade = st.selectbox("Trade", ["Electrician", "Plumber", "Carpenter", "HVAC", "Builder", "Roofer", "Painter", "Other"])
    
    col1, col2 = st.columns(2)
    with col1:
        location = st.text_input("Location", placeholder="e.g. Sydney")
    with col2:
        team_size = st.selectbox("Team size", ["Just me", "2-3 people", "4-6 people", "7+"])
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # === SECTION 2: Current Numbers ===
    st.markdown('<div class="section"><div class="section-label">Your Numbers</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        hourly_rate = st.number_input("Hourly rate ($)", min_value=50, max_value=300, value=95, help="What you typically charge")
    with col2:
        jobs_per_week = st.selectbox("Jobs per week", ["1-5", "5-10", "10-20", "20+"])
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # === SECTION 3: Pain Point ===
    st.markdown('<div class="section"><div class="section-label">Biggest Challenge Right Now</div>', unsafe_allow_html=True)
    
    frustration = st.radio(
        "frustration",
        ["Not charging enough", "Chasing payments", "Quoting takes forever", "Too much admin", "Not enough work"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # === SECTION 4: Files ===
    st.markdown('<div class="section"><div class="section-label">Upload Your Files</div>', unsafe_allow_html=True)
    
    invoices = st.file_uploader("Invoices (last 12 months)", type=['pdf', 'xlsx', 'csv'], accept_multiple_files=True, key="inv")
    if invoices:
        st.success(f"✓ {len(invoices)} invoice file(s) ready")
    
    expenses = st.file_uploader("Expenses or bank statements", type=['pdf', 'xlsx', 'csv'], accept_multiple_files=True, key="exp")
    if expenses:
        st.success(f"✓ {len(expenses)} file(s) ready")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # === SECTION 5: Optional Note ===
    st.markdown('<div class="section"><div class="section-label">Anything Specific? (Optional)</div>', unsafe_allow_html=True)
    
    notes = st.text_area("notes", placeholder="e.g. I think I'm undercharging for emergency call-outs...", label_visibility="collapsed", height=80)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Close card body
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Submit button (inside card but after body)
    st.markdown('<div style="padding: 0 28px 24px;">', unsafe_allow_html=True)
    
    if st.button("Run My Audit →"):
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
                trade=trade.lower(),
                location=location or "Australia",
                team_size=team_size,
                hourly_rate=hourly_rate,
                jobs_per_week=jobs_per_week,
                frustration=frustration,
                notes=notes,
                invoices=invoices or [],
                expenses=expenses or []
            )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <span class="footer-text">🔒 Bank-level encryption · Data deleted after 30 days</span>
    </div>
    </div>
    """, unsafe_allow_html=True)


def run_audit(business_name, email, trade, location, team_size, hourly_rate, jobs_per_week, frustration, notes, invoices, expenses):
    from src.utils.file_handler import FileHandler
    from src.agents.data_extractor import DataExtractor
    from src.agents.analyzer import Analyzer, BusinessContext
    from src.agents.report_generator import ReportGenerator
    
    with st.status("Analyzing your business...", expanded=True) as status:
        
        st.write("📁 Saving your files...")
        handler = FileHandler()
        folder = handler.create_customer_folder(business_name)
        
        for files, cat in [(invoices, "invoices"), (expenses, "expenses")]:
            for f in files:
                path = folder / cat / f.name
                path.parent.mkdir(exist_ok=True)
                with open(path, 'wb') as out:
                    out.write(f.read())
        
        # Save intake with all context for Claude
        intake_data = {
            "business_name": business_name,
            "email": email,
            "trade": trade,
            "location": location,
            "team_size": team_size,
            "hourly_rate": hourly_rate,
            "jobs_per_week": jobs_per_week,
            "biggest_frustration": frustration,
            "specific_concerns": notes,
            "submitted_at": datetime.now().isoformat()
        }
        
        with open(folder / "intake.json", 'w') as f:
            json.dump(intake_data, f, indent=2)
        
        st.write("🔍 Extracting data from files...")
        extractor = DataExtractor()
        results = extractor.extract_from_folder(str(folder))
        combined = extractor.combine_results(results)
        
        st.write("📊 Running 9-point analysis...")
        context = BusinessContext(
            trade_type=trade,
            location=location,
            years_in_business=5,
            current_rate=float(hourly_rate),
            hours_per_week=45,
            revenue_goal=250000
        )
        
        analyzer = Analyzer()
        analysis = analyzer.analyze(combined, context)
        
        st.write("📄 Generating your reports...")
        generator = ReportGenerator(output_dir="./output")
        report = generator.generate_report(analysis, context, business_name)
        
        status.update(label="✅ Audit complete!", state="complete")
    
    # Results
    opp = analysis.guarantee_check.get('total_opportunity', 0) * 0.7
    
    st.markdown(f"""
    <div class="result">
        <div class="result-label">Conservative opportunity identified</div>
        <div class="result-value">${opp:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if Path(report['html_report']).exists():
            with open(report['html_report'], 'r') as f:
                st.download_button("📄 Download Report", f.read(), file_name=f"{business_name.replace(' ', '_')}_report.html", mime="text/html", use_container_width=True)
    with col2:
        if Path(report['excel_report']).exists():
            with open(report['excel_report'], 'rb') as f:
                st.download_button("📊 Download Excel", f.read(), file_name=f"{business_name.replace(' ', '_')}_workbook.xlsx", use_container_width=True)
    
    st.markdown(f'<div class="info-box">📧 We\'ve also sent these reports to <strong>{email}</strong></div>', unsafe_allow_html=True)


def show_locked():
    st.markdown("""
    <div class="card">
        <div class="card-header" style="text-align: center;">
            <div class="brand" style="justify-content: center;"><span class="brand-dot"></span> Brace</div>
            <h1 class="title">Access Required</h1>
            <p class="subtitle">Complete your purchase to start your audit.</p>
        </div>
        <div class="card-body" style="text-align: center;">
    """, unsafe_allow_html=True)
    
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
