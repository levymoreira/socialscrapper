# LinkedIn Scraper API Documentation

## Overview

The LinkedIn Scraper API allows you to scrape LinkedIn search results for multiple keywords asynchronously. The API returns results immediately with a task ID, while the scraping continues in the background.

**Base URL**: `http://localhost:8080`

## Authentication

Make sure the `AZURE_API_TOKEN` environment variable is set with your Azure OpenAI API key before starting the server.

## Endpoints

### 1. Start Scraping Task

**POST** `/scrape`

Initiates a LinkedIn scraping task for the provided search keywords.

#### Request Body

```json
{
  "searches": ["search keyword 1", "search keyword 2", "..."]
}
```

#### Parameters

- `searches` (array, required): Array of search keywords to scrape from LinkedIn

#### Response

```json
{
  "task_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "started",
  "message": "Scraping task started for 2 searches. Use the task_id to check results."
}
```

#### Example Request

```bash
curl -X POST "http://localhost:8080/scrape" \
  -H "Content-Type: application/json" \
  -d '{
    "searches": ["vibe coding", "python developer", "machine learning"]
  }'
```

### 2. Get Results

**GET** `/results/{task_id}`

Retrieves the results of a scraping task using the task ID.

#### Parameters

- `task_id` (string, required): The task ID returned from the POST request

#### Response

**Success (200)**:
```json
{
  "task_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "completed",
  "searches": ["vibe coding", "python developer"],
  "results": [
    {
      "search_keyword": "vibe coding",
      "data": [
        {
          "author_name": "John Doe",
          "author_url": "https://linkedin.com/in/johndoe",
          "post_text": "Great insights on vibe coding...",
          "post_url": "https://linkedin.com/posts/...",
          "post_date": "2025-01-15",
          "likes_count": "42",
          "comments_count": "7",
          "shares_count": "3"
        }
      ],
      "scraped_at": "2025-01-15T10:30:00"
    }
  ],
  "error": null,
  "completed_at": "2025-01-15T10:35:00"
}
```

**Not Found (404)**:
```json
{
  "detail": "Task not found or not completed yet"
}
```

**Processing Status**:
```json
{
  "task_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "processing",
  "searches": ["vibe coding", "python developer"],
  "results": [],
  "error": null,
  "completed_at": null
}
```

#### Example Request

```bash
curl "http://localhost:8080/results/123e4567-e89b-12d3-a456-426614174000"
```

### 3. Health Check

**GET** `/health`

Check if the API is running.

#### Response

```json
{
  "status": "healthy",
  "timestamp": "2025-01-15T10:30:00"
}
```

## Status Values

- `started`: Task has been initiated
- `processing`: Task is currently running
- `completed`: Task has finished successfully
- `error`: Task encountered an error

## Error Handling

### HTTP Status Codes

- `200`: Success
- `400`: Bad Request (invalid input)
- `404`: Task not found or not completed
- `500`: Internal Server Error

### Error Response Format

```json
{
  "detail": "Error description"
}
```

## Data Structure

### LinkedIn Post Schema

Each scraped post contains the following fields:

```json
{
  "author_name": "string",
  "author_url": "string", 
  "post_text": "string",
  "post_url": "string",
  "post_date": "string (YYYY-MM-DD)",
  "likes_count": "string",
  "comments_count": "string",
  "shares_count": "string"
}
```

## Usage Workflow

1. **Start Task**: Send a POST request to `/scrape` with your search keywords
2. **Get Task ID**: Save the `task_id` from the response
3. **Poll for Results**: Periodically call GET `/results/{task_id}` to check if processing is complete
4. **Process Results**: Once `status` is `completed`, process the scraped data

## Example Python Client

```python
import requests
import time
import json

# Start scraping
response = requests.post('http://localhost:8080/scrape', json={
    'searches': ['python developer', 'machine learning engineer']
})

task_id = response.json()['task_id']
print(f"Task started with ID: {task_id}")

# Poll for results
while True:
    result = requests.get(f'http://localhost:8080/results/{task_id}')
    
    if result.status_code == 404:
        print("Task still processing...")
        time.sleep(5)
        continue
    
    data = result.json()
    
    if data['status'] == 'completed':
        print("Task completed!")
        print(json.dumps(data, indent=2))
        break
    elif data['status'] == 'error':
        print(f"Task failed: {data.get('error')}")
        break
    else:
        print(f"Status: {data['status']}")
        time.sleep(5)
```

## Running the Server

```bash
# Set environment variable
export AZURE_API_TOKEN="your-azure-api-key"

# Start the server
python api.py

# Or using uvicorn directly
uvicorn api:app --host 0.0.0.0 --port 8080
```

The server will be available at `http://localhost:8080`

## Notes

- Results are stored as JSON files in the `results/` directory
- The API uses your existing Chrome profile with LinkedIn login
- Each search keyword generates a separate LinkedIn search URL
- Processing time varies based on the number of searches and LinkedIn's response time
- Make sure LinkedIn is already logged in your Chrome profile before starting the API