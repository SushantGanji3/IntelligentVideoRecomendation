from pydantic import BaseModel
from typing import List, Optional
from app.schemas.video import VideoResponse


class Recommendation(BaseModel):
    video: VideoResponse
    similarity_score: float
    reason: str


class RecommendationResponse(BaseModel):
    user_id: int
    recommendations: List[Recommendation]
    total: int

