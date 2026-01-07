# Tradie Audit Agent - Makefile
# Common commands for development and deployment

.PHONY: setup install test run-test web audit clean help

# Default target
help:
	@echo "Tradie Audit Agent - Available commands:"
	@echo ""
	@echo "  make setup      - Full setup (create venv, install deps)"
	@echo "  make install    - Install dependencies only"
	@echo "  make test       - Run test audit with sample data"
	@echo "  make web        - Start the Streamlit web app"
	@echo "  make clean      - Remove temp files and cache"
	@echo ""
	@echo "To run a custom audit:"
	@echo "  python src/main.py --customer 'Name' --data ./data/folder"
	@echo ""

# Full setup
setup:
	@chmod +x scripts/*.sh
	@./scripts/setup.sh

# Install dependencies only
install:
	pip install -r requirements.txt

# Run test with sample data
test:
	@if [ ! -d "venv" ]; then echo "Run 'make setup' first"; exit 1; fi
	@source venv/bin/activate && python tests/test_sample_data.py

# Start web app
web:
	@chmod +x scripts/start_app.sh
	@./scripts/start_app.sh

# Run CLI audit (requires CUSTOMER and DATA vars)
audit:
ifndef CUSTOMER
	$(error CUSTOMER is not set. Use: make audit CUSTOMER="Name" DATA=./path/to/data)
endif
ifndef DATA
	$(error DATA is not set. Use: make audit CUSTOMER="Name" DATA=./path/to/data)
endif
	@source venv/bin/activate && python src/main.py --customer "$(CUSTOMER)" --data "$(DATA)"

# Clean up
clean:
	rm -rf __pycache__ src/__pycache__ src/**/__pycache__
	rm -rf .pytest_cache
	rm -rf temp/*
	find . -name "*.pyc" -delete
	find . -name ".DS_Store" -delete

# Remove all generated outputs
clean-outputs:
	rm -rf output/*

# Development: watch for changes
dev:
	@echo "Starting in development mode..."
	streamlit run src/app.py --server.runOnSave true

