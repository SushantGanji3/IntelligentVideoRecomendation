# Configuration Guide

## Required Configuration

### Backend Configuration

Create a `.env` file in the `backend/` directory with the following variables:

```env
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/video_recommendations

# Redis Configuration
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# ML Model Configuration
EMBEDDING_MODEL=all-MiniLM-L6-v2
FAISS_INDEX_PATH=data/faiss_index.bin
EMBEDDING_DIMENSION=384

# Recommendation Configuration
DEFAULT_RECOMMENDATION_LIMIT=10
CACHE_TTL=3600

# Application Configuration
DEBUG=true

# CORS Origins (comma-separated)
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

### Frontend Configuration

Create a `.env.local` file in the `frontend/` directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Optional Configuration

### Google Cloud Platform (GCP)

If deploying to GCP, you'll need:

1. **GCP Project ID**: Your Google Cloud Platform project ID
2. **Service Account Key**: JSON key file for service account authentication
3. **Cloud SQL Credentials**: If using Cloud SQL instead of local PostgreSQL
4. **Cloud Run Configuration**: For containerized deployment

**Example GCP Configuration:**
```env
# Backend .env
DATABASE_URL=postgresql://user:password@/video_recommendations?host=/cloudsql/project:region:instance
REDIS_URL=redis://your-redis-instance:6379
GCP_PROJECT_ID=your-project-id
```

### Pinecone (Alternative to FAISS)

If you want to use Pinecone instead of FAISS for vector storage:

1. **Pinecone API Key**: Get from [Pinecone Dashboard](https://app.pinecone.io/)
2. **Pinecone Environment**: Your Pinecone environment name
3. **Pinecone Index Name**: Name of your Pinecone index

**Note**: You would need to modify the code to use Pinecone instead of FAISS.

### YouTube Data API (Optional)

If you want to fetch real video metadata from YouTube:

1. **YouTube API Key**: Get from [Google Cloud Console](https://console.cloud.google.com/)
2. Enable YouTube Data API v3 in your GCP project

**Note**: This requires additional code to integrate YouTube API.

## Environment Variables Explained

### Database Configuration

- **DATABASE_URL**: PostgreSQL connection string
  - Format: `postgresql://user:password@host:port/database`
  - Example: `postgresql://user:password@localhost:5432/video_recommendations`

### Redis Configuration

- **REDIS_URL**: Redis connection string
  - Format: `redis://host:port`
  - Example: `redis://localhost:6379`
  - For Redis with password: `redis://:password@host:port`

### Security Configuration

- **SECRET_KEY**: Secret key for JWT token generation
  - **Important**: Change this in production!
  - Generate a strong secret: `openssl rand -hex 32`
- **ALGORITHM**: JWT algorithm (default: HS256)
- **ACCESS_TOKEN_EXPIRE_MINUTES**: Token expiration time in minutes

### ML Model Configuration

- **EMBEDDING_MODEL**: Sentence transformer model name
  - Default: `all-MiniLM-L6-v2`
  - Alternatives: `all-mpnet-base-v2`, `paraphrase-multilingual-MiniLM-L12-v2`
- **FAISS_INDEX_PATH**: Path to FAISS index file
- **EMBEDDING_DIMENSION**: Dimension of embedding vectors (384 for all-MiniLM-L6-v2)

### Recommendation Configuration

- **DEFAULT_RECOMMENDATION_LIMIT**: Default number of recommendations to return
- **CACHE_TTL**: Cache time-to-live in seconds (default: 3600 = 1 hour)

### Application Configuration

- **DEBUG**: Enable debug mode (set to `false` in production)
- **CORS_ORIGINS**: Comma-separated list of allowed CORS origins

## Production Configuration

For production deployment, consider the following:

1. **Set DEBUG=false**: Disable debug mode
2. **Use Strong SECRET_KEY**: Generate a secure random key
3. **Use Managed Databases**: Use Cloud SQL, Redis Cloud, or similar
4. **Configure CORS Properly**: Only allow your frontend domain
5. **Use Environment-Specific Configs**: Different configs for dev/staging/prod
6. **Enable SSL/TLS**: Use HTTPS for all connections
7. **Set Up Monitoring**: Use Cloud Monitoring, Datadog, or similar
8. **Configure Logging**: Set up structured logging
9. **Use Secrets Management**: Use GCP Secret Manager or similar
10. **Enable Rate Limiting**: Prevent API abuse

## Docker Configuration

When using Docker, environment variables can be set in:

1. **docker-compose.yml**: Environment section
2. **.env file**: Docker Compose automatically loads `.env` file
3. **Dockerfile**: ENV instructions (not recommended for secrets)

## Verifying Configuration

### Backend

1. Check environment variables are loaded:
   ```bash
   cd backend
   python -c "from app.core.config import settings; print(settings.DATABASE_URL)"
   ```

2. Test database connection:
   ```bash
   python -c "from app.core.database import engine; engine.connect()"
   ```

3. Test Redis connection:
   ```bash
   python -c "from app.core.redis_client import redis_client; redis_client.ping()"
   ```

### Frontend

1. Check environment variables:
   ```bash
   cd frontend
   echo $NEXT_PUBLIC_API_URL
   ```

2. Verify API URL in browser console:
   ```javascript
   console.log(process.env.NEXT_PUBLIC_API_URL)
   ```

## Troubleshooting

### Configuration Not Loading

1. Check file location: `.env` should be in `backend/` directory
2. Check file name: Should be exactly `.env` (not `.env.local` or `.env.example`)
3. Restart the server after changing `.env` file
4. Check for syntax errors in `.env` file

### Database Connection Issues

1. Verify DATABASE_URL format
2. Check database is running: `psql -l`
3. Verify credentials are correct
4. Check firewall rules if using cloud database

### Redis Connection Issues

1. Verify REDIS_URL format
2. Check Redis is running: `redis-cli ping`
3. Verify credentials if using password
4. Check firewall rules if using cloud Redis

### ML Model Download Issues

1. Check internet connection
2. Verify EMBEDDING_MODEL name is correct
3. Check disk space (models can be large)
4. Model will be downloaded on first use

## Security Best Practices

1. **Never commit .env files**: Already in .gitignore
2. **Use environment variables**: Don't hardcode secrets
3. **Rotate secrets regularly**: Change SECRET_KEY periodically
4. **Use strong passwords**: For database and Redis
5. **Enable encryption**: Use SSL/TLS for all connections
6. **Limit access**: Use firewall rules and VPCs
7. **Monitor access**: Log all authentication attempts
8. **Use secrets management**: GCP Secret Manager, AWS Secrets Manager, etc.

