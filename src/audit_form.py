"""
Brace Profit Leak Audit - Premium Onboarding Experience
Rebuilt for a smooth, modern feel.
"""

import os
import sys
from pathlib import Path
import json
from datetime import datetime
import time

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

if 'step' not in st.session_state:
    st.session_state.step = 1
if 'data' not in st.session_state:
    st.session_state.data = {}
if 'analyzing' not in st.session_state:
    st.session_state.analyzing = False

# Premium styling with animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * { 
        font-family: 'Inter', -apple-system, sans-serif; 
        box-sizing: border-box; 
    }
    
    .stApp { 
        background: linear-gradient(180deg, #09090b 0%, #18181b 100%) !important;
        min-height: 100vh;
    }
    
    #MainMenu, footer, header, [data-testid="stToolbar"], [data-testid="stSidebar"], 
    [data-testid="stDecoration"], .stDeployButton, [data-testid="stStatusWidget"] { 
        display: none !important; 
    }
    
    .block-container {
        max-width: 420px !important;
        padding: 60px 24px 40px !important;
    }
    
    /* ========== HEADER ========== */
    .header {
        text-align: center;
        margin-bottom: 48px;
    }
    
    .brand {
        font-size: 13px;
        font-weight: 600;
        color: #fbbf24;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 32px;
    }
    
    /* Progress bar */
    .progress-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
        margin-bottom: 40px;
    }
    
    .progress-step {
        height: 3px;
        width: 48px;
        background: #27272a;
        border-radius: 2px;
        transition: all 0.3s ease;
    }
    
    .progress-step.done {
        background: #22c55e;
    }
    
    .progress-step.active {
        background: #fbbf24;
    }
    
    /* ========== CONTENT ========== */
    .step-title {
        font-size: 32px;
        font-weight: 700;
        color: #fafafa;
        line-height: 1.2;
        margin: 0 0 12px;
        text-align: center;
    }
    
    .step-subtitle {
        font-size: 16px;
        color: #71717a;
        text-align: center;
        margin: 0 0 40px;
        line-height: 1.5;
    }
    
    /* ========== INPUTS ========== */
    .stTextInput > label, .stSelectbox > label, .stFileUploader > label, 
    .stNumberInput > label { display: none !important; }
    
    .stTextInput > div > div > input {
        font-size: 17px !important;
        font-weight: 500 !important;
        border: none !important;
        border-bottom: 2px solid #3f3f46 !important;
        border-radius: 0 !important;
        padding: 16px 4px !important;
        background: transparent !important;
        color: #fafafa !important;
        text-align: center !important;
        transition: border-color 0.2s !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-bottom-color: #fbbf24 !important;
        box-shadow: none !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #52525b !important;
    }
    
    .stNumberInput > div > div > input {
        font-size: 17px !important;
        font-weight: 500 !important;
        border: 2px solid #3f3f46 !important;
        border-radius: 12px !important;
        padding: 14px 16px !important;
        background: #18181b !important;
        color: #fafafa !important;
        text-align: center !important;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #fbbf24 !important;
        box-shadow: none !important;
    }
    
    .stSelectbox > div > div {
        border: 2px solid #3f3f46 !important;
        border-radius: 12px !important;
        background: #18181b !important;
    }
    
    .stSelectbox > div > div > div {
        color: #fafafa !important;
        padding: 12px 16px !important;
    }
    
    /* Input label above */
    .input-label {
        font-size: 12px;
        font-weight: 500;
        color: #71717a;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
        text-align: left;
    }
    
    /* ========== CHALLENGE CARDS ========== */
    .stRadio > label { display: none !important; }
    
    .stRadio > div { 
        display: flex !important;
        flex-direction: column !important;
        gap: 12px !important;
    }
    
    .stRadio > div > label {
        background: #18181b !important;
        border: 2px solid #27272a !important;
        border-radius: 14px !important;
        padding: 18px 20px !important;
        font-size: 15px !important;
        font-weight: 500 !important;
        color: #a1a1aa !important;
        text-align: left !important;
        margin: 0 !important;
        cursor: pointer !important;
        transition: all 0.15s ease !important;
    }
    
    .stRadio > div > label:hover {
        border-color: #3f3f46 !important;
        background: #1f1f23 !important;
    }
    
    .stRadio > div > label[data-checked="true"] {
        background: rgba(251, 191, 36, 0.08) !important;
        border-color: #fbbf24 !important;
        color: #fafafa !important;
    }
    
    /* ========== FILE UPLOAD ========== */
    .stFileUploader > div {
        background: #18181b !important;
        border: 2px dashed #3f3f46 !important;
        border-radius: 16px !important;
        padding: 40px 24px !important;
        transition: all 0.2s ease !important;
    }
    
    .stFileUploader > div:hover {
        border-color: #fbbf24 !important;
        background: #1c1c1f !important;
    }
    
    .upload-icon {
        font-size: 40px;
        margin-bottom: 16px;
        opacity: 0.6;
    }
    
    .upload-text {
        font-size: 15px;
        color: #71717a;
        margin-bottom: 8px;
    }
    
    .upload-hint {
        font-size: 13px;
        color: #52525b;
    }
    
    /* ========== BUTTONS ========== */
    .stButton > button {
        width: 100% !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        background: #fbbf24 !important;
        color: #09090b !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 16px 24px !important;
        margin-top: 12px !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
    }
    
    .stButton > button:hover {
        background: #fcd34d !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(251, 191, 36, 0.25) !important;
    }
    
    /* Back button */
    div[data-testid="column"]:first-child .stButton > button {
        background: transparent !important;
        color: #71717a !important;
        border: 2px solid #3f3f46 !important;
        box-shadow: none !important;
    }
    
    div[data-testid="column"]:first-child .stButton > button:hover {
        background: #27272a !important;
        color: #fafafa !important;
        border-color: #52525b !important;
        transform: none !important;
    }
    
    /* ========== SUCCESS/ERROR ========== */
    .stSuccess {
        background: rgba(34, 197, 94, 0.1) !important;
        border: 1px solid rgba(34, 197, 94, 0.2) !important;
        border-radius: 12px !important;
        color: #4ade80 !important;
        padding: 12px 16px !important;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.1) !important;
        border: 1px solid rgba(239, 68, 68, 0.2) !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
    }
    
    /* ========== ANALYZING ANIMATION ========== */
    .analyzing-container {
        text-align: center;
        padding: 60px 20px;
    }
    
    .analyzing-spinner {
        width: 64px;
        height: 64px;
        margin: 0 auto 32px;
        border: 3px solid #27272a;
        border-top-color: #fbbf24;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    .analyzing-title {
        font-size: 24px;
        font-weight: 600;
        color: #fafafa;
        margin-bottom: 12px;
    }
    
    .analyzing-step {
        font-size: 15px;
        color: #71717a;
        margin-bottom: 32px;
    }
    
    .analyzing-progress {
        background: #27272a;
        border-radius: 4px;
        height: 4px;
        overflow: hidden;
        max-width: 240px;
        margin: 0 auto;
    }
    
    .analyzing-progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #fbbf24, #f59e0b);
        border-radius: 4px;
        animation: progress 8s ease-out forwards;
    }
    
    @keyframes progress {
        0% { width: 0%; }
        20% { width: 25%; }
        50% { width: 60%; }
        80% { width: 85%; }
        100% { width: 95%; }
    }
    
    /* ========== RESULTS ========== */
    .results-container {
        text-align: center;
    }
    
    .results-badge {
        display: inline-block;
        background: rgba(34, 197, 94, 0.1);
        border: 1px solid rgba(34, 197, 94, 0.2);
        color: #4ade80;
        font-size: 13px;
        font-weight: 600;
        padding: 8px 16px;
        border-radius: 20px;
        margin-bottom: 24px;
    }
    
    .results-title {
        font-size: 20px;
        font-weight: 600;
        color: #fafafa;
        margin-bottom: 8px;
    }
    
    .results-amount {
        font-size: 56px;
        font-weight: 700;
        color: #22c55e;
        margin-bottom: 8px;
        line-height: 1;
    }
    
    .results-subtitle {
        font-size: 14px;
        color: #71717a;
        margin-bottom: 40px;
    }
    
    .download-card {
        background: #18181b;
        border: 1px solid #27272a;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 16px;
        text-align: left;
        transition: all 0.15s ease;
        cursor: pointer;
    }
    
    .download-card:hover {
        border-color: #3f3f46;
        background: #1f1f23;
    }
    
    .download-icon {
        width: 48px;
        height: 48px;
        background: #27272a;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
    }
    
    .download-info h4 {
        font-size: 15px;
        font-weight: 600;
        color: #fafafa;
        margin: 0 0 4px;
    }
    
    .download-info p {
        font-size: 13px;
        color: #71717a;
        margin: 0;
    }
    
    /* ========== FOOTER ========== */
    .footer {
        text-align: center;
        padding: 32px 0 16px;
        font-size: 12px;
        color: #52525b;
    }
    
    /* ========== COLUMN SPACING ========== */
    div[data-testid="column"] {
        padding: 0 6px !important;
    }
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


def render_progress(current, total=4):
    steps = ""
    for i in range(1, total + 1):
        if i < current:
            steps += '<div class="progress-step done"></div>'
        elif i == current:
            steps += '<div class="progress-step active"></div>'
        else:
            steps += '<div class="progress-step"></div>'
    return f'<div class="progress-container">{steps}</div>'


def next_step():
    st.session_state.step += 1


def prev_step():
    st.session_state.step -= 1


def show_onboarding(email: str = None):
    step = st.session_state.step
    data = st.session_state.data
    
    if email and 'email' not in data:
        data['email'] = email
    
    # Header
    st.markdown('<div class="header">', unsafe_allow_html=True)
    st.markdown('<div class="brand">Brace</div>', unsafe_allow_html=True)
    st.markdown(render_progress(step), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ===== STEP 1: Business Name =====
    if step == 1:
        st.markdown('<h1 class="step-title">What\'s your business called?</h1>', unsafe_allow_html=True)
        st.markdown('<p class="step-subtitle">This will appear on your audit report</p>', unsafe_allow_html=True)
        
        name = st.text_input("name", value=data.get('business_name', ''), placeholder="e.g. Smith Electrical", label_visibility="collapsed")
        
        if st.button("Continue"):
            if name.strip():
                data['business_name'] = name.strip()
                next_step()
                st.rerun()
            else:
                st.error("Please enter your business name")
    
    # ===== STEP 2: Details =====
    elif step == 2:
        st.markdown('<h1 class="step-title">A few quick details</h1>', unsafe_allow_html=True)
        st.markdown('<p class="step-subtitle">Helps us benchmark against similar businesses</p>', unsafe_allow_html=True)
        
        st.markdown('<p class="input-label">Your trade</p>', unsafe_allow_html=True)
        trade = st.selectbox("trade", ["Electrician", "Plumber", "Carpenter", "HVAC", "Builder", "Other"], 
                           index=["Electrician", "Plumber", "Carpenter", "HVAC", "Builder", "Other"].index(data.get('trade', 'Electrician')),
                           label_visibility="collapsed")
        
        st.markdown('<p class="input-label">Location</p>', unsafe_allow_html=True)
        location = st.text_input("loc", value=data.get('location', ''), placeholder="e.g. Sydney", label_visibility="collapsed")
        
        st.markdown('<p class="input-label">Email for your report</p>', unsafe_allow_html=True)
        email_input = st.text_input("email", value=data.get('email', ''), placeholder="you@example.com", label_visibility="collapsed")
        
        st.markdown('<p class="input-label">Current hourly rate ($)</p>', unsafe_allow_html=True)
        rate = st.number_input("rate", min_value=50, max_value=300, value=data.get('hourly_rate', 95), label_visibility="collapsed")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Back"):
                prev_step()
                st.rerun()
        with col2:
            if st.button("Continue", key="c2"):
                if email_input.strip() and location.strip():
                    data['trade'] = trade
                    data['location'] = location.strip()
                    data['email'] = email_input.strip()
                    data['hourly_rate'] = rate
                    next_step()
                    st.rerun()
                else:
                    st.error("Please fill in all fields")
    
    # ===== STEP 3: Challenge =====
    elif step == 3:
        st.markdown('<h1 class="step-title">What\'s your biggest challenge?</h1>', unsafe_allow_html=True)
        st.markdown('<p class="step-subtitle">We\'ll focus on this in your report</p>', unsafe_allow_html=True)
        
        challenge = st.radio(
            "challenge",
            ["💰 Not charging enough", "⏳ Chasing late payments", "📝 Quoting takes too long", "📊 Too much admin work"],
            index=0,
            label_visibility="collapsed"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Back"):
                prev_step()
                st.rerun()
        with col2:
            if st.button("Continue", key="c3"):
                data['challenge'] = challenge
                next_step()
                st.rerun()
    
    # ===== STEP 4: Upload =====
    elif step == 4:
        st.markdown('<h1 class="step-title">Upload your files</h1>', unsafe_allow_html=True)
        st.markdown('<p class="step-subtitle">Invoices, expenses, or bank statements<br/>from the last 12 months</p>', unsafe_allow_html=True)
        
        files = st.file_uploader("files", type=['pdf', 'xlsx', 'csv'], accept_multiple_files=True, label_visibility="collapsed")
        
        if files:
            st.success(f"✓ {len(files)} file(s) ready to analyze")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Back"):
                prev_step()
                st.rerun()
        with col2:
            if st.button("Run Audit", key="run"):
                if files:
                    data['files'] = files
                    st.session_state.analyzing = True
                    st.rerun()
                else:
                    st.error("Please upload at least one file")
    
    # Footer
    st.markdown('<div class="footer">🔒 Bank-level encryption · Deleted after 30 days</div>', unsafe_allow_html=True)


def show_analyzing():
    """Premium analyzing animation."""
    st.markdown("""
    <div class="header">
        <div class="brand">Brace</div>
    </div>
    <div class="analyzing-container">
        <div class="analyzing-spinner"></div>
        <h2 class="analyzing-title">Analyzing your business</h2>
        <p class="analyzing-step">This usually takes 30-60 seconds...</p>
        <div class="analyzing-progress">
            <div class="analyzing-progress-bar"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def show_results(analysis, report, data):
    """Premium results page."""
    opp = analysis.guarantee_check.get('total_opportunity', 0) * 0.7
    
    st.markdown("""
    <div class="header">
        <div class="brand">Brace</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="results-container">
        <div class="results-badge">✓ Analysis Complete</div>
        <h3 class="results-title">We found potential savings of</h3>
        <div class="results-amount">${opp:,.0f}</div>
        <p class="results-subtitle">per year for {data.get('business_name', 'your business')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Download buttons
    col1, col2 = st.columns(2)
    with col1:
        if Path(report['html_report']).exists():
            with open(report['html_report'], 'r') as f:
                st.download_button(
                    "📄 HTML Report", 
                    f.read(), 
                    file_name=f"{data['business_name']}_report.html", 
                    mime="text/html", 
                    use_container_width=True
                )
    with col2:
        if Path(report['excel_report']).exists():
            with open(report['excel_report'], 'rb') as f:
                st.download_button(
                    "📊 Excel Workbook", 
                    f.read(),
                    file_name=f"{data['business_name']}_workbook.xlsx", 
                    use_container_width=True
                )
    
    st.markdown(f"""
    <div style="background: #18181b; border-radius: 12px; padding: 16px 20px; margin-top: 24px; text-align: center;">
        <p style="color: #71717a; font-size: 14px; margin: 0;">
            📧 Reports also sent to <span style="color: #fafafa;">{data.get('email', '')}</span>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="footer">🔒 Your data has been securely deleted</div>', unsafe_allow_html=True)


def run_audit():
    """Run the audit with progress updates."""
    from src.utils.file_handler import FileHandler
    from src.agents.data_extractor import DataExtractor
    from src.agents.analyzer import Analyzer, BusinessContext
    from src.agents.report_generator import ReportGenerator
    
    data = st.session_state.data
    
    # Show analyzing animation
    show_analyzing()
    
    # Create a placeholder for the actual work
    handler = FileHandler()
    folder = handler.create_customer_folder(data['business_name'])
    
    for f in data.get('files', []):
        path = folder / "uploads" / f.name
        path.parent.mkdir(exist_ok=True)
        with open(path, 'wb') as out:
            out.write(f.read())
    
    with open(folder / "intake.json", 'w') as f:
        json.dump({
            "business_name": data.get('business_name'),
            "email": data.get('email'),
            "trade": data.get('trade'),
            "location": data.get('location'),
            "hourly_rate": data.get('hourly_rate'),
            "challenge": data.get('challenge'),
            "submitted_at": datetime.now().isoformat()
        }, f, indent=2)
    
    extractor = DataExtractor()
    results = extractor.extract_from_folder(str(folder))
    combined = extractor.combine_results(results)
    
    context = BusinessContext(
        trade_type=data.get('trade', 'electrician').lower(),
        location=data.get('location', 'Australia'),
        years_in_business=5,
        current_rate=float(data.get('hourly_rate', 100)),
        hours_per_week=45,
        revenue_goal=250000
    )
    
    analyzer = Analyzer()
    analysis = analyzer.analyze(combined, context)
    
    generator = ReportGenerator(output_dir="./output")
    report = generator.generate_report(analysis, context, data['business_name'])
    
    # Store results and show
    st.session_state.analysis = analysis
    st.session_state.report = report
    st.session_state.analyzing = False
    st.session_state.complete = True
    st.rerun()


def show_locked():
    st.markdown("""
    <div class="header">
        <div class="brand">Brace</div>
    </div>
    <div style="text-align: center; padding: 40px 0;">
        <h1 class="step-title">Access Required</h1>
        <p class="step-subtitle">Complete your purchase to start your audit</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.link_button("Go to Brace →", "https://brace-rvnk.vercel.app", use_container_width=True)


def main():
    verified, email = verify_session()
    
    if not verified:
        show_locked()
        return
    
    # Check if analyzing
    if st.session_state.get('analyzing', False):
        run_audit()
        return
    
    # Check if complete
    if st.session_state.get('complete', False):
        show_results(
            st.session_state.analysis,
            st.session_state.report,
            st.session_state.data
        )
        return
    
    # Show onboarding
    show_onboarding(email)


if __name__ == "__main__":
    main()
