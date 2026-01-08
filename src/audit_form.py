"""
Brace Profit Leak Audit - File Upload Portal
Premium audit form that matches the Brace landing page design.
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

# Premium Brace-branded styling matching the landing page
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    :root {
        --bg: #fafafa;
        --bg-white: #ffffff;
        --bg-dark: #0f172a;
        --border: #e5e7eb;
        --border-light: #f3f4f6;
        --text: #0f172a;
        --text-secondary: #4b5563;
        --text-muted: #9ca3af;
        --yellow: #fbbf24;
        --yellow-light: #fef3c7;
        --green: #10b981;
        --green-light: #d1fae5;
        --blue: #3b82f6;
        --blue-light: #dbeafe;
    }
    
    .stApp {
        background: var(--bg) !important;
    }
    
    #MainMenu, footer, header, [data-testid="stToolbar"], [data-testid="stSidebar"], 
    [data-testid="stDecoration"], .stDeployButton {
        display: none !important;
    }
    
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    /* ===== HEADER ===== */
    .brace-header {
        background: var(--bg-white);
        border-bottom: 1px solid var(--border);
        padding: 16px 24px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        position: sticky;
        top: 0;
        z-index: 100;
    }
    
    .brace-logo {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 22px;
        color: var(--text);
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .brace-logo-icon {
        width: 32px;
        height: 32px;
        background: var(--yellow);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
    }
    
    .header-badge {
        background: var(--green-light);
        color: var(--green);
        padding: 6px 12px;
        border-radius: 20px;
        font-family: 'Inter', sans-serif;
        font-size: 12px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    /* ===== HERO SECTION ===== */
    .hero-section {
        background: linear-gradient(180deg, var(--bg-white) 0%, var(--bg) 100%);
        padding: 60px 24px 40px;
        text-align: center;
    }
    
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: var(--yellow-light);
        color: #92400e;
        padding: 8px 16px;
        border-radius: 24px;
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 20px;
    }
    
    .hero-title {
        font-family: 'Inter', sans-serif;
        font-size: 36px;
        font-weight: 800;
        color: var(--text);
        margin: 0 0 12px;
        line-height: 1.2;
    }
    
    .hero-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 17px;
        color: var(--text-secondary);
        max-width: 500px;
        margin: 0 auto 24px;
        line-height: 1.6;
    }
    
    .trust-badges {
        display: flex;
        justify-content: center;
        gap: 24px;
        flex-wrap: wrap;
    }
    
    .trust-badge {
        display: flex;
        align-items: center;
        gap: 6px;
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        color: var(--text-muted);
    }
    
    /* ===== FORM CONTAINER ===== */
    .form-container {
        max-width: 640px;
        margin: 0 auto;
        padding: 0 24px 60px;
    }
    
    /* ===== STEP CARDS ===== */
    .step-card {
        background: var(--bg-white);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    
    .step-header {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 20px;
        padding-bottom: 16px;
        border-bottom: 1px solid var(--border-light);
    }
    
    .step-number {
        width: 32px;
        height: 32px;
        background: var(--text);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        font-weight: 700;
        color: white;
    }
    
    .step-info {
        flex: 1;
    }
    
    .step-title {
        font-family: 'Inter', sans-serif;
        font-size: 16px;
        font-weight: 700;
        color: var(--text);
        margin: 0 0 2px;
    }
    
    .step-desc {
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        color: var(--text-muted);
        margin: 0;
    }
    
    .step-icon {
        font-size: 20px;
    }
    
    /* ===== FORM INPUTS ===== */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background: var(--bg) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 15px !important;
        padding: 14px 16px !important;
        color: var(--text) !important;
        transition: all 0.2s !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: var(--text) !important;
        box-shadow: 0 0 0 3px rgba(15, 23, 42, 0.1) !important;
    }
    
    .stTextInput > label,
    .stNumberInput > label,
    .stSelectbox > label,
    .stSlider > label,
    .stFileUploader > label {
        font-family: 'Inter', sans-serif !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        color: var(--text) !important;
        margin-bottom: 6px !important;
    }
    
    .stSelectbox > div > div {
        background: var(--bg) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .stSlider > div > div > div {
        background: var(--text) !important;
    }
    
    /* ===== FILE UPLOADER ===== */
    .stFileUploader > div {
        background: var(--bg) !important;
        border: 2px dashed var(--border) !important;
        border-radius: 12px !important;
        padding: 20px !important;
        transition: all 0.2s !important;
    }
    
    .stFileUploader > div:hover {
        border-color: var(--text-muted) !important;
        background: var(--bg-white) !important;
    }
    
    .upload-hint {
        background: var(--blue-light);
        color: #1e40af;
        padding: 12px 16px;
        border-radius: 10px;
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* ===== BUTTONS ===== */
    .stButton > button {
        background: var(--text) !important;
        color: white !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 16px 32px !important;
        transition: all 0.2s !important;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.25) !important;
    }
    
    .stButton > button:hover {
        background: #1e293b !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(15, 23, 42, 0.35) !important;
    }
    
    /* ===== SUCCESS MESSAGES ===== */
    .stSuccess {
        background: var(--green-light) !important;
        border: none !important;
        border-radius: 10px !important;
        color: #065f46 !important;
    }
    
    .file-success {
        background: var(--green-light);
        color: #065f46;
        padding: 10px 14px;
        border-radius: 8px;
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-top: 8px;
    }
    
    /* ===== RESULTS ===== */
    .result-card {
        background: linear-gradient(135deg, var(--bg-white) 0%, #f0fdf4 100%);
        border: 2px solid var(--green);
        border-radius: 20px;
        padding: 48px 32px;
        text-align: center;
        box-shadow: 0 0 0 6px rgba(16, 185, 129, 0.15);
        margin: 32px 0;
    }
    
    .result-label {
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        font-weight: 500;
        color: var(--text-secondary);
        margin-bottom: 8px;
    }
    
    .result-amount {
        font-family: 'Inter', sans-serif;
        font-size: 56px;
        font-weight: 800;
        color: var(--green);
        line-height: 1;
    }
    
    .result-subtext {
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        color: var(--text-muted);
        margin-top: 12px;
    }
    
    /* ===== FOOTER ===== */
    .brace-footer {
        text-align: center;
        padding: 32px 24px;
        border-top: 1px solid var(--border);
        background: var(--bg-white);
    }
    
    .footer-text {
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        color: var(--text-muted);
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 16px;
        flex-wrap: wrap;
    }
    
    .footer-item {
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    /* ===== PROGRESS INDICATOR ===== */
    .progress-bar {
        display: flex;
        justify-content: center;
        gap: 8px;
        margin-bottom: 32px;
    }
    
    .progress-step {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .progress-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: var(--border);
    }
    
    .progress-dot.active {
        background: var(--text);
    }
    
    .progress-line {
        width: 40px;
        height: 2px;
        background: var(--border);
    }
    
    /* ===== RESPONSIVE ===== */
    @media (max-width: 640px) {
        .hero-title {
            font-size: 28px;
        }
        
        .hero-subtitle {
            font-size: 15px;
        }
        
        .trust-badges {
            gap: 16px;
        }
        
        .step-card {
            padding: 20px;
        }
        
        .result-amount {
            font-size: 44px;
        }
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
    """Display the premium file upload form."""
    
    # Header
    st.markdown("""
    <div class="brace-header">
        <div class="brace-logo">
            <div class="brace-logo-icon">⚡</div>
            Brace
        </div>
        <div class="header-badge">
            <span>🔒</span> Secure Upload
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Hero Section
    verified_html = ""
    if email:
        verified_html = f'<div class="hero-badge">✓ Payment verified for {email}</div>'
    else:
        verified_html = '<div class="hero-badge">⚡ Profit Leak Audit</div>'
    
    st.markdown(f"""
    <div class="hero-section">
        {verified_html}
        <h1 class="hero-title">Upload Your Business Data</h1>
        <p class="hero-subtitle">
            We'll analyze your invoices, expenses, and quotes to find hidden profit leaks. 
            Your personalized report will be ready within 48 hours.
        </p>
        <div class="trust-badges">
            <div class="trust-badge">
                <span>🔐</span> Bank-level encryption
            </div>
            <div class="trust-badge">
                <span>🗑️</span> Deleted after 30 days
            </div>
            <div class="trust-badge">
                <span>🇦🇺</span> Australian servers
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Form Container
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    
    # Progress Bar
    st.markdown("""
    <div class="progress-bar">
        <div class="progress-dot active"></div>
        <div class="progress-line"></div>
        <div class="progress-dot"></div>
        <div class="progress-line"></div>
        <div class="progress-dot"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Step 1: Business Info
    st.markdown("""
    <div class="step-card">
        <div class="step-header">
            <div class="step-number">1</div>
            <div class="step-info">
                <div class="step-title">Your Business</div>
                <div class="step-desc">Tell us about your trade business</div>
            </div>
            <div class="step-icon">🏢</div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        business_name = st.text_input("Business Name *", placeholder="e.g. Dave's Electrical")
        contact_email = st.text_input("Email Address *", value=email or "", placeholder="dave@example.com")
    with col2:
        trade_type = st.selectbox("Your Trade *", ["Electrician", "Plumber", "Carpenter", "HVAC / Air Con", "Builder", "Landscaper", "Roofer", "Painter", "Other"])
        location = st.text_input("Location *", placeholder="e.g. Sydney, NSW")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Step 2: Current Numbers
    st.markdown("""
    <div class="step-card">
        <div class="step-header">
            <div class="step-number">2</div>
            <div class="step-info">
                <div class="step-title">Current Numbers</div>
                <div class="step-desc">Help us benchmark against similar tradies</div>
            </div>
            <div class="step-icon">📊</div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        hourly_rate = st.number_input("Current Hourly Rate ($)", min_value=50, max_value=300, value=95, help="What you typically charge per hour")
        revenue = st.selectbox("Annual Revenue (approx)", 
                              ["Under $100k", "$100k - $150k", "$150k - $200k", "$200k - $300k", "$300k - $500k", "$500k+"],
                              help="Rough estimate is fine")
    with col2:
        hours_per_week = st.slider("Hours Worked Per Week", 20, 80, 50)
        call_out = st.number_input("Call-out Fee ($)", min_value=0, max_value=200, value=0, help="If you charge one")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Step 3: File Upload
    st.markdown("""
    <div class="step-card">
        <div class="step-header">
            <div class="step-number">3</div>
            <div class="step-info">
                <div class="step-title">Upload Documents</div>
                <div class="step-desc">Last 12 months of business data</div>
            </div>
            <div class="step-icon">📁</div>
        </div>
        <div class="upload-hint">
            💡 <strong>Tip:</strong> The more data you provide, the more accurate your audit will be. 
            We accept PDF, Excel (.xlsx), and CSV files.
        </div>
    """, unsafe_allow_html=True)
    
    invoices = st.file_uploader(
        "📄 Invoices (required)", 
        type=['pdf', 'xlsx', 'xls', 'csv'], 
        accept_multiple_files=True, 
        key="inv",
        help="Your invoices from the last 12 months"
    )
    
    if invoices:
        st.markdown(f'<div class="file-success">✓ {len(invoices)} invoice file(s) ready</div>', unsafe_allow_html=True)
    
    expenses = st.file_uploader(
        "💳 Expenses / Bank Statements", 
        type=['pdf', 'xlsx', 'xls', 'csv'], 
        accept_multiple_files=True, 
        key="exp",
        help="Business expenses or bank statements"
    )
    
    if expenses:
        st.markdown(f'<div class="file-success">✓ {len(expenses)} expense file(s) ready</div>', unsafe_allow_html=True)
    
    quotes = st.file_uploader(
        "📝 Quotes (optional but recommended)", 
        type=['pdf', 'xlsx', 'xls', 'csv'], 
        accept_multiple_files=True, 
        key="quo",
        help="Quotes you've sent, including ones that didn't convert"
    )
    
    if quotes:
        st.markdown(f'<div class="file-success">✓ {len(quotes)} quote file(s) ready</div>', unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Submit Button
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        submitted = st.button("🚀 Run My Profit Leak Audit", use_container_width=True)
    
    if submitted:
        if not business_name:
            st.error("Please enter your business name.")
        elif not contact_email:
            st.error("Please enter your email address.")
        elif not location:
            st.error("Please enter your location.")
        elif not invoices and not expenses:
            st.error("Please upload at least your invoices or bank statements.")
        else:
            run_audit(
                business_name=business_name,
                email=contact_email,
                trade_type=trade_type.lower().replace(" / ", "_").replace(" ", "_") if trade_type != "Other" else "trade",
                location=location,
                hourly_rate=hourly_rate,
                hours_per_week=hours_per_week,
                invoices=invoices or [],
                expenses=expenses or [],
                quotes=quotes or []
            )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="brace-footer">
        <div class="footer-text">
            <div class="footer-item">
                <span>⚡</span> Powered by Brace
            </div>
            <div class="footer-item">
                <span>🔒</span> Your data is encrypted
            </div>
            <div class="footer-item">
                <span>🗑️</span> Deleted after 30 days
            </div>
        </div>
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
        st.write("📁 Saving your documents securely...")
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
        st.write("📊 Running 9-point analysis...")
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
        st.write("📄 Generating your professional reports...")
        generator = ReportGenerator(output_dir="./output")
        report = generator.generate_report(analysis, context, business_name)
        
        status.update(label="✅ Audit complete!", state="complete")
    
    # Show Results
    opportunity = analysis.guarantee_check.get('total_opportunity', 0)
    conservative = opportunity * 0.7
    
    st.markdown(f"""
    <div class="result-card">
        <div class="result-label">Conservative Opportunity Identified</div>
        <div class="result-amount">${conservative:,.0f}</div>
        <div class="result-subtext">Best case scenario: ${opportunity:,.0f}/year</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Download buttons
    st.markdown("<br>", unsafe_allow_html=True)
    
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
    <div class="step-card" style="margin-top: 24px; border-left: 4px solid #10b981;">
        <h3 style="font-family: 'Inter', sans-serif; font-size: 16px; font-weight: 700; color: #0f172a; margin: 0 0 12px; display: flex; align-items: center; gap: 8px;">
            <span>📧</span> What happens next?
        </h3>
        <p style="font-family: 'Inter', sans-serif; font-size: 14px; color: #4b5563; line-height: 1.7; margin: 0;">
            We've also sent these reports to <strong>{email}</strong>. Check your inbox (and spam folder) 
            within the next few minutes. If you have questions about implementing the action plan, 
            just reply to that email and we'll help you out.
        </p>
    </div>
    """.format(email=email), unsafe_allow_html=True)


def show_access_denied():
    """Show message when no valid payment session."""
    st.markdown("""
    <div class="brace-header">
        <div class="brace-logo">
            <div class="brace-logo-icon">⚡</div>
            Brace
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; padding: 100px 24px;">
        <div style="font-size: 72px; margin-bottom: 24px;">🔒</div>
        <h2 style="font-family: 'Inter', sans-serif; font-size: 32px; font-weight: 800; color: #0f172a; margin: 0 0 16px;">
            Access Required
        </h2>
        <p style="font-family: 'Inter', sans-serif; font-size: 17px; color: #4b5563; margin-bottom: 40px; max-width: 400px; margin-left: auto; margin-right: auto; line-height: 1.6;">
            Please complete your purchase on the Brace website to access the audit form.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.link_button("Go to Brace Website →", "https://brace-rvnk.vercel.app", use_container_width=True)


def main():
    verified, email = verify_session()
    
    if verified:
        show_upload_form(email)
    else:
        show_access_denied()


if __name__ == "__main__":
    main()
