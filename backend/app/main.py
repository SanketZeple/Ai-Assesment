"""
Main FastAPI application for AI Document Summarizer
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.api.endpoints import summarizer, health
from app.core.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def create_application() -> FastAPI:
    """Create and configure FastAPI application"""
    app = FastAPI(
        title="AI Document Summarizer API",
        description="API for generating structured summaries from documents using LLM",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(
        summarizer.router,
        prefix="/api/v1/summarize",
        tags=["summarizer"],
    )
    app.include_router(
        health.router,
        prefix="/api/v1",
        tags=["health"],
    )

    @app.on_event("startup")
    async def startup_event():
        """Run on application startup"""
        logger.info("Starting AI Document Summarizer API")
        # Initialize database connection here if needed

    @app.on_event("shutdown")
    async def shutdown_event():
        """Run on application shutdown"""
        logger.info("Shutting down AI Document Summarizer API")
        # Clean up database connections here if needed

    return app

# Create application instance
app = create_application()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )