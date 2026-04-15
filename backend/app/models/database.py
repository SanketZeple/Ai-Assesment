"""
Database models for the summarizer application
"""
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import Column, String, Text, Integer, DateTime, JSON, Boolean, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Summary(Base):
    """Model for storing summarization requests and results"""
    __tablename__ = "summaries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Input information
    input_type = Column(String(10), nullable=False)  # 'file' or 'text'
    original_text = Column(Text, nullable=True)  # For text input
    file_path = Column(String(500), nullable=True)  # For file uploads
    file_name = Column(String(255), nullable=True)
    file_type = Column(String(50), nullable=True)
    file_size = Column(Integer, nullable=True)  # In bytes
    
    # Processing information
    status = Column(String(20), nullable=False, default="pending")  # pending, processing, completed, failed
    error_message = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0)
    
    # Output information
    summary = Column(JSON, nullable=True)  # Stores the structured output
    processing_time_ms = Column(Integer, nullable=True)  # Processing time in milliseconds
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Optional user tracking (for future auth)
    user_id = Column(UUID(as_uuid=True), nullable=True)
    session_id = Column(String(100), nullable=True)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return {
            "id": str(self.id),
            "input_type": self.input_type,
            "file_name": self.file_name,
            "file_type": self.file_type,
            "status": self.status,
            "summary": self.summary,
            "error_message": self.error_message,
            "retry_count": self.retry_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "processing_time_ms": self.processing_time_ms,
        }
    
    def is_completed(self) -> bool:
        """Check if summary is completed"""
        return self.status == "completed"
    
    def is_failed(self) -> bool:
        """Check if summary failed"""
        return self.status == "failed"
    
    def can_retry(self, max_retries: int = 2) -> bool:
        """Check if summary can be retried"""
        return self.status == "failed" and self.retry_count < max_retries