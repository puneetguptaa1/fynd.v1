"""
AI Client module providing abstraction for LLM interactions.
"""
from abc import ABC, abstractmethod
import os
import logging
from typing import Dict, List, Optional, AsyncGenerator, Any
from together import Together

logger = logging.getLogger(__name__)

class AIClient(ABC):
    """Abstract base class for AI clients."""
    
    @abstractmethod
    def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate a response from the LLM."""
        pass
    
    @abstractmethod
    async def generate_response_stream(self, prompt: str, **kwargs) -> AsyncGenerator[str, None]:
        """Generate a streaming response from the LLM."""
        pass
    
    def format_messages(self, prompt: str, system_message: Optional[str] = None) -> List[Dict[str, str]]:
        """Format messages for the chat API."""
        messages = []
        
        if system_message:
            messages.append({"role": "system", "content": system_message})
            
        messages.append({"role": "user", "content": prompt})
        return messages

class TogetherAIClient(AIClient):
    """Implementation of AIClient using together.ai API."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free"):
        """Initialize the Together AI client."""
        self.api_key = api_key or os.getenv("TOGETHER_API_KEY")
        if not self.api_key:
            raise ValueError("TOGETHER_API_KEY environment variable not set")
        
        self.model = model
        self.client = Together(api_key=self.api_key)
        logger.info(f"Initialized TogetherAIClient with model: {self.model}")
    
    def generate_response(self, prompt: str, stream: bool = False, system_message: Optional[str] = None, **kwargs) -> str:
        """Generate a response from the LLM."""
        try:
            messages = self.format_messages(prompt, system_message)
            
            logger.info(f"Sending request to Together AI with messages: {messages}")
            
            if stream:
                # For streaming, we need to capture all chunks and combine
                full_response = ""
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    stream=True,
                    **kwargs
                )
                
                for chunk in response:
                    if hasattr(chunk, 'choices') and chunk.choices:
                        content = chunk.choices[0].delta.content
                        if content:
                            full_response += content
                
                return full_response
            else:
                # For non-streaming, we get the complete response at once
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    stream=False,
                    **kwargs
                )
                
                return response.choices[0].message.content
                
        except Exception as e:
            logger.error(f"Error generating response from Together AI: {str(e)}")
            raise
    
    async def generate_response_stream(self, prompt: str, system_message: Optional[str] = None, **kwargs) -> AsyncGenerator[str, None]:
        """Generate a streaming response from the LLM."""
        try:
            messages = self.format_messages(prompt, system_message)
            
            logger.info(f"Sending streaming request to Together AI with messages: {messages}")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True,
                **kwargs
            )
            
            for chunk in response:
                if hasattr(chunk, 'choices') and chunk.choices:
                    content = chunk.choices[0].delta.content
                    if content:
                        yield content
                        
        except Exception as e:
            logger.error(f"Error generating streaming response from Together AI: {str(e)}")
            raise

def get_ai_client() -> AIClient:
    """Factory function to get the appropriate AI client based on environment."""
    # For now, we only support TogetherAI
    # Later, this could check environment variables to determine which client to use
    return TogetherAIClient() 