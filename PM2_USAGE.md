# PM2 Usage Guide for LinkedIn Scraper API

This guide shows you how to run your LinkedIn Scraper API in the background using PM2, similar to how you'd use PM2 with Node.js applications.

## Quick Start

### 1. Start the API
```bash
./start.sh
```

### 2. Check status
```bash
pm2 status
pm2 logs linkedin-api
```

### 3. Stop the API
```bash
./stop.sh
```

## PM2 Commands

### Basic Commands
```bash
# Start the API (using ecosystem config)
pm2 start ecosystem.config.js

# Start directly (alternative)
pm2 start api.py --name linkedin-api --interpreter python3

# Stop the API
pm2 stop linkedin-api

# Restart the API
pm2 restart linkedin-api

# Delete from PM2 (stops and removes)
pm2 delete linkedin-api

# Show all processes
pm2 list
pm2 status
```

### Monitoring & Logs
```bash
# View real-time logs
pm2 logs linkedin-api

# View last 100 log lines
pm2 logs linkedin-api --lines 100

# Clear logs
pm2 flush

# Monitor CPU/Memory usage
pm2 monit

# Show process details
pm2 show linkedin-api
```

### Auto-restart on System Reboot
```bash
# Generate startup script (run once)
pm2 startup

# Save current PM2 processes
pm2 save

# After this, your API will auto-start when the server reboots
```

## File Structure

```
socialscrapper/
├── ecosystem.config.js    # PM2 configuration
├── api.py                 # Main API script
├── api.sh                 # Enhanced startup script
├── start.sh               # Easy start script
├── stop.sh                # Easy stop script
├── restart.sh             # Easy restart script
└── logs/                  # Log files directory
    ├── err.log            # Error logs
    ├── out.log            # Output logs
    └── combined.log       # Combined logs
```

## Configuration Details

### Ecosystem Configuration (`ecosystem.config.js`)

- **Name**: `linkedin-api`
- **Interpreter**: `python3`
- **Auto-restart**: Enabled
- **Memory limit**: 1GB (restarts if exceeded)
- **Environment**: AZURE_API_TOKEN pre-configured
- **Logs**: Stored in `./logs/` directory with timestamps

### Environment Variables

The API requires:
- `AZURE_API_TOKEN`: Your Azure OpenAI API key (configured in ecosystem.config.js)

## Usage Examples

### Start and monitor
```bash
# Start
./start.sh

# Watch logs in real-time
pm2 logs linkedin-api --follow

# Check status
pm2 status
```

### Test the API
```bash
# Health check
curl http://localhost:8080/health

# Start scraping
curl -X POST "http://localhost:8080/api/linkedin/scrape" \
  -H "Content-Type: application/json" \
  -d '{"searches": ["python developer"]}'

# Get results (replace with actual task_id)
curl "http://localhost:8080/api/linkedin/results/YOUR-TASK-ID"
```

### Troubleshooting

#### API won't start
```bash
# Check PM2 status
pm2 status

# View error logs
pm2 logs linkedin-api --err

# Try manual start to see errors
./api.sh
```

#### Port already in use
```bash
# Stop all and restart
./stop.sh
./start.sh

# Or kill processes on port 8080
sudo lsof -ti:8080 | xargs kill -9
```

#### Memory issues
```bash
# Check memory usage
pm2 monit

# Restart to free memory
pm2 restart linkedin-api
```

## Alternative Methods

If PM2 is not available, the scripts will fallback to:

### Using Screen
```bash
# Start in screen session
screen -S linkedin-api
./api.sh
# Press Ctrl+A, then D to detach

# Reattach later
screen -r linkedin-api
```

### Using nohup
```bash
# Start in background
nohup ./api.sh > logs/api.log 2>&1 &

# Check if running
ps aux | grep api.py

# Stop
pkill -f api.py
```

## Best Practices

1. **Always check logs** when troubleshooting: `pm2 logs linkedin-api`
2. **Use the provided scripts** (`./start.sh`, `./stop.sh`) for consistency
3. **Set up auto-startup** for production: `pm2 startup && pm2 save`
4. **Monitor resource usage**: `pm2 monit`
5. **Regular restarts** for long-running processes: `pm2 restart linkedin-api`

## API Endpoints

Once running, your API will be available at:

- **Health Check**: http://localhost:8080/health
- **Scrape**: POST http://localhost:8080/api/linkedin/scrape  
- **Results**: GET http://localhost:8080/api/linkedin/results/{task_id}
- **Docs**: http://localhost:8080/docs (FastAPI auto-generated documentation)