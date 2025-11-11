from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class WatchHistoryBase(BaseModel):
    video_id: int
    watch_duration: Optional[float] = None
    watch_percentage: Optional[float] = None


class WatchHistoryCreate(WatchHistoryBase):
    user_id: int


class WatchHistory(WatchHistoryBase):
    id: int
    user_id: int
    watched_at: datetime

    class Config:
        from_attributes = True

