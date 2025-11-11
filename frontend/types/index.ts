export interface Video {
  id: number
  video_id: string
  title: string
  description: string | null
  tags: string[] | null
  category: string | null
  duration: number | null
  thumbnail_url: string | null
  views: number
  likes: number
  created_at: string
}

export interface Recommendation {
  video: Video
  similarity_score: number
  reason: string
}

export interface RecommendationResponse {
  user_id: number
  recommendations: Recommendation[]
  total: number
}

