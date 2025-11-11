import { Recommendation, Video } from '@/types'
import { TrendingUp, Sparkles } from 'lucide-react'

interface RecommendationSidebarProps {
  recommendations: Recommendation[]
  onVideoClick: (video: Video) => void
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
              <div className="flex-shrink-0 w-16 h-12 bg-gray-200 rounded overflow-hidden">
                {rec.video.thumbnail_url ? (
                  <img
                    src={rec.video.thumbnail_url}
                    alt={rec.video.title}
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <div className="w-full h-full flex items-center justify-center text-gray-400 text-xs">
                    {idx + 1}
                  </div>
                )}
              </div>
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

