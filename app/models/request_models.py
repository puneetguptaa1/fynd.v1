from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    """Request model for dining queries."""
    query: str = Field(..., description="User's natural language dining request")
    stream: bool = Field(False, description="Whether to stream the response") 