#!/bin/bash

# Exit on error
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    log_error "Python3 is not installed!"
    exit 1
fi

# Set the Azure API token (you need to replace YOUR_API_TOKEN with your actual token)
export AZURE_API_TOKEN="7X36bPbHvy6muxdJvkCfxLXvaFNzKfp2Eg4NmPx15L2quvA3W1QYJQQJ99BHACYeBjFXJ3w3AAAAACOGVkXk"

# Create logs directory if it doesn't exist
mkdir -p logs

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    log_info "Activating venv virtual environment..."
    source venv/bin/activate
elif [ -d "env" ]; then
    log_info "Activating env virtual environment..."
    source env/bin/activate
elif [ -d ".venv" ]; then
    log_info "Activating .venv virtual environment..."
    source .venv/bin/activate
else
    log_warning "No virtual environment found, using system Python"
fi

# Check if required packages are installed
log_info "Checking dependencies..."
python3 -c "import fastapi" 2>/dev/null || {
    log_error "FastAPI is not installed. Please install requirements."
    exit 1
}

# Run the API script
log_info "Starting LinkedIn Scraper API on port 8080..."
log_info "API will be available at http://localhost:8080"
log_info "API documentation: http://localhost:8080/docs"

# Run with unbuffered output for real-time logs
export PYTHONUNBUFFERED=1
python3 api.py