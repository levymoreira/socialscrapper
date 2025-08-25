import asyncio
import json
import os
from datetime import datetime
from typing import List
import time

import litellm
from crawl4ai import (AsyncWebCrawler, BrowserConfig, CacheMode,
                      CrawlerRunConfig, LLMConfig, LLMExtractionStrategy)
from pydantic import BaseModel, Field

# Configure litellm to drop unsupported parameters for O-series models
litellm.drop_params = True

# IMPORTANT: Before running this script, launch Chrome with remote debugging enabled:
# /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-debug
# 
# Then navigate to LinkedIn and log in manually in that Chrome window.
# Once logged in, run this script to use the existing session.

# search results
URL_TO_SCRAPE = "https://www.linkedin.com/search/results/content/?keywords=vibe%20coding&origin=SWITCH_SEARCH_VERTICAL" 
INSTRUCTION_TO_LLM = f"Extract the posts data , post url, author url, and stats (date (fomat %Y-%m-%d), number of comments (social-actions__comments), number of social actions (social-actions__reaction-count), etc) into a JSON. Current date: {datetime.now().strftime('%Y-%m-%d')}"

# 1 post 
# URL_TO_SCRAPE = "https://www.linkedin.com/feed/update/urn:li:activity:7356282040301813761/"
# INSTRUCTION_TO_LLM = f"Extract the post data, post url, author url, and stats (date (fomat %Y-%m-%d), number of comments (social-actions__comments), number of social actions (social-actions__reaction-count), etc) into a JSON. Current date: {datetime.now().strftime('%Y-%m-%d')}"

class Product(BaseModel):
    name: str
    price: str


proxy_config = {
    "server": "http://mp.evomi.com:3000",
    "username": "levymoreir",
    "password": "TtZDmxDLkdQdH8zxHNau_country-IE_city-dublin",
}


async def main():

    # Azure OpenAI Configuration
    endpoint = "https://automapost-ai-foundry.cognitiveservices.azure.com/"
    model_name = "o3-mini"
    deployment = "o3-mini"
    api_version = "2024-12-01-preview"
    
    # Set Azure API version as environment variable
    os.environ['AZURE_API_VERSION'] = api_version
    
    llm_config = LLMConfig(
        provider="azure/o3-mini",
        api_token=os.getenv('AZURE_API_TOKEN'),
        base_url=f"{endpoint}openai/deployments/{deployment}",
        temperature=1.0,
        max_tokens=800
    )
    
    llm_strategy = LLMExtractionStrategy(
        llm_config=llm_config,
        schema=Product.model_json_schema(),
        extraction_type="schema",
        instruction=INSTRUCTION_TO_LLM,
        chunk_token_threshold=1000,
        overlap_rate=0.0,
        apply_chunking=True,
        input_format="markdown",
    )

    crawl_config = CrawlerRunConfig(
        extraction_strategy=llm_strategy,
        cache_mode=CacheMode.BYPASS,
        process_iframes=False,
        remove_overlay_elements=True,
        exclude_external_links=True,
    )

    browser_cfg = BrowserConfig(
        proxy_config=proxy_config,
        headless=False,
        viewport_width=1920,
        viewport_height=1080,
        use_managed_browser=True,
        browser_endpoint="ws://localhost:9222",  # Connect to existing Chrome instance
        extra_args=[
            "--disable-blink-features=AutomationControlled",
            "--disable-features=site-per-process",
            "--window-size=1920,1080"
        ]
    )

    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        print("Connected to existing Chrome session...")
        
        # Now scrape the target URL
        print(f"Scraping target URL: {URL_TO_SCRAPE}")
        result = await crawler.arun(
            url=URL_TO_SCRAPE, 
            config=CrawlerRunConfig(
                extraction_strategy=llm_strategy,
                cache_mode=CacheMode.BYPASS,
                process_iframes=False,
                remove_overlay_elements=True,
                exclude_external_links=True,
                wait_until="networkidle",
                wait_for=3000,  # Wait 3 seconds for content to load
                js_code="""
                // Scroll to load more content
                window.scrollTo(0, document.body.scrollHeight);
                await new Promise(r => setTimeout(r, 2000));
                """
            )
        )

        if result.success:
            data = json.loads(result.extracted_content)

            print("Extracted items:", data)

            llm_strategy.show_usage()
        else:
            print("Error:", result.error_message)


if __name__ == "__main__":
    asyncio.run(main())
