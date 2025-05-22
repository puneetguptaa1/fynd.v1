from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class QueryResponse(BaseModel):
    """Response model for dining queries."""
    response: str = Field(..., description="LLM generated response")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata about the response") 