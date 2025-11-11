import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Optional
import os
from app.core.config import settings


class EmbeddingService:
    """Service for generating video embeddings using sentence transformers"""
    
    def __init__(self):
        self.model_name = settings.EMBEDDING_MODEL
        self.model = SentenceTransformer(self.model_name)
        self.dimension = settings.EMBEDDING_DIMENSION
    
    def generate_video_embedding(self, title: str, description: Optional[str] = None, 
                                 tags: Optional[List[str]] = None, 
                                 category: Optional[str] = None) -> np.ndarray:
        """
        Generate embedding for a video based on its metadata
        
        Args:
            title: Video title
            description: Video description
            tags: List of tags
            category: Video category
            
        Returns:
            numpy array of embedding vector
        """
        # Combine all text metadata
        text_parts = [title]
        
        if description:
            text_parts.append(description)
        
        if tags:
            text_parts.append(", ".join(tags))
        
        if category:
            text_parts.append(category)
        
        # Join all parts
        combined_text = " ".join(text_parts)
        
        # Generate embedding
        embedding = self.model.encode(combined_text, normalize_embeddings=True)
        
        return embedding
    
    def generate_embeddings_batch(self, videos: List[dict]) -> np.ndarray:
        """
        Generate embeddings for multiple videos
        
        Args:
            videos: List of video dictionaries with title, description, tags, category
            
        Returns:
            numpy array of embeddings (n_videos, embedding_dim)
        """
        texts = []
        for video in videos:
            text_parts = [video.get("title", "")]
            if video.get("description"):
                text_parts.append(video["description"])
            if video.get("tags"):
                text_parts.append(", ".join(video["tags"]))
            if video.get("category"):
                text_parts.append(video["category"])
            texts.append(" ".join(text_parts))
        
        embeddings = self.model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
        return embeddings


# Global instance
embedding_service = EmbeddingService()

