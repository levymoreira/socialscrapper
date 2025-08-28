#!/usr/bin/env python3
import requests
import json
import time

API_URL = "http://localhost:8080/api/linkedin"

def test_cache_functionality():
    # Test 1: Make first request - should create new task
    print("Test 1: First request with searches ['vibe coding']")
    response = requests.post(f"{API_URL}/scrape", json={"searches": ["vibe coding"]})
    data = response.json()
    print(f"Response: {data}")
    first_task_id = data["task_id"]
    
    # Wait a bit
    time.sleep(2)
    
    # Test 2: Make same request - should return cached result
    print("\nTest 2: Same request with searches ['vibe coding'] - should return cached")
    response = requests.post(f"{API_URL}/scrape", json={"searches": ["vibe coding"]})
    data = response.json()
    print(f"Response: {data}")
    cached_task_id = data["task_id"]
    
    # Verify cache is working (cached_task_id should start with first_task_id)
    if data["status"] == "cached" and (cached_task_id == first_task_id or first_task_id.startswith(cached_task_id)):
        print("✓ Cache working correctly - cached result returned")
    else:
        print("✗ Cache not working - different task_id or status")
    
    # Test 3: Get results by task_id
    print(f"\nTest 3: Getting results for task_id: {first_task_id}")
    response = requests.get(f"{API_URL}/results/{first_task_id}")
    if response.status_code == 200:
        print("✓ Results retrieved successfully")
    else:
        print(f"✗ Failed to retrieve results: {response.status_code}")
    
    # Test 4: Different searches - should create new task
    print("\nTest 4: Different searches ['python developer'] - should create new task")
    response = requests.post(f"{API_URL}/scrape", json={"searches": ["python developer"]})
    data = response.json()
    print(f"Response: {data}")
    if data["status"] == "started":
        print("✓ New task created for different searches")
    else:
        print("✗ Unexpected status for new searches")

if __name__ == "__main__":
    test_cache_functionality()