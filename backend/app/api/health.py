from fastapi import APIRouter
from app.core.redis_client import redis_client

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    # Check Redis connection
    try:
        redis_client.ping()
        redis_status = "connected"
    except:
        redis_status = "disconnected"
    
    return {
        "status": "healthy",
        "redis": redis_status
    }

