from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class VideoBase(BaseModel):
    title: str
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    category: Optional[str] = None
    duration: Optional[int] = None
    thumbnail_url: Optional[str] = None


class VideoCreate(VideoBase):
    video_id: str


class VideoResponse(VideoBase):
    id: int
    video_id: str
    views: int
    likes: int
    created_at: datetime

    class Config:
        from_attributes = True


class Video(VideoResponse):
    pass

