'use client'

import { useEffect, useState } from 'react'
import VideoCard from '@/components/VideoCard'
import RecommendationSidebar from '@/components/RecommendationSidebar'
import { Video, Recommendation } from '@/types'
import { getRecommendations, getVideos } from '@/lib/api'

export default function Home() {
  const [recommendations, setRecommendations] = useState<Recommendation[]>([])
  const [videos, setVideos] = useState<Video[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedVideo, setSelectedVideo] = useState<Video | null>(null)
  const [userId] = useState(1) // Default user ID for demo

  useEffect(() => {
    loadData()
  }, [userId])

  const loadData = async () => {
    try {
      setLoading(true)
      const [recs, vids] = await Promise.all([
        getRecommendations(userId),
        getVideos()
      ])
      setRecommendations(recs.recommendations || [])
      setVideos(vids || [])
    } catch (error) {
      console.error('Error loading data:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleVideoClick = async (video: Video) => {
    setSelectedVideo(video)
    // Record watch event
    try {
      await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/videos/${video.id}/watch`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: userId,
          watch_duration: 10,
          watch_percentage: 5
        }),
      })
      // Reload recommendations after watch
      const recs = await getRecommendations(userId)
      setRecommendations(recs.recommendations || [])
    } catch (error) {
      console.error('Error recording watch:', error)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Loading...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <h1 className="text-2xl font-bold text-gray-900">
            Intelligent Video Recommendation
          </h1>
          <p className="text-sm text-gray-600 mt-1">
            ML-powered video recommendations
          </p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          <div className="lg:col-span-3">
            {selectedVideo ? (
              <div className="mb-6">
                <div className="bg-white rounded-lg shadow-md p-6">
                  <h2 className="text-2xl font-bold mb-4">{selectedVideo.title}</h2>
                  <div className="aspect-video bg-gray-200 rounded-lg mb-4 flex items-center justify-center">
                    {selectedVideo.thumbnail_url ? (
                      <img
                        src={selectedVideo.thumbnail_url}
                        alt={selectedVideo.title}
                        className="w-full h-full object-cover rounded-lg"
                      />
                    ) : (
                      <div className="text-gray-500">Video Player</div>
                    )}
                  </div>
                  <div className="flex items-center gap-4 text-sm text-gray-600 mb-4">
                    <span>{selectedVideo.views} views</span>
                    <span>{selectedVideo.likes} likes</span>
                    <span>{selectedVideo.category}</span>
                  </div>
                  <p className="text-gray-700">{selectedVideo.description}</p>
                  <button
                    onClick={() => setSelectedVideo(null)}
                    className="mt-4 px-4 py-2 bg-gray-200 rounded hover:bg-gray-300"
                  >
                    Back to Recommendations
                  </button>
                </div>
              </div>
            ) : null}

            <div>
              <h2 className="text-xl font-semibold mb-4">
                {selectedVideo ? 'More Videos' : 'Recommended for You'}
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {(selectedVideo ? videos : recommendations.map(r => r.video)).map((video) => (
                  <VideoCard
                    key={video.id}
                    video={video}
                    onClick={() => handleVideoClick(video)}
                    similarityScore={recommendations.find(r => r.video.id === video.id)?.similarity_score}
                    reason={recommendations.find(r => r.video.id === video.id)?.reason}
                  />
                ))}
              </div>
            </div>
          </div>

          <div className="lg:col-span-1">
            <RecommendationSidebar
              recommendations={recommendations}
              onVideoClick={handleVideoClick}
            />
          </div>
        </div>
      </main>
    </div>
  )
}

