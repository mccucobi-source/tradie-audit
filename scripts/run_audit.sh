#!/bin/bash
# Quick script to run an audit from command line

# Activate virtual environment if not already active
if [ -z "$VIRTUAL_ENV" ]; then
    if [ -d "venv" ]; then
        source venv/bin/activate
    else
        echo "❌ Virtual environment not found. Run scripts/setup.sh first."
        exit 1
    fi
fi

# Check for API key
if [ -z "$ANTHROPIC_API_KEY" ]; then
    if [ -f ".env" ]; then
        export $(grep -v '^#' .env | xargs)
    fi
fi

if [ -z "$ANTHROPIC_API_KEY" ] || [ "$ANTHROPIC_API_KEY" == "your_api_key_here" ]; then
    echo "❌ ANTHROPIC_API_KEY not set. Edit .env and add your key."
    exit 1
fi

# Run the audit
python src/main.py "$@"

