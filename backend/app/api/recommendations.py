from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.redis_client import get_cache, set_cache
from app.schemas.recommendation import RecommendationResponse
from app.ml.recommender import recommendation_service
from app.core.config import settings
from typing import Optional

router = APIRouter()


@router.get("/user/{user_id}", response_model=RecommendationResponse)
async def get_recommendations(
    user_id: int,
    limit: int = Query(default=10, ge=1, le=50),
    exclude_watched: bool = Query(default=True),
    db: Session = Depends(get_db)
):
    """Get video recommendations for a user"""
    # Check cache
    cache_key = f"recommendations:user:{user_id}:limit:{limit}:exclude:{exclude_watched}"
    cached = get_cache(cache_key)
    if cached:
        return RecommendationResponse(**cached)
    
    # Get recommendations
    recommendations = recommendation_service.get_recommendations(
        db=db,
        user_id=user_id,
        limit=limit,
        exclude_watched=exclude_watched
    )
    
    # Cache results
    set_cache(cache_key, recommendations.model_dump(), ttl=settings.CACHE_TTL)
    
    return recommendations


@router.get("/similar/{video_id}")
async def get_similar_videos(
    video_id: int,
    limit: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get videos similar to a specific video"""
    from app.models.video import Video
    from app.schemas.video import VideoResponse
    from app.ml.faiss_index import faiss_index
    import numpy as np
    
    # Get video
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    # Check if video has embedding
    if not video.embedding:
        from app.ml.recommender import recommendation_service
        recommendation_service.update_video_embedding(db, video_id)
        video = db.query(Video).filter(Video.id == video_id).first()
    
    # Search for similar videos
    embedding = np.array(video.embedding)
    similar_videos = faiss_index.search(embedding, k=limit + 1)  # +1 to exclude self
    
    # Filter out the same video and format
    results = []
    for vid_id, similarity in similar_videos:
        if vid_id == video_id:
            continue
        similar_video = db.query(Video).filter(Video.id == vid_id).first()
        if similar_video:
            results.append({
                "video": VideoResponse.model_validate(similar_video),
                "similarity_score": float(similarity)
            })
        if len(results) >= limit:
            break
    
    return {
        "video": VideoResponse.model_validate(video),
        "similar_videos": results,
        "total": len(results)
    }

