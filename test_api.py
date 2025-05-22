"""
Test script for the Fynd API.
"""
import requests
import json
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
BASE_URL = f"http://{os.getenv('HOST', '0.0.0.0')}:{os.getenv('PORT', '8000')}"

def test_health_check():
    """Test the health check endpoint."""
    response = requests.get(f"{BASE_URL}/")
    print(f"Health check status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)

def test_query_endpoint():
    """Test the regular query endpoint."""
    data = {
        "query": "Find me a romantic Italian place in NYC that stays open past 11 p.m.",
        "stream": False
    }
    
    start_time = time.time()
    response = requests.post(f"{BASE_URL}/query", json=data)
    end_time = time.time()
    
    print(f"Query endpoint status: {response.status_code}")
    print(f"Time taken: {end_time - start_time:.2f} seconds")
    
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Error: {response.text}")
    print("-" * 50)

def test_streaming_endpoint():
    """Test the streaming query endpoint."""
    data = {
        "query": "Find me a casual Mexican restaurant in San Francisco with good margaritas.",
        "stream": True
    }
    
    print("Streaming response:")
    start_time = time.time()
    with requests.post(f"{BASE_URL}/query/stream", json=data, stream=True) as response:
        if response.status_code == 200:
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith("data: ") and not line.endswith("[DONE]"):
                        chunk = line[6:]  # Remove "data: " prefix
                        print(chunk, end="", flush=True)
        else:
            print(f"Error: {response.text}")
    
    end_time = time.time()
    print(f"\nTime taken: {end_time - start_time:.2f} seconds")
    print("-" * 50)

if __name__ == "__main__":
    print("Testing Fynd API...")
    test_health_check()
    
    choice = input("Test regular query endpoint? (y/n): ")
    if choice.lower() == 'y':
        test_query_endpoint()
    
    choice = input("Test streaming endpoint? (y/n): ")
    if choice.lower() == 'y':
        test_streaming_endpoint() 