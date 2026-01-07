# Tradie Audit Agent - Quick Start Guide

Get your automated audit system running in 5 minutes.

## 1. Setup (One Time)

```bash
# Clone or download this project
cd audit-agent

# Run setup script
chmod +x scripts/setup.sh
./scripts/setup.sh

# Or use make
make setup
```

## 2. Add Your API Key

Edit the `.env` file and add your Anthropic API key:

```bash
# Get your key from: https://console.anthropic.com/
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx
```

## 3. Run a Test

```bash
# Activate virtual environment
source venv/bin/activate

# Run test with sample data
python tests/test_sample_data.py

# Or use make
make test
```

Expected output:
```
✓ Created sample data
✓ Extracted 50 transactions
✓ Revenue: $65,000
✓ Opportunity found: $28,500
✓ Meets $10k guarantee: Yes
```

## 4. Run Your First Real Audit

### Option A: Command Line

```bash
# Put customer files in a folder
mkdir -p data/johns_electrical
# Copy their invoices, expenses, quotes into the folder

# Run the audit
python src/main.py \
  --customer "John's Electrical" \
  --data ./data/johns_electrical \
  --trade electrician \
  --location Sydney \
  --rate 95 \
  --hours 50
```

### Option B: Web Interface

```bash
# Start the web app
streamlit run src/app.py

# Or use make
make web
```

Open http://localhost:8501 in your browser.

## 5. Review Output

Reports are saved to `./output/[customer_name]_[timestamp]/`:
- `profit_leak_audit_report.html` - Beautiful PDF-ready report
- `profit_leak_audit_workbook.xlsx` - Excel with calculators
- `analysis_data.json` - Raw data for customization

## Cost Per Audit

- **Claude API:** ~$8-15 (depends on document volume)
- **Your Time:** 15-30 minutes to review
- **Margin:** $780+ on $797 price

## Common Issues

### "ANTHROPIC_API_KEY not set"
```bash
# Check your .env file
cat .env

# Make sure it's loaded
source .env
echo $ANTHROPIC_API_KEY
```

### "Module not found"
```bash
# Make sure venv is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### PDF extraction fails
```bash
# Install system dependencies for PDF processing
# macOS:
brew install poppler

# Ubuntu:
sudo apt-get install poppler-utils
```

## Next Steps

1. **Run 3-5 audits manually** - Get a feel for the process
2. **Refine prompts** - Adjust `src/templates/prompts.py` based on results
3. **Build benchmark database** - Each audit adds to your market data
4. **Scale up** - Once confident, increase marketing

## File Structure

```
audit-agent/
├── src/
│   ├── agents/           # The AI agents
│   │   ├── data_extractor.py   # Reads documents
│   │   ├── analyzer.py          # Finds opportunities
│   │   └── report_generator.py  # Creates reports
│   ├── templates/        # Claude prompts
│   ├── utils/            # Helpers
│   ├── app.py            # Web interface
│   └── main.py           # CLI interface
├── data/                 # Customer documents go here
├── output/               # Reports saved here
├── tests/                # Test files
└── scripts/              # Setup/run scripts
```

## Support

Questions? Issues? 
- Check the `AUTOMATION_PLAN.md` for detailed architecture
- Review prompts in `src/templates/prompts.py`
- Test with sample data first before real audits

