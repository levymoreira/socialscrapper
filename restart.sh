#!/bin/bash

# Colors for output
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${YELLOW}Restarting LinkedIn Scraper API...${NC}"

# Stop the API
./stop.sh

# Wait a moment
sleep 2

# Start the API
./start.sh

echo -e "${GREEN}✓ API restarted successfully!${NC}"