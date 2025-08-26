#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Stopping LinkedIn Scraper API...${NC}"

# Try PM2 first
if command -v pm2 &> /dev/null; then
    if pm2 list | grep -q "linkedin-api"; then
        pm2 stop linkedin-api
        pm2 delete linkedin-api
        echo -e "${GREEN}✓ API stopped successfully via PM2${NC}"
    else
        echo -e "${YELLOW}No PM2 process found for linkedin-api${NC}"
    fi
fi

# Also kill any direct Python processes running api.py
if pgrep -f "python3 api.py" > /dev/null; then
    pkill -f "python3 api.py"
    echo -e "${GREEN}✓ Stopped direct Python processes${NC}"
fi

# Check if any process is still using port 8080
if lsof -i:8080 > /dev/null 2>&1; then
    echo -e "${YELLOW}Port 8080 is still in use. Attempting to free it...${NC}"
    lsof -ti:8080 | xargs kill -9 2>/dev/null || true
    echo -e "${GREEN}✓ Port 8080 freed${NC}"
fi

echo -e "${GREEN}✓ LinkedIn Scraper API stopped${NC}"