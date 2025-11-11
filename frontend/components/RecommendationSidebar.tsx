'use client'

import { Recommendation, Video } from '@/types'
import { TrendingUp, Sparkles } from 'lucide-react'
import Image from 'next/image'
import { useState } from 'react'

interface RecommendationSidebarProps {
  recommendations: Recommendation[]
  onVideoClick: (video: Video) => void
}

const Thumbnail = ({ video, index }: { video: Video; index: number }) => {
  const [imageError, setImageError] = useState(false)
  return (
    <div className="relative flex-shrink-0 w-16 h-12 bg-gray-200 rounded overflow-hidden">
      {video.thumbnail_url && !imageError ? (
        <Image
          src={video.thumbnail_url}
          alt={video.title}
          fill
          className="object-cover"
          sizes="64px"
          onError={() => setImageError(true)}
          unoptimized={video.thumbnail_url?.includes('placeholder')}
        />
      ) : (
        <div className="w-full h-full flex items-center justify-center text-gray-400 text-xs">
          {index + 1}
        </div>
      )}
    </div>
  )
}

export default function RecommendationSidebar({
  recommendations,
  onVideoClick,
}: RecommendationSidebarProps) {
  const topRecommendations = recommendations
    .sort((a, b) => b.similarity_score - a.similarity_score)
    .slice(0, 5)

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex items-center gap-2 mb-4">
        <Sparkles className="w-5 h-5 text-blue-600" />
        <h2 className="text-lg font-semibold">Top Recommendations</h2>
      </div>
      <div className="space-y-4">
        {topRecommendations.map((rec, idx) => (
          <div
            key={rec.video.id}
            className="cursor-pointer hover:bg-gray-50 p-2 rounded transition-colors"
            onClick={() => onVideoClick(rec.video)}
          >
            <div className="flex items-start gap-3">
              <Thumbnail video={rec.video} index={idx} />
              <div className="flex-1 min-w-0">
                <h3 className="text-sm font-medium line-clamp-2 mb-1">
                  {rec.video.title}
                </h3>
                <div className="flex items-center gap-2">
                  <TrendingUp className="w-3 h-3 text-green-600" />
                  <span className="text-xs text-gray-600">
                    {Math.round(rec.similarity_score * 100)}% match
                  </span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
      {recommendations.length > 0 && (
        <div className="mt-6 pt-4 border-t">
          <p className="text-xs text-gray-500">
            Recommendations are based on your viewing history and video similarity analysis.
          </p>
        </div>
      )}
    </div>
  )
}
