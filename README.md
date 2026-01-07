# Tradie Profit Leak Audit - AI Agent

Automated financial audit system for Australian trade businesses. Analyzes invoices, expenses, and quotes to find realistic profit opportunities.

**Price Point:** $797/audit  
**API Cost:** $0.15-$0.40/audit  
**Profit Margin:** 99.9%+

## What It Does

Helps electricians, plumbers, carpenters, and other tradies find $10k-$50k+ in profit leaks by:
- Analyzing pricing vs 2026 market benchmarks
- Identifying profitable vs unprofitable job types
- Grading customers (A/B/C/Fire)
- Analyzing cash flow patterns
- Generating actionable plans with word-for-word scripts

## Features

### 🤖 AI-Powered Analysis
- **Data Extractor**: Extracts structured data from PDFs, Excel, CSV
- **Analyzer**: Comprehensive business analysis with 2026 market context
- **Report Generator**: Professional HTML reports + Excel workbooks

### 📊 Analysis Includes
1. **Pricing Audit**: Your rate vs market, with conservative impact calculations
2. **Job Profitability**: Which jobs make money, which don't
3. **Customer Analysis**: A/B/C/Fire grading with recommendations
4. **Cash Flow Insights**: Payment timing, seasonal patterns, risks
5. **Expense Analysis**: Material markup, cost recovery opportunities
6. **90-Day Action Plan**: Prioritized quick wins with scripts

### 💼 Customer Portal
- Professional landing page with Stripe payment integration
- Multi-step intake form for business details and file upload
- Dark theme, premium design (not "AI slop")

### 📈 Quality Metrics
- Conservative estimates (under-promise, over-deliver)
- Every recommendation backed by customer's actual data
- Calculations shown (not just numbers)
- Realistic timelines and effort scores
- Risk assessments included

## Setup

### Prerequisites
- Python 3.9+
- Anthropic API key (Claude Sonnet 4)
- Stripe API key (for payments)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/tradie-audit-agent.git
cd tradie-audit-agent

# Run setup
make setup

# Or manually:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Configuration

Create a `.env` file:

```env
# Required
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Optional - for payments
STRIPE_SECRET_KEY=sk_test_your_stripe_key_here
APP_BASE_URL=http://localhost:8501

# Optional - for testing
BYPASS_PAYMENT=false
```

## Usage

### Quick Test

```bash
make test
```

This will:
1. Create sample data (invoices, expenses, quotes)
2. Run extraction
3. Perform analysis
4. Generate HTML report + Excel workbook

Output in `output/test_electrical_TIMESTAMP/`

### Run Customer Portal

```bash
make run-portal

# Or manually:
streamlit run src/portal.py --server.port 8501
```

Opens at http://localhost:8501

### Command Line

```bash
# Run audit on a folder of files
python src/main.py --input data/customer_files --output output/customer_name

# Specify business context
python src/main.py \
  --input data/customer_files \
  --trade electrician \
  --location Sydney \
  --rate 95 \
  --hours 50
```

## Project Structure

```
audit-agent/
├── src/
│   ├── agents/
│   │   ├── data_extractor.py    # Extract data from files
│   │   ├── analyzer.py           # Analyze & find opportunities
│   │   └── report_generator.py  # Generate reports
│   ├── templates/
│   │   └── prompts.py           # Claude prompts (the "secret sauce")
│   ├── utils/
│   │   ├── market_data.py       # 2026 benchmarks for AU tradies
│   │   └── file_handler.py      # File operations
│   ├── payments.py              # Stripe integration
│   ├── portal.py                # Customer-facing portal
│   ├── admin_dashboard.py       # Admin interface
│   └── main.py                  # CLI
├── data/                        # Sample data
├── output/                      # Generated reports
├── tests/                       # Test suite
└── scripts/                     # Helper scripts
```

## Example Output

From a real test audit (57 transactions, 3 files):

**Opportunity Found:** $33,314 (conservative)
- $5,814: Add call-out fees
- $2,500: Implement minimum job size
- $17,000: Target more industrial clients
- $8,000: Quote accurately at real rate

**Key Insight:**
> "You're already charging $147/hr effective rate but quoting $95/hr - there's a massive disconnect between your stated rate and what customers actually pay you."

**Cost:** $0.21 API fees

## Market Data (2026)

Updated benchmarks for Australian trades:

| Trade | Sydney | Melbourne | Brisbane |
|-------|--------|-----------|----------|
| Electrician | $115-165/hr | $110-155/hr | $105-150/hr |
| Plumber | $110-160/hr | $105-150/hr | $100-145/hr |
| Carpenter | $95-140/hr | $90-135/hr | $85-130/hr |
| HVAC | $120-170/hr | $115-165/hr | $110-155/hr |

Plus premiums for:
- Level 2 ASP: +25%
- Solar installation: +20%
- Emergency 24hr: +50%

## Cost Analysis

**Typical Audit:**
- Extraction: $0.10-0.25
- Analysis: $0.08-0.12
- **Total: $0.20-0.37**

**Revenue Model:**
- Charge: $797
- Cost: $0.20-0.37
- **Profit: $796.63+**
- **Margin: 99.9%**

**Monthly Volume:**
- 20 audits = $15,940 revenue, ~$6 cost
- 100 audits = $79,700 revenue, ~$30 cost

## Quality Principles

1. **Conservative Estimates**: Under-promise, over-deliver
2. **Show Evidence**: Reference their actual data (customer names, job amounts)
3. **Show Calculations**: Never just state numbers
4. **Realistic Assumptions**: Factor in customer loss, execution challenges
5. **Actionable**: Word-for-word scripts, specific next steps
6. **Honest**: Acknowledge risks and what could go wrong

## Development

### Run Tests

```bash
make test
```

### Lint Code

```bash
make lint
```

### Check Costs

```bash
make test
# Shows API costs at the end
```

## Tech Stack

- **AI**: Claude Sonnet 4 (Anthropic)
- **Web**: Streamlit
- **Payments**: Stripe
- **Data**: Pandas, OpenPyXL
- **PDF**: pdfplumber, PyPDF2
- **Reports**: Jinja2, HTML

## License

MIT

## Support

For questions or issues:
1. Check existing issues on GitHub
2. Create a new issue with details
3. Include sample data (anonymized) if possible

## Roadmap

- [ ] Add quote tracking system
- [ ] Implement follow-up audit (quarterly)
- [ ] Add benchmarking database (aggregate insights)
- [ ] Mobile-responsive reports
- [ ] WhatsApp/SMS notifications
- [ ] Integration with Xero/MYOB/QuickBooks

---

**Built for tradies, by someone who understands the business.**

Not just another AI tool - this is about helping hardworking tradies see what they're actually worth and get paid accordingly.
