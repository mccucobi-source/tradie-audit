"""
Tradie Profit Audit - Premium Portal
Clean, light design inspired by modern SaaS aesthetics.
Justifies the $797 price point through professional presentation.
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
    page_title="Profit Leak Audit | Find Your Hidden Revenue",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

from dotenv import load_dotenv
load_dotenv()

# Import payment module
from src.payments import create_checkout_session, verify_payment, is_test_mode

# Premium light theme - clean SaaS aesthetic
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    
    :root {
        --bg: #ffffff;
        --bg-soft: #f8fafc;
        --bg-muted: #f1f5f9;
        --surface: #ffffff;
        --border: #e2e8f0;
        --border-light: #f1f5f9;
        --text: #0f172a;
        --text-secondary: #475569;
        --text-muted: #94a3b8;
        --primary: #f97316;
        --primary-hover: #ea580c;
        --primary-light: #fff7ed;
        --primary-glow: rgba(249, 115, 22, 0.15);
        --green: #10b981;
        --green-light: #ecfdf5;
        --blue: #3b82f6;
        --shadow-sm: 0 1px 2px rgba(0,0,0,0.04);
        --shadow: 0 4px 6px -1px rgba(0,0,0,0.07), 0 2px 4px -1px rgba(0,0,0,0.04);
        --shadow-lg: 0 20px 25px -5px rgba(0,0,0,0.08), 0 10px 10px -5px rgba(0,0,0,0.03);
        --shadow-xl: 0 25px 50px -12px rgba(0,0,0,0.15);
    }
    
    .stApp {
        background: var(--bg);
    }
    
    #MainMenu, footer, header, [data-testid="stToolbar"], [data-testid="stSidebar"] {
        display: none !important;
    }
    
    [data-testid="stSidebarNav"] {
        display: none !important;
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
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-bottom: 1px solid var(--border-light);
        padding: 16px 5%;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .nav-brand {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 800;
        font-size: 20px;
        color: var(--text);
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .nav-brand-icon {
        width: 36px;
        height: 36px;
        background: linear-gradient(135deg, var(--primary) 0%, #fb923c 100%);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 18px;
    }
    
    .nav-links {
        display: flex;
        align-items: center;
        gap: 32px;
    }
    
    .nav-link {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 14px;
        font-weight: 500;
        color: var(--text-secondary);
        text-decoration: none;
        transition: color 0.2s;
    }
    
    .nav-link:hover {
        color: var(--text);
    }
    
    .nav-cta {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 14px;
        font-weight: 600;
        color: white;
        background: var(--text);
        padding: 10px 20px;
        border-radius: 8px;
        text-decoration: none;
        transition: all 0.2s;
    }
    
    .nav-cta:hover {
        background: #1e293b;
        transform: translateY(-1px);
    }
    
    /* Hero */
    .hero {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 140px 5% 80px;
        position: relative;
        text-align: center;
        background: 
            radial-gradient(ellipse 80% 50% at 50% -20%, var(--primary-glow), transparent),
            var(--bg);
        overflow: hidden;
    }
    
    /* Floating cards */
    .floating-card {
        position: absolute;
        background: white;
        border-radius: 16px;
        box-shadow: var(--shadow-lg);
        padding: 16px 20px;
        font-family: 'Plus Jakarta Sans', sans-serif;
        animation: float 6s ease-in-out infinite, fadeIn 0.8s ease-out both;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .floating-card:hover {
        box-shadow: var(--shadow-xl);
        z-index: 20;
    }
    
    .floating-card.left-1 {
        left: 8%;
        top: 25%;
        transform: rotate(-6deg);
        animation-delay: 0s, 0.2s;
    }
    
    .floating-card.left-2 {
        left: 5%;
        top: 55%;
        transform: rotate(3deg);
        animation-delay: 1s, 0.4s;
    }
    
    .floating-card.right-1 {
        right: 8%;
        top: 20%;
        transform: rotate(6deg);
        animation-delay: 0.5s, 0.3s;
    }
    
    .floating-card.right-2 {
        right: 5%;
        top: 50%;
        transform: rotate(-3deg);
        animation-delay: 1.5s, 0.5s;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0) rotate(var(--rotate, 0deg)); }
        50% { transform: translateY(-10px) rotate(var(--rotate, 0deg)); }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-40px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(40px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes scaleIn {
        from {
            opacity: 0;
            transform: scale(0.9);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    
    @keyframes countUp {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .floating-card-icon {
        width: 40px;
        height: 40px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        margin-bottom: 8px;
    }
    
    .floating-card-title {
        font-size: 13px;
        font-weight: 600;
        color: var(--text);
        margin-bottom: 2px;
    }
    
    .floating-card-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 18px;
        font-weight: 600;
        color: var(--green);
    }
    
    .floating-card-sub {
        font-size: 11px;
        color: var(--text-muted);
    }
    
    /* Hero content */
    .hero-content {
        position: relative;
        z-index: 10;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        max-width: 700px;
    }
    
    .hero-badge {
        animation: fadeInUp 0.6s ease-out 0.2s both;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: var(--primary-light);
        border: 1px solid rgba(249, 115, 22, 0.2);
        padding: 8px 16px;
        border-radius: 100px;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 13px;
        font-weight: 600;
        color: var(--primary);
        margin-bottom: 24px;
    }
    
    .hero-icon {
        width: 56px;
        height: 56px;
        background: linear-gradient(135deg, var(--primary) 0%, #fb923c 100%);
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 24px;
        box-shadow: 0 8px 24px var(--primary-glow);
        animation: scaleIn 0.5s ease-out 0.3s both;
    }
    
    .hero-icon-dots {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 6px;
    }
    
    .hero-icon-dot {
        width: 10px;
        height: 10px;
        background: white;
        border-radius: 3px;
    }
    
    .hero h1 {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: clamp(36px, 5vw, 56px);
        font-weight: 800;
        color: var(--text);
        line-height: 1.15;
        letter-spacing: -0.03em;
        margin: 0 0 8px;
        max-width: 700px;
        animation: fadeInUp 0.7s ease-out 0.4s both;
    }
    
    .hero h1 span {
        color: var(--text-muted);
        font-weight: 600;
    }
    
    .hero-text {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 18px;
        color: var(--text-secondary);
        line-height: 1.7;
        margin-bottom: 32px;
        max-width: 520px;
        animation: fadeInUp 0.7s ease-out 0.5s both;
    }
    
    .hero-cta {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 16px;
        font-weight: 600;
        color: white;
        background: var(--primary);
        padding: 16px 32px;
        border-radius: 12px;
        text-decoration: none;
        transition: all 0.25s;
        box-shadow: 0 4px 14px var(--primary-glow);
        animation: fadeInUp 0.7s ease-out 0.6s both;
    }
    
    .hero-cta:hover {
        background: var(--primary-hover);
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 12px 28px var(--primary-glow);
    }
    
    .hero-cta:active {
        transform: translateY(-1px) scale(0.98);
    }
    
    /* Stats strip */
    .stats-strip {
        display: flex;
        justify-content: center;
        gap: 48px;
        margin-top: 64px;
        padding-top: 32px;
        border-top: 1px solid var(--border);
        animation: fadeInUp 0.7s ease-out 0.8s both;
    }
    
    .stat-item {
        text-align: center;
    }
    
    .stat-item:nth-child(1) { animation: countUp 0.5s ease-out 1s both; }
    .stat-item:nth-child(2) { animation: countUp 0.5s ease-out 1.1s both; }
    .stat-item:nth-child(3) { animation: countUp 0.5s ease-out 1.2s both; }
    
    .stat-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 28px;
        font-weight: 700;
        color: var(--text);
    }
    
    .stat-label {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 13px;
        color: var(--text-muted);
        margin-top: 4px;
    }
    
    /* Section */
    .section {
        padding: 100px 5%;
    }
    
    .section-gray {
        background: var(--bg-soft);
    }
    
    .section-header {
        text-align: center;
        max-width: 600px;
        margin: 0 auto 64px;
        animation: fadeInUp 0.6s ease-out both;
    }
    
    .section-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: var(--bg-muted);
        padding: 6px 14px;
        border-radius: 100px;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 12px;
        font-weight: 600;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 16px;
    }
    
    .section-title {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 36px;
        font-weight: 800;
        color: #0f172a !important;
        letter-spacing: -0.02em;
        margin: 0 0 16px;
        line-height: 1.2;
    }
    
    .section-desc {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 17px;
        color: var(--text-secondary);
        line-height: 1.6;
    }
    
    /* Process steps */
    .process-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 24px;
        max-width: 1100px;
        margin: 0 auto;
    }
    
    @media (max-width: 900px) {
        .process-grid { grid-template-columns: repeat(2, 1fr); }
    }
    
    @media (max-width: 600px) {
        .process-grid { grid-template-columns: 1fr; }
    }
    
    .process-card {
        background: white;
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 28px;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        opacity: 0;
        animation: fadeInUp 0.6s ease-out forwards;
    }
    
    .process-card:nth-child(1) { animation-delay: 0.1s; }
    .process-card:nth-child(2) { animation-delay: 0.2s; }
    .process-card:nth-child(3) { animation-delay: 0.3s; }
    .process-card:nth-child(4) { animation-delay: 0.4s; }
    
    .process-card:hover {
        border-color: var(--primary);
        box-shadow: var(--shadow-lg);
        transform: translateY(-8px);
    }
    
    .process-num {
        width: 40px;
        height: 40px;
        background: var(--bg-muted);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'JetBrains Mono', monospace;
        font-size: 14px;
        font-weight: 600;
        color: var(--text-secondary);
        margin: 0 auto 16px;
    }
    
    .process-card:hover .process-num {
        background: var(--primary);
        color: white;
    }
    
    .process-card h3 {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 17px;
        font-weight: 700;
        color: var(--text);
        margin: 0 0 8px;
    }
    
    .process-card p {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 14px;
        color: var(--text-muted);
        line-height: 1.6;
        margin: 0;
    }
    
    /* Features grid */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
        max-width: 1000px;
        margin: 0 auto;
    }
    
    @media (max-width: 800px) {
        .features-grid { grid-template-columns: repeat(2, 1fr); }
    }
    
    @media (max-width: 500px) {
        .features-grid { grid-template-columns: 1fr; }
    }
    
    .feature-card {
        background: white;
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 24px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        opacity: 0;
        animation: fadeInUp 0.5s ease-out forwards;
    }
    
    .feature-card:nth-child(1) { animation-delay: 0.05s; }
    .feature-card:nth-child(2) { animation-delay: 0.1s; }
    .feature-card:nth-child(3) { animation-delay: 0.15s; }
    .feature-card:nth-child(4) { animation-delay: 0.2s; }
    .feature-card:nth-child(5) { animation-delay: 0.25s; }
    .feature-card:nth-child(6) { animation-delay: 0.3s; }
    
    .feature-card:hover {
        border-color: transparent;
        box-shadow: var(--shadow-lg);
        transform: translateY(-6px);
    }
    
    .feature-icon {
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover .feature-icon {
        transform: scale(1.1);
    }
    
    .feature-icon {
        width: 44px;
        height: 44px;
        background: var(--primary-light);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        margin-bottom: 16px;
    }
    
    .feature-card h4 {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 16px;
        font-weight: 700;
        color: var(--text);
        margin: 0 0 8px;
    }
    
    .feature-card p {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 14px;
        color: var(--text-muted);
        line-height: 1.6;
        margin: 0;
    }
    
    /* Testimonials */
    .testimonials-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 24px;
        max-width: 900px;
        margin: 0 auto;
    }
    
    @media (max-width: 700px) {
        .testimonials-grid { grid-template-columns: 1fr; }
    }
    
    .testimonial-card {
        background: white;
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 32px;
        position: relative;
        transition: all 0.3s ease;
        opacity: 0;
        animation: fadeInUp 0.6s ease-out forwards;
    }
    
    .testimonial-card:nth-child(1) { animation-delay: 0.1s; }
    .testimonial-card:nth-child(2) { animation-delay: 0.25s; }
    
    .testimonial-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-lg);
    }
    
    .testimonial-stars {
        color: #fbbf24;
        font-size: 16px;
        letter-spacing: 2px;
        margin-bottom: 16px;
    }
    
    .testimonial-quote {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 15px;
        color: var(--text-secondary);
        line-height: 1.7;
        margin: 0 0 20px;
    }
    
    .testimonial-result {
        background: var(--green-light);
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 8px;
        transition: all 0.3s ease;
    }
    
    .testimonial-card:hover .testimonial-result {
        transform: scale(1.02);
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.15);
    }
    
    .testimonial-result-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 15px;
        font-weight: 600;
        color: var(--green);
    }
    
    .testimonial-author {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .testimonial-avatar {
        width: 44px;
        height: 44px;
        background: linear-gradient(135deg, var(--primary), #fbbf24);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 700;
        font-size: 16px;
        color: white;
    }
    
    .testimonial-name {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 600;
        font-size: 14px;
        color: var(--text);
    }
    
    .testimonial-role {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 13px;
        color: var(--text-muted);
    }
    
    /* Pricing */
    .pricing-container {
        display: grid;
        grid-template-columns: 1.1fr 0.9fr;
        gap: 24px;
        max-width: 900px;
        margin: 0 auto;
    }
    
    @media (max-width: 700px) {
        .pricing-container { grid-template-columns: 1fr; }
    }
    
    .pricing-card {
        background: white;
        border: 2px solid var(--border);
        border-radius: 24px;
        padding: 40px;
        position: relative;
        transition: all 0.3s ease;
        opacity: 0;
        animation: scaleIn 0.5s ease-out 0.1s forwards;
    }
    
    .pricing-card:hover {
        transform: translateY(-4px);
    }
    
    .pricing-card.featured {
        border-color: var(--primary);
        box-shadow: 0 0 0 4px var(--primary-light);
        animation: scaleIn 0.5s ease-out forwards;
    }
    
    .pricing-card.featured:hover {
        box-shadow: 0 0 0 4px var(--primary-light), var(--shadow-lg);
    }
    
    .pricing-badge {
        position: absolute;
        top: -14px;
        left: 50%;
        transform: translateX(-50%);
        background: var(--primary);
        color: white;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.05em;
        padding: 6px 16px;
        border-radius: 100px;
        text-transform: uppercase;
    }
    
    .pricing-label {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 13px;
        font-weight: 600;
        color: var(--primary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
    }
    
    .pricing-amount {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 52px;
        font-weight: 800;
        color: var(--text);
        letter-spacing: -0.03em;
        animation: countUp 0.6s ease-out 0.2s both;
    }
    
    .pricing-amount sup {
        font-size: 24px;
        font-weight: 600;
        vertical-align: super;
    }
    
    .pricing-period {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 14px;
        color: var(--text-muted);
        margin-bottom: 24px;
    }
    
    .pricing-features {
        list-style: none;
        padding: 0;
        margin: 0 0 28px;
    }
    
    .pricing-features li {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 14px;
        color: var(--text-secondary);
        padding: 12px 0;
        border-bottom: 1px solid var(--border-light);
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .pricing-features li::before {
        content: "✓";
        color: var(--green);
        font-weight: 700;
    }
    
    .guarantee-box {
        background: var(--green-light);
        border-radius: 12px;
        padding: 16px 20px;
        display: flex;
        align-items: center;
        gap: 12px;
        transition: all 0.3s ease;
        animation: fadeInUp 0.5s ease-out 0.3s both;
    }
    
    .guarantee-box:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.15);
    }
    
    .guarantee-box-icon {
        font-size: 24px;
    }
    
    .guarantee-box-text {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 14px;
        color: var(--text);
    }
    
    .guarantee-box-text strong {
        color: var(--green);
    }
    
    /* Math card */
    .math-card {
        background: var(--bg-soft);
        border: 1px solid var(--border);
        border-radius: 24px;
        padding: 36px;
        opacity: 0;
        animation: slideInRight 0.6s ease-out 0.2s forwards;
    }
    
    .math-card h3 {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 20px;
        font-weight: 700;
        color: var(--text);
        margin: 0 0 24px;
    }
    
    .math-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 14px 0;
        border-bottom: 1px solid var(--border);
    }
    
    .math-row:last-child {
        border-bottom: none;
        padding-top: 20px;
        margin-top: 8px;
        border-top: 2px solid var(--border);
    }
    
    .math-label {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 14px;
        color: var(--text-muted);
    }
    
    .math-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 18px;
        font-weight: 600;
        color: var(--text);
    }
    
    .math-value.highlight {
        color: var(--green);
        font-size: 22px;
        animation: pulse 2s ease-in-out infinite;
    }
    
    /* FAQ */
    .faq-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 20px;
        max-width: 900px;
        margin: 0 auto;
    }
    
    @media (max-width: 700px) {
        .faq-grid { grid-template-columns: 1fr; }
    }
    
    .faq-item {
        background: white;
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 28px;
        transition: all 0.3s ease;
        opacity: 0;
        animation: fadeInUp 0.5s ease-out forwards;
    }
    
    .faq-item:nth-child(1) { animation-delay: 0.05s; }
    .faq-item:nth-child(2) { animation-delay: 0.1s; }
    .faq-item:nth-child(3) { animation-delay: 0.15s; }
    .faq-item:nth-child(4) { animation-delay: 0.2s; }
    
    .faq-item:hover {
        border-color: var(--primary);
        box-shadow: var(--shadow);
        transform: translateY(-4px);
    }
    
    .faq-question {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 16px;
        font-weight: 700;
        color: #0f172a;
        margin: 0 0 12px;
    }
    
    .faq-answer {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 14px;
        color: #475569;
        line-height: 1.7;
        margin: 0;
    }
    
    /* CTA Section */
    .cta-section {
        padding: 100px 5%;
        background: linear-gradient(180deg, var(--bg-soft) 0%, white 100%);
        text-align: center;
    }
    
    .cta-title {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 36px;
        font-weight: 800;
        color: var(--text);
        margin: 0 0 16px;
        letter-spacing: -0.02em;
        animation: fadeInUp 0.6s ease-out both;
    }
    
    .cta-text {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 17px;
        color: var(--text-muted);
        margin: 0 0 32px;
        animation: fadeInUp 0.6s ease-out 0.1s both;
    }
    
    .cta-trust {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 24px;
        margin-top: 24px;
    }
    
    .cta-trust-item {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 13px;
        color: var(--text-muted);
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    /* Footer */
    .footer {
        padding: 40px 5%;
        border-top: 1px solid var(--border);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .footer-brand {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 14px;
        color: var(--text-muted);
    }
    
    .footer-links {
        display: flex;
        gap: 24px;
    }
    
    .footer-links a {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 13px;
        color: var(--text-muted);
        text-decoration: none;
        transition: color 0.2s;
    }
    
    .footer-links a:hover {
        color: var(--text);
    }
    
    /* Form Styles */
    .form-container {
        max-width: 640px;
        margin: 0 auto;
        padding: 100px 24px;
    }
    
    .form-header {
        text-align: center;
        margin-bottom: 48px;
    }
    
    .form-card {
        background: white;
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 32px;
        margin-bottom: 20px;
    }
    
    .form-card-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 24px;
        padding-bottom: 16px;
        border-bottom: 1px solid var(--border-light);
    }
    
    .form-card-num {
        width: 32px;
        height: 32px;
        background: var(--primary);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'JetBrains Mono', monospace;
        font-size: 13px;
        font-weight: 600;
        color: white;
    }
    
    .form-card-title {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 17px;
        font-weight: 700;
        color: var(--text);
    }
    
    /* Streamlit overrides */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {
        background: var(--bg-soft) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        color: var(--text) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        padding: 12px 16px !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px var(--primary-light) !important;
    }
    
    .stTextInput > label,
    .stNumberInput > label,
    .stSelectbox > label,
    .stSlider > label,
    .stFileUploader > label {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        color: var(--text-secondary) !important;
    }
    
    .stButton > button {
        background: var(--primary) !important;
        color: white !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 28px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        animation: fadeInUp 0.5s ease-out 0.2s both;
    }
    
    .stButton > button:hover {
        background: var(--primary-hover) !important;
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 20px var(--primary-glow) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(0.98) !important;
    }
    
    .stFileUploader > div {
        background: var(--bg-soft) !important;
        border: 2px dashed var(--border) !important;
        border-radius: 12px !important;
    }
    
    .stSuccess {
        background: var(--green-light) !important;
        border: 1px solid rgba(16, 185, 129, 0.2) !important;
        border-radius: 10px !important;
    }
    
    /* Results */
    .result-card {
        background: white;
        border: 2px solid var(--primary);
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        box-shadow: 0 0 0 4px var(--primary-light);
    }
    
    .result-label {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 14px;
        color: var(--text-muted);
        margin-bottom: 8px;
    }
    
    .result-amount {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 48px;
        font-weight: 800;
        color: var(--green);
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .hero { padding: 120px 5% 60px; }
        .hero h1 { font-size: 32px; }
        .floating-card { display: none; }
        .stats-strip { flex-direction: column; gap: 24px; }
        .section { padding: 60px 5%; }
        .nav-links { display: none; }
    }
</style>
""", unsafe_allow_html=True)


def show_landing_page():
    """Display the premium landing page."""
    
    # Navigation
    st.markdown("""
    <div class="nav">
        <div class="nav-brand">
            <div class="nav-brand-icon">⚡</div>
            Profit Leak Audit
        </div>
        <div class="nav-links">
            <a href="#how-it-works" class="nav-link">How it works</a>
            <a href="#features" class="nav-link">Features</a>
            <a href="#pricing" class="nav-link">Pricing</a>
            <a href="#start" class="nav-cta">Get started</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Hero Section - all in one block
    st.markdown("""
    <div class="hero">
        <div class="floating-card left-1">
            <div class="floating-card-icon" style="background: #fef3c7;">💰</div>
            <div class="floating-card-title">Pricing Gap Found</div>
            <div class="floating-card-value">+$18,500</div>
            <div class="floating-card-sub">per year</div>
        </div>
        <div class="floating-card left-2">
            <div class="floating-card-icon" style="background: #dbeafe;">📊</div>
            <div class="floating-card-title">Quote Win Rate</div>
            <div class="floating-card-value">68%</div>
            <div class="floating-card-sub">vs 45% industry avg</div>
        </div>
        <div class="floating-card right-1">
            <div class="floating-card-icon" style="background: #dcfce7;">⏱️</div>
            <div class="floating-card-title">Time Recovered</div>
            <div class="floating-card-value">12 hrs</div>
            <div class="floating-card-sub">per week</div>
        </div>
        <div class="floating-card right-2">
            <div class="floating-card-icon" style="background: #fce7f3;">🎯</div>
            <div class="floating-card-title">Action Items</div>
            <div class="floating-card-value">14</div>
            <div class="floating-card-sub">quick wins identified</div>
        </div>
        <div class="hero-content">
            <div class="hero-badge">For tradies doing $150k-$500k/year</div>
            <div class="hero-icon">
                <div class="hero-icon-dots">
                    <div class="hero-icon-dot"></div>
                    <div class="hero-icon-dot"></div>
                    <div class="hero-icon-dot"></div>
                    <div class="hero-icon-dot"></div>
                </div>
            </div>
            <h1>Find your profit leaks<br><span>all in one audit</span></h1>
            <p class="hero-text">Most tradies leave $20k-50k on the table every year. We analyze your numbers, find the leaks, and give you a step-by-step plan to fix them.</p>
            <a href="#start" class="hero-cta">Get your free audit →</a>
            <div class="stats-strip">
                <div class="stat-item">
                    <div class="stat-value">$38k</div>
                    <div class="stat-label">Average opportunity found</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">7 days</div>
                    <div class="stat-label">Report delivered</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">127+</div>
                    <div class="stat-label">Tradies audited</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # How it works
    st.markdown("""
    <div class="section section-gray" id="how-it-works">
        <div class="section-header">
            <div class="section-badge">How it works</div>
            <h2 class="section-title">Four simple steps to more profit</h2>
            <p class="section-desc">No complicated software. No long-term contracts. Just clear answers about your business.</p>
        </div>
        <div class="process-grid">
            <div class="process-card">
                <div class="process-num">1</div>
                <h3>Upload your data</h3>
                <p>Send us 12 months of invoices, expenses, and quotes. Takes 15 minutes.</p>
            </div>
            <div class="process-card">
                <div class="process-num">2</div>
                <h3>We analyze everything</h3>
                <p>Every job, customer, and expense. Benchmarked against similar tradies.</p>
            </div>
            <div class="process-card">
                <div class="process-num">3</div>
                <h3>Get your action plan</h3>
                <p>Clear report with exact numbers and scripts for what to say to customers.</p>
            </div>
            <div class="process-card">
                <div class="process-num">4</div>
                <h3>Strategy call</h3>
                <p>60 minutes to walk through findings and plan your next moves.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Features
    st.markdown("""
    <div class="section" id="features">
        <div class="section-header">
            <div class="section-badge">What's included</div>
            <h2 class="section-title">Everything you need to fix the leaks</h2>
        </div>
        <div class="features-grid">
            <div class="feature-card">
                <div class="feature-icon">📊</div>
                <h4>Pricing Audit</h4>
                <p>Your rate vs 2026 market data. Exact recommended rates with scripts that work.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">💰</div>
                <h4>Job Profitability</h4>
                <p>Which jobs make money, which don't. Customer rankings by value.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📈</div>
                <h4>Quote Analysis</h4>
                <p>Your win rate vs benchmarks. Why you're losing quotes and how to close more.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">⏱️</div>
                <h4>Time Leak Report</h4>
                <p>Where your hours go. What to delegate or automate first.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🎯</div>
                <h4>90-Day Action Plan</h4>
                <p>Prioritized quick wins ranked by impact. Conservative estimates.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📝</div>
                <h4>Word-for-Word Scripts</h4>
                <p>Exactly what to say to customers. How to handle pushback.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Testimonials
    st.markdown("""
    <div class="section section-gray">
        <div class="section-header">
            <div class="section-badge">Results</div>
            <h2 class="section-title">What tradies are saying</h2>
        </div>
        <div class="testimonials-grid">
            <div class="testimonial-card">
                <div class="testimonial-stars">★★★★★</div>
                <p class="testimonial-quote">
                    "I thought I was doing okay. Turns out I was leaving $60k on the table. 
                    Raised my rates last week — not a single customer complained."
                </p>
                <div class="testimonial-result">
                    <span class="testimonial-result-value">+$60k/year identified</span>
                </div>
                <div class="testimonial-author">
                    <div class="testimonial-avatar">D</div>
                    <div>
                        <div class="testimonial-name">Dave M.</div>
                        <div class="testimonial-role">Electrician, Sydney</div>
                    </div>
                </div>
            </div>
            <div class="testimonial-card">
                <div class="testimonial-stars">★★★★★</div>
                <p class="testimonial-quote">
                    "Finally someone who speaks my language. No accounting jargon, just 
                    'here's what you're losing and here's how to fix it.' Scripts were gold."
                </p>
                <div class="testimonial-result">
                    <span class="testimonial-result-value">+$42k/year identified</span>
                </div>
                <div class="testimonial-author">
                    <div class="testimonial-avatar">M</div>
                    <div>
                        <div class="testimonial-name">Mark T.</div>
                        <div class="testimonial-role">Plumber, Melbourne</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Pricing
    st.markdown("""
    <div class="section" id="pricing">
        <div class="section-header">
            <div class="section-badge">Investment</div>
            <h2 class="section-title">One audit. Thousands in returns.</h2>
        </div>
        <div class="pricing-container">
            <div class="pricing-card featured">
                <div class="pricing-badge">Most Popular</div>
                <div class="pricing-label">Complete Profit Leak Audit</div>
                <div class="pricing-amount"><sup>$</sup>797</div>
                <div class="pricing-period">One-time investment · AUD</div>
                <ul class="pricing-features">
                    <li>Complete business financial analysis</li>
                    <li>Market rate benchmarking (2026 data)</li>
                    <li>Job-by-job profitability breakdown</li>
                    <li>Customer value ranking</li>
                    <li>Detailed PDF report + Excel workbook</li>
                    <li>Word-for-word scripts for price increases</li>
                    <li>60-minute strategy call</li>
                    <li>30/60/90 day follow-up check-ins</li>
                </ul>
                <div class="guarantee-box">
                    <span class="guarantee-box-icon">🛡️</span>
                    <span class="guarantee-box-text"><strong>$10k+ Guarantee:</strong> We find it or you pay nothing.</span>
                </div>
            </div>
            <div class="math-card">
                <h3>Is this worth it?</h3>
                <div class="math-row">
                    <span class="math-label">Average opportunity found</span>
                    <span class="math-value">$38,500</span>
                </div>
                <div class="math-row">
                    <span class="math-label">Even at 50% implementation</span>
                    <span class="math-value">$19,250</span>
                </div>
                <div class="math-row">
                    <span class="math-label">Your investment</span>
                    <span class="math-value">$797</span>
                </div>
                <div class="math-row">
                    <span class="math-label">Your return</span>
                    <span class="math-value highlight">24x ROI</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # FAQ
    st.markdown("""
    <div class="section section-gray">
        <div class="section-header">
            <div class="section-badge">FAQ</div>
            <h2 class="section-title">Common questions</h2>
        </div>
        <div class="faq-grid">
            <div class="faq-item">
                <div class="faq-question">What if my records are a mess?</div>
                <div class="faq-answer">We work with messy data all the time. Bank statements, random invoices — we'll piece it together. Just send what you have.</div>
            </div>
            <div class="faq-item">
                <div class="faq-question">Will I lose customers if I raise prices?</div>
                <div class="faq-answer">We give you word-for-word scripts for how to raise prices without losing good customers. Most tradies are 15-30% under market rate — your customers expect it.</div>
            </div>
            <div class="faq-item">
                <div class="faq-question">What if you don't find $10k?</div>
                <div class="faq-answer">Full refund. No questions asked. In practice, we've never had this happen — the average opportunity we find is $38k.</div>
            </div>
            <div class="faq-item">
                <div class="faq-question">Can I do this myself?</div>
                <div class="faq-answer">Technically yes, if you have 20+ hours spare and know financial analysis. Most tradies don't — that's exactly why we built this.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # CTA
    st.markdown("""
    <div class="cta-section" id="start">
        <h2 class="cta-title">Ready to find your profit leaks?</h2>
        <p class="cta-text">Takes 15 minutes to submit your data. Report delivered in 7 days.</p>
    </div>
    """, unsafe_allow_html=True)


def show_intake_form():
    """Display the intake form."""
    
    st.markdown("""
    <div class="form-container">
        <div class="form-header">
            <div class="section-badge">Get Started</div>
            <h2 class="section-title">Submit your data</h2>
            <p class="section-desc">Fill out the form below. Takes about 15 minutes.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Step 1
    st.markdown("""
    <div class="form-card">
        <div class="form-card-header">
            <div class="form-card-num">1</div>
            <div class="form-card-title">Your business</div>
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
    
    # Step 2
    st.markdown("""
    <div class="form-card">
        <div class="form-card-header">
            <div class="form-card-num">2</div>
            <div class="form-card-title">Current numbers</div>
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
    
    # Step 3
    st.markdown("""
    <div class="form-card">
        <div class="form-card-header">
            <div class="form-card-num">3</div>
            <div class="form-card-title">Upload documents</div>
        </div>
        <p style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 14px; color: #64748b; margin-bottom: 16px;">
            Upload your invoices, expenses, and quotes from the last 12 months.
        </p>
    """, unsafe_allow_html=True)
    
    invoices = st.file_uploader("Invoices", type=['pdf', 'xlsx', 'xls', 'csv'], accept_multiple_files=True, key="inv")
    expenses = st.file_uploader("Expenses / Bank statements", type=['pdf', 'xlsx', 'xls', 'csv'], accept_multiple_files=True, key="exp")
    quotes = st.file_uploader("Quotes (optional)", type=['pdf', 'xlsx', 'xls', 'csv'], accept_multiple_files=True, key="quo")
    
    if invoices:
        st.success(f"✓ {len(invoices)} invoice files uploaded")
    if expenses:
        st.success(f"✓ {len(expenses)} expense files uploaded")
    
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
    """Run the audit pipeline."""
    from src.utils.file_handler import FileHandler
    from src.agents.data_extractor import DataExtractor
    from src.agents.analyzer import Analyzer, BusinessContext
    from src.agents.report_generator import ReportGenerator
    
    with st.status("Running your audit...", expanded=True) as status:
        st.write("📁 Saving documents...")
        handler = FileHandler()
        folder = handler.create_customer_folder(business_name)
        
        for files, cat in [(invoices, "invoices"), (expenses, "expenses"), (quotes, "quotes")]:
            for f in files:
                path = folder / cat / f.name
                path.parent.mkdir(exist_ok=True)
                with open(path, 'wb') as out:
                    out.write(f.read())
        
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
        
        st.write("🔍 Extracting data...")
        extractor = DataExtractor()
        results = extractor.extract_from_folder(str(folder))
        combined = extractor.combine_results(results)
        st.write(f"✓ Found {combined['summary']['total_transactions']} transactions")
        
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
        
        st.write("📄 Generating report...")
        generator = ReportGenerator(output_dir="./output")
        report = generator.generate_report(analysis, context, business_name)
        
        status.update(label="✅ Audit complete!", state="complete")
    
    # Results
    opportunity = analysis.guarantee_check.get('total_opportunity', 0)
    conservative = opportunity * 0.7
    
    st.markdown(f"""
    <div class="result-card">
        <div class="result-label">Conservative Opportunity Identified</div>
        <div class="result-amount">${conservative:,.0f}</div>
        <div class="result-label" style="margin-top: 8px;">Best case: ${opportunity:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)
    
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


def show_payment_success():
    """Show success page after payment."""
    st.markdown("""
    <div class="form-container" style="text-align: center;">
        <div style="font-size: 64px; margin-bottom: 24px;">✅</div>
        <h2 class="section-title">Payment Successful!</h2>
        <p class="section-desc">Thank you for your purchase. You're ready to start your audit.</p>
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
    <div class="form-container" style="text-align: center;">
        <div style="font-size: 64px; margin-bottom: 24px;">↩️</div>
        <h2 class="section-title">Payment Cancelled</h2>
        <p class="section-desc">No worries. Your card hasn't been charged.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("← Back to Home", use_container_width=True):
            st.query_params.clear()
            st.rerun()


def handle_stripe_checkout():
    """Redirect to Stripe checkout."""
    base_url = os.getenv("APP_BASE_URL", "http://localhost:8501")
    
    success_url = f"{base_url}?payment=success&session_id={{CHECKOUT_SESSION_ID}}"
    cancel_url = f"{base_url}?payment=cancelled"
    
    result = create_checkout_session(
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={"source": "portal"}
    )
    
    if result["success"]:
        st.session_state.checkout_session_id = result["session_id"]
        st.markdown(f"""
        <meta http-equiv="refresh" content="0;url={result['checkout_url']}">
        <script>window.location.href = "{result['checkout_url']}";</script>
        """, unsafe_allow_html=True)
        st.info("Redirecting to secure payment page...")
    else:
        st.error(f"Payment error: {result.get('error', 'Unknown error')}. Please try again.")


def main():
    params = st.query_params
    
    if params.get("payment") == "success":
        session_id = params.get("session_id")
        if session_id:
            verification = verify_payment(session_id)
            if verification.get("paid"):
                st.session_state.payment_verified = True
                st.session_state.customer_email = verification.get("customer_email")
        show_payment_success()
        return
    
    if params.get("payment") == "cancelled":
        show_payment_cancelled()
        return
    
    if is_test_mode():
        st.markdown("""
        <div style="background: #fef3c7; border-bottom: 1px solid #fcd34d; padding: 10px 20px; text-align: center; position: fixed; top: 0; left: 0; right: 0; z-index: 1000;">
            <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 13px; color: #92400e;">
                🧪 <strong>Test Mode</strong> — Use card 4242 4242 4242 4242
            </span>
        </div>
        <div style="height: 40px;"></div>
        """, unsafe_allow_html=True)
    
    if st.session_state.get('show_form'):
        if st.session_state.get('payment_verified') or os.getenv("BYPASS_PAYMENT") == "true":
            show_intake_form()
        else:
            st.warning("Please complete payment to access the audit form.")
            if st.button("← Back to Home"):
                st.session_state.show_form = False
                st.rerun()
    else:
        show_landing_page()
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if os.getenv("STRIPE_SECRET_KEY"):
                if st.button("Start Your Audit — $797 →", use_container_width=True):
                    handle_stripe_checkout()
            else:
                st.markdown("""
                <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px; margin-bottom: 16px; text-align: center;">
                    <p style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 14px; color: #64748b; margin: 0;">
                        ⚠️ Stripe not configured. Running in demo mode.
                    </p>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Start Your Audit (Demo) →", use_container_width=True):
                    st.session_state.show_form = True
                    st.session_state.payment_verified = True
                    st.rerun()
        
        st.markdown("""
        <div class="cta-trust">
            <span class="cta-trust-item">🔒 Secure payment</span>
            <span class="cta-trust-item">💳 All cards accepted</span>
            <span class="cta-trust-item">🛡️ Money-back guarantee</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Footer
        st.markdown("""
        <div class="footer">
            <div class="footer-brand">© 2026 Profit Leak Audit</div>
            <div class="footer-links">
                <a href="mailto:hello@profitleakaudit.com.au">Contact</a>
                <a href="#">Privacy</a>
                <a href="#">Terms</a>
            </div>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
