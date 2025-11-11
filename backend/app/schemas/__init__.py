from app.schemas.user import User, UserCreate, UserResponse
from app.schemas.video import Video, VideoCreate, VideoResponse
from app.schemas.watch_history import WatchHistory, WatchHistoryCreate
from app.schemas.recommendation import Recommendation, RecommendationResponse

__all__ = [
    "User", "UserCreate", "UserResponse",
    "Video", "VideoCreate", "VideoResponse",
    "WatchHistory", "WatchHistoryCreate",
    "Recommendation", "RecommendationResponse"
]

