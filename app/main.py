from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from dotenv import load_dotenv

from app.models.request_models import QueryRequest
from app.models.response_models import QueryResponse
from app.services.ai_client import get_ai_client

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Fynd - AI-assisted Dining Recommendations",
    description="An API for AI-assisted dining recommendations",
    version="0.1.0"
)

# Add CORS middleware to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI client
ai_client = get_ai_client()

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "Fynd API is running"}

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """Process a dining query and return LLM response."""
    try:
        # Simple pass-through to LLM for now
        prompt = f"User query: {request.query}"
        response = ai_client.generate_response(prompt, stream=request.stream)
        
        return QueryResponse(response=response)
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.post("/query/stream")
async def stream_query(request: QueryRequest):
    """Stream a dining query response."""
    try:
        prompt = f"User query: {request.query}"
        
        # Return a streaming response
        async def response_generator():
            async for chunk in ai_client.generate_response_stream(prompt):
                yield f"data: {chunk}\n\n"
            yield f"data: [DONE]\n\n"
        
        from fastapi.responses import StreamingResponse
        return StreamingResponse(
            response_generator(),
            media_type="text/event-stream"
        )
    except Exception as e:
        logger.error(f"Error processing streaming query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}") 