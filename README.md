# Fynd - Version 1
AI Enabled Evening Planner with a Restaurant focus

## Features

- Natural language processing of dining requests
- Structured analysis of user criteria (location, cuisine, ambiance, etc.)
- Integration with Yelp Fusion API and Google Places for restaurant data
- AI-driven explanation of how restaurants match user criteria
- Streaming and non-streaming API responses

## Project Structure

```
fynd.v1/
├── app/                      # Main application package
│   ├── models/               # Data models
│   │   ├── request_models.py # Request models
│   │   └── response_models.py# Response models
│   ├── services/             # Service modules
│   │   └── ai_client.py      # AI client interface and implementation
│   └── main.py               # FastAPI application
├── .env                      # Environment variables
├── server.py                 # Server entry point
└── requirements.txt          # Python dependencies
```

## Development Setup

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/fynd.git
cd fynd
```

2. **Set up a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Edit the `.env` file and add your Together.ai API key:

```
TOGETHER_API_KEY=your_together_ai_api_key_here
```

5. **Run the development server**

```bash
python server.py
```

The server will start at `http://localhost:8000`

## Model Testing

```bash
python test_api.py
```

## API Endpoints

### Health Check

```
GET /
```

Returns a simple status message to confirm the API is running.

### Process Query

```
POST /query
```

Body:
```json
{
  "query": "Find me a romantic Thai place in NYC that stays open past 11 p.m.",
  "stream": false
}
```

Returns a JSON response with the LLM's analysis.

### Stream Query

```
POST /query/stream
```

Same request body as above, but returns a streaming response using server-sent events.

## Future Development

This is phase 1 of the project, focusing on the backend AI integration. Future phases will include:
- Frontend development with React, Vite, and Tailwind
- Third-party API integration (Yelp, Google Places)
- Structured data processing
- Deployed containerization with Docker
