"""
LLM client service for generating summaries
"""
import json
import logging
import time
import asyncio
from typing import Optional, Dict, Any
from openai import AsyncOpenAI
from app.core.config import settings
from app.models.schemas import LLMResponseSchema

logger = logging.getLogger(__name__)

class LLMClient:
    """Client for interacting with LLM APIs"""
    
    def __init__(self):
        self.api_key = settings.LLM_API_KEY
        self.model = settings.LLM_MODEL
        self.max_tokens = settings.LLM_MAX_TOKENS
        self.temperature = settings.LLM_TEMPERATURE
        self.max_retries = settings.MAX_RETRIES
        self.retry_delay = settings.RETRY_DELAY
        
        # Initialize OpenAI client
        self.client = AsyncOpenAI(api_key=self.api_key)
        
        # Define the prompt template
        self.prompt_template = """You are an expert document summarizer. Analyze the following text and provide a structured summary in JSON format with the following fields:
1. summary: A concise 2-3 sentence summary of the main content
2. key_points: 3-5 bullet points highlighting the most important information
3. action_items: 2-4 actionable items derived from the text

Text to analyze:
{text}

Return ONLY valid JSON with no additional text. Use this exact format:
{{
  "summary": "your summary here",
  "key_points": ["point 1", "point 2", "point 3"],
  "action_items": ["action 1", "action 2"]
}}"""
    
    async def generate_summary(self, text: str) -> Dict[str, Any]:
        """
        Generate summary from text using LLM
        
        Args:
            text: Text to summarize
            
        Returns:
            Dictionary with summary, key_points, and action_items
        """
        if not text or len(text.strip()) < 10:
            raise ValueError("Text must be at least 10 characters long")
        
        # Truncate text if too long (to avoid token limits)
        max_chars = 10000  # Conservative limit
        if len(text) > max_chars:
            logger.warning(f"Text truncated from {len(text)} to {max_chars} characters")
            text = text[:max_chars] + "\n\n[Text truncated due to length]"
        
        prompt = self.prompt_template.format(text=text)
        
        for attempt in range(self.max_retries + 1):
            try:
                logger.info(f"Generating summary with {self.model} (attempt {attempt + 1}/{self.max_retries + 1})")
                
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that returns JSON responses."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                    response_format={"type": "json_object"}
                )
                
                content = response.choices[0].message.content
                
                # Parse and validate response
                result = self._parse_and_validate_response(content)
                
                logger.info("Successfully generated summary")
                return result
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse LLM response as JSON (attempt {attempt + 1}): {str(e)}")
                if attempt < self.max_retries:
                    await asyncio.sleep(self.retry_delay * (2 ** attempt))  # Exponential backoff
                    continue
                raise ValueError(f"Invalid JSON response from LLM: {str(e)}")
                
            except Exception as e:
                logger.error(f"Error generating summary (attempt {attempt + 1}): {str(e)}")
                if attempt < self.max_retries:
                    await asyncio.sleep(self.retry_delay * (2 ** attempt))
                    continue
                raise
    
    def _parse_and_validate_response(self, content: str) -> Dict[str, Any]:
        """
        Parse and validate LLM response
        
        Args:
            content: Raw response content from LLM
            
        Returns:
            Validated and parsed response
        """
        try:
            # Parse JSON
            data = json.loads(content)
            
            # Validate against schema
            validated = LLMResponseSchema(**data)
            
            # Convert to dict
            result = validated.dict()
            
            # Ensure arrays are not empty (except action_items which can be empty)
            if not result.get("key_points"):
                result["key_points"] = ["No key points identified"]
            
            if not result.get("action_items"):
                result["action_items"] = ["No specific action items identified"]
            
            # Ensure summary is not empty
            if not result.get("summary") or not result["summary"].strip():
                result["summary"] = "Summary could not be generated"
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to validate LLM response: {str(e)}")
            raise ValueError(f"Invalid response format: {str(e)}")
    
    async def generate_fallback_response(self, error_message: str = "") -> Dict[str, Any]:
        """
        Generate a fallback response when LLM fails
        
        Args:
            error_message: Optional error message to include
            
        Returns:
            Fallback response
        """
        logger.warning(f"Generating fallback response due to: {error_message}")
        
        return {
            "summary": "Unable to generate summary due to technical issues. Please try again later.",
            "key_points": [
                "The summarization service is currently unavailable",
                "Please check your internet connection",
                "Try uploading a different file or text"
            ],
            "action_items": [
                "Retry the request",
                "Check your input format",
                "Contact support if the issue persists"
            ]
        }
    
    def estimate_token_count(self, text: str) -> int:
        """
        Estimate token count for text (rough approximation)
        
        Args:
            text: Text to estimate
            
        Returns:
            Estimated token count
        """
        # Rough approximation: 1 token ≈ 4 characters for English text
        return len(text) // 4
    
    def is_available(self) -> bool:
        """
        Check if LLM service is available
        
        Returns:
            True if API key is set, False otherwise
        """
        return bool(self.api_key and self.api_key.strip())