from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.redis_client import get_cache, set_cache
from app.schemas.video import VideoCreate, VideoResponse
from app.models.video import Video
from app.ml.recommender import recommendation_service
from typing import List, Optional

router = APIRouter()


@router.post("/", response_model=VideoResponse)
async def create_video(video: VideoCreate, db: Session = Depends(get_db)):
    """Create a new video"""
    # Check if video_id already exists
    db_video = db.query(Video).filter(Video.video_id == video.video_id).first()
    if db_video:
        raise HTTPException(status_code=400, detail="Video ID already exists")
    
    # Create video
    db_video = Video(**video.dict())
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    
    # Generate embedding and add to FAISS index
    recommendation_service.update_video_embedding(db, db_video.id)
    
    return db_video


@router.get("/{video_id}", response_model=VideoResponse)
async def get_video(video_id: int, db: Session = Depends(get_db)):
    """Get video by ID"""
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video


@router.get("/", response_model=List[VideoResponse])
async def get_videos(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get videos with optional filtering"""
    query = db.query(Video)
    
    if category:
        query = query.filter(Video.category == category)
    
    if search:
        query = query.filter(
            Video.title.ilike(f"%{search}%") |
            Video.description.ilike(f"%{search}%")
        )
    
    videos = query.order_by(Video.created_at.desc()).offset(skip).limit(limit).all()
    return videos


@router.post("/{video_id}/watch")
async def record_watch(
    video_id: int,
    user_id: int,
    watch_duration: Optional[float] = None,
    watch_percentage: Optional[float] = None,
    db: Session = Depends(get_db)
):
    """Record a video watch event"""
    from app.models.watch_history import WatchHistory
    
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    # Update video views
    video.views += 1
    db.commit()
    
    # Record watch history
    watch_history = WatchHistory(
        user_id=user_id,
        video_id=video_id,
        watch_duration=watch_duration,
        watch_percentage=watch_percentage
    )
    db.add(watch_history)
    db.commit()
    
    # Clear user recommendation cache
    from app.core.redis_client import clear_user_cache
    clear_user_cache(user_id)
    
    return {"message": "Watch recorded", "video_id": video_id, "user_id": user_id}

