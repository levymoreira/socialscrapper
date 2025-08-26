# LinkedIn Scraper API

A FastAPI-based LinkedIn scraper that performs dual searches (relevance + date-sorted) for comprehensive data collection. Runs as a background service using PM2 for production reliability.

## 🚀 Features

- **Dual Search Strategy**: Each keyword searched with both relevance and date-posted sorting
- **Background Processing**: Async task processing with immediate UUID response
- **Session Persistence**: Browser session stays open for efficiency  
- **Auto-restart**: PM2 handles crashes and memory limits
- **Comprehensive Logging**: Timestamped logs for debugging
- **LLM-Powered Extraction**: Uses Azure OpenAI O3-mini model to intelligently extract structured data
- **LinkedIn Integration**: Uses existing Chrome profile with LinkedIn login

## 📋 Requirements

- Python 3.10+
- Node.js (for PM2)
- Chrome browser with LinkedIn logged in
- Azure OpenAI API key

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd socialscrapper
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment**
   - Your Azure API token is pre-configured in `ecosystem.config.js`
   - Make sure Chrome has LinkedIn logged in

4. **Make scripts executable**
   ```bash
   chmod +x *.sh
   ```

## 🚀 Quick Start

### 1. Start the API
```bash
./start.sh
```

### 2. Check if it's running
```bash
pm2 status
```

### 3. View logs
```bash
pm2 logs linkedin-api
```

### 4. Stop the API
```bash
./stop.sh
```

## 🏃‍♂️ Running the API

### Simple Method (Recommended)
```bash
# Start
./start.sh

# Stop  
./stop.sh

# Restart
./restart.sh
```

### PM2 Commands

#### Basic Operations
```bash
# Start with PM2
pm2 start ecosystem.config.js

# View all processes
pm2 list
pm2 status

# Stop the API
pm2 stop linkedin-api

# Restart without downtime
pm2 restart linkedin-api

# Delete from PM2
pm2 delete linkedin-api
```

#### Monitoring & Debugging
```bash
# Real-time logs
pm2 logs linkedin-api

# Last 100 lines
pm2 logs linkedin-api --lines 100

# Monitor CPU/Memory
pm2 monit

# Process details
pm2 show linkedin-api

# Clear all logs
pm2 flush
```

#### Auto-startup on Reboot
```bash
# Generate startup script (run once)
pm2 startup

# Save current processes
pm2 save

# Now API will auto-start on server restart
```

## 📡 API Usage

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/linkedin/scrape` | Start scraping task |
| GET | `/api/linkedin/results/{task_id}` | Get results |
| GET | `/health` | Health check |
| GET | `/docs` | API documentation |

### Example Usage

**1. Start a scraping task:**
```bash
curl -X POST "http://localhost:8080/api/linkedin/scrape" \
  -H "Content-Type: application/json" \
  -d '{
    "searches": ["python developer", "machine learning", "data scientist"]
  }'
```

**Response:**
```json
{
  "task_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "started", 
  "message": "Scraping task started for 3 searches..."
}
```

**2. Check results:**
```bash
curl "http://localhost:8080/api/linkedin/results/123e4567-e89b-12d3-a456-426614174000"
```

**3. Health check:**
```bash
curl http://localhost:8080/health
```

## 📊 Data Structure

Each scraped post contains:

```json
{
  "author_name": "John Doe",
  "author_url": "https://linkedin.com/in/johndoe", 
  "post_text": "Great insights on Python development...",
  "post_url": "https://linkedin.com/posts/...",
  "post_date": "2025-01-15",
  "likes_count": "42",
  "comments_count": "7", 
  "shares_count": "3",
  "sort_type": "default" // or "date_posted"
}
```

## 🔧 Configuration

### Environment Variables
- `AZURE_API_TOKEN` - Pre-configured in ecosystem.config.js
- `PYTHONUNBUFFERED=1` - For real-time logs

### PM2 Configuration (`ecosystem.config.js`)
- **Memory limit**: 1GB (auto-restart if exceeded)
- **Auto-restart**: On crashes and errors
- **Logging**: Timestamped logs in `./logs/` directory
- **Graceful shutdown**: 3-second timeout

## 📁 Project Structure

```
socialscrapper/
├── api.py                 # Main FastAPI application
├── ecosystem.config.js    # PM2 configuration  
├── api.sh                 # Enhanced startup script
├── start.sh               # Easy start command
├── stop.sh                # Easy stop command
├── restart.sh             # Easy restart command
├── api.md                 # API documentation
├── PM2_USAGE.md          # Detailed PM2 guide
├── logs/                  # Log files (created automatically)
│   ├── err.log           # Error logs
│   ├── out.log           # Output logs  
│   └── combined.log      # Combined logs
└── results/              # Scraped data (gitignored)
```

## 🐛 Troubleshooting

### API Won't Start
```bash
# Check PM2 status
pm2 status

# View error logs
pm2 logs linkedin-api --err

# Try manual start to debug
./api.sh
```

### Port Already in Use
```bash
# Stop everything and restart
./stop.sh
./start.sh

# Or manually kill port 8080 processes
sudo lsof -ti:8080 | xargs kill -9
```

### High Memory Usage
```bash
# Monitor usage
pm2 monit

# Restart to free memory
pm2 restart linkedin-api
```

### Chrome/LinkedIn Issues
- Ensure Chrome has LinkedIn logged in
- Check Chrome profile path in `api.py`
- Verify Chrome browser is accessible

## 📈 Features

- **Dual Search Strategy**: Each keyword searched with both relevance and date-posted sorting
- **Background Processing**: Async task processing with immediate UUID response
- **Session Persistence**: Browser session stays open for efficiency  
- **Auto-restart**: PM2 handles crashes and memory limits
- **Comprehensive Logging**: Timestamped logs for debugging
- **Graceful Shutdown**: Clean process termination
- **Health Monitoring**: Built-in health check endpoint

## 🔗 Useful Links

- **API Docs**: http://localhost:8080/docs (when running)
- **Health Check**: http://localhost:8080/health
- **PM2 Documentation**: https://pm2.keymetrics.io/docs/

## 📝 Notes

- Results are stored as JSON files in `results/` directory
- Browser session uses existing Chrome profile with LinkedIn login
- Each search generates 2 LinkedIn URLs (default + date-sorted)
- Processing time varies based on search complexity
- Port 8080 is used by default

---

*Generated with PM2 process management for production reliability*
