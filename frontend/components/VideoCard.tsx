import { Video } from '@/types'
import { Play } from 'lucide-react'

interface VideoCardProps {
  video: Video
  onClick: () => void
  similarityScore?: number
  reason?: string
}

export default function VideoCard({ video, onClick, similarityScore, reason }: VideoCardProps) {
  return (
    <div
      className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow cursor-pointer"
      onClick={onClick}
    >
      <div className="relative aspect-video bg-gray-200">
        {video.thumbnail_url ? (
          <img
            src={video.thumbnail_url}
            alt={video.title}
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-gray-400">
            <Play size={48} />
          </div>
        )}
        {similarityScore !== undefined && (
          <div className="absolute top-2 right-2 bg-blue-600 text-white px-2 py-1 rounded text-xs font-semibold">
            {Math.round(similarityScore * 100)}% match
          </div>
        )}
      </div>
      <div className="p-4">
        <h3 className="font-semibold text-lg mb-2 line-clamp-2">{video.title}</h3>
        <div className="flex items-center gap-4 text-sm text-gray-600 mb-2">
          <span>{video.views.toLocaleString()} views</span>
          <span>{video.likes} likes</span>
          {video.category && <span className="px-2 py-1 bg-gray-100 rounded">{video.category}</span>}
        </div>
        {reason && (
          <p className="text-xs text-gray-500 mt-2 line-clamp-2">{reason}</p>
        )}
        {video.tags && video.tags.length > 0 && (
          <div className="flex flex-wrap gap-1 mt-2">
            {video.tags.slice(0, 3).map((tag, idx) => (
              <span
                key={idx}
                className="text-xs px-2 py-1 bg-blue-50 text-blue-700 rounded"
              >
                {tag}
              </span>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

