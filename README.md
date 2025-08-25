# Scraper on Steroids

An advanced web scraper built with Crawl4AI that can extract structured data from web pages using LLM-powered extraction strategies.

## Features

- **LLM-Powered Extraction**: Uses OpenAI's O3-mini model to intelligently extract structured data
- **Proxy Support**: Built-in proxy configuration for reliable scraping
- **LinkedIn Scraping**: Specifically configured to scrape LinkedIn posts and extract post details
- **Async Architecture**: Built with Python asyncio for high performance
- **Browser Automation**: Uses Playwright for robust web automation

## Prerequisites

- Python 3.8 or higher
- Git (for cloning the repository)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd scraper-on-steroids
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install crawl4ai pydantic litellm
```

### 4. Install Playwright Browsers
```bash
playwright install
```

This will download the necessary browser binaries (Chromium, Firefox, Webkit) required for web scraping.

### 5. Configure API Credentials

The script is currently configured to use OpenAI's O3-mini model through Azure AI. You'll need to:

1. Set up your OpenAI API credentials
2. Update the API token and base URL in `scraper-on-steroids/main.py`:

```python
llm_config = LLMConfig(
    provider="openai/o3-mini",
    api_token="YOUR_API_TOKEN_HERE",
    base_url="YOUR_API_BASE_URL_HERE",
    temperature=1.0,
    max_tokens=800
)
```

### 6. Configure Proxy (Optional)

If you need proxy support, update the proxy configuration in `main.py`:

```python
proxy_config = {
    "server": "http://your-proxy-server:port",
    "username": "your-username",
    "password": "your-password",
}
```

## Running the Scraper

### Activate Virtual Environment
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Run the Script
```bash
python main.py
```

## Configuration

### Target URL
Change the URL to scrape by modifying the `URL_TO_SCRAPE` variable:

```python
URL_TO_SCRAPE = "https://your-target-url.com"
```

### Extraction Instructions
Customize what data to extract by modifying the `INSTRUCTION_TO_LLM` variable:

```python
INSTRUCTION_TO_LLM = "Extract specific data you want from the page"
```

### Data Schema
Define the expected output structure by modifying the `Product` class:

```python
class Product(BaseModel):
    field1: str
    field2: str
    # Add more fields as needed
```

## Project Structure

```
scraper-on-steroids/
├── scraper-on-steroids/
│   └── main.py              # Main scraper script
├── simple-scraper/          # Alternative TypeScript scraper
│   ├── src/
│   │   ├── index.ts
│   │   └── scraper.ts
│   └── package.json
├── venv/                    # Python virtual environment
├── README.md               # This file
└── requirements.txt        # Python dependencies (if created)
```

## Dependencies

### Python Packages
- **crawl4ai**: Advanced web crawling and extraction framework
- **pydantic**: Data validation and serialization
- **litellm**: LLM provider abstraction layer
- **playwright**: Browser automation (automatically installed with crawl4ai)
- **aiohttp**: Async HTTP client
- **beautifulsoup4**: HTML parsing
- **lxml**: XML/HTML processing

### System Requirements
- **Playwright Browsers**: Chromium, Firefox, Webkit (installed via `playwright install`)
- **Python 3.8+**: Required for asyncio and modern Python features

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Make sure you've activated the virtual environment and installed all dependencies
2. **Playwright browsers not found**: Run `playwright install` to download browser binaries
3. **API errors**: Check your API credentials and model configuration
4. **Proxy errors**: Verify proxy settings and credentials
5. **Permission errors**: Ensure you have proper permissions to install packages

### Debug Mode
To enable debug logging for LiteLLM:
```python
import litellm
litellm._turn_on_debug()
```

### Alternative Models
If O3-mini doesn't work, try other models:
```python
# OpenAI GPT models
provider="openai/gpt-4o"
provider="openai/gpt-3.5-turbo"

# Local models (requires Ollama)
provider="ollama/llama2"
```

## Notes

- The scraper respects robots.txt and implements rate limiting
- Some websites may require specific headers or authentication
- LinkedIn scraping may require session cookies for full access
- Always comply with website terms of service and legal requirements

## Support

For issues and questions:
1. Check the Crawl4AI documentation: [Crawl4AI Docs](https://crawl4ai.com)
2. Review Playwright documentation: [Playwright Docs](https://playwright.dev)
3. Check LiteLLM documentation: [LiteLLM Docs](https://docs.litellm.ai)
