#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Starting LinkedIn Scraper API with PM2...${NC}"

# Create logs directory if it doesn't exist
mkdir -p logs

# Check if PM2 is installed
if ! command -v pm2 &> /dev/null; then
    echo -e "${YELLOW}PM2 is not installed. Using alternative method...${NC}"
    echo "Starting with nohup instead..."
    nohup ./api.sh > logs/api.log 2>&1 &
    echo "API started in background. PID: $!"
    echo "Check logs at: logs/api.log"
    exit 0
fi

# Stop any existing instance
pm2 stop linkedin-api 2>/dev/null || true
pm2 delete linkedin-api 2>/dev/null || true

# Start with PM2 using ecosystem file
pm2 start ecosystem.config.js

# Show status
pm2 status linkedin-api

echo -e "${GREEN}✓ API started successfully!${NC}"
echo ""
echo "Useful PM2 commands:"
echo "  pm2 logs linkedin-api    - View real-time logs"
echo "  pm2 status               - Check API status"
echo "  pm2 restart linkedin-api - Restart the API"
echo "  pm2 stop linkedin-api    - Stop the API"
echo "  pm2 monit                - Monitor CPU/Memory usage"
echo ""
echo "API Endpoints:"
echo "  http://localhost:8080/api/linkedin/scrape  - POST endpoint"
echo "  http://localhost:8080/api/linkedin/results - GET results"
echo "  http://localhost:8080/docs                 - API documentation"