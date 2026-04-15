"""
Pydantic schemas for request/response validation
"""
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from enum import Enum

class InputType(str, Enum):
    """Input type enumeration"""
    FILE = "file"
    TEXT = "text"

class SummaryStatus(str, Enum):
    """Summary status enumeration"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

# Request Schemas
class TextSummaryRequest(BaseModel):
    """Request schema for text summarization"""
    text: str = Field(..., min_length=10, max_length=10000, description="Text to summarize")
    language: Optional[str] = Field("en", description="Language of the text")
    
    @validator('text')
    def text_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Text cannot be empty or whitespace only")
        return v.strip()

class FileSummaryRequest(BaseModel):
    """Request schema for file upload (used for documentation)"""
    file_name: str = Field(..., description="Name of the uploaded file")
    file_type: str = Field(..., description="MIME type of the file")
    file_size: int = Field(..., description="Size of the file in bytes")

# Response Schemas
class SummaryResponse(BaseModel):
    """Response schema for summary result"""
    summary: str = Field(..., description="Concise summary of the content")
    key_points: List[str] = Field(..., description="List of key points")
    action_items: List[str] = Field(..., description="List of actionable items")

class SummaryMetadata(BaseModel):
    """Metadata about the summarization request"""
    id: uuid.UUID
    input_type: InputType
    status: SummaryStatus
    file_name: Optional[str] = None
    file_type: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    processing_time_ms: Optional[int] = None
    error_message: Optional[str] = None
    retry_count: int = 0

class SummaryResult(BaseModel):
    """Complete summary result with metadata"""
    metadata: SummaryMetadata
    summary: Optional[SummaryResponse] = None

class SummaryCreateResponse(BaseModel):
    """Response when creating a new summary request"""
    id: uuid.UUID
    status: SummaryStatus
    message: str

class ErrorResponse(BaseModel):
    """Error response schema"""
    detail: str
    error_code: Optional[str] = None
    request_id: Optional[str] = None

# Health check
class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: datetime
    version: str = "1.0.0"
    database: bool = False
    llm_service: bool = False

# Validation schemas
class LLMResponseSchema(BaseModel):
    """Schema for validating LLM response"""
    summary: str
    key_points: List[str]
    action_items: List[str]
    
    @validator('key_points')
    def validate_key_points(cls, v):
        if len(v) == 0:
            raise ValueError("At least one key point is required")
        return v
    
    @validator('action_items')
    def validate_action_items(cls, v):
        return v  # Action items can be empty