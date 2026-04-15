"""
Health check endpoints
"""
import logging
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.db.session import get_async_session
from app.models.schemas import HealthResponse
from app.services.llm_client import LLMClient

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check(
    db: AsyncSession = Depends(get_async_session)
) -> HealthResponse:
    """
    Health check endpoint
    
    Returns:
        Health status of the application
    """
    # Check database connection
    db_status = False
    try:
        await db.execute(text("SELECT 1"))
        db_status = True
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
    
    # Check LLM service
    llm_status = False
    try:
        llm_client = LLMClient()
        llm_status = llm_client.is_available()
    except Exception as e:
        logger.error(f"LLM service health check failed: {str(e)}")
    
    # Determine overall status
    overall_status = "healthy" if db_status and llm_status else "degraded"
    if not db_status:
        overall_status = "unhealthy"
    
    return HealthResponse(
        status=overall_status,
        timestamp=datetime.now(),
        database=db_status,
        llm_service=llm_status,
    )