import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

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

export const getRecommendations = async (userId: number, limit: number = 10): Promise<RecommendationResponse> => {
  const response = await api.get(`/api/recommendations/user/${userId}`, {
    params: { limit },
  })
  return response.data
}

export const getVideos = async (limit: number = 20): Promise<Video[]> => {
  const response = await api.get('/api/videos', {
    params: { limit },
  })
  return response.data
}

export const getVideo = async (videoId: number): Promise<Video> => {
  const response = await api.get(`/api/videos/${videoId}`)
  return response.data
}

export const getSimilarVideos = async (videoId: number, limit: number = 10) => {
  const response = await api.get(`/api/recommendations/similar/${videoId}`, {
    params: { limit },
  })
  return response.data
}

export const recordWatch = async (
  videoId: number,
  userId: number,
  watchDuration?: number,
  watchPercentage?: number
) => {
  const response = await api.post(`/api/videos/${videoId}/watch`, {
    user_id: userId,
    watch_duration: watchDuration,
    watch_percentage: watchPercentage,
  })
  return response.data
}

