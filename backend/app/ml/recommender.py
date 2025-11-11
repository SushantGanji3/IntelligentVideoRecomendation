from typing import List, Dict, Optional
import numpy as np
from sqlalchemy.orm import Session
from app.models.video import Video
from app.models.watch_history import WatchHistory
from app.ml.embeddings import embedding_service
from app.ml.faiss_index import faiss_index
from app.schemas.recommendation import Recommendation, RecommendationResponse
from app.schemas.video import VideoResponse


class RecommendationService:
    """Service for generating video recommendations"""
    
    def __init__(self):
        self.embedding_service = embedding_service
        self.faiss_index = faiss_index
    
    def get_recommendations(
        self,
        db: Session,
        user_id: int,
        limit: int = 10,
        exclude_watched: bool = True
    ) -> RecommendationResponse:
        """
        Get video recommendations for a user
        
        Args:
            db: Database session
            user_id: User ID
            limit: Number of recommendations to return
            exclude_watched: Whether to exclude videos the user has already watched
            
        Returns:
            RecommendationResponse with recommended videos
        """
        # Get user's watch history
        watched_videos = db.query(WatchHistory.video_id).filter(
            WatchHistory.user_id == user_id
        ).all()
        watched_video_ids = [w[0] for w in watched_videos]
        
        if not watched_video_ids:
            # New user - return popular videos
            return self._get_popular_recommendations(db, user_id, limit)
        
        # Get embeddings of watched videos
        watched_videos_data = db.query(Video).filter(
            Video.id.in_(watched_video_ids)
        ).all()
        
        if not watched_videos_data:
            return self._get_popular_recommendations(db, user_id, limit)
        
        # Compute average embedding of watched videos (user profile)
        embeddings = []
        for video in watched_videos_data:
            if video.embedding:
                embeddings.append(np.array(video.embedding))
        
        if not embeddings:
            # Generate embeddings for watched videos if not present
            for video in watched_videos_data:
                embedding = self.embedding_service.generate_video_embedding(
                    title=video.title,
                    description=video.description,
                    tags=video.tags,
                    category=video.category
                )
                # Update video embedding in database
                video.embedding = embedding.tolist()
                embeddings.append(embedding)
            db.commit()
        
        # Average embedding (user preference vector)
        user_embedding = np.mean(embeddings, axis=0)
        
        # Search for similar videos
        search_limit = limit * 3  # Get more results to filter
        similar_videos = self.faiss_index.search(user_embedding, k=search_limit)
        
        # Filter and format results
        recommendations = []
        seen_video_ids = set(watched_video_ids) if exclude_watched else set()
        
        for video_id, similarity_score in similar_videos:
            if video_id in seen_video_ids:
                continue
            
            video = db.query(Video).filter(Video.id == video_id).first()
            if not video:
                continue
            
            # Generate recommendation reason
            reason = self._generate_reason(video, watched_videos_data, similarity_score)
            
            recommendations.append(Recommendation(
                video=VideoResponse.model_validate(video),
                similarity_score=float(similarity_score),
                reason=reason
            ))
            
            seen_video_ids.add(video_id)
            
            if len(recommendations) >= limit:
                break
        
        # If we don't have enough recommendations, fill with popular videos
        if len(recommendations) < limit:
            popular = self._get_popular_recommendations(db, user_id, limit - len(recommendations))
            # Merge without duplicates
            existing_ids = {r.video.id for r in recommendations}
            for rec in popular.recommendations:
                if rec.video.id not in existing_ids:
                    recommendations.append(rec)
                    if len(recommendations) >= limit:
                        break
        
        return RecommendationResponse(
            user_id=user_id,
            recommendations=recommendations[:limit],
            total=len(recommendations)
        )
    
    def _get_popular_recommendations(
        self,
        db: Session,
        user_id: int,
        limit: int
    ) -> RecommendationResponse:
        """Get popular videos as recommendations"""
        videos = db.query(Video).order_by(
            Video.views.desc(),
            Video.likes.desc()
        ).limit(limit * 2).all()
        
        recommendations = []
        for video in videos[:limit]:
            recommendations.append(Recommendation(
                video=VideoResponse.model_validate(video),
                similarity_score=0.0,
                reason="Popular video"
            ))
        
        return RecommendationResponse(
            user_id=user_id,
            recommendations=recommendations,
            total=len(recommendations)
        )
    
    def _generate_reason(
        self,
        video: Video,
        watched_videos: List[Video],
        similarity_score: float
    ) -> str:
        """Generate explanation for why video is recommended"""
        reasons = []
        
        # Similarity score
        similarity_pct = int(similarity_score * 100)
        reasons.append(f"{similarity_pct}% similarity")
        
        # Category match
        watched_categories = {v.category for v in watched_videos if v.category}
        if video.category and video.category in watched_categories:
            reasons.append(f"same category: {video.category}")
        
        # Tag overlap
        watched_tags = set()
        for v in watched_videos:
            if v.tags:
                watched_tags.update(v.tags)
        
        if video.tags:
            video_tags = set(video.tags)
            overlap = watched_tags.intersection(video_tags)
            if overlap:
                reasons.append(f"shared tags: {', '.join(list(overlap)[:3])}")
        
        if reasons:
            return "Recommended because: " + ", ".join(reasons)
        else:
            return "Recommended based on your viewing history"
    
    def update_video_embedding(self, db: Session, video_id: int):
        """Update embedding for a video in the FAISS index"""
        video = db.query(Video).filter(Video.id == video_id).first()
        if not video:
            return
        
        # Generate embedding
        embedding = self.embedding_service.generate_video_embedding(
            title=video.title,
            description=video.description,
            tags=video.tags,
            category=video.category
        )
        
        # Update in database
        video.embedding = embedding.tolist()
        db.commit()
        
        # Update in FAISS index
        self.faiss_index.update_vector(video_id, embedding)
        self.faiss_index.save()


# Global instance
recommendation_service = RecommendationService()

