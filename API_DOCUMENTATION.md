# API Documentation

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API does not require authentication for demo purposes. In production, you would implement JWT-based authentication.

## Endpoints

### Health Check

#### GET `/api/health`

Check the health status of the API and connected services.

**Response:**
```json
{
  "status": "healthy",
  "redis": "connected"
}
```

---

### Users

#### POST `/api/users/`

Create a new user.

**Request Body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password"
}
```

**Response:**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### GET `/api/users/{user_id}`

Get user by ID.

**Response:**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### GET `/api/users/`

Get all users.

**Query Parameters:**
- `skip` (int, default: 0): Number of users to skip
- `limit` (int, default: 100): Maximum number of users to return

**Response:**
```json
[
  {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "is_active": true,
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

---

### Videos

#### POST `/api/videos/`

Create a new video.

**Request Body:**
```json
{
  "video_id": "unique_video_id",
  "title": "Video Title",
  "description": "Video description",
  "tags": ["tag1", "tag2"],
  "category": "Education",
  "duration": 600,
  "thumbnail_url": "https://example.com/thumbnail.jpg"
}
```

**Response:**
```json
{
  "id": 1,
  "video_id": "unique_video_id",
  "title": "Video Title",
  "description": "Video description",
  "tags": ["tag1", "tag2"],
  "category": "Education",
  "duration": 600,
  "thumbnail_url": "https://example.com/thumbnail.jpg",
  "views": 0,
  "likes": 0,
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### GET `/api/videos/{video_id}`

Get video by ID.

**Response:**
```json
{
  "id": 1,
  "video_id": "unique_video_id",
  "title": "Video Title",
  "description": "Video description",
  "tags": ["tag1", "tag2"],
  "category": "Education",
  "duration": 600,
  "thumbnail_url": "https://example.com/thumbnail.jpg",
  "views": 100,
  "likes": 10,
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### GET `/api/videos/`

Get videos with optional filtering.

**Query Parameters:**
- `skip` (int, default: 0): Number of videos to skip
- `limit` (int, default: 100): Maximum number of videos to return
- `category` (string, optional): Filter by category
- `search` (string, optional): Search in title and description

**Response:**
```json
[
  {
    "id": 1,
    "video_id": "unique_video_id",
    "title": "Video Title",
    "description": "Video description",
    "tags": ["tag1", "tag2"],
    "category": "Education",
    "duration": 600,
    "thumbnail_url": "https://example.com/thumbnail.jpg",
    "views": 100,
    "likes": 10,
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

#### POST `/api/videos/{video_id}/watch`

Record a video watch event.

**Request Body:**
```json
{
  "user_id": 1,
  "watch_duration": 120.5,
  "watch_percentage": 50.0
}
```

**Response:**
```json
{
  "message": "Watch recorded",
  "video_id": 1,
  "user_id": 1
}
```

---

### Recommendations

#### GET `/api/recommendations/user/{user_id}`

Get video recommendations for a user.

**Query Parameters:**
- `limit` (int, default: 10, min: 1, max: 50): Number of recommendations to return
- `exclude_watched` (bool, default: true): Whether to exclude videos the user has already watched

**Response:**
```json
{
  "user_id": 1,
  "recommendations": [
    {
      "video": {
        "id": 2,
        "video_id": "video_2",
        "title": "Recommended Video",
        "description": "Video description",
        "tags": ["tag1", "tag2"],
        "category": "Education",
        "duration": 600,
        "thumbnail_url": "https://example.com/thumbnail.jpg",
        "views": 100,
        "likes": 10,
        "created_at": "2024-01-01T00:00:00Z"
      },
      "similarity_score": 0.85,
      "reason": "Recommended because: 85% similarity, same category: Education, shared tags: tag1, tag2"
    }
  ],
  "total": 1
}
```

#### GET `/api/recommendations/similar/{video_id}`

Get videos similar to a specific video.

**Query Parameters:**
- `limit` (int, default: 10, min: 1, max: 50): Number of similar videos to return

**Response:**
```json
{
  "video": {
    "id": 1,
    "video_id": "video_1",
    "title": "Video Title",
    "description": "Video description",
    "tags": ["tag1", "tag2"],
    "category": "Education",
    "duration": 600,
    "thumbnail_url": "https://example.com/thumbnail.jpg",
    "views": 100,
    "likes": 10,
    "created_at": "2024-01-01T00:00:00Z"
  },
  "similar_videos": [
    {
      "video": {
        "id": 2,
        "video_id": "video_2",
        "title": "Similar Video",
        "description": "Similar video description",
        "tags": ["tag1", "tag2"],
        "category": "Education",
        "duration": 600,
        "thumbnail_url": "https://example.com/thumbnail.jpg",
        "views": 100,
        "likes": 10,
        "created_at": "2024-01-01T00:00:00Z"
      },
      "similarity_score": 0.85
    }
  ],
  "total": 1
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Error message describing what went wrong"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Interactive API Documentation

The API provides interactive documentation using Swagger UI and ReDoc:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Rate Limiting

Currently, there is no rate limiting implemented. In production, you would implement rate limiting to prevent abuse.

---

## Caching

Recommendations are cached in Redis for 1 hour (3600 seconds) by default. The cache key format is:
```
recommendations:user:{user_id}:limit:{limit}:exclude:{exclude_watched}
```

---

## ML Model Details

### Embedding Model
- **Model**: `all-MiniLM-L6-v2` (Sentence Transformers)
- **Dimension**: 384
- **Description**: Generates embeddings from video metadata (title, description, tags, category)

### Similarity Search
- **Method**: FAISS (Facebook AI Similarity Search)
- **Index Type**: Inner Product (for cosine similarity)
- **Normalization**: L2 normalization for cosine similarity

### Recommendation Algorithm
1. Get user's watch history
2. Compute average embedding of watched videos (user profile)
3. Search for similar videos using FAISS
4. Filter out already watched videos (if `exclude_watched=true`)
5. Return top-N recommendations with similarity scores and reasons

---

## Example Usage

### Get Recommendations for User

```bash
curl -X GET "http://localhost:8000/api/recommendations/user/1?limit=10" \
  -H "Content-Type: application/json"
```

### Record Video Watch

```bash
curl -X POST "http://localhost:8000/api/videos/1/watch" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "watch_duration": 120.5,
    "watch_percentage": 50.0
  }'
```

### Get Similar Videos

```bash
curl -X GET "http://localhost:8000/api/recommendations/similar/1?limit=10" \
  -H "Content-Type: application/json"
```

---

## Notes

- All timestamps are in ISO 8601 format (UTC)
- Video durations are in seconds
- Watch percentages are in range 0-100
- Similarity scores are in range 0-1 (higher is more similar)
- Embeddings are generated automatically when videos are created
- The FAISS index is updated when videos are created or updated

