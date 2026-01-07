"""
Tradie Profit Audit - Professional Portal
Clean, premium design that builds trust and justifies $797.
"""

import os
import sys
from pathlib import Path
import json
from datetime import datetime
from urllib.parse import urlencode

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import streamlit as st

st.set_page_config(
    page_title="Profit Leak Audit",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

from dotenv import load_dotenv
load_dotenv()

# Import payment module
from src.payments import create_checkout_session, verify_payment, is_test_mode

# Premium dark theme - professional but approachable
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    
    :root {
        --bg: #09090b;
        --bg-subtle: #18181b;
        --surface: #1c1c1f;
        --surface-hover: #27272a;
        --border: #27272a;
        --border-subtle: #3f3f46;
        --text: #fafafa;
        --text-secondary: #a1a1aa;
        --text-muted: #71717a;
        --orange: #f97316;
        --orange-hover: #fb923c;
        --orange-subtle: rgba(249, 115, 22, 0.1);
        --green: #22c55e;
        --green-subtle: rgba(34, 197, 94, 0.1);
    }
    
    .stApp {
        background: var(--bg);
    }
    
    #MainMenu, footer, header {
        visibility: hidden;
    }
    
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    /* Navigation */
    .nav {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 100;
        background: rgba(9, 9, 11, 0.8);
        backdrop-filter: blur(12px);
        border-bottom: 1px solid var(--border);
        padding: 16px 6%;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .nav-brand {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 18px;
        color: var(--text);
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .nav-brand span {
        color: var(--orange);
    }
    
    /* Hero */
    .hero {
        min-height: 100vh;
        display: flex;
        align-items: center;
        padding: 120px 6% 80px;
        background: 
            radial-gradient(ellipse 80% 50% at 50% -20%, rgba(249, 115, 22, 0.15), transparent),
            var(--bg);
    }
    
    .hero-content {
        max-width: 720px;
    }
    
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: var(--orange-subtle);
        border: 1px solid rgba(249, 115, 22, 0.3);
        padding: 8px 16px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 12px;
        font-weight: 500;
        color: var(--orange);
        margin-bottom: 24px;
        letter-spacing: 0.02em;
    }
    
    .hero h1 {
        font-family: 'Inter', sans-serif;
        font-size: clamp(40px, 6vw, 64px);
        font-weight: 800;
        color: var(--text);
        line-height: 1.1;
        letter-spacing: -0.03em;
        margin: 0 0 24px;
    }
    
    .hero h1 .highlight {
        background: linear-gradient(135deg, var(--orange) 0%, #fbbf24 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .hero-text {
        font-family: 'Inter', sans-serif;
        font-size: 18px;
        color: var(--text-secondary);
        line-height: 1.7;
        margin-bottom: 40px;
        max-width: 560px;
    }
    
    .hero-cta {
        display: flex;
        gap: 16px;
        flex-wrap: wrap;
        margin-bottom: 48px;
    }
    
    .btn-primary {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        font-family: 'Inter', sans-serif;
        font-size: 15px;
        font-weight: 600;
        color: var(--bg);
        background: var(--orange);
        padding: 14px 28px;
        border: none;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .btn-primary:hover {
        background: var(--orange-hover);
        transform: translateY(-2px);
    }
    
    .btn-secondary {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        font-family: 'Inter', sans-serif;
        font-size: 15px;
        font-weight: 500;
        color: var(--text);
        background: transparent;
        padding: 14px 28px;
        border: 1px solid var(--border-subtle);
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .btn-secondary:hover {
        background: var(--surface);
        border-color: var(--text-muted);
    }
    
    /* Stats row */
    .stats-row {
        display: flex;
        gap: 48px;
        padding-top: 32px;
        border-top: 1px solid var(--border);
    }
    
    .stat-item {
        display: flex;
        flex-direction: column;
        gap: 4px;
    }
    
    .stat-value {
        font-family: 'Inter', sans-serif;
        font-size: 28px;
        font-weight: 700;
        color: var(--text);
    }
    
    .stat-label {
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        color: var(--text-muted);
    }
    
    /* Section */
    .section {
        padding: 100px 6%;
    }
    
    .section-dark {
        background: var(--bg-subtle);
    }
    
    .section-header {
        max-width: 600px;
        margin-bottom: 56px;
    }
    
    .section-eyebrow {
        font-family: 'JetBrains Mono', monospace;
        font-size: 12px;
        font-weight: 500;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: var(--orange);
        margin-bottom: 16px;
    }
    
    .section-title {
        font-family: 'Inter', sans-serif;
        font-size: 36px;
        font-weight: 700;
        color: var(--text);
        letter-spacing: -0.02em;
        margin: 0 0 16px;
    }
    
    .section-desc {
        font-family: 'Inter', sans-serif;
        font-size: 16px;
        color: var(--text-secondary);
        line-height: 1.6;
    }
    
    /* Process grid */
    .process-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
        gap: 24px;
    }
    
    .process-card {
        background: var(--surface);
        border: 1px solid var(--border);
        padding: 32px;
        transition: all 0.2s;
    }
    
    .process-card:hover {
        background: var(--surface-hover);
        border-color: var(--border-subtle);
    }
    
    .process-num {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        font-weight: 500;
        color: var(--orange);
        margin-bottom: 20px;
    }
    
    .process-card h3 {
        font-family: 'Inter', sans-serif;
        font-size: 18px;
        font-weight: 600;
        color: var(--text);
        margin: 0 0 12px;
    }
    
    .process-card p {
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        color: var(--text-muted);
        line-height: 1.6;
        margin: 0;
    }
    
    /* Features list */
    .features-list {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 32px;
    }
    
    .feature-item {
        display: flex;
        gap: 16px;
    }
    
    .feature-icon {
        width: 40px;
        height: 40px;
        background: var(--orange-subtle);
        border: 1px solid rgba(249, 115, 22, 0.2);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        flex-shrink: 0;
    }
    
    .feature-content h4 {
        font-family: 'Inter', sans-serif;
        font-size: 16px;
        font-weight: 600;
        color: var(--text);
        margin: 0 0 6px;
    }
    
    .feature-content p {
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        color: var(--text-muted);
        line-height: 1.5;
        margin: 0;
    }
    
    /* Testimonial */
    .testimonial-card {
        background: var(--surface);
        border: 1px solid var(--border);
        padding: 40px;
        margin-top: 48px;
    }
    
    .testimonial-quote {
        font-family: 'Inter', sans-serif;
        font-size: 20px;
        font-weight: 500;
        color: var(--text);
        line-height: 1.6;
        margin: 0 0 24px;
    }
    
    .testimonial-author {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .testimonial-avatar {
        width: 44px;
        height: 44px;
        background: linear-gradient(135deg, var(--orange), #fbbf24);
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 16px;
        color: var(--bg);
    }
    
    .testimonial-name {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 15px;
        color: var(--text);
    }
    
    .testimonial-role {
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        color: var(--text-muted);
    }
    
    /* Pricing */
    .pricing-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 32px;
        max-width: 900px;
    }
    
    .pricing-card {
        background: var(--surface);
        border: 1px solid var(--border);
        padding: 40px;
    }
    
    .pricing-card.featured {
        border-color: var(--orange);
        background: linear-gradient(180deg, rgba(249, 115, 22, 0.05) 0%, var(--surface) 50%);
    }
    
    .pricing-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        font-weight: 500;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: var(--orange);
        margin-bottom: 8px;
    }
    
    .pricing-amount {
        font-family: 'Inter', sans-serif;
        font-size: 48px;
        font-weight: 800;
        color: var(--text);
        margin-bottom: 4px;
    }
    
    .pricing-period {
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        color: var(--text-muted);
        margin-bottom: 24px;
    }
    
    .pricing-features {
        list-style: none;
        padding: 0;
        margin: 0 0 32px;
    }
    
    .pricing-features li {
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        color: var(--text-secondary);
        padding: 12px 0;
        border-bottom: 1px solid var(--border);
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .pricing-features li::before {
        content: "✓";
        color: var(--green);
        font-weight: 600;
    }
    
    .guarantee-badge {
        background: var(--green-subtle);
        border: 1px solid rgba(34, 197, 94, 0.2);
        padding: 16px;
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        color: var(--green);
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .guarantee-badge strong {
        color: var(--text);
    }
    
    /* FAQ */
    .faq-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
        gap: 24px;
    }
    
    .faq-item {
        padding: 24px 0;
        border-bottom: 1px solid var(--border);
    }
    
    .faq-question {
        font-family: 'Inter', sans-serif;
        font-size: 16px;
        font-weight: 600;
        color: var(--text);
        margin: 0 0 12px;
    }
    
    .faq-answer {
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        color: var(--text-muted);
        line-height: 1.6;
        margin: 0;
    }
    
    /* CTA Section */
    .cta-section {
        padding: 80px 6%;
        background: linear-gradient(180deg, var(--bg-subtle) 0%, var(--bg) 100%);
        text-align: center;
    }
    
    .cta-title {
        font-family: 'Inter', sans-serif;
        font-size: 32px;
        font-weight: 700;
        color: var(--text);
        margin: 0 0 16px;
    }
    
    .cta-text {
        font-family: 'Inter', sans-serif;
        font-size: 16px;
        color: var(--text-muted);
        margin: 0 0 32px;
    }
    
    /* Footer */
    .footer {
        padding: 40px 6%;
        border-top: 1px solid var(--border);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .footer-brand {
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        color: var(--text-muted);
    }
    
    .footer-links {
        display: flex;
        gap: 24px;
    }
    
    .footer-links a {
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        color: var(--text-muted);
        text-decoration: none;
    }
    
    .footer-links a:hover {
        color: var(--text);
    }
    
    /* Form Styles */
    .form-container {
        max-width: 640px;
        margin: 0 auto;
        padding: 80px 24px;
    }
    
    .form-header {
        text-align: center;
        margin-bottom: 48px;
    }
    
    .form-step {
        background: var(--surface);
        border: 1px solid var(--border);
        padding: 32px;
        margin-bottom: 24px;
    }
    
    .form-step-title {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 24px;
        padding-bottom: 16px;
        border-bottom: 1px solid var(--border);
    }
    
    .form-step-num {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        font-weight: 500;
        color: var(--orange);
        background: var(--orange-subtle);
        padding: 6px 12px;
    }
    
    .form-step-title h3 {
        font-family: 'Inter', sans-serif;
        font-size: 18px;
        font-weight: 600;
        color: var(--text);
        margin: 0;
    }
    
    /* Streamlit overrides */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {
        background: var(--bg-subtle) !important;
        border: 1px solid var(--border) !important;
        border-radius: 0 !important;
        color: var(--text) !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: var(--orange) !important;
        box-shadow: 0 0 0 1px var(--orange) !important;
    }
    
    .stTextInput > label,
    .stNumberInput > label,
    .stSelectbox > label,
    .stSlider > label,
    .stFileUploader > label,
    .stTextArea > label,
    .stMultiSelect > label {
        font-family: 'Inter', sans-serif !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        color: var(--text-secondary) !important;
    }
    
    .stButton > button {
        background: var(--orange) !important;
        color: var(--bg) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 0 !important;
        padding: 14px 28px !important;
        transition: all 0.2s !important;
    }
    
    .stButton > button:hover {
        background: var(--orange-hover) !important;
        transform: translateY(-2px);
    }
    
    .stFileUploader > div {
        background: var(--bg-subtle) !important;
        border: 2px dashed var(--border) !important;
        border-radius: 0 !important;
    }
    
    .stSlider > div > div > div {
        background: var(--orange) !important;
    }
    
    .stProgress > div > div {
        background: var(--orange) !important;
    }
    
    .stSuccess {
        background: var(--green-subtle) !important;
        border: 1px solid rgba(34, 197, 94, 0.3) !important;
        color: var(--green) !important;
    }
    
    /* Results styling */
    .result-card {
        background: var(--surface);
        border: 1px solid var(--border);
        padding: 32px;
        margin: 16px 0;
    }
    
    .result-amount {
        font-family: 'Inter', sans-serif;
        font-size: 48px;
        font-weight: 800;
        color: var(--text);
    }
    
    .result-label {
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        color: var(--text-muted);
    }
    
    .action-preview {
        background: var(--bg-subtle);
        border-left: 3px solid var(--orange);
        padding: 16px 20px;
        margin: 8px 0;
    }
    
    .action-preview-title {
        font-family: 'Inter', sans-serif;
        font-size: 15px;
        font-weight: 500;
        color: var(--text);
    }
    
    .action-preview-impact {
        font-family: 'JetBrains Mono', monospace;
        font-size: 14px;
        color: var(--green);
        float: right;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .hero { padding: 100px 5% 60px; }
        .hero h1 { font-size: 36px; }
        .stats-row { flex-direction: column; gap: 24px; }
        .section { padding: 60px 5%; }
        .pricing-container { grid-template-columns: 1fr; }
        .faq-grid { grid-template-columns: 1fr; }
    }
</style>
""", unsafe_allow_html=True)


def show_landing_page():
    """Display the polished landing page."""
    
    # Navigation
    st.markdown("""
    <div class="nav">
        <div class="nav-brand">
            <span>⚡</span> Profit Leak Audit
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
    <div class="hero">
        <div class="hero-content">
            <div class="hero-badge">
                For electricians, plumbers & tradies doing $150k-500k/year
            </div>
            <h1>Find the <span class="highlight">$20k-50k</span> you're leaving on the table</h1>
            <p class="hero-text">
                Most tradies work 50+ hours a week but make less per hour than their employees. 
                We analyze your numbers, find the profit leaks, and give you a step-by-step 
                plan to fix them.
            </p>
            <div class="stats-row">
                <div class="stat-item">
                    <div class="stat-value">$38k</div>
                    <div class="stat-label">Average opportunity found</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">7 days</div>
                    <div class="stat-label">Report delivered</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">$10k+</div>
                    <div class="stat-label">Guaranteed or refund</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # How it works
    st.markdown("""
    <div class="section section-dark">
        <div class="section-header">
            <div class="section-eyebrow">How it works</div>
            <h2 class="section-title">Four steps to more profit</h2>
            <p class="section-desc">No complicated software. No long-term contracts. Just clear answers about your business.</p>
        </div>
        <div class="process-grid">
            <div class="process-card">
                <div class="process-num">01</div>
                <h3>Send your data</h3>
                <p>Upload 12 months of invoices, expenses, and quotes. Takes 15 minutes. We handle messy spreadsheets.</p>
            </div>
            <div class="process-card">
                <div class="process-num">02</div>
                <h3>We analyze everything</h3>
                <p>Every job, every customer, every expense. Benchmarked against hundreds of similar tradies in your area.</p>
            </div>
            <div class="process-card">
                <div class="process-num">03</div>
                <h3>Get your action plan</h3>
                <p>Clear report with exact numbers, scripts for what to say to customers, and realistic timelines.</p>
            </div>
            <div class="process-card">
                <div class="process-num">04</div>
                <h3>Strategy call</h3>
                <p>60 minutes to walk through the findings, answer questions, and plan your next moves.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # What you get - Clean card layout
    st.markdown("""
    <div class="section">
        <div class="section-header">
            <div class="section-eyebrow">What's included</div>
            <h2 class="section-title">Everything you need to fix the leaks</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Use Streamlit columns for cleaner rendering
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: #1c1c1f; border: 1px solid #27272a; padding: 28px; margin-bottom: 20px;">
            <h4 style="font-family: 'Inter', sans-serif; font-size: 17px; font-weight: 600; color: #fafafa; margin: 0 0 10px;">
                📊 Pricing Audit
            </h4>
            <p style="font-family: 'Inter', sans-serif; font-size: 14px; color: #a1a1aa; line-height: 1.6; margin: 0;">
                Your rate vs market data. Exact recommended rates. Price increase scripts that actually work.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: #1c1c1f; border: 1px solid #27272a; padding: 28px; margin-bottom: 20px;">
            <h4 style="font-family: 'Inter', sans-serif; font-size: 17px; font-weight: 600; color: #fafafa; margin: 0 0 10px;">
                📈 Quote Win Rate Analysis
            </h4>
            <p style="font-family: 'Inter', sans-serif; font-size: 14px; color: #a1a1aa; line-height: 1.6; margin: 0;">
                Your win rate vs industry benchmarks. Why you're losing quotes. How to close more jobs.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: #1c1c1f; border: 1px solid #27272a; padding: 28px; margin-bottom: 20px;">
            <h4 style="font-family: 'Inter', sans-serif; font-size: 17px; font-weight: 600; color: #fafafa; margin: 0 0 10px;">
                🎯 90-Day Action Plan
            </h4>
            <p style="font-family: 'Inter', sans-serif; font-size: 14px; color: #a1a1aa; line-height: 1.6; margin: 0;">
                Prioritised quick wins ranked by impact. Conservative and best-case estimates. No fluff.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #1c1c1f; border: 1px solid #27272a; padding: 28px; margin-bottom: 20px;">
            <h4 style="font-family: 'Inter', sans-serif; font-size: 17px; font-weight: 600; color: #fafafa; margin: 0 0 10px;">
                💰 Job Profitability Breakdown
            </h4>
            <p style="font-family: 'Inter', sans-serif; font-size: 14px; color: #a1a1aa; line-height: 1.6; margin: 0;">
                Which jobs make money, which don't. Customer rankings. What work to chase, what to drop.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: #1c1c1f; border: 1px solid #27272a; padding: 28px; margin-bottom: 20px;">
            <h4 style="font-family: 'Inter', sans-serif; font-size: 17px; font-weight: 600; color: #fafafa; margin: 0 0 10px;">
                ⏱️ Time Leak Report
            </h4>
            <p style="font-family: 'Inter', sans-serif; font-size: 14px; color: #a1a1aa; line-height: 1.6; margin: 0;">
                Where your hours actually go. Admin burden analysis. What to delegate or automate first.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: #1c1c1f; border: 1px solid #27272a; padding: 28px; margin-bottom: 20px;">
            <h4 style="font-family: 'Inter', sans-serif; font-size: 17px; font-weight: 600; color: #fafafa; margin: 0 0 10px;">
                📝 Word-for-Word Scripts
            </h4>
            <p style="font-family: 'Inter', sans-serif; font-size: 14px; color: #a1a1aa; line-height: 1.6; margin: 0;">
                Exactly what to say to customers. How to handle pushback. Ready-to-use email templates.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Testimonial
    st.markdown("""
    <div style="background: #1c1c1f; border: 1px solid #27272a; padding: 40px; margin: 40px 6% 0;">
        <p style="font-family: 'Inter', sans-serif; font-size: 20px; font-weight: 500; color: #fafafa; line-height: 1.6; margin: 0 0 24px; font-style: italic;">
            "I thought I was doing okay. Turns out I was leaving $60k on the table. 
            Raised my rates last week — not a single customer complained. Kicking myself for not doing this years ago."
        </p>
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="width: 44px; height: 44px; background: linear-gradient(135deg, #f97316, #fbbf24); display: flex; align-items: center; justify-content: center; font-family: 'Inter', sans-serif; font-weight: 700; font-size: 16px; color: #09090b;">D</div>
            <div>
                <div style="font-family: 'Inter', sans-serif; font-weight: 600; font-size: 15px; color: #fafafa;">Dave M.</div>
                <div style="font-family: 'Inter', sans-serif; font-size: 13px; color: #71717a;">Electrician, Sydney · Revenue: $220k → $280k</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Pricing
    st.markdown("""
    <div class="section section-dark">
        <div class="section-header">
            <div class="section-eyebrow">Investment</div>
            <h2 class="section-title">One audit. Thousands in returns.</h2>
        </div>
        <div class="pricing-container">
            <div class="pricing-card featured">
                <div class="pricing-label">Profit Leak Audit</div>
                <div class="pricing-amount">$797</div>
                <div class="pricing-period">One-time investment</div>
                <ul class="pricing-features">
                    <li>Full business analysis</li>
                    <li>Market benchmark comparison</li>
                    <li>Detailed PDF report</li>
                    <li>Excel action workbook</li>
                    <li>60-minute strategy call</li>
                    <li>30/60/90 day check-ins</li>
                </ul>
                <div class="guarantee-badge">
                    <strong>🛡️ Guarantee:</strong> We find $10k+ in opportunities or full refund.
                </div>
            </div>
            <div class="pricing-card">
                <div class="pricing-label">The math</div>
                <div class="pricing-amount" style="font-size: 28px; margin-bottom: 16px;">Is this worth it?</div>
                <div class="pricing-period" style="margin-bottom: 16px;">Consider this:</div>
                <p style="font-family: 'Inter', sans-serif; font-size: 14px; color: var(--text-secondary); line-height: 1.7; margin-bottom: 16px;">
                    Average opportunity we find: <strong style="color: var(--text);">$38,500/year</strong>
                </p>
                <p style="font-family: 'Inter', sans-serif; font-size: 14px; color: var(--text-secondary); line-height: 1.7; margin-bottom: 16px;">
                    Even at 50% implementation: <strong style="color: var(--text);">$19,250</strong>
                </p>
                <p style="font-family: 'Inter', sans-serif; font-size: 14px; color: var(--text-secondary); line-height: 1.7; margin-bottom: 16px;">
                    Your investment: <strong style="color: var(--text);">$797</strong>
                </p>
                <p style="font-family: 'Inter', sans-serif; font-size: 14px; color: var(--green); line-height: 1.7;">
                    <strong>Return: 24x your investment</strong>
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # FAQ
    st.markdown("""
    <div class="section">
        <div class="section-header">
            <div class="section-eyebrow">Questions</div>
            <h2 class="section-title">Common questions</h2>
        </div>
        <div class="faq-grid">
            <div class="faq-item">
                <h4 class="faq-question">What if my records are a mess?</h4>
                <p class="faq-answer">We work with messy data all the time. Bank statements, random invoices, spreadsheets — we'll piece it together. Might take an extra day or two.</p>
            </div>
            <div class="faq-item">
                <h4 class="faq-question">Will you tell me to raise prices and lose customers?</h4>
                <p class="faq-answer">We'll show you the data. Most tradies are 15-30% under market rate. We also give you scripts for how to raise prices without losing good customers.</p>
            </div>
            <div class="faq-item">
                <h4 class="faq-question">What if you don't find $10k in opportunities?</h4>
                <p class="faq-answer">Full refund. No questions. In practice, we've never had this happen — the average is $38k.</p>
            </div>
            <div class="faq-item">
                <h4 class="faq-question">Can I do this myself?</h4>
                <p class="faq-answer">Technically yes, if you have 20+ hours and know how to analyze business financials. Most tradies don't have either. That's why you're here.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # CTA
    st.markdown("""
    <div class="cta-section">
        <h2 class="cta-title">Ready to find your profit leaks?</h2>
        <p class="cta-text">Takes 15 minutes to submit your data. Report delivered in 7 days.</p>
    </div>
    """, unsafe_allow_html=True)


def show_intake_form():
    """Display the intake form."""
    
    st.markdown("""
    <div class="form-container">
        <div class="form-header">
            <div class="section-eyebrow">Get Started</div>
            <h2 class="section-title">Submit your data</h2>
            <p class="section-desc">Fill out the form below. Takes about 15 minutes.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Step 1: Business
    st.markdown("""
    <div class="form-step">
        <div class="form-step-title">
            <span class="form-step-num">01</span>
            <h3>Your business</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        business_name = st.text_input("Business name", placeholder="e.g. Dave's Electrical")
        email = st.text_input("Email", placeholder="dave@example.com")
    with col2:
        trade_type = st.selectbox("Trade", ["Electrician", "Plumber", "Carpenter", "HVAC", "Builder", "Other"])
        location = st.text_input("Location", placeholder="Sydney")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Step 2: Numbers
    st.markdown("""
    <div class="form-step">
        <div class="form-step-title">
            <span class="form-step-num">02</span>
            <h3>Current numbers</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        hourly_rate = st.number_input("Hourly rate ($)", min_value=50, max_value=300, value=95)
        revenue = st.selectbox("Annual revenue", ["Under $100k", "$100k-$150k", "$150k-$200k", "$200k-$300k", "$300k-$500k", "$500k+"])
    with col2:
        hours_per_week = st.slider("Hours worked / week", 20, 80, 50)
        call_out = st.number_input("Call-out fee ($)", min_value=0, max_value=200, value=0)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Step 3: Documents
    st.markdown("""
    <div class="form-step">
        <div class="form-step-title">
            <span class="form-step-num">03</span>
            <h3>Upload documents</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <p style="font-family: 'Inter', sans-serif; font-size: 14px; color: var(--text-muted); margin-bottom: 16px;">
        Upload your invoices, expenses, and quotes from the last 12 months. PDF, Excel, or CSV.
    </p>
    """, unsafe_allow_html=True)
    
    invoices = st.file_uploader("Invoices", type=['pdf', 'xlsx', 'xls', 'csv'], accept_multiple_files=True, key="inv")
    expenses = st.file_uploader("Expenses / Bank statements", type=['pdf', 'xlsx', 'xls', 'csv'], accept_multiple_files=True, key="exp")
    quotes = st.file_uploader("Quotes (optional)", type=['pdf', 'xlsx', 'xls', 'csv'], accept_multiple_files=True, key="quo")
    
    if invoices:
        st.success(f"✓ {len(invoices)} invoice files")
    if expenses:
        st.success(f"✓ {len(expenses)} expense files")
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Submit
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        submitted = st.button("Submit & Start Audit →", use_container_width=True)
    
    if submitted:
        if not business_name or not email or not (invoices or expenses):
            st.error("Please fill in business name, email, and upload at least invoices or expenses.")
        else:
            run_audit_pipeline(
                business_name=business_name,
                email=email,
                trade_type=trade_type.lower(),
                location=location,
                hourly_rate=hourly_rate,
                hours_per_week=hours_per_week,
                invoices=invoices or [],
                expenses=expenses or [],
                quotes=quotes or []
            )


def run_audit_pipeline(business_name, email, trade_type, location, hourly_rate, hours_per_week, invoices, expenses, quotes):
    """Run the audit."""
    from src.utils.file_handler import FileHandler
    from src.agents.data_extractor import DataExtractor
    from src.agents.analyzer import Analyzer, BusinessContext
    from src.agents.report_generator import ReportGenerator
    
    with st.status("Running your audit...", expanded=True) as status:
        # Save files
        st.write("📁 Saving documents...")
        handler = FileHandler()
        folder = handler.create_customer_folder(business_name)
        
        for files, cat in [(invoices, "invoices"), (expenses, "expenses"), (quotes, "quotes")]:
            for f in files:
                path = folder / cat / f.name
                path.parent.mkdir(exist_ok=True)
                with open(path, 'wb') as out:
                    out.write(f.read())
        
        # Save form data
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
        
        # Extract
        st.write("🔍 Extracting data...")
        extractor = DataExtractor()
        results = extractor.extract_from_folder(str(folder))
        combined = extractor.combine_results(results)
        st.write(f"✓ Found {combined['summary']['total_transactions']} transactions")
        
        # Analyze
        st.write("📊 Analyzing...")
        context = BusinessContext(
            trade_type=trade_type if trade_type != "other" else "electrician",
            location=location or "Sydney",
            years_in_business=5,
            current_rate=float(hourly_rate),
            hours_per_week=hours_per_week,
            revenue_goal=250000
        )
        
        analyzer = Analyzer()
        analysis = analyzer.analyze(combined, context)
        
        # Generate report
        st.write("📄 Generating report...")
        generator = ReportGenerator(output_dir="./output")
        report = generator.generate_report(analysis, context, business_name)
        
        status.update(label="✅ Audit complete", state="complete")
    
    # Show results
    opportunity = analysis.guarantee_check.get('total_opportunity', 0)
    conservative = opportunity * 0.7
    
    st.markdown(f"""
    <div class="result-card" style="text-align: center; border-color: var(--orange);">
        <div class="result-label">Conservative Opportunity Identified</div>
        <div class="result-amount" style="color: var(--green);">${conservative:,.0f}</div>
        <div class="result-label">Best case: ${opportunity:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h3 style='color: var(--text); font-family: Inter, sans-serif; margin: 24px 0 16px;'>Top Actions</h3>", unsafe_allow_html=True)
    
    for i, action in enumerate(analysis.action_plan[:3], 1):
        impact = action.get('impact_conservative', action.get('impact_annual', 0)) * 0.85
        st.markdown(f"""
        <div class="action-preview">
            <span class="action-preview-impact">+${impact:,.0f}/yr</span>
            <span class="action-preview-title">{i}. {action.get('action', 'N/A')}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Downloads
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if Path(report['html_report']).exists():
            with open(report['html_report'], 'r') as f:
                st.download_button("📄 Download Report", f.read(), 
                                   file_name=f"{business_name.replace(' ', '_')}_report.html",
                                   mime="text/html", use_container_width=True)
    with col2:
        if Path(report['excel_report']).exists():
            with open(report['excel_report'], 'rb') as f:
                st.download_button("📊 Download Workbook", f.read(),
                                   file_name=f"{business_name.replace(' ', '_')}_workbook.xlsx",
                                   use_container_width=True)
    
    st.markdown("""
    <div style="background: var(--surface); border: 1px solid var(--border); padding: 24px; margin-top: 24px; text-align: center;">
        <p style="font-family: 'Inter', sans-serif; color: var(--text); margin: 0 0 8px;">
            We'll email you within 24 hours to book your strategy call.
        </p>
        <p style="font-family: 'Inter', sans-serif; font-size: 13px; color: var(--text-muted); margin: 0;">
            Questions? Reply to your confirmation email.
        </p>
    </div>
    """, unsafe_allow_html=True)


def show_payment_success():
    """Show success page after payment."""
    st.markdown("""
    <div class="form-container" style="text-align: center; padding: 80px 20px;">
        <div style="font-size: 64px; margin-bottom: 24px;">✅</div>
        <h2 style="font-family: 'Inter', sans-serif; color: var(--text); font-size: 32px; margin-bottom: 16px;">
            Payment Successful!
        </h2>
        <p style="font-family: 'Inter', sans-serif; color: var(--text-secondary); font-size: 18px; margin-bottom: 32px;">
            Thank you for your purchase. You're ready to start your audit.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Continue to Audit Form →", use_container_width=True):
            st.session_state.payment_verified = True
            st.session_state.show_form = True
            st.query_params.clear()
            st.rerun()


def show_payment_cancelled():
    """Show cancelled page."""
    st.markdown("""
    <div class="form-container" style="text-align: center; padding: 80px 20px;">
        <div style="font-size: 64px; margin-bottom: 24px;">↩️</div>
        <h2 style="font-family: 'Inter', sans-serif; color: var(--text); font-size: 32px; margin-bottom: 16px;">
            Payment Cancelled
        </h2>
        <p style="font-family: 'Inter', sans-serif; color: var(--text-secondary); font-size: 18px; margin-bottom: 32px;">
            No worries. Your card hasn't been charged.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("← Back to Home", use_container_width=True):
            st.query_params.clear()
            st.rerun()


def handle_stripe_checkout():
    """Redirect to Stripe checkout."""
    # Get the base URL (works for both local and deployed)
    # In production, you'd set this via environment variable
    base_url = os.getenv("APP_BASE_URL", "http://localhost:8501")
    
    success_url = f"{base_url}?payment=success&session_id={{CHECKOUT_SESSION_ID}}"
    cancel_url = f"{base_url}?payment=cancelled"
    
    result = create_checkout_session(
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={"source": "portal"}
    )
    
    if result["success"]:
        # Store session ID for verification
        st.session_state.checkout_session_id = result["session_id"]
        # Redirect to Stripe
        st.markdown(f"""
        <meta http-equiv="refresh" content="0;url={result['checkout_url']}">
        <script>window.location.href = "{result['checkout_url']}";</script>
        """, unsafe_allow_html=True)
        st.info("Redirecting to secure payment page...")
    else:
        st.error(f"Payment error: {result.get('error', 'Unknown error')}. Please try again.")


def main():
    # Check URL parameters for payment status
    params = st.query_params
    
    # Handle payment callbacks
    if params.get("payment") == "success":
        session_id = params.get("session_id")
        if session_id:
            # Verify the payment
            verification = verify_payment(session_id)
            if verification.get("paid"):
                st.session_state.payment_verified = True
                st.session_state.customer_email = verification.get("customer_email")
        show_payment_success()
        return
    
    if params.get("payment") == "cancelled":
        show_payment_cancelled()
        return
    
    # Show test mode banner if applicable
    if is_test_mode():
        st.markdown("""
        <div style="background: #422006; border: 1px solid #f97316; padding: 12px 20px; text-align: center; position: fixed; top: 0; left: 0; right: 0; z-index: 1000;">
            <span style="font-family: 'Inter', sans-serif; font-size: 13px; color: #fed7aa;">
                🧪 <strong>Test Mode</strong> — Use card 4242 4242 4242 4242, any future date, any CVC
            </span>
        </div>
        <div style="height: 48px;"></div>
        """, unsafe_allow_html=True)
    
    # Main flow
    if st.session_state.get('show_form'):
        # Check if payment is verified (or bypass for testing)
        if st.session_state.get('payment_verified') or os.getenv("BYPASS_PAYMENT") == "true":
            show_intake_form()
        else:
            # Need to pay first
            st.warning("Please complete payment to access the audit form.")
            if st.button("← Back to Home"):
                st.session_state.show_form = False
                st.rerun()
    else:
        show_landing_page()
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Check if Stripe is configured
            if os.getenv("STRIPE_SECRET_KEY"):
                if st.button("Start Your Audit — $797 →", use_container_width=True):
                    handle_stripe_checkout()
            else:
                # No Stripe key - show setup message or bypass
                st.markdown("""
                <div style="background: var(--surface); border: 1px solid var(--border); padding: 16px; margin-bottom: 16px; text-align: center;">
                    <p style="font-family: 'Inter', sans-serif; font-size: 14px; color: var(--text-muted); margin: 0;">
                        ⚠️ Stripe not configured. Add STRIPE_SECRET_KEY to .env
                    </p>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Start Your Audit (Demo Mode) →", use_container_width=True):
                    st.session_state.show_form = True
                    st.session_state.payment_verified = True
                    st.rerun()
        
        # Footer
        st.markdown("""
        <div class="footer">
            <div class="footer-brand">© 2024 Profit Leak Audit</div>
            <div class="footer-links">
                <a href="mailto:hello@example.com">Contact</a>
                <a href="#">Privacy</a>
                <a href="#">Terms</a>
            </div>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
