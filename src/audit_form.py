"""
Brace Profit Leak Audit - Step-by-Step Onboarding
Clean, guided flow that doesn't overwhelm.
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

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'data' not in st.session_state:
    st.session_state.data = {}

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * { font-family: 'Inter', -apple-system, sans-serif; box-sizing: border-box; }
    
    .stApp { background: #0a0a0a !important; }
    
    #MainMenu, footer, header, [data-testid="stToolbar"], [data-testid="stSidebar"], 
    [data-testid="stDecoration"], .stDeployButton { display: none !important; }
    
    .block-container {
        max-width: 440px !important;
        padding: 0 20px !important;
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    /* Header */
    .header {
        text-align: center;
        padding: 40px 0 32px;
    }
    
    .brand {
        font-size: 15px;
        font-weight: 600;
        color: #fbbf24;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 24px;
    }
    
    .step-indicator {
        display: flex;
        justify-content: center;
        gap: 8px;
        margin-bottom: 32px;
    }
    
    .step-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #333;
    }
    
    .step-dot.active {
        background: #fbbf24;
        width: 24px;
        border-radius: 4px;
    }
    
    .step-dot.done {
        background: #22c55e;
    }
    
    .question {
        font-size: 28px;
        font-weight: 600;
        color: #ffffff;
        line-height: 1.3;
        margin: 0 0 8px;
        text-align: center;
    }
    
    .hint {
        font-size: 15px;
        color: #71717a;
        text-align: center;
        margin: 0 0 32px;
    }
    
    /* Input styling */
    .stTextInput > label, .stSelectbox > label, .stFileUploader > label, 
    .stTextArea > label, .stNumberInput > label {
        display: none !important;
    }
    
    .stTextInput > div > div > input, .stNumberInput > div > div > input {
        font-size: 18px !important;
        font-weight: 500 !important;
        border: none !important;
        border-bottom: 2px solid #333 !important;
        border-radius: 0 !important;
        padding: 16px 0 !important;
        background: transparent !important;
        color: #fff !important;
        text-align: center !important;
    }
    
    .stTextInput > div > div > input:focus, .stNumberInput > div > div > input:focus {
        border-bottom-color: #fbbf24 !important;
        box-shadow: none !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #52525b !important;
    }
    
    .stSelectbox > div > div {
        border: 2px solid #333 !important;
        border-radius: 12px !important;
        background: transparent !important;
        color: #fff !important;
    }
    
    .stSelectbox > div > div > div {
        color: #fff !important;
    }
    
    /* File uploader */
    .stFileUploader > div {
        background: #18181b !important;
        border: 2px dashed #333 !important;
        border-radius: 16px !important;
        padding: 32px 24px !important;
    }
    
    .stFileUploader > div:hover {
        border-color: #fbbf24 !important;
        background: #1f1f23 !important;
    }
    
    /* Buttons */
    .stButton > button {
        width: 100% !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        background: #fbbf24 !important;
        color: #000 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 16px 24px !important;
        margin-top: 24px !important;
        transition: all 0.2s !important;
    }
    
    .stButton > button:hover {
        background: #fcd34d !important;
        transform: translateY(-2px) !important;
    }
    
    /* Secondary button */
    .back-btn {
        text-align: center;
        margin-top: 16px;
    }
    
    .back-btn a {
        color: #71717a;
        font-size: 14px;
        text-decoration: none;
    }
    
    /* Success states */
    .stSuccess {
        background: rgba(34, 197, 94, 0.1) !important;
        border: 1px solid rgba(34, 197, 94, 0.3) !important;
        border-radius: 12px !important;
        color: #22c55e !important;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.1) !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
        border-radius: 12px !important;
    }
    
    /* Option cards */
    .option-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        margin-bottom: 8px;
    }
    
    .option-card {
        background: #18181b;
        border: 2px solid #27272a;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        cursor: pointer;
        transition: all 0.15s;
    }
    
    .option-card:hover {
        border-color: #fbbf24;
        background: #1f1f23;
    }
    
    .option-card.selected {
        border-color: #fbbf24;
        background: rgba(251, 191, 36, 0.1);
    }
    
    .option-icon {
        font-size: 24px;
        margin-bottom: 8px;
    }
    
    .option-label {
        font-size: 14px;
        font-weight: 500;
        color: #fff;
    }
    
    /* Result */
    .result-card {
        background: linear-gradient(135deg, #064e3b 0%, #0a0a0a 100%);
        border: 1px solid #22c55e;
        border-radius: 20px;
        padding: 40px 24px;
        text-align: center;
        margin: 20px 0;
    }
    
    .result-label {
        font-size: 14px;
        color: #86efac;
        margin-bottom: 8px;
    }
    
    .result-value {
        font-size: 48px;
        font-weight: 700;
        color: #22c55e;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 24px 0;
        font-size: 12px;
        color: #52525b;
    }
    
    /* Radio as cards */
    .stRadio > label { display: none !important; }
    .stRadio > div { 
        display: grid !important;
        grid-template-columns: 1fr 1fr !important;
        gap: 10px !important;
    }
    
    .stRadio > div > label {
        background: #18181b !important;
        border: 2px solid #27272a !important;
        border-radius: 10px !important;
        padding: 14px 12px !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        color: #a1a1aa !important;
        text-align: center !important;
        margin: 0 !important;
        cursor: pointer !important;
    }
    
    .stRadio > div > label:hover {
        border-color: #52525b !important;
    }
    
    .stRadio > div > label[data-checked="true"] {
        background: rgba(251, 191, 36, 0.1) !important;
        border-color: #fbbf24 !important;
        color: #fbbf24 !important;
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


def render_step_dots(current, total=4):
    dots = ""
    for i in range(1, total + 1):
        if i < current:
            dots += '<div class="step-dot done"></div>'
        elif i == current:
            dots += '<div class="step-dot active"></div>'
        else:
            dots += '<div class="step-dot"></div>'
    return f'<div class="step-indicator">{dots}</div>'


def next_step():
    st.session_state.step += 1


def prev_step():
    st.session_state.step -= 1


def show_onboarding(email: str = None):
    
    step = st.session_state.step
    data = st.session_state.data
    
    # Pre-fill email if provided
    if email and 'email' not in data:
        data['email'] = email
    
    st.markdown('<div class="header"><div class="brand">Brace</div>', unsafe_allow_html=True)
    st.markdown(render_step_dots(step), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ===== STEP 1: Business Name =====
    if step == 1:
        st.markdown('<h1 class="question">What\'s your business name?</h1>', unsafe_allow_html=True)
        st.markdown('<p class="hint">We\'ll use this to personalize your report</p>', unsafe_allow_html=True)
        
        name = st.text_input("name", value=data.get('business_name', ''), placeholder="e.g. Smith Electrical", label_visibility="collapsed")
        
        if st.button("Continue →"):
            if name:
                data['business_name'] = name
                next_step()
                st.rerun()
            else:
                st.error("Please enter your business name")
    
    # ===== STEP 2: Quick Details =====
    elif step == 2:
        st.markdown('<h1 class="question">Tell us a bit more</h1>', unsafe_allow_html=True)
        st.markdown('<p class="hint">Helps us benchmark against similar tradies</p>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            trade = st.selectbox("trade", ["Electrician", "Plumber", "Carpenter", "HVAC", "Builder", "Other"], 
                               index=["Electrician", "Plumber", "Carpenter", "HVAC", "Builder", "Other"].index(data.get('trade', 'Electrician')),
                               label_visibility="collapsed")
        with col2:
            location = st.text_input("loc", value=data.get('location', ''), placeholder="Location (e.g. Sydney)", label_visibility="collapsed")
        
        col1, col2 = st.columns(2)
        with col1:
            email_input = st.text_input("email", value=data.get('email', ''), placeholder="Your email", label_visibility="collapsed")
        with col2:
            rate = st.number_input("rate", min_value=50, max_value=300, value=data.get('hourly_rate', 95), 
                                  placeholder="Hourly rate ($)", label_visibility="collapsed")
        
        if st.button("Continue →"):
            if email_input and location:
                data['trade'] = trade
                data['location'] = location
                data['email'] = email_input
                data['hourly_rate'] = rate
                next_step()
                st.rerun()
            else:
                st.error("Please fill in all fields")
        
        if st.button("← Back", key="back2", type="secondary"):
            prev_step()
            st.rerun()
    
    # ===== STEP 3: Biggest Challenge =====
    elif step == 3:
        st.markdown('<h1 class="question">What\'s your biggest challenge?</h1>', unsafe_allow_html=True)
        st.markdown('<p class="hint">We\'ll prioritize this in your report</p>', unsafe_allow_html=True)
        
        challenge = st.radio(
            "challenge",
            ["Not charging enough", "Chasing payments", "Quoting takes too long", "Too much admin"],
            index=0,
            label_visibility="collapsed"
        )
        
        if st.button("Continue →"):
            data['challenge'] = challenge
            next_step()
            st.rerun()
        
        if st.button("← Back", key="back3", type="secondary"):
            prev_step()
            st.rerun()
    
    # ===== STEP 4: Upload Files =====
    elif step == 4:
        st.markdown('<h1 class="question">Upload your files</h1>', unsafe_allow_html=True)
        st.markdown('<p class="hint">Invoices, expenses, or bank statements from the last 12 months</p>', unsafe_allow_html=True)
        
        files = st.file_uploader("files", type=['pdf', 'xlsx', 'csv'], accept_multiple_files=True, label_visibility="collapsed")
        
        if files:
            st.success(f"✓ {len(files)} file(s) ready")
        
        if st.button("Run My Audit →"):
            if files:
                data['files'] = files
                run_audit(data)
            else:
                st.error("Please upload at least one file")
        
        if st.button("← Back", key="back4", type="secondary"):
            prev_step()
            st.rerun()
    
    # Footer
    st.markdown('<div class="footer">🔒 Bank-level encryption · Deleted after 30 days</div>', unsafe_allow_html=True)


def run_audit(data):
    from src.utils.file_handler import FileHandler
    from src.agents.data_extractor import DataExtractor
    from src.agents.analyzer import Analyzer, BusinessContext
    from src.agents.report_generator import ReportGenerator
    
    with st.status("Analyzing your business...", expanded=True) as status:
        
        st.write("Uploading files...")
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
        
        st.write("Extracting data...")
        extractor = DataExtractor()
        results = extractor.extract_from_folder(str(folder))
        combined = extractor.combine_results(results)
        
        st.write("Running analysis...")
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
        
        st.write("Creating report...")
        generator = ReportGenerator(output_dir="./output")
        report = generator.generate_report(analysis, context, data['business_name'])
        
        status.update(label="✅ Complete!", state="complete")
    
    opp = analysis.guarantee_check.get('total_opportunity', 0) * 0.7
    
    st.markdown(f"""
    <div class="result-card">
        <div class="result-label">Opportunity identified</div>
        <div class="result-value">${opp:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if Path(report['html_report']).exists():
            with open(report['html_report'], 'r') as f:
                st.download_button("📄 Download Report", f.read(), 
                    file_name=f"{data['business_name']}_report.html", mime="text/html", use_container_width=True)
    with col2:
        if Path(report['excel_report']).exists():
            with open(report['excel_report'], 'rb') as f:
                st.download_button("📊 Download Excel", f.read(),
                    file_name=f"{data['business_name']}_workbook.xlsx", use_container_width=True)
    
    st.success(f"📧 Reports also sent to {data.get('email')}")


def show_locked():
    st.markdown("""
    <div class="header">
        <div class="brand">Brace</div>
        <h1 class="question">Access Required</h1>
        <p class="hint">Complete your purchase to start your audit</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.link_button("Go to Brace →", "https://brace-rvnk.vercel.app", use_container_width=True)


def main():
    verified, email = verify_session()
    if verified:
        show_onboarding(email)
    else:
        show_locked()


if __name__ == "__main__":
    main()
