"""
Tradie Audit Agent - Streamlit Web Interface
A beautiful, user-friendly way to run audits.
"""

import os
import sys
from pathlib import Path
import tempfile
import json
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def load_css(file_path):
    """Load a CSS file and return its content."""
    with open(file_path) as f:
        return f.read()

css_file = Path(__file__).parent.parent / "styles" / "main.css"
st.markdown(f'<style>{load_css(css_file)}</style>', unsafe_allow_html=True)



def show_header():
    """Display the main header."""
    st.markdown("""
    <div class="section">
        <h1>🚀 Tradie Growth Audit</h1>
        <p>Comprehensive business analysis + 90-minute growth strategy call</p>
        <p style="font-size: 0.9rem; opacity: 0.8;">Find hidden profit, fix operational bottlenecks, and get a clear path to your revenue goals</p>
    </div>
    """, unsafe_allow_html=True)


def show_data_collection():
    """Show the data collection form."""
    st.sidebar.header("📋 Business Details")
    
    customer_name = st.sidebar.text_input(
        "Business Name",
        placeholder="Dave's Electrical"
    )
    
    trade_type = st.sidebar.selectbox(
        "Trade Type",
        ["electrician", "plumber", "carpenter", "hvac", "builder", "other"]
    )
    
    location = st.sidebar.text_input(
        "Location (City)",
        value="Sydney"
    )
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        current_rate = st.number_input(
            "Current Rate ($/hr)",
            min_value=50,
            max_value=300,
            value=95
        )
    with col2:
        hours_per_week = st.number_input(
            "Hours/Week",
            min_value=20,
            max_value=80,
            value=50
        )
    
    col3, col4 = st.sidebar.columns(2)
    with col3:
        years_in_business = st.number_input(
            "Years in Business",
            min_value=1,
            max_value=50,
            value=5
        )
    with col4:
        revenue_goal = st.number_input(
            "Revenue Goal ($k)",
            min_value=100,
            max_value=1000,
            value=250
        ) * 1000
    
    return {
        'customer_name': customer_name,
        'trade_type': trade_type,
        'location': location,
        'current_rate': current_rate,
        'hours_per_week': hours_per_week,
        'years_in_business': years_in_business,
        'revenue_goal': revenue_goal
    }


def show_file_upload():
    """Show the file upload section."""
    st.header("📄 Upload Your Documents")
    
    st.markdown("""
    Upload your financial documents. We accept:
    - **Invoices** (PDF, Excel, CSV)
    - **Bank Statements** (PDF)
    - **Expense Reports** (Excel, CSV)
    - **Quote History** (any format)
    """)
    
    uploaded_files = st.file_uploader(
        "Drop files here or click to browse",
        type=['pdf', 'xlsx', 'xls', 'csv'],
        accept_multiple_files=True,
        help="Upload 12 months of financial data for best results"
    )
    
    if uploaded_files:
        st.success(f"✓ {len(uploaded_files)} files uploaded")
        with st.expander("View uploaded files"):
            for f in uploaded_files:
                st.write(f"📄 {f.name} ({f.size / 1024:.1f} KB)")
    
    return uploaded_files


def run_analysis(files, business_info):
    """Run the full audit analysis."""
    from src.agents.data_extractor import DataExtractor
    from src.agents.analyzer import Analyzer, BusinessContext
    from src.agents.report_generator import ReportGenerator
    
    # Save uploaded files to temp directory
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        for f in files:
            file_path = temp_path / f.name
            with open(file_path, 'wb') as out_file:
                out_file.write(f.read())
        
        # Step 1: Extract
        with st.status("🔍 Analyzing your documents...", expanded=True) as status:
            st.write("📄 Extracting data from documents...")
            
            extractor = DataExtractor()
            extraction_results = extractor.extract_from_folder(str(temp_path))
            combined_data = extractor.combine_results(extraction_results)
            
            st.write(f"✓ Found {combined_data['summary']['total_transactions']} transactions")
            st.write(f"✓ Revenue: ${combined_data['summary']['total_revenue']:,.2f}")
            st.write(f"✓ Expenses: ${combined_data['summary']['total_expenses']:,.2f}")
            
            # Step 2: Analyze
            st.write("📊 Analyzing profitability...")
            
            context = BusinessContext(
                trade_type=business_info['trade_type'],
                location=business_info['location'],
                years_in_business=business_info['years_in_business'],
                current_rate=business_info['current_rate'],
                hours_per_week=business_info['hours_per_week'],
                revenue_goal=business_info['revenue_goal']
            )
            
            analyzer = Analyzer()
            analysis = analyzer.analyze(combined_data, context)
            
            st.write(f"✓ Identified ${analysis.guarantee_check.get('total_opportunity', 0):,.2f} in opportunities")
            
            # Step 3: Generate reports
            st.write("📑 Generating your reports...")
            
            generator = ReportGenerator(output_dir="./output")
            report_result = generator.generate_report(
                analysis, context, business_info['customer_name']
            )
            
            status.update(label="✅ Analysis Complete!", state="complete")
        
        return {
            'analysis': analysis,
            'context': context,
            'report_result': report_result,
            'combined_data': combined_data
        }


def show_results(results):
    """Display the analysis results."""
    analysis = results['analysis']
    context = results['context']
    report = results['report_result']
    
    # Guarantee box
    opportunity = analysis.guarantee_check.get('total_opportunity', 0)
    st.markdown(f"""
    <div class="section cta-section">
        <h2>💰 Total Opportunity Identified</h2>
        <div class="feature-card" style="max-width: 400px; margin: 0 auto;">
            <h3 style="text-align: center; font-size: 2.5rem; margin-bottom: 0;">${opportunity:,.0f}</h3>
            <p style="text-align: center; margin-top: 0;">{"✓ $10k Guarantee Met!" if opportunity >= 10000 else "Review recommended"}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Key metrics
    st.header("📊 Key Findings")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Current Rate",
            f"${context.current_rate}/hr",
            f"+${analysis.pricing_audit.get('recommended_rate', context.current_rate) - context.current_rate}/hr potential"
        )
    
    with col2:
        st.metric(
            "Recommended Rate",
            f"${analysis.pricing_audit.get('recommended_rate', context.current_rate)}/hr"
        )
    
    with col3:
        margin = analysis.summary.get('profit_margin', 0)
        st.metric(
            "Profit Margin",
            f"{margin * 100 if isinstance(margin, float) else margin:.0f}%"
        )
    
    with col4:
        st.metric(
            "Actions Identified",
            len(analysis.action_plan)
        )
    
    # Action Plan
    st.header("🎯 90-Day Action Plan")
    
    for i, action in enumerate(analysis.action_plan[:10], 1):
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{i}. {action.get('action', 'N/A')}**")
                if action.get('how'):
                    st.caption(action['how'])
            with col2:
                impact = action.get('impact_annual', 0)
                st.metric("Impact", f"${impact:,.0f}/yr", label_visibility="collapsed")
            
            # Tags
            tags = []
            if action.get('effort'):
                tags.append(f"Effort: {action['effort']}")
            if action.get('timeline'):
                tags.append(f"Timeline: {action['timeline']}")
            
            if tags:
                st.caption(" • ".join(tags))
            
            st.divider()
    
    # Executive Summary
    st.header("📝 Executive Summary")
    st.markdown(report.get('executive_summary', 'Summary not available'))
    
    # Download section
    st.header("📥 Download Your Reports")
    
    col1, col2, col3 = st.columns(3)
    
    html_path = report.get('html_report')
    excel_path = report.get('excel_report')
    json_path = report.get('json_data')
    
    if html_path and Path(html_path).exists():
        with col1:
            with open(html_path, 'r') as f:
                st.download_button(
                    "📄 Download HTML Report",
                    f.read(),
                    file_name="profit_leak_audit_report.html",
                    mime="text/html"
                )
    
    if excel_path and Path(excel_path).exists():
        with col2:
            with open(excel_path, 'rb') as f:
                st.download_button(
                    "📊 Download Excel Workbook",
                    f.read(),
                    file_name="profit_leak_audit_workbook.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    
    if json_path and Path(json_path).exists():
        with col3:
            with open(json_path, 'r') as f:
                st.download_button(
                    "📋 Download Raw Data (JSON)",
                    f.read(),
                    file_name="analysis_data.json",
                    mime="application/json"
                )


def home_page():
    """Main application."""
    # Check for API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        st.error("⚠️ ANTHROPIC_API_KEY not set. Please configure your environment.")
        st.code("export ANTHROPIC_API_KEY='your-key-here'")
        st.stop()
    
    show_header()
    
    # Sidebar: Business details
    business_info = show_data_collection()
    
    # Main area: File upload
    uploaded_files = show_file_upload()
    
    # Run analysis button
    st.divider()
    
    ready = (
        business_info['customer_name'] and 
        uploaded_files and 
        len(uploaded_files) > 0
    )
    
    if ready:
        if st.button("🚀 Run Growth Audit", type="primary", use_container_width=True):
            try:
                results = run_analysis(uploaded_files, business_info)
                st.session_state['results'] = results
            except Exception as e:
                st.error(f"Error running analysis: {e}")
                import traceback
                st.code(traceback.format_exc())
    else:
        st.button(
            "🚀 Run Growth Audit", 
            type="primary", 
            use_container_width=True,
            disabled=True,
            help="Enter business name and upload at least one document"
        )
    
    # Show results if available
    if 'results' in st.session_state:
        st.divider()
        show_results(st.session_state['results'])


if __name__ == "__main__":
    home_page()

