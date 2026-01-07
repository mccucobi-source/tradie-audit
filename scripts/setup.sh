#!/bin/bash
# Setup script for Tradie Audit Agent

set -e

echo "🔧 Setting up Tradie Audit Agent..."

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "   Python version: $PYTHON_VERSION"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "   Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "   Upgrading pip..."
pip install --upgrade pip --quiet

# Install dependencies
echo "   Installing dependencies..."
pip install -r requirements.txt --quiet

# Create directories
echo "   Creating directories..."
mkdir -p data output temp

# Check for .env file
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  No .env file found!"
    echo "   Creating from template..."
    
    # Create .env with placeholder
    cat > .env << EOF
# Anthropic API Key (required)
# Get from: https://console.anthropic.com/
ANTHROPIC_API_KEY=your_api_key_here

# Model configuration
ANTHROPIC_MODEL=claude-sonnet-4-20250514
MAX_TOKENS=4096

# Cost limits (safety)
MAX_COST_PER_AUDIT=20.00

# Application settings
OUTPUT_DIR=./output
DATA_DIR=./data
TEMP_DIR=./temp
EOF
    
    echo "   ✓ Created .env file"
    echo ""
    echo "🔑 IMPORTANT: Edit .env and add your ANTHROPIC_API_KEY"
    echo "   Get your key from: https://console.anthropic.com/"
else
    echo "   ✓ .env file exists"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Add your ANTHROPIC_API_KEY to .env"
echo "  2. Activate the virtual environment: source venv/bin/activate"
echo "  3. Run a test: python tests/test_sample_data.py"
echo "  4. Or start the web app: streamlit run src/app.py"
echo ""

