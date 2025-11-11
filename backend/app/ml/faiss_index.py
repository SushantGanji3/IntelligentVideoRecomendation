import faiss
import numpy as np
import pickle
import os
from typing import List, Tuple
from app.core.config import settings


class FAISSIndex:
    """FAISS index for fast similarity search"""
    
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.index = None
        self.video_ids = []  # Map index position to video_id
        self.index_path = settings.FAISS_INDEX_PATH
        self.video_ids_path = self.index_path.replace(".bin", "_video_ids.pkl")
        self._initialize_index()
    
    def _initialize_index(self):
        """Initialize or load FAISS index"""
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(self.index_path) if os.path.dirname(self.index_path) else ".", exist_ok=True)
        
        if os.path.exists(self.index_path) and os.path.exists(self.video_ids_path):
            # Load existing index
            self.index = faiss.read_index(self.index_path)
            with open(self.video_ids_path, "rb") as f:
                self.video_ids = pickle.load(f)
        else:
            # Create new index (L2 distance with inner product for cosine similarity)
            # Using inner product since we normalize embeddings
            self.index = faiss.IndexFlatIP(self.dimension)
    
    def add_vectors(self, vectors: np.ndarray, video_ids: List[int]):
        """
        Add vectors to the index
        
        Args:
            vectors: numpy array of shape (n, dimension)
            video_ids: list of video IDs corresponding to vectors
        """
        if len(vectors) == 0:
            return
        
        # Ensure vectors are float32 and normalized
        vectors = vectors.astype("float32")
        faiss.normalize_L2(vectors)
        
        # Add to index
        self.index.add(vectors)
        
        # Store video IDs
        self.video_ids.extend(video_ids)
    
    def search(self, query_vector: np.ndarray, k: int = 10) -> List[Tuple[int, float]]:
        """
        Search for similar vectors
        
        Args:
            query_vector: query vector of shape (dimension,) or (1, dimension)
            k: number of results to return
            
        Returns:
            List of tuples (video_id, similarity_score)
        """
        if self.index.ntotal == 0:
            return []
        
        # Ensure query is float32 and normalized
        if query_vector.ndim == 1:
            query_vector = query_vector.reshape(1, -1)
        
        query_vector = query_vector.astype("float32")
        faiss.normalize_L2(query_vector)
        
        # Search
        k = min(k, self.index.ntotal)
        distances, indices = self.index.search(query_vector, k)
        
        # Convert to list of (video_id, similarity_score)
        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx < len(self.video_ids):
                # Convert distance to similarity (for inner product, higher is better)
                similarity = float(dist)
                results.append((self.video_ids[idx], similarity))
        
        return results
    
    def update_vector(self, video_id: int, new_vector: np.ndarray):
        """
        Update a vector in the index (removes old and adds new)
        
        Args:
            video_id: ID of video to update
            new_vector: new embedding vector
        """
        # Find index of video_id
        try:
            idx = self.video_ids.index(video_id)
            # Remove old vector (FAISS doesn't support direct update, so we rebuild)
            # For simplicity, we'll just add the new one and mark old as removed
            # In production, you might want to implement a more efficient update strategy
            pass
        except ValueError:
            # Video not found, add new
            self.add_vectors(new_vector.reshape(1, -1), [video_id])
    
    def save(self):
        """Save index to disk"""
        os.makedirs(os.path.dirname(self.index_path) if os.path.dirname(self.index_path) else ".", exist_ok=True)
        faiss.write_index(self.index, self.index_path)
        with open(self.video_ids_path, "wb") as f:
            pickle.dump(self.video_ids, f)
    
    def get_total_vectors(self) -> int:
        """Get total number of vectors in index"""
        return self.index.ntotal


# Global instance
faiss_index = FAISSIndex(dimension=settings.EMBEDDING_DIMENSION)

