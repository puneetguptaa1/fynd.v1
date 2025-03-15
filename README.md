# Fynd - Version 1
AI Enabled Evening Planner with a Restaurant focus

## Prerequisites
- [Ollama](https://ollama.ai/) must be installed and running locally on port `11434` (Port Currently hardcoded Oopsies).
  - Download and install Ollama from [here](https://ollama.ai/).
  - I am using llama3.2 3b (2gb)
  - Start the Ollama server by running:
    ```
    ollama serve
    ```
- Yelp Search API key which should be free for the first month (5000 calls)

## Next Steps
- As of 03/14/2025:
    - Review Yelp's Search API documentation (https://docs.developer.yelp.com/reference/v3_business_search) and update the LLM-based parameter parsing to align with Yelp's predefined parameters.