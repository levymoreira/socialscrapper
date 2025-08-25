import asyncio
import json
import os
import uuid
from datetime import datetime
from typing import List
import time
from pathlib import Path

import litellm
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from crawl4ai import (AsyncWebCrawler, BrowserConfig, CacheMode,
                      CrawlerRunConfig, LLMConfig, LLMExtractionStrategy)

# Configure litellm to drop unsupported parameters for O-series models
litellm.drop_params = True

app = FastAPI(title="LinkedIn Scraper API", description="API for scraping LinkedIn content", version="1.0.0")

# Create results directory if it doesn't exist
RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)

class LinkedInPost(BaseModel):
    author_name: str = Field(description="Name of the post author")
    author_url: str = Field(description="LinkedIn profile URL of the author") 
    post_text: str = Field(description="Main text content of the post")
    post_url: str = Field(description="URL to the specific LinkedIn post")
    post_date: str = Field(description="Date when the post was published")
    likes_count: str = Field(description="Number of likes/reactions", default="0")
    comments_count: str = Field(description="Number of comments", default="0")
    shares_count: str = Field(description="Number of shares", default="0")

class SearchRequest(BaseModel):
    searches: List[str] = Field(description="Array of search keywords to scrape from LinkedIn")

class SearchResponse(BaseModel):
    task_id: str = Field(description="Unique identifier for the scraping task")
    status: str = Field(description="Status of the request")
    message: str = Field(description="Human readable message")

class SearchResult(BaseModel):
    task_id: str
    status: str
    searches: List[str]
    results: List[dict] = Field(default_factory=list)
    error: str = None
    completed_at: str = None

proxy_config = {
    "server": "mp.evomi.com:3000",
    "username": "levymoreir",
    "password": "TtZDmxDLkdQdH8zxHNau_country-IE_city-dublin",
}

async def scrape_linkedin_search(search_keyword: str) -> List[dict]:
    """Scrape LinkedIn for a single search keyword with both default and date-sorted results"""
    
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
    
    browser_cfg = BrowserConfig(
        # proxy_config=proxy_config,  # Disabled temporarily to test basic functionality
        headless=False,  # Keep as False but will run headless due to server environment
        viewport_width=1920,
        viewport_height=1080,
        use_managed_browser=True,  # Use crawl4ai's managed browser
        browser_type="chromium",
        user_data_dir="/home/azureuser/.config/google-chrome",  # Use existing profile
        extra_args=[
            "--disable-blink-features=AutomationControlled",
            "--disable-features=site-per-process",
            "--window-size=1920,1080",
            "--no-sandbox",  # Required for server environments
            "--disable-dev-shm-usage",  # Overcome limited resource problems
            "--disable-gpu",  # Disable GPU acceleration in server environment
        ],
        debugging_port=9222  # Enable remote debugging
    )

    all_results = []
    
    # Keep browser session open for both searches
    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        # Define search configurations
        search_configs = [
            {
                "sort": "default",
                "url": f"https://www.linkedin.com/search/results/content/?keywords={search_keyword.replace(' ', '%20')}&origin=SWITCH_SEARCH_VERTICAL"
            },
            {
                "sort": "date_posted", 
                "url": f"https://www.linkedin.com/search/results/content/?keywords={search_keyword.replace(' ', '%20')}&origin=SWITCH_SEARCH_VERTICAL&sortBy=%22date_posted%22"
            }
        ]
        
        for config in search_configs:
            print(f"Scraping search: {search_keyword} (sort: {config['sort']})")
            print(f"URL: {config['url']}")
            
            instruction = f"Extract any visible LinkedIn posts or articles from this page. Include author names, titles, and any engagement metrics you can find. Search keyword: {search_keyword}. Sort: {config['sort']}. Current date: {datetime.now().strftime('%Y-%m-%d')}"
            
            llm_strategy = LLMExtractionStrategy(
                llm_config=llm_config,
                schema=LinkedInPost.model_json_schema(),
                extraction_type="schema",
                instruction=instruction,
                chunk_token_threshold=1000,
                overlap_rate=0.0,
                apply_chunking=True,
                input_format="markdown",
            )
            
            result = await crawler.arun(
                url=config['url'], 
                config=CrawlerRunConfig(
                    extraction_strategy=llm_strategy,
                    cache_mode=CacheMode.BYPASS,
                    process_iframes=False,
                    remove_overlay_elements=True,
                    exclude_external_links=True,
                    wait_until="networkidle",
                    js_code="""
                    // Check if user is logged in and click on user account if needed
                    const userButton = document.querySelector('button[data-ember-action*="selectUser"]') || 
                                     document.querySelector('.account-switcher__user') ||
                                     document.querySelector('[data-test="account-switcher-button"]') ||
                                     document.querySelector('.global-nav__me-button');
                    
                    if (userButton && !document.querySelector('.global-nav__me-photo')) {
                        console.log('Clicking on user account selector...');
                        userButton.click();
                        await new Promise(r => setTimeout(r, 2000));
                        
                        // Look for user profiles in dropdown and click the first one
                        const userProfile = document.querySelector('[data-test="account-switcher-user-item"]') ||
                                          document.querySelector('.account-switcher__item') ||
                                          document.querySelector('[role="menuitem"]');
                        
                        if (userProfile) {
                            console.log('Clicking on user profile...');
                            userProfile.click();
                            await new Promise(r => setTimeout(r, 3000));
                        }
                    }
                    
                    // Wait a bit more if we're still on login/signin page
                    if (window.location.href.includes('/login') || window.location.href.includes('/signin')) {
                        console.log('Still on login page, waiting for redirect...');
                        await new Promise(r => setTimeout(r, 5000));
                    }
                    
                    // Scroll to load more content - first scroll
                    window.scrollTo(0, document.body.scrollHeight);
                    await new Promise(r => setTimeout(r, 1000));
                    
                    // Second scroll to load even more content
                    window.scrollTo(0, document.body.scrollHeight);
                    await new Promise(r => setTimeout(r, 1000));
                    """
                )
            )

            if result.success:
                try:
                    data = json.loads(result.extracted_content)
                    results = data if isinstance(data, list) else [data]
                    # Add sort type to each result
                    for item in results:
                        item['sort_type'] = config['sort']
                    all_results.extend(results)
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON for search '{search_keyword}' (sort: {config['sort']}): {e}")
                    all_results.append({
                        "error": f"JSON parsing error: {str(e)}", 
                        "search_keyword": search_keyword,
                        "sort_type": config['sort']
                    })
            else:
                print(f"Error scraping '{search_keyword}' (sort: {config['sort']}): {result.error_message}")
                all_results.append({
                    "error": result.error_message, 
                    "search_keyword": search_keyword,
                    "sort_type": config['sort']
                })
    
    return all_results

async def process_searches(task_id: str, searches: List[str]):
    """Background task to process all searches and save results to file"""
    result_file = RESULTS_DIR / f"{task_id}.json"
    
    # Initialize result structure
    search_result = SearchResult(
        task_id=task_id,
        status="processing",
        searches=searches,
        results=[]
    )
    
    try:
        # Save initial status
        with open(result_file, 'w') as f:
            json.dump(search_result.model_dump(), f, indent=2)
        
        all_results = []
        
        # Process each search
        for search_keyword in searches:
            try:
                search_data = await scrape_linkedin_search(search_keyword)
                all_results.extend([{
                    "search_keyword": search_keyword,
                    "data": search_data,
                    "scraped_at": datetime.now().isoformat()
                }])
            except Exception as e:
                print(f"Error processing search '{search_keyword}': {e}")
                all_results.append({
                    "search_keyword": search_keyword,
                    "error": str(e),
                    "scraped_at": datetime.now().isoformat()
                })
        
        # Update final result
        search_result.status = "completed"
        search_result.results = all_results
        search_result.completed_at = datetime.now().isoformat()
        
        # Save final result
        with open(result_file, 'w') as f:
            json.dump(search_result.model_dump(), f, indent=2)
            
        print(f"Task {task_id} completed successfully")
        
    except Exception as e:
        print(f"Error in background task {task_id}: {e}")
        search_result.status = "error"
        search_result.error = str(e)
        
        # Save error result
        with open(result_file, 'w') as f:
            json.dump(search_result.model_dump(), f, indent=2)

@app.post("/scrape", response_model=SearchResponse)
async def start_scraping(request: SearchRequest, background_tasks: BackgroundTasks):
    """
    Start a LinkedIn scraping task for multiple search keywords.
    Returns immediately with a task ID while processing continues in the background.
    """
    if not request.searches:
        raise HTTPException(status_code=400, detail="At least one search keyword is required")
    
    # Generate unique task ID
    task_id = str(uuid.uuid4())
    
    # Start background processing
    background_tasks.add_task(process_searches, task_id, request.searches)
    
    return SearchResponse(
        task_id=task_id,
        status="started",
        message=f"Scraping task started for {len(request.searches)} searches. Use the task_id to check results."
    )

@app.get("/results/{task_id}")
async def get_results(task_id: str):
    """
    Get the results of a scraping task by task ID.
    Returns 404 if the task doesn't exist or hasn't completed yet.
    """
    result_file = RESULTS_DIR / f"{task_id}.json"
    
    if not result_file.exists():
        raise HTTPException(status_code=404, detail="Task not found or not completed yet")
    
    try:
        with open(result_file, 'r') as f:
            result_data = json.load(f)
        return result_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading results: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
