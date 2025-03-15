import json
import time
import os
import requests
from flask import Flask
from dotenv import load_dotenv


app = Flask(__name__)
load_dotenv()

YELP_API_KEY = os.getenv('YELP_API_KEY')
YELP_SEARCH_URL = "https://api.yelp.com/v3/businesses/search"
OLLAMA_URL = "http://localhost:11434/api/generate"


@app.route('/hello')
def hello():
    return 'Hello, World! This is a Flask app.'

@app.route('/search')
def search():
    return 'Search page'

def parseQuery(user_query):
    prompt = f"""
    You are an AI that extracts search parameters from a user query.
    More specifically, you are given a user query that asks for a restaurant recommendation
    and you need to extract the location, cuisine, and open_until fields. 
    The user query: "{user_query}"
    your job is to ONLY return a JSON object with the following fields:
    {{
        "location": "<string>",
        "cuisine": "<string>",
        "open_until": "<string>"
    }}
    If any of the locationm cuisine or open_until fields are not found, use an empty string.
    Your response should be a valid JSON object with the required fields, do not return any explanation text or any code that produces the json in your response. 
    only return JSON, nothing else.
    for example, if the user query is "show me some italian restaurants in san francisco that are open until 10pm"
    your response should be:
    {{
        "location": "san francisco",
        "cuisine": "italian",
        "open_until": "2200"
    }}
    """

    response = requests.post(OLLAMA_URL, json=
                             {
                                 "model": "llama3.2",
                                 "prompt": prompt,
                                 "stream": False
                             })
    if response.status_code != 200:
        raise ValueError(f"Error from OLLAMA_URL: {response.status_code}, {response.text}")

    data = response.json()
    llm_json_str = data["response"]

    if not llm_json_str:
        raise ValueError("Empty response from OLLAMA_URL")

    return llm_json_str

def yelp_search(query):
    now = int(time.time())
    query["open-at"] = now+3600*4
    query["limit"] = 5
    response = requests.get(YELP_SEARCH_URL, params=query, headers = {
        "Authorization": f"Bearer {YELP_API_KEY}"
    })
    print(response.json())

if __name__ == "__main__":
    # app.run(debug=True)
    query = input("Enter your query: ")
    query = parseQuery(query)
    try:
        query = json.loads(query)  # Convert JSON string to dictionary
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON returned by parseQuery: {query}") from e
    yelp_search(query)