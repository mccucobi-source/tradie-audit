"""
Admin Dashboard - Your control panel for managing audits.
Run with: streamlit run src/admin_dashboard.py
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
    page_title="Audit Admin Dashboard",
    page_icon="⚙️",
    layout="wide"
)

from dotenv import load_dotenv
load_dotenv()

st.markdown("""
<style>
    .admin-header {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
    }
    
    .stat-box {
        background: white;
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        text-align: center;
    }
    
    .stat-box .number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #10b981;
    }
    
    .stat-box .label {
        color: #64748b;
        font-size: 0.9rem;
    }
    
    .customer-card {
        background: white;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border-left: 4px solid #10b981;
    }
    
    .status-pending {
        background: #fef3c7;
        color: #92400e;
        padding: 0.25rem 0.75rem;
        border-radius: 100px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .status-complete {
        background: #d1fae5;
        color: #065f46;
        padding: 0.25rem 0.75rem;
        border-radius: 100px;
        font-size: 0.8rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


def get_all_submissions():
    """Get all customer submissions from the data folder."""
    data_dir = Path("./data")
    if not data_dir.exists():
        return []
    
    submissions = []
    for folder in data_dir.iterdir():
        if folder.is_dir() and folder.name != "sample_test":
            intake_file = folder / "intake_form.json"
            
            # Count files
            file_count = sum(1 for _ in folder.rglob("*") if _.is_file() and _.name != "intake_form.json")
            
            # Check for output
            output_dir = Path("./output")
            has_output = any(
                o.name.startswith(folder.name.split("_")[0]) 
                for o in output_dir.iterdir() if o.is_dir()
            ) if output_dir.exists() else False
            
            if intake_file.exists():
                with open(intake_file) as f:
                    data = json.load(f)
                submissions.append({
                    'folder': str(folder),
                    'folder_name': folder.name,
                    'data': data,
                    'file_count': file_count,
                    'has_output': has_output,
                    'created': datetime.fromisoformat(data.get('submitted_at', folder.stat().st_ctime.__str__()))
                })
            else:
                # Folder without intake form (manual upload)
                submissions.append({
                    'folder': str(folder),
                    'folder_name': folder.name,
                    'data': {'business_info': {'business_name': folder.name}},
                    'file_count': file_count,
                    'has_output': has_output,
                    'created': datetime.fromtimestamp(folder.stat().st_ctime)
                })
    
    return sorted(submissions, key=lambda x: x['created'], reverse=True)


def get_all_outputs():
    """Get all completed audit outputs."""
    output_dir = Path("./output")
    if not output_dir.exists():
        return []
    
    outputs = []
    for folder in output_dir.iterdir():
        if folder.is_dir():
            json_file = folder / "analysis_data.json"
            if json_file.exists():
                with open(json_file) as f:
                    data = json.load(f)
                outputs.append({
                    'folder': str(folder),
                    'folder_name': folder.name,
                    'customer_name': data.get('customer_name', folder.name),
                    'opportunity': data.get('guarantee_check', {}).get('total_opportunity', 0),
                    'created': datetime.fromtimestamp(folder.stat().st_ctime)
                })
    
    return sorted(outputs, key=lambda x: x['created'], reverse=True)


def run_audit_for_submission(folder_path: str, trade: str = "electrician", 
                              location: str = "Sydney", rate: float = 95):
    """Run audit on a customer folder."""
    from src.agents.data_extractor import DataExtractor
    from src.agents.analyzer import Analyzer, BusinessContext
    from src.agents.report_generator import ReportGenerator
    
    # Load intake form if exists
    intake_file = Path(folder_path) / "intake_form.json"
    if intake_file.exists():
        with open(intake_file) as f:
            intake = json.load(f)
        business_info = intake.get('business_info', {})
        numbers = intake.get('numbers', {})
        
        trade = business_info.get('trade_type', trade).lower()
        if 'electric' in trade: trade = 'electrician'
        elif 'plumb' in trade: trade = 'plumber'
        elif 'carp' in trade: trade = 'carpenter'
        else: trade = 'other'
        
        location = business_info.get('location', location)
        rate = numbers.get('hourly_rate', rate) or rate
        customer_name = business_info.get('business_name', 'Customer')
    else:
        customer_name = Path(folder_path).name
    
    context = BusinessContext(
        trade_type=trade,
        location=location,
        years_in_business=5,
        current_rate=float(rate),
        hours_per_week=50,
        revenue_goal=250000
    )
    
    # Run pipeline
    extractor = DataExtractor()
    results = extractor.extract_from_folder(folder_path)
    combined = extractor.combine_results(results)
    
    analyzer = Analyzer()
    analysis = analyzer.analyze(combined, context)
    
    generator = ReportGenerator(output_dir="./output")
    report = generator.generate_report(analysis, context, customer_name)
    
    return {
        'analysis': analysis,
        'report': report,
        'combined_data': combined
    }


def main():
    st.markdown("""
    <div class="admin-header">
        <h1>⚙️ Audit Admin Dashboard</h1>
        <p>Manage customer audits and track your business</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get data
    submissions = get_all_submissions()
    outputs = get_all_outputs()
    
    # Stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Submissions", len(submissions))
    
    with col2:
        st.metric("Completed Audits", len(outputs))
    
    with col3:
        pending = len([s for s in submissions if not s['has_output']])
        st.metric("Pending Review", pending)
    
    with col4:
        total_opportunity = sum(o['opportunity'] for o in outputs)
        st.metric("Total Opportunity Found", f"${total_opportunity:,.0f}")
    
    st.divider()
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["📥 Pending Audits", "✅ Completed", "🔧 Manual Audit"])
    
    with tab1:
        st.header("Pending Customer Submissions")
        
        pending_submissions = [s for s in submissions if not s['has_output']]
        
        if not pending_submissions:
            st.info("No pending audits. Great job! 🎉")
        else:
            for sub in pending_submissions:
                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        business_name = sub['data'].get('business_info', {}).get('business_name', sub['folder_name'])
                        st.subheader(business_name)
                        
                        info = sub['data'].get('business_info', {})
                        st.caption(f"📍 {info.get('location', 'Unknown')} | 🔧 {info.get('trade_type', 'Unknown')} | 📁 {sub['file_count']} files")
                        
                        if sub['data'].get('goals', {}).get('biggest_question'):
                            st.write(f"**Main question:** {sub['data']['goals']['biggest_question']}")
                    
                    with col2:
                        rate = sub['data'].get('numbers', {}).get('hourly_rate', 95) or 95
                        st.metric("Hourly Rate", f"${rate}")
                    
                    with col3:
                        if st.button("▶️ Run Audit", key=f"run_{sub['folder_name']}"):
                            with st.spinner("Running audit..."):
                                try:
                                    result = run_audit_for_submission(sub['folder'])
                                    opp = result['analysis'].guarantee_check.get('total_opportunity', 0)
                                    st.success(f"✓ Audit complete! Found ${opp:,.0f} in opportunities")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Error: {e}")
                    
                    st.divider()
    
    with tab2:
        st.header("Completed Audits")
        
        if not outputs:
            st.info("No completed audits yet.")
        else:
            for output in outputs:
                with st.container():
                    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                    
                    with col1:
                        st.subheader(output['customer_name'])
                        st.caption(f"Completed: {output['created'].strftime('%Y-%m-%d %H:%M')}")
                    
                    with col2:
                        st.metric("Opportunity", f"${output['opportunity']:,.0f}")
                    
                    with col3:
                        html_path = Path(output['folder']) / "profit_leak_audit_report.html"
                        if html_path.exists():
                            with open(html_path, 'r') as f:
                                st.download_button(
                                    "📄 Report",
                                    f.read(),
                                    file_name=f"{output['customer_name']}_report.html",
                                    mime="text/html",
                                    key=f"dl_html_{output['folder_name']}"
                                )
                    
                    with col4:
                        excel_path = Path(output['folder']) / "profit_leak_audit_workbook.xlsx"
                        if excel_path.exists():
                            with open(excel_path, 'rb') as f:
                                st.download_button(
                                    "📊 Excel",
                                    f.read(),
                                    file_name=f"{output['customer_name']}_workbook.xlsx",
                                    key=f"dl_xlsx_{output['folder_name']}"
                                )
                    
                    st.divider()
    
    with tab3:
        st.header("Run Manual Audit")
        st.write("Upload files directly and run an audit without using the customer portal.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            customer_name = st.text_input("Customer Name", placeholder="Dave's Electrical")
            trade = st.selectbox("Trade", ["electrician", "plumber", "carpenter", "hvac", "builder", "other"])
            location = st.text_input("Location", value="Sydney")
        
        with col2:
            rate = st.number_input("Hourly Rate ($)", min_value=50, max_value=300, value=95)
            hours = st.number_input("Hours/Week", min_value=20, max_value=80, value=50)
        
        files = st.file_uploader(
            "Upload documents (invoices, expenses, quotes)",
            type=['pdf', 'xlsx', 'xls', 'csv'],
            accept_multiple_files=True
        )
        
        if st.button("🚀 Run Audit", type="primary") and customer_name and files:
            from src.utils.file_handler import FileHandler
            
            # Save files
            handler = FileHandler()
            folder = handler.create_customer_folder(customer_name)
            
            for f in files:
                file_path = folder / "invoices" / f.name
                file_path.parent.mkdir(exist_ok=True)
                with open(file_path, 'wb') as out:
                    out.write(f.read())
            
            # Run audit
            with st.status("Running audit...", expanded=True) as status:
                st.write(f"📁 Files saved to {folder}")
                st.write("🔬 Analyzing...")
                
                try:
                    result = run_audit_for_submission(str(folder), trade, location, rate)
                    opp = result['analysis'].guarantee_check.get('total_opportunity', 0)
                    
                    status.update(label="✅ Audit Complete!", state="complete")
                    
                    st.success(f"Found **${opp:,.0f}** in opportunities!")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        html_path = result['report']['html_report']
                        with open(html_path, 'r') as f:
                            st.download_button(
                                "📄 Download Report",
                                f.read(),
                                file_name="audit_report.html",
                                mime="text/html"
                            )
                    with col2:
                        excel_path = result['report']['excel_report']
                        with open(excel_path, 'rb') as f:
                            st.download_button(
                                "📊 Download Excel",
                                f.read(),
                                file_name="audit_workbook.xlsx"
                            )
                
                except Exception as e:
                    st.error(f"Error: {e}")
                    import traceback
                    st.code(traceback.format_exc())


if __name__ == "__main__":
    main()

