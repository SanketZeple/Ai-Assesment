"""
Summarizer API endpoints
"""
import uuid
import logging
import time
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_async_session, AsyncSessionLocal
from app.models.database import Summary
from app.models.schemas import (
    TextSummaryRequest,
    SummaryCreateResponse,
    SummaryResult,
    SummaryMetadata,
    SummaryResponse,
    InputType,
    SummaryStatus,
    ErrorResponse,
)
from app.services.file_processor import FileProcessor
from app.services.llm_client import LLMClient
from app.services.summarizer_service import SummarizerService

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize services
file_processor = FileProcessor()
llm_client = LLMClient()
summarizer_service = SummarizerService()

@router.post("/file", response_model=SummaryCreateResponse)
async def summarize_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_async_session),
) -> SummaryCreateResponse:
    """
    Upload a file for summarization
    
    Args:
        file: File to upload
        db: Database session
        
    Returns:
        Summary creation response with ID and status
    """
    try:
        # Validate file
        is_valid, error_message = await file_processor.validate_file(file)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_message)
        
        # Save file temporarily
        file_path, error_message = await file_processor.save_file(file)
        if not file_path:
            raise HTTPException(status_code=500, detail=error_message)
        
        # Create summary record in database
        summary_id = uuid.uuid4()
        summary_record = Summary(
            id=summary_id,
            input_type=InputType.FILE.value,
            file_name=file.filename,
            file_type=file.content_type,
            file_size=file.size if hasattr(file, 'size') else None,
            file_path=file_path,
            status=SummaryStatus.PENDING.value,
        )
        
        db.add(summary_record)
        await db.commit()
        await db.refresh(summary_record)
        
        # Start background processing
        background_tasks.add_task(
            process_file_summary,
            summary_id,
            file_path,
            file.content_type,
            file.filename,
        )
        
        logger.info(f"File upload initiated: {file.filename} (ID: {summary_id})")
        
        return SummaryCreateResponse(
            id=summary_id,
            status=SummaryStatus.PENDING,
            message="File uploaded successfully. Processing started.",
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing file upload: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/text", response_model=SummaryCreateResponse)
async def summarize_text(
    background_tasks: BackgroundTasks,
    request: TextSummaryRequest,
    db: AsyncSession = Depends(get_async_session),
) -> SummaryCreateResponse:
    """
    Submit text for summarization
    
    Args:
        request: Text summary request
        db: Database session
        
    Returns:
        Summary creation response with ID and status
    """
    try:
        # Create summary record in database
        summary_id = uuid.uuid4()
        summary_record = Summary(
            id=summary_id,
            input_type=InputType.TEXT.value,
            original_text=request.text,
            status=SummaryStatus.PENDING.value,
        )
        
        db.add(summary_record)
        await db.commit()
        await db.refresh(summary_record)
        
        # Start background processing
        background_tasks.add_task(
            process_text_summary,
            summary_id,
            request.text,
        )
        
        logger.info(f"Text summarization initiated (ID: {summary_id})")
        
        return SummaryCreateResponse(
            id=summary_id,
            status=SummaryStatus.PENDING,
            message="Text submitted successfully. Processing started.",
        )
        
    except Exception as e:
        logger.error(f"Error processing text summarization: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/{summary_id}", response_model=SummaryResult)
async def get_summary(
    summary_id: uuid.UUID,
    db: AsyncSession = Depends(get_async_session),
) -> SummaryResult:
    """
    Get summarization result by ID
    
    Args:
        summary_id: Summary ID
        db: Database session
        
    Returns:
        Summary result with metadata
    """
    try:
        # Query database
        result = await db.execute(
            select(Summary).where(Summary.id == summary_id)
        )
        summary_record = result.scalar_one_or_none()
        
        if not summary_record:
            raise HTTPException(status_code=404, detail="Summary not found")
        
        # Prepare metadata
        metadata = SummaryMetadata(
            id=summary_record.id,
            input_type=InputType(summary_record.input_type),
            status=SummaryStatus(summary_record.status),
            file_name=summary_record.file_name,
            file_type=summary_record.file_type,
            created_at=summary_record.created_at,
            updated_at=summary_record.updated_at,
            processing_time_ms=summary_record.processing_time_ms,
            error_message=summary_record.error_message,
            retry_count=summary_record.retry_count,
        )
        
        # Prepare summary response if available
        summary_response = None
        if summary_record.summary and summary_record.status == SummaryStatus.COMPLETED.value:
            summary_response = SummaryResponse(**summary_record.summary)
        
        return SummaryResult(
            metadata=metadata,
            summary=summary_response,
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving summary {summary_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

async def process_file_summary(
    summary_id: uuid.UUID,
    file_path: str,
    file_type: str,
    file_name: str,
):
    """
    Background task to process file summary
    
    Args:
        summary_id: Summary ID
        file_path: Path to the file
        file_type: File MIME type
        file_name: Original file name
    """
    db = AsyncSessionLocal()
    try:
        # Update status to processing
        await summarizer_service.update_summary_status(
            db, summary_id, SummaryStatus.PROCESSING
        )
        
        # Extract text from file
        text, error_message = await file_processor.extract_text(file_path, file_type)
        if not text:
            await summarizer_service.fail_summary(
                db, summary_id, f"Failed to extract text: {error_message}"
            )
            return
        
        # Generate summary
        await process_text_with_llm(db, summary_id, text)
        
        # Clean up file
        file_processor.cleanup_file(file_path)
        
    except Exception as e:
        logger.error(f"Error processing file summary {summary_id}: {str(e)}")
        await summarizer_service.fail_summary(db, summary_id, str(e))
        # Clean up file even on error
        try:
            file_processor.cleanup_file(file_path)
        except:
            pass
    finally:
        await db.close()

async def process_text_summary(
    summary_id: uuid.UUID,
    text: str,
):
    """
    Background task to process text summary
    
    Args:
        summary_id: Summary ID
        text: Text to summarize
    """
    db = AsyncSessionLocal()
    try:
        # Update status to processing
        await summarizer_service.update_summary_status(
            db, summary_id, SummaryStatus.PROCESSING
        )
        
        # Generate summary
        await process_text_with_llm(db, summary_id, text)
        
    except Exception as e:
        logger.error(f"Error processing text summary {summary_id}: {str(e)}")
        await summarizer_service.fail_summary(db, summary_id, str(e))
    finally:
        await db.close()

async def process_text_with_llm(
    db: AsyncSession,
    summary_id: uuid.UUID,
    text: str,
):
    """
    Process text with LLM and update database
    
    Args:
        db: Database session
        summary_id: Summary ID
        text: Text to summarize
    """
    start_time = time.time()
    
    try:
        # Generate summary using LLM
        summary_result = await llm_client.generate_summary(text)
        
        # Calculate processing time
        processing_time_ms = int((time.time() - start_time) * 1000)
        
        # Update database with success
        await summarizer_service.complete_summary(
            db, summary_id, summary_result, processing_time_ms
        )
        
        logger.info(f"Successfully processed summary {summary_id} in {processing_time_ms}ms")
        
    except Exception as e:
        logger.error(f"LLM processing failed for {summary_id}: {str(e)}")
        
        # Try fallback
        try:
            fallback_result = await llm_client.generate_fallback_response(str(e))
            processing_time_ms = int((time.time() - start_time) * 1000)
            
            await summarizer_service.complete_summary(
                db, summary_id, fallback_result, processing_time_ms
            )
            
            logger.info(f"Used fallback for summary {summary_id}")
            
        except Exception as fallback_error:
            logger.error(f"Fallback also failed for {summary_id}: {str(fallback_error)}")
            await summarizer_service.fail_summary(
                db, summary_id, f"LLM and fallback failed: {str(e)}"
            )