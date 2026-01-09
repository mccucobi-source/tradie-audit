"""
Customer Portal - STREAMLINED VERSION
Reduced from 30 min to 10 min while keeping AI quality.
Only asks what Claude actually needs for the best output.
"""

import os
import sys
from pathlib import Path
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
    st.markdown("""
    <div class="section">
        <h1>🚀 Business Audit - Quick Setup</h1>
        <p>Get your comprehensive business analysis in 10 minutes. Upload your data, we'll handle the rest.</p>
    </div>
    """, unsafe_allow_html=True)


def step_basic_info():
    """Step 1: Essential business information."""
    with st.container():
        st.markdown("## Step 1: Your Business")
        st.markdown("Just the basics so we can benchmark your business correctly.")

        col1, col2 = st.columns(2)

        with col1:
            business_name = st.text_input(
                "Business Name *",
                placeholder="e.g., Dave's Electrical Services",
                help="Your trading name"
            )

            owner_name = st.text_input(
                "Your Name *",
                placeholder="e.g., Dave Smith",
                help="We'll personalize your report with this"
            )

            email = st.text_input(
                "Email Address *",
                placeholder="dave@example.com",
                help="We'll send your report here in 48 hours"
            )

        with col2:
            trade_type = st.selectbox(
                "Your Trade *",
                options=[
                    "Select your trade...",
                    "Electrician",
                    "Plumber",
                    "Carpenter / Joiner",
                    "HVAC / Air Conditioning",
                    "Builder",
                    "Painter",
                    "Roofer",
                    "Landscaper",
                    "Other"
                ],
                help="For market benchmarking"
            )

            if trade_type == "Other":
                trade_other = st.text_input("Please specify:")

            location = st.text_input(
                "Service Area *",
                placeholder="e.g., Sydney, Brisbane, Regional NSW",
                help="Your primary location for market rate comparison"
            )

    return {
        'business_name': business_name,
        'owner_name': owner_name,
        'email': email,
        'trade_type': trade_type if trade_type != "Select your trade..." else "",
        'trade_other': trade_other if trade_type == "Other" else "",
        'location': location
    }


def step_pricing():
    """Step 2: Current pricing."""
    with st.container():
        st.markdown("## Step 2: Your Current Pricing")
        st.markdown("This helps us identify if you're undercharging vs the market.")

        col1, col2 = st.columns(2)

        with col1:
            hourly_rate = st.number_input(
                "Your Standard Hourly Rate ($) *",
                min_value=0,
                max_value=500,
                value=0,
                step=5,
                help="What you charge per hour for labor"
            )

            call_out_fee = st.number_input(
                "Call-out / Service Fee ($)",
                min_value=0,
                max_value=300,
                value=0,
                step=5,
                help="If you charge one. Enter 0 if you don't."
            )

        with col2:
            material_markup = st.selectbox(
                "Material Markup *",
                options=[
                    "I don't know",
                    "Cost price (0%)",
                    "5-10%",
                    "10-20%",
                    "20-30%",
                    "30%+"
                ],
                help="How much you add to materials"
            )

            hours_per_week = st.slider(
                "Hours Worked Per Week *",
                min_value=20,
                max_value=80,
                value=50,
                help="Total hours including admin, travel, everything"
            )

    return {
        'hourly_rate': hourly_rate,
        'call_out_fee': call_out_fee,
        'material_markup': material_markup,
        'hours_per_week': hours_per_week
    }


def step_goals():
    """Step 3: Goals and priorities."""
    with st.container():
        st.markdown("## Step 3: What You Want")
        st.markdown("This helps us focus on what matters most to you.")

        col1, col2 = st.columns(2)

        with col1:
            revenue_goal = st.number_input(
                "Revenue Goal (next 12 months) $ *",
                min_value=0,
                max_value=2000000,
                value=250000,
                step=10000,
                help="What you'd like to hit"
            )

            main_goal = st.selectbox(
                "Primary Goal *",
                options=[
                    "Select...",
                    "Increase profit (keep same hours)",
                    "Same profit, work fewer hours",
                    "Grow the business significantly",
                    "Prepare to hire first employee",
                    "Reduce stress / better work-life balance",
                    "Other"
                ],
                help="What's your #1 priority?"
            )

        with col2:
            frustrations = st.multiselect(
                "Biggest Frustrations (select all that apply) *",
                options=[
                    "Working too many hours",
                    "Not enough profit for the effort",
                    "Too much time on admin/paperwork",
                    "Chasing payments",
                    "Winning enough quotes",
                    "Unreliable customers",
                    "Material costs eating margins",
                    "Competition on price",
                    "Not sure where money goes"
                ],
                help="What's driving you crazy?"
            )

            biggest_question = st.text_area(
                "The #1 question you want answered *",
                placeholder="e.g., 'Am I charging enough?' or 'Which jobs should I stop doing?'",
                help="We'll make sure to address this in your report"
            )

    return {
        'revenue_goal': revenue_goal,
        'main_goal': main_goal if main_goal != "Select..." else "",
        'frustrations': frustrations,
        'biggest_question': biggest_question
    }


def step_file_upload():
    """Step 4: Upload financial documents."""
    with st.container():
        st.markdown("## Step 4: Upload Your Data")
        st.markdown("This is where the magic happens. The more data, the better your audit.")
        st.warning("🔒 **Your data is secure.** We only use it for your audit and never share it.")

        # Invoices (REQUIRED)
        st.subheader("📄 Invoices (Required)")
        st.markdown("""
        Upload your invoices from the last **6-12 months**. Accepted: PDF, Excel, CSV

        **Where to get them:**
        - Export from Xero, MYOB, QuickBooks
        - PDF copies of sent invoices
        - Excel/CSV export
        """)

        invoices = st.file_uploader(
            "Drop invoice files here",
            type=['pdf', 'xlsx', 'xls', 'csv'],
            accept_multiple_files=True,
            key="invoices",
            help="The more invoices, the better the analysis"
        )

        if invoices:
            st.success(f"✓ {len(invoices)} invoice file(s) uploaded")

        st.divider()

        # Expenses (OPTIONAL)
        st.subheader("💳 Expenses (Optional but Helpful)")
        st.markdown("""
        Upload business expenses if you have them. Helps with profitability analysis.
        - Bank statement exports
        - Expense reports
        - Receipt summaries
        """)

        expenses = st.file_uploader(
            "Drop expense files here (optional)",
            type=['pdf', 'xlsx', 'xls', 'csv'],
            accept_multiple_files=True,
            key="expenses"
        )

        if expenses:
            st.success(f"✓ {len(expenses)} expense file(s) uploaded")

    return {
        'invoices': invoices,
        'expenses': expenses
    }


def validate_form(all_data: dict) -> tuple[bool, str]:
    """Validate required fields."""
    basic = all_data.get('basic_info', {})
    pricing = all_data.get('pricing', {})
    goals = all_data.get('goals', {})
    files = all_data.get('files', {})

    # Check required fields
    if not basic.get('business_name'):
        return False, "Business name is required"
    if not basic.get('owner_name'):
        return False, "Your name is required"
    if not basic.get('email'):
        return False, "Email is required"
    if not basic.get('trade_type'):
        return False, "Trade type is required"
    if not basic.get('location'):
        return False, "Service area is required"

    if pricing.get('hourly_rate', 0) == 0:
        return False, "Hourly rate is required"
    if not pricing.get('material_markup'):
        return False, "Material markup is required"

    if not goals.get('main_goal'):
        return False, "Primary goal is required"
    if not goals.get('frustrations'):
        return False, "Please select at least one frustration"
    if not goals.get('biggest_question'):
        return False, "Please tell us your #1 question"

    if not files.get('invoices'):
        return False, "At least one invoice file is required"

    return True, ""


def save_submission(all_data: dict) -> str:
    """Save the submission and return folder path."""
    from src.utils.file_handler import FileHandler

    handler = FileHandler(base_dir="./data")
    customer_folder = handler.create_customer_folder(all_data['basic_info']['business_name'])

    # Save form data as JSON
    form_data_path = customer_folder / "intake_form.json"
    saveable_data = {
        'basic_info': all_data['basic_info'],
        'pricing': all_data['pricing'],
        'goals': all_data['goals'],
        'submitted_at': datetime.now().isoformat()
    }

    with open(form_data_path, 'w') as f:
        json.dump(saveable_data, f, indent=2, default=str)

    # Save uploaded files
    if all_data['files']['invoices']:
        invoices_dir = customer_folder / "invoices"
        invoices_dir.mkdir(exist_ok=True)
        for file in all_data['files']['invoices']:
            file_path = invoices_dir / file.name
            with open(file_path, 'wb') as f:
                f.write(file.getbuffer())

    if all_data['files'].get('expenses'):
        expenses_dir = customer_folder / "expenses"
        expenses_dir.mkdir(exist_ok=True)
        for file in all_data['files']['expenses']:
            file_path = expenses_dir / file.name
            with open(file_path, 'wb') as f:
                f.write(file.getbuffer())

    return str(customer_folder)


def main():
    st.set_page_config(
        page_title="Business Audit - Data Collection",
        page_icon="📝",
        layout="wide"
    )

    show_header()

    # Progress indicator
    st.markdown("""
    <div style="background: #f5f5f5; padding: 16px; border-radius: 8px; margin-bottom: 30px;">
        <div style="font-family: 'IBM Plex Mono', monospace; font-size: 12px; color: #737373; margin-bottom: 8px;">
            PROGRESS: 4 SIMPLE STEPS
        </div>
        <div style="font-size: 14px;">
            ⏱️ Takes ~10 minutes · 🔒 Secure & confidential
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Collect data from each step
    basic_info = step_basic_info()

    st.divider()

    pricing = step_pricing()

    st.divider()

    goals = step_goals()

    st.divider()

    files = step_file_upload()

    st.divider()

    # Submit button
    st.markdown("## Ready to Submit?")
    st.markdown("We'll analyze your data and send your comprehensive report within **48 hours**.")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:
        submit_button = st.button(
            "🚀 Submit & Get My Report",
            type="primary",
            use_container_width=True
        )

    if submit_button:
        # Collect all data
        all_data = {
            'basic_info': basic_info,
            'pricing': pricing,
            'goals': goals,
            'files': files
        }

        # Validate
        is_valid, error_msg = validate_form(all_data)

        if not is_valid:
            st.error(f"⚠️ {error_msg}")
        else:
            with st.spinner("Saving your submission..."):
                try:
                    folder_path = save_submission(all_data)

                    st.success("✅ Submission successful!")

                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #16a34a 0%, #22c55e 100%); color: white; padding: 40px; border-radius: 12px; text-align: center; margin: 30px 0;">
                        <h2 style="color: white; margin-bottom: 16px;">🎉 You're All Set!</h2>
                        <p style="font-size: 18px; margin-bottom: 24px;">
                            We're analyzing your data now. Your comprehensive business audit report will be ready in <strong>48 hours</strong>.
                        </p>
                        <div style="background: rgba(255,255,255,0.2); padding: 20px; border-radius: 8px; margin-top: 24px;">
                            <p style="font-size: 16px; margin-bottom: 8px;"><strong>What Happens Next:</strong></p>
                            <p style="font-size: 14px; margin-bottom: 4px;">✓ Check your email for confirmation</p>
                            <p style="font-size: 14px; margin-bottom: 4px;">✓ We'll send your report in 48 hours</p>
                            <p style="font-size: 14px; margin-bottom: 4px;">✓ Book your 30-min strategy call (link in email)</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.balloons()

                    # Show what we saved
                    with st.expander("📁 Submission Details"):
                        st.write(f"**Saved to:** `{folder_path}`")
                        st.write(f"**Invoices uploaded:** {len(files['invoices'])} files")
                        if files.get('expenses'):
                            st.write(f"**Expenses uploaded:** {len(files['expenses'])} files")
                        st.json(all_data['basic_info'])

                except Exception as e:
                    st.error(f"Error saving submission: {str(e)}")
                    st.write("Please try again or contact support.")


if __name__ == "__main__":
    main()
