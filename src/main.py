"""
# TradieAudit App

Welcome to the TradieAudit app! This application is designed to help tradies analyze their business, identify profit leaks, and get actionable insights to improve their bottom line.

### Key Features:

*   **Automated Data Analysis:** Upload your financial documents (invoices, expenses, etc.), and the app will automatically extract and analyze the data.
*   **Profit Leak Detection:** The core of the app, this feature identifies areas where you might be losing money, such as under-bidding jobs, inefficient scheduling, or high material costs.
*   **Actionable Recommendations:** Based on the analysis, you'll get a personalized action plan with concrete steps to plug the leaks and boost your profits.
*   **Benchmarking:** See how your business stacks up against industry benchmarks for your trade and location.

### How to Use:

1.  **Navigate to the Customer Portal:** Use the sidebar to go to the Customer Portal page.
2.  **Fill out the Form:** Provide some basic information about your business.
3.  **Upload Documents:** Upload your financial documents for the last 6-12 months. The more data you provide, the more accurate the analysis will be.
4.  **Run the Audit:** Click the "Run Audit" button and let the app work its magic.
5.  **Review Your Report:** Once the analysis is complete, you'll get a detailed report with your profit leak analysis and action plan.

Ready to find your profit leaks? Head over to the Customer Portal to get started!
"""
import streamlit as st
import base64
from pathlib import Path

# Page Config
st.set_page_config(
    page_title="TradieAudit - Uncover Hidden Profits",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def load_css(file_path):
    """Load a CSS file and return its content."""
    with open(file_path) as f:
        return f.read()

def get_image_as_base64(file_path):
    """Load an image and return it as a base64 encoded string."""
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# --- ASSETS ---
css_file = Path(__file__).parent / "styles" / "main.css"
logo_file = Path(__file__).parent / "assets" / "logo.svg"

# --- UI ---
st.markdown(f'<style>{load_css(css_file)}</style>', unsafe_allow_html=True)
logo_base64 = get_image_as_base64(logo_file)

# --- HEADER ---
st.markdown(f"""
<div class="header">
    <div class="logo">
        <img src="data:image/svg+xml;base64,{logo_base64}" alt="TradieAudit Logo">
        <span>TradieAudit</span>
    </div>
    <div class="nav">
        <a href="#why-choose-us">Why Choose Us</a>
        <a href="#how-it-works">How It Works</a>
    </div>
</div>
""", unsafe_allow_html=True)

# --- HERO SECTION ---
st.markdown("""
<div class="hero-section">
    <div class="hero-text">
        <h1>Stop Guessing. Start Growing.</h1>
        <p>The #1 tool for tradies to find and fix profit leaks, optimize pricing, and boost their bottom line. Guaranteed.</p>
        <a href="/Customer_Portal" target="_self" class="hero-button">Start Your Free Audit</a>
    </div>
</div>
""", unsafe_allow_html=True)

# --- "WHY CHOOSE US?" SECTION ---
st.markdown("""
<div id="why-choose-us" class="section">
    <h2>Why Choose TradieAudit?</h2>
    <div class="features-grid">
        <div class="feature-card">
            <h3>📈 Find Hidden Profits</h3>
            <p>Our AI-powered analysis uncovers an average of $25,000 in annual profit leaks for our users.</p>
        </div>
        <div class="feature-card">
            <h3>💰 Smarter Pricing</h3>
            <p>Benchmark your rates against the market to ensure you're charging what you're worth.</p>
        </div>
        <div class="feature-card">
            <h3>⏱️ Save Time</h3>
            <p>Automate your financial analysis and get a clear action plan in minutes, not weeks.</p>
        </div>
        <div class="feature-card">
            <h3>🔒 Bank-Level Security</h3>
            <p>Your data is encrypted and secure. We never share your financial information.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- "HOW IT WORKS" SECTION ---
st.markdown("""
<div id="how-it-works" class="section dark-section">
    <h2>How It Works in 3 Simple Steps</h2>
    <div class="steps-container">
        <div class="step">
            <div class="step-number">1</div>
            <h3>Upload Your Data</h3>
            <p>Securely connect your accounting software or upload your financial documents (invoices, expenses, etc.).</p>
        </div>
        <div class="step">
            <div class="step-number">2</div>
            <h3>Run the Analysis</h3>
            <p>Our AI engine analyzes your numbers, identifies profit leaks, and compares you to market benchmarks.</p>
        </div>
        <div class="step">
            <div class="step-number">3</div>
            <h3>Get Your Action Plan</h3>
            <p>Receive a personalized report with a clear, step-by-step plan to boost your profitability.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- FINAL CTA ---
st.markdown("""
<div class="section cta-section">
    <h2>Ready to Unlock Your True Profit Potential?</h2>
    <p>Stop leaving money on the table. Get the insights you need to build a more profitable and sustainable business.</p>
    <a href="/Customer_Portal" target="_self" class="hero-button">Start Your Free Audit Now</a>
</div>
""", unsafe_allow_html=True)

# --- FOOTER ---
st.markdown(f"""
<div class="footer">
    <div class="logo">
        <img src="data:image/svg+xml;base64,{logo_base64}" alt="TradieAudit Logo">
        <span>TradieAudit</span>
    </div>
    <div class="footer-links">
        <a href="#why-choose-us">Why Choose Us</a>
        <a href="#how-it-works">How It Works</a>
        <a href="#">Privacy Policy</a>
        <a href="#">Terms of Service</a>
    </div>
</div>
""", unsafe_allow_html=True)