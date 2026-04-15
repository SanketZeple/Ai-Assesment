"""
Summarizer service for managing summary operations
"""
import logging
from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.models.database import Summary
from app.models.schemas import SummaryStatus

logger = logging.getLogger(__name__)

class SummarizerService:
    """Service for managing summary operations"""
    
    async def update_summary_status(
        self,
        db: AsyncSession,
        summary_id: str,
        status: SummaryStatus,
        error_message: Optional[str] = None,
        retry_count: Optional[int] = None,
    ) -> None:
        """
        Update summary status in database
        
        Args:
            db: Database session
            summary_id: Summary ID
            status: New status
            error_message: Optional error message
            retry_count: Optional retry count
        """
        try:
            update_data = {
                "status": status.value,
            }
            
            if error_message is not None:
                update_data["error_message"] = error_message
            
            if retry_count is not None:
                update_data["retry_count"] = retry_count
            
            await db.execute(
                update(Summary)
                .where(Summary.id == summary_id)
                .values(**update_data)
            )
            await db.commit()
            
            logger.info(f"Updated summary {summary_id} status to {status.value}")
            
        except Exception as e:
            logger.error(f"Error updating summary {summary_id} status: {str(e)}")
            raise
    
    async def complete_summary(
        self,
        db: AsyncSession,
        summary_id: str,
        summary_result: Dict[str, Any],
        processing_time_ms: int,
    ) -> None:
        """
        Mark summary as completed with result
        
        Args:
            db: Database session
            summary_id: Summary ID
            summary_result: Summary result from LLM
            processing_time_ms: Processing time in milliseconds
        """
        try:
            await db.execute(
                update(Summary)
                .where(Summary.id == summary_id)
                .values(
                    status=SummaryStatus.COMPLETED.value,
                    summary=summary_result,
                    processing_time_ms=processing_time_ms,
                    error_message=None,
                )
            )
            await db.commit()
            
            logger.info(f"Completed summary {summary_id} with result")
            
        except Exception as e:
            logger.error(f"Error completing summary {summary_id}: {str(e)}")
            raise
    
    async def fail_summary(
        self,
        db: AsyncSession,
        summary_id: str,
        error_message: str,
        increment_retry: bool = True,
    ) -> None:
        """
        Mark summary as failed
        
        Args:
            db: Database session
            summary_id: Summary ID
            error_message: Error message
            increment_retry: Whether to increment retry count
        """
        try:
            # Get current retry count
            result = await db.execute(
                select(Summary.retry_count).where(Summary.id == summary_id)
            )
            current_retry_count = result.scalar_one_or_none() or 0
            
            update_data = {
                "status": SummaryStatus.FAILED.value,
                "error_message": error_message,
            }
            
            if increment_retry:
                update_data["retry_count"] = current_retry_count + 1
            
            await db.execute(
                update(Summary)
                .where(Summary.id == summary_id)
                .values(**update_data)
            )
            await db.commit()
            
            logger.error(f"Failed summary {summary_id}: {error_message}")
            
        except Exception as e:
            logger.error(f"Error failing summary {summary_id}: {str(e)}")
            raise
    
    async def get_summary(
        self,
        db: AsyncSession,
        summary_id: str,
    ) -> Optional[Summary]:
        """
        Get summary by ID
        
        Args:
            db: Database session
            summary_id: Summary ID
            
        Returns:
            Summary record or None
        """
        try:
            result = await db.execute(
                select(Summary).where(Summary.id == summary_id)
            )
            return result.scalar_one_or_none()
            
        except Exception as e:
            logger.error(f"Error getting summary {summary_id}: {str(e)}")
            raise
    
    async def retry_summary(
        self,
        db: AsyncSession,
        summary_id: str,
    ) -> bool:
        """
        Retry a failed summary
        
        Args:
            db: Database session
            summary_id: Summary ID
            
        Returns:
            True if retry initiated, False otherwise
        """
        try:
            # Get summary
            summary = await self.get_summary(db, summary_id)
            if not summary:
                return False
            
            # Check if can retry
            if not summary.can_retry():
                return False
            
            # Reset status to pending
            await self.update_summary_status(
                db,
                summary_id,
                SummaryStatus.PENDING,
                error_message=None,
            )
            
            logger.info(f"Retrying summary {summary_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error retrying summary {summary_id}: {str(e)}")
            return False