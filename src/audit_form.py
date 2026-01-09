"""
Brace Business Growth Audit - Enhanced Onboarding Experience
Captures comprehensive business data for deep analysis + agent roadmap building.
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
    page_title="Brace | Business Growth Audit",
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
if 'analyzing' not in st.session_state:
    st.session_state.analyzing = False

TOTAL_STEPS = 7

# Premium styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * { font-family: 'Inter', -apple-system, sans-serif; box-sizing: border-box; }
    
    .stApp { 
        background: linear-gradient(180deg, #09090b 0%, #18181b 100%) !important;
        min-height: 100vh;
    }
    
    #MainMenu, footer, header, [data-testid="stToolbar"], [data-testid="stSidebar"], 
    [data-testid="stDecoration"], .stDeployButton, [data-testid="stStatusWidget"] { 
        display: none !important; 
    }
    
    .block-container {
        max-width: 520px !important;
        padding: 40px 24px 40px !important;
    }
    
    /* ========== HEADER ========== */
    .header {
        text-align: center;
        margin-bottom: 32px;
    }
    
    .brand {
        font-size: 13px;
        font-weight: 600;
        color: #fbbf24;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 24px;
    }
    
    .step-indicator {
        font-size: 12px;
        color: #52525b;
        margin-bottom: 8px;
    }
    
    /* Progress bar */
    .progress-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 4px;
        margin-bottom: 32px;
    }
    
    .progress-step {
        height: 3px;
        width: 36px;
        background: #27272a;
        border-radius: 2px;
        transition: all 0.3s ease;
    }
    
    .progress-step.done { background: #22c55e; }
    .progress-step.active { background: #fbbf24; }
    
    /* ========== CONTENT ========== */
    .step-title {
        font-size: 28px;
        font-weight: 700;
        color: #fafafa;
        line-height: 1.2;
        margin: 0 0 8px;
        text-align: center;
    }
    
    .step-subtitle {
        font-size: 15px;
        color: #71717a;
        text-align: center;
        margin: 0 0 32px;
        line-height: 1.5;
    }
    
    .section-header {
        font-size: 11px;
        font-weight: 600;
        color: #fbbf24;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin: 24px 0 16px;
        padding-top: 16px;
        border-top: 1px solid #27272a;
    }
    
    .section-header:first-of-type {
        border-top: none;
        margin-top: 0;
        padding-top: 0;
    }
    
    /* ========== INPUTS ========== */
    .stTextInput > label, .stSelectbox > label, .stFileUploader > label, 
    .stNumberInput > label, .stTextArea > label, .stMultiSelect > label { 
        display: none !important; 
    }
    
    .input-label {
        font-size: 13px;
        font-weight: 500;
        color: #a1a1aa;
        margin-bottom: 8px;
        display: block;
    }
    
    .input-hint {
        font-size: 12px;
        color: #52525b;
        margin-top: 4px;
        font-style: italic;
    }
    
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        font-size: 15px !important;
        font-weight: 500 !important;
        border: 2px solid #3f3f46 !important;
        border-radius: 10px !important;
        padding: 12px 14px !important;
        background: #18181b !important;
        color: #fafafa !important;
        transition: border-color 0.2s !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #fbbf24 !important;
        box-shadow: none !important;
    }
    
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: #52525b !important;
    }
    
    .stNumberInput > div > div > input {
        font-size: 15px !important;
        font-weight: 500 !important;
        border: 2px solid #3f3f46 !important;
        border-radius: 10px !important;
        padding: 12px 14px !important;
        background: #18181b !important;
        color: #fafafa !important;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #fbbf24 !important;
        box-shadow: none !important;
    }
    
    .stSelectbox > div > div {
        border: 2px solid #3f3f46 !important;
        border-radius: 10px !important;
        background: #18181b !important;
    }
    
    .stSelectbox > div > div > div {
        color: #fafafa !important;
        padding: 10px 14px !important;
    }
    
    .stMultiSelect > div > div {
        border: 2px solid #3f3f46 !important;
        border-radius: 10px !important;
        background: #18181b !important;
    }
    
    /* ========== RADIO/CHECKBOX CARDS ========== */
    .stRadio > label { display: none !important; }
    
    .stRadio > div { 
        display: flex !important;
        flex-direction: column !important;
        gap: 10px !important;
    }
    
    .stRadio > div > label {
        background: #18181b !important;
        border: 2px solid #27272a !important;
        border-radius: 12px !important;
        padding: 14px 16px !important;
        font-size: 14px !important;
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
    
    /* Checkbox styling */
    .stCheckbox > label {
        background: #18181b !important;
        border: 2px solid #27272a !important;
        border-radius: 10px !important;
        padding: 12px 14px !important;
        margin: 4px 0 !important;
    }
    
    .stCheckbox > label:hover {
        border-color: #3f3f46 !important;
    }
    
    /* ========== FILE UPLOAD ========== */
    .stFileUploader > div {
        background: #18181b !important;
        border: 2px dashed #3f3f46 !important;
        border-radius: 14px !important;
        padding: 32px 20px !important;
        transition: all 0.2s ease !important;
    }
    
    .stFileUploader > div:hover {
        border-color: #fbbf24 !important;
        background: #1c1c1f !important;
    }
    
    /* ========== SLIDER ========== */
    .stSlider > div > div > div {
        background: #3f3f46 !important;
    }
    
    .stSlider > div > div > div > div {
        background: #fbbf24 !important;
    }
    
    /* ========== BUTTONS ========== */
    .stButton > button {
        width: 100% !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        background: #fbbf24 !important;
        color: #09090b !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 14px 20px !important;
        margin-top: 8px !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
    }
    
    .stButton > button:hover {
        background: #fcd34d !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(251, 191, 36, 0.25) !important;
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
        border-radius: 10px !important;
        color: #4ade80 !important;
        padding: 10px 14px !important;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.1) !important;
        border: 1px solid rgba(239, 68, 68, 0.2) !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
    }
    
    /* ========== INFO BOX ========== */
    .info-box {
        background: rgba(59, 130, 246, 0.08);
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 10px;
        padding: 12px 16px;
        margin: 16px 0;
        font-size: 13px;
        color: #93c5fd;
    }
    
    /* ========== ANALYZING ANIMATION ========== */
    .analyzing-container {
        text-align: center;
        padding: 60px 20px;
    }
    
    .analyzing-spinner {
        width: 56px;
        height: 56px;
        margin: 0 auto 28px;
        border: 3px solid #27272a;
        border-top-color: #fbbf24;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin { to { transform: rotate(360deg); } }
    
    .analyzing-title {
        font-size: 22px;
        font-weight: 600;
        color: #fafafa;
        margin-bottom: 10px;
    }
    
    .analyzing-step {
        font-size: 14px;
        color: #71717a;
        margin-bottom: 28px;
    }
    
    .analyzing-progress {
        background: #27272a;
        border-radius: 4px;
        height: 4px;
        overflow: hidden;
        max-width: 200px;
        margin: 0 auto;
    }
    
    .analyzing-progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #fbbf24, #f59e0b);
        border-radius: 4px;
        animation: progress 12s ease-out forwards;
    }
    
    @keyframes progress {
        0% { width: 0%; }
        15% { width: 20%; }
        40% { width: 50%; }
        70% { width: 75%; }
        90% { width: 90%; }
        100% { width: 95%; }
    }
    
    /* ========== RESULTS ========== */
    .results-container { text-align: center; }
    
    .results-badge {
        display: inline-block;
        background: rgba(34, 197, 94, 0.1);
        border: 1px solid rgba(34, 197, 94, 0.2);
        color: #4ade80;
        font-size: 12px;
        font-weight: 600;
        padding: 6px 14px;
        border-radius: 16px;
        margin-bottom: 20px;
    }
    
    .results-title {
        font-size: 18px;
        font-weight: 600;
        color: #fafafa;
        margin-bottom: 6px;
    }
    
    .results-amount {
        font-size: 48px;
        font-weight: 700;
        color: #22c55e;
        margin-bottom: 6px;
        line-height: 1;
    }
    
    .results-subtitle {
        font-size: 13px;
        color: #71717a;
        margin-bottom: 32px;
    }
    
    .next-steps-card {
        background: #18181b;
        border: 1px solid #27272a;
        border-radius: 14px;
        padding: 20px;
        margin: 20px 0;
        text-align: left;
    }
    
    .next-steps-title {
        font-size: 14px;
        font-weight: 600;
        color: #fbbf24;
        margin-bottom: 12px;
    }
    
    .next-steps-item {
        font-size: 14px;
        color: #a1a1aa;
        margin: 8px 0;
        padding-left: 20px;
        position: relative;
    }
    
    .next-steps-item::before {
        content: "✓";
        position: absolute;
        left: 0;
        color: #22c55e;
    }
    
    /* ========== FOOTER ========== */
    .footer {
        text-align: center;
        padding: 24px 0 12px;
        font-size: 11px;
        color: #52525b;
    }
    
    /* ========== COLUMN SPACING ========== */
    div[data-testid="column"] { padding: 0 4px !important; }
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


def render_progress(current, total=TOTAL_STEPS):
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
    st.markdown('<div class="brand">Brace Growth Audit</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="step-indicator">Step {step} of {TOTAL_STEPS}</div>', unsafe_allow_html=True)
    st.markdown(render_progress(step), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ===== STEP 1: Business Basics =====
    if step == 1:
        st.markdown('<h1 class="step-title">Let\'s start with the basics</h1>', unsafe_allow_html=True)
        st.markdown('<p class="step-subtitle">This helps us personalize your audit</p>', unsafe_allow_html=True)
        
        st.markdown('<p class="input-label">Business Name</p>', unsafe_allow_html=True)
        name = st.text_input("name", value=data.get('business_name', ''), placeholder="e.g. Smith Electrical", label_visibility="collapsed")
        
        st.markdown('<p class="input-label">Your Trade</p>', unsafe_allow_html=True)
        trade = st.selectbox("trade", ["Electrician", "Plumber", "Carpenter", "HVAC", "Builder", "Painter", "Other"], 
                           index=["Electrician", "Plumber", "Carpenter", "HVAC", "Builder", "Painter", "Other"].index(data.get('trade', 'Electrician')),
                           label_visibility="collapsed")
        
        st.markdown('<p class="input-label">Location</p>', unsafe_allow_html=True)
        location = st.text_input("loc", value=data.get('location', ''), placeholder="e.g. Sydney, NSW", label_visibility="collapsed")
        
        st.markdown('<p class="input-label">Email (for your reports)</p>', unsafe_allow_html=True)
        email_input = st.text_input("email", value=data.get('email', ''), placeholder="you@example.com", label_visibility="collapsed")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown('<p class="input-label">Years in Business</p>', unsafe_allow_html=True)
            years = st.number_input("years", min_value=0, max_value=50, value=data.get('years_in_business', 5), label_visibility="collapsed")
        with col2:
            st.markdown('<p class="input-label">Team Size</p>', unsafe_allow_html=True)
            team = st.selectbox("team", ["Just me", "2-3", "4-6", "7-10", "10+"], 
                              index=["Just me", "2-3", "4-6", "7-10", "10+"].index(data.get('team_size', 'Just me')),
                              label_visibility="collapsed")
        
        if st.button("Continue"):
            if name.strip() and location.strip() and email_input.strip():
                data['business_name'] = name.strip()
                data['trade'] = trade
                data['location'] = location.strip()
                data['email'] = email_input.strip()
                data['years_in_business'] = years
                data['team_size'] = team
                next_step()
                st.rerun()
            else:
                st.error("Please fill in all fields")
    
    # ===== STEP 2: Financial Data =====
    elif step == 2:
        st.markdown('<h1 class="step-title">Your Pricing & Financials</h1>', unsafe_allow_html=True)
        st.markdown('<p class="step-subtitle">We\'ll benchmark against 2026 market data</p>', unsafe_allow_html=True)
        
        st.markdown('<p class="input-label">Current Hourly Rate ($)</p>', unsafe_allow_html=True)
        rate = st.number_input("rate", min_value=50, max_value=400, value=data.get('hourly_rate', 95), label_visibility="collapsed")
        
        st.markdown('<p class="input-label">Do you charge a call-out fee?</p>', unsafe_allow_html=True)
        callout = st.radio("callout", ["No call-out fee", "Yes - under $80", "Yes - $80 to $120", "Yes - over $120"], 
                          index=["No call-out fee", "Yes - under $80", "Yes - $80 to $120", "Yes - over $120"].index(data.get('callout_fee', 'No call-out fee')),
                          label_visibility="collapsed")
        
        st.markdown('<p class="input-label">Materials Markup (%)</p>', unsafe_allow_html=True)
        markup = st.slider("markup", 0, 50, data.get('materials_markup', 15), format="%d%%", label_visibility="collapsed")
        st.markdown(f'<p class="input-hint">You currently add {markup}% to materials cost</p>', unsafe_allow_html=True)
        
        st.markdown('<p class="input-label">Approximate Annual Revenue</p>', unsafe_allow_html=True)
        revenue = st.selectbox("revenue", ["Under $150k", "$150k - $250k", "$250k - $400k", "$400k - $600k", "$600k - $800k", "$800k+"],
                             index=["Under $150k", "$150k - $250k", "$250k - $400k", "$400k - $600k", "$600k - $800k", "$800k+"].index(data.get('revenue_range', '$150k - $250k')),
                             label_visibility="collapsed")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Back"):
                prev_step()
                st.rerun()
        with col2:
            if st.button("Continue", key="c2"):
                data['hourly_rate'] = rate
                data['callout_fee'] = callout
                data['materials_markup'] = markup
                data['revenue_range'] = revenue
                next_step()
                st.rerun()
    
    # ===== STEP 3: Lead Generation =====
    elif step == 3:
        st.markdown('<h1 class="step-title">How You Get Customers</h1>', unsafe_allow_html=True)
        st.markdown('<p class="step-subtitle">Understanding your lead sources helps us find growth opportunities</p>', unsafe_allow_html=True)
        
        st.markdown('<p class="input-label">Where do most of your customers come from?</p>', unsafe_allow_html=True)
        lead_sources = st.multiselect("sources", 
            ["Google Search", "Word of Mouth / Referrals", "Facebook / Social Media", "Repeat Customers", "HiPages / Airtasker", "Paid Ads", "Other"],
            default=data.get('lead_sources', ["Word of Mouth / Referrals"]),
            label_visibility="collapsed"
        )
        
        st.markdown('<p class="input-label">How many leads/enquiries per week?</p>', unsafe_allow_html=True)
        leads_per_week = st.radio("leads", ["1-3", "4-7", "8-15", "15+"],
                                 index=["1-3", "4-7", "8-15", "15+"].index(data.get('leads_per_week', '4-7')),
                                 label_visibility="collapsed", horizontal=True)
        
        st.markdown('<p class="input-label">What % of leads turn into paid jobs?</p>', unsafe_allow_html=True)
        close_rate = st.slider("close", 10, 90, data.get('close_rate', 40), format="%d%%", label_visibility="collapsed")
        
        st.markdown('<p class="input-label">Your Google Business star rating</p>', unsafe_allow_html=True)
        google_rating = st.selectbox("rating", ["No Google profile", "Under 4.0", "4.0 - 4.4", "4.5 - 4.7", "4.8 - 5.0"],
                                    index=["No Google profile", "Under 4.0", "4.0 - 4.4", "4.5 - 4.7", "4.8 - 5.0"].index(data.get('google_rating', '4.5 - 4.7')),
                                    label_visibility="collapsed")
        
        st.markdown('<p class="input-label">Number of Google reviews</p>', unsafe_allow_html=True)
        google_reviews = st.selectbox("reviews", ["0", "1-5", "6-15", "16-30", "30+"],
                                     index=["0", "1-5", "6-15", "16-30", "30+"].index(data.get('google_reviews', '6-15')),
                                     label_visibility="collapsed")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Back"):
                prev_step()
                st.rerun()
        with col2:
            if st.button("Continue", key="c3"):
                data['lead_sources'] = lead_sources
                data['leads_per_week'] = leads_per_week
                data['close_rate'] = close_rate
                data['google_rating'] = google_rating
                data['google_reviews'] = google_reviews
                next_step()
                st.rerun()
    
    # ===== STEP 4: Quoting Process =====
    elif step == 4:
        st.markdown('<h1 class="step-title">Your Quoting Process</h1>', unsafe_allow_html=True)
        st.markdown('<p class="step-subtitle">Quoting is often the biggest time drain—let\'s see where you stand</p>', unsafe_allow_html=True)
        
        st.markdown('<p class="input-label">How do you create quotes?</p>', unsafe_allow_html=True)
        quote_method = st.radio("method", 
            ["Mental math + text/call", "Email with rough numbers", "Word doc / PDF template", "Quoting software (Tradify, ServiceM8, etc)", "Spreadsheet template"],
            index=["Mental math + text/call", "Email with rough numbers", "Word doc / PDF template", "Quoting software (Tradify, ServiceM8, etc)", "Spreadsheet template"].index(data.get('quote_method', 'Mental math + text/call')),
            label_visibility="collapsed"
        )
        
        st.markdown('<p class="input-label">How long does a typical quote take you?</p>', unsafe_allow_html=True)
        quote_time = st.radio("time", ["5-10 minutes", "15-30 minutes", "30-60 minutes", "Over an hour"],
                             index=["5-10 minutes", "15-30 minutes", "30-60 minutes", "Over an hour"].index(data.get('quote_time', '15-30 minutes')),
                             label_visibility="collapsed")
        
        st.markdown('<p class="input-label">Quotes you send per month</p>', unsafe_allow_html=True)
        quotes_per_month = st.selectbox("quotes", ["Under 10", "10-20", "20-40", "40+"],
                                       index=["Under 10", "10-20", "20-40", "40+"].index(data.get('quotes_per_month', '10-20')),
                                       label_visibility="collapsed")
        
        st.markdown('<p class="input-label">How quickly do quotes go out after the enquiry?</p>', unsafe_allow_html=True)
        quote_speed = st.radio("speed", ["Same day", "Within 48 hours", "Within a week", "Longer / depends"],
                              index=["Same day", "Within 48 hours", "Within a week", "Longer / depends"].index(data.get('quote_speed', 'Within 48 hours')),
                              label_visibility="collapsed")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Back"):
                prev_step()
                st.rerun()
        with col2:
            if st.button("Continue", key="c4"):
                data['quote_method'] = quote_method
                data['quote_time'] = quote_time
                data['quotes_per_month'] = quotes_per_month
                data['quote_speed'] = quote_speed
                next_step()
                st.rerun()
    
    # ===== STEP 5: Operations & Tools =====
    elif step == 5:
        st.markdown('<h1 class="step-title">How You Work</h1>', unsafe_allow_html=True)
        st.markdown('<p class="step-subtitle">Understanding your systems helps us find efficiency gains</p>', unsafe_allow_html=True)
        
        st.markdown('<p class="input-label">Software/tools you use (select all that apply)</p>', unsafe_allow_html=True)
        tools = st.multiselect("tools",
            ["Xero", "MYOB", "QuickBooks", "Tradify", "ServiceM8", "Simpro", "Google Sheets / Excel", "Paper / manual", "None"],
            default=data.get('tools_used', ["Paper / manual"]),
            label_visibility="collapsed"
        )
        
        st.markdown('<p class="input-label">How do you track jobs/schedule?</p>', unsafe_allow_html=True)
        job_tracking = st.radio("tracking",
            ["Paper diary / notebook", "Google Calendar / phone", "Job management software", "Spreadsheet", "In my head"],
            index=["Paper diary / notebook", "Google Calendar / phone", "Job management software", "Spreadsheet", "In my head"].index(data.get('job_tracking', 'Google Calendar / phone')),
            label_visibility="collapsed"
        )
        
        st.markdown('<p class="input-label">How do you follow up with leads who haven\'t responded?</p>', unsafe_allow_html=True)
        follow_up = st.radio("followup",
            ["I remember to check manually", "Calendar reminders", "Automated system", "I don't follow up consistently"],
            index=["I remember to check manually", "Calendar reminders", "Automated system", "I don't follow up consistently"].index(data.get('follow_up_method', 'I don\'t follow up consistently')),
            label_visibility="collapsed"
        )
        
        st.markdown('<p class="input-label">What takes the most non-billable time each week?</p>', unsafe_allow_html=True)
        biggest_time_waste = st.radio("timewaste",
            ["Creating quotes", "Following up with leads", "Invoicing / chasing payments", "Scheduling jobs", "General admin / paperwork", "Finding new customers"],
            index=["Creating quotes", "Following up with leads", "Invoicing / chasing payments", "Scheduling jobs", "General admin / paperwork", "Finding new customers"].index(data.get('biggest_time_waste', 'Creating quotes')),
            label_visibility="collapsed"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Back"):
                prev_step()
                st.rerun()
        with col2:
            if st.button("Continue", key="c5"):
                data['tools_used'] = tools
                data['job_tracking'] = job_tracking
                data['follow_up_method'] = follow_up
                data['biggest_time_waste'] = biggest_time_waste
                next_step()
                st.rerun()
    
    # ===== STEP 6: Goals & Challenges =====
    elif step == 6:
        st.markdown('<h1 class="step-title">Your Goals & Challenges</h1>', unsafe_allow_html=True)
        st.markdown('<p class="step-subtitle">This helps us tailor recommendations to what matters to you</p>', unsafe_allow_html=True)
        
        st.markdown('<p class="input-label">Revenue goal for 2026</p>', unsafe_allow_html=True)
        revenue_goal = st.selectbox("goal",
            ["Stay comfortable where I am", "$250k - $350k", "$350k - $500k", "$500k - $700k", "$700k - $1M", "$1M+"],
            index=["Stay comfortable where I am", "$250k - $350k", "$350k - $500k", "$500k - $700k", "$700k - $1M", "$1M+"].index(data.get('revenue_goal', '$350k - $500k')),
            label_visibility="collapsed"
        )
        
        st.markdown('<p class="input-label">Are you looking to hire in 2026?</p>', unsafe_allow_html=True)
        hiring = st.radio("hiring",
            ["No, staying solo", "Maybe, if the numbers work", "Yes, planning to hire", "Already have employees"],
            index=["No, staying solo", "Maybe, if the numbers work", "Yes, planning to hire", "Already have employees"].index(data.get('hiring_plans', 'Maybe, if the numbers work')),
            label_visibility="collapsed"
        )
        
        st.markdown('<p class="input-label">What\'s your biggest frustration in your business right now?</p>', unsafe_allow_html=True)
        frustration = st.text_area("frustration", value=data.get('biggest_frustration', ''), 
                                  placeholder="e.g. I spend too much time quoting jobs that don't convert...",
                                  height=80, label_visibility="collapsed")
        
        st.markdown('<p class="input-label">If you could fix ONE thing in your business, what would it be?</p>', unsafe_allow_html=True)
        magic_wand = st.text_area("magic", value=data.get('magic_wand', ''), 
                                 placeholder="e.g. Get paid faster, find better customers, spend less time on admin...",
                                 height=80, label_visibility="collapsed")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Back"):
                prev_step()
                st.rerun()
        with col2:
            if st.button("Continue", key="c6"):
                data['revenue_goal'] = revenue_goal
                data['hiring_plans'] = hiring
                data['biggest_frustration'] = frustration
                data['magic_wand'] = magic_wand
                next_step()
                st.rerun()
    
    # ===== STEP 7: Upload Files =====
    elif step == 7:
        st.markdown('<h1 class="step-title">Upload Your Files</h1>', unsafe_allow_html=True)
        st.markdown('<p class="step-subtitle">Invoices, quotes, expenses from the last 6-12 months<br/>The more data, the better the analysis</p>', unsafe_allow_html=True)
        
        files = st.file_uploader("files", type=['pdf', 'xlsx', 'csv', 'xls'], accept_multiple_files=True, label_visibility="collapsed")
        
        if files:
            st.success(f"✓ {len(files)} file(s) ready to analyze")
        
        st.markdown("""
        <div class="info-box">
            <strong>What to upload:</strong><br/>
            • Xero/MYOB export (ideal)<br/>
            • Invoices (PDF or spreadsheet)<br/>
            • Bank statements<br/>
            • Any quotes or expense records
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<p class="input-label">Anything else we should know? (optional)</p>', unsafe_allow_html=True)
        notes = st.text_area("notes", value=data.get('additional_notes', ''), 
                            placeholder="e.g. I had a slow few months due to injury...",
                            height=60, label_visibility="collapsed")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Back"):
                prev_step()
                st.rerun()
        with col2:
            if st.button("Run Growth Audit", key="run"):
                if files:
                    data['files'] = files
                    data['additional_notes'] = notes
                    st.session_state.analyzing = True
                    st.rerun()
                else:
                    st.error("Please upload at least one file")
    
    # Footer
    st.markdown('<div class="footer">🔒 Bank-level encryption · Your data is deleted after analysis</div>', unsafe_allow_html=True)


def show_analyzing():
    """Premium analyzing animation."""
    st.markdown("""
    <div class="header">
        <div class="brand">Brace Growth Audit</div>
    </div>
    <div class="analyzing-container">
        <div class="analyzing-spinner"></div>
        <h2 class="analyzing-title">Analyzing your business</h2>
        <p class="analyzing-step">Building your comprehensive growth report...</p>
        <div class="analyzing-progress">
            <div class="analyzing-progress-bar"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def show_results(analysis, report, data):
    """Premium results page with next steps."""
    opp = analysis.guarantee_check.get('total_opportunity', 0) * 0.7
    
    st.markdown("""
    <div class="header">
        <div class="brand">Brace Growth Audit</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="results-container">
        <div class="results-badge">✓ Analysis Complete</div>
        <h3 class="results-title">Growth opportunity identified</h3>
        <div class="results-amount">${opp:,.0f}</div>
        <p class="results-subtitle">potential annual improvement for {data.get('business_name', 'your business')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Download buttons
    col1, col2 = st.columns(2)
    with col1:
        if Path(report['html_report']).exists():
            with open(report['html_report'], 'r') as f:
                st.download_button(
                    "📄 Full Report (HTML)", 
                    f.read(), 
                    file_name=f"{data['business_name']}_growth_audit.html", 
                    mime="text/html", 
                    use_container_width=True
                )
    with col2:
        if Path(report['excel_report']).exists():
            with open(report['excel_report'], 'rb') as f:
                st.download_button(
                    "📊 Workbook (Excel)", 
                    f.read(),
                    file_name=f"{data['business_name']}_workbook.xlsx", 
                    use_container_width=True
                )
    
    # Next steps
    st.markdown("""
    <div class="next-steps-card">
        <div class="next-steps-title">What Happens Next</div>
        <div class="next-steps-item">Reports sent to your email</div>
        <div class="next-steps-item">We'll reach out within 24 hours to schedule your Growth Call</div>
        <div class="next-steps-item">90-minute strategy session to walk through your results</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background: #18181b; border-radius: 12px; padding: 14px 18px; margin-top: 16px; text-align: center;">
        <p style="color: #71717a; font-size: 13px; margin: 0;">
            📧 Reports sent to <span style="color: #fafafa;">{data.get('email', '')}</span>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="footer">Questions? Reply to your confirmation email.</div>', unsafe_allow_html=True)


def run_audit():
    """Run the audit with progress updates."""
    from src.utils.file_handler import FileHandler
    from src.agents.data_extractor import DataExtractor
    from src.agents.analyzer import Analyzer, BusinessContext
    from src.agents.report_generator import ReportGenerator
    
    data = st.session_state.data
    
    # Show analyzing animation
    show_analyzing()
    
    # Save all onboarding data
    handler = FileHandler()
    folder = handler.create_customer_folder(data['business_name'])
    
    for f in data.get('files', []):
        path = folder / "uploads" / f.name
        path.parent.mkdir(exist_ok=True)
        with open(path, 'wb') as out:
            out.write(f.read())
    
    # Save comprehensive intake data
    intake_data = {
        # Basic info
        "business_name": data.get('business_name'),
        "email": data.get('email'),
        "trade": data.get('trade'),
        "location": data.get('location'),
        "years_in_business": data.get('years_in_business'),
        "team_size": data.get('team_size'),
        
        # Financial
        "hourly_rate": data.get('hourly_rate'),
        "callout_fee": data.get('callout_fee'),
        "materials_markup": data.get('materials_markup'),
        "revenue_range": data.get('revenue_range'),
        
        # Lead generation
        "lead_sources": data.get('lead_sources'),
        "leads_per_week": data.get('leads_per_week'),
        "close_rate": data.get('close_rate'),
        "google_rating": data.get('google_rating'),
        "google_reviews": data.get('google_reviews'),
        
        # Quoting
        "quote_method": data.get('quote_method'),
        "quote_time": data.get('quote_time'),
        "quotes_per_month": data.get('quotes_per_month'),
        "quote_speed": data.get('quote_speed'),
        
        # Operations
        "tools_used": data.get('tools_used'),
        "job_tracking": data.get('job_tracking'),
        "follow_up_method": data.get('follow_up_method'),
        "biggest_time_waste": data.get('biggest_time_waste'),
        
        # Goals
        "revenue_goal": data.get('revenue_goal'),
        "hiring_plans": data.get('hiring_plans'),
        "biggest_frustration": data.get('biggest_frustration'),
        "magic_wand": data.get('magic_wand'),
        
        # Meta
        "additional_notes": data.get('additional_notes'),
        "submitted_at": datetime.now().isoformat()
    }
    
    with open(folder / "intake.json", 'w') as f:
        json.dump(intake_data, f, indent=2)
    
    # Run extraction
    extractor = DataExtractor()
    results = extractor.extract_from_folder(str(folder))
    combined = extractor.combine_results(results)
    
    # Build context with all the new data
    context = BusinessContext(
        trade_type=data.get('trade', 'electrician').lower(),
        location=data.get('location', 'Australia'),
        years_in_business=data.get('years_in_business', 5),
        current_rate=float(data.get('hourly_rate', 100)),
        hours_per_week=45,
        revenue_goal=500000,  # Could parse from revenue_goal string
        # Additional context from intake
        team_size=data.get('team_size', 'Just me'),
        lead_sources=data.get('lead_sources', []),
        close_rate=data.get('close_rate', 40),
        quote_method=data.get('quote_method', ''),
        quote_time=data.get('quote_time', ''),
        biggest_frustration=data.get('biggest_frustration', ''),
        magic_wand=data.get('magic_wand', '')
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
        <div class="brand">Brace Growth Audit</div>
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
