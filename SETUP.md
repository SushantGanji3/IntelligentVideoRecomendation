# Setup Instructions

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11+**: [Download Python](https://www.python.org/downloads/)
- **Node.js 18+**: [Download Node.js](https://nodejs.org/)
- **PostgreSQL 14+**: [Download PostgreSQL](https://www.postgresql.org/download/)
- **Redis 6+**: [Download Redis](https://redis.io/download)
- **Git**: [Download Git](https://git-scm.com/downloads)

## Optional (for enhanced features):

- **Docker & Docker Compose**: [Download Docker](https://www.docker.com/get-started)
- **Google Cloud Platform Account**: For cloud deployment
- **Pinecone API Key**: For managed vector database (alternative to FAISS)
- **YouTube Data API Key**: For fetching real video metadata

## Step-by-Step Setup

### 1. Clone the Repository

```bash
git clone https://github.com/SushantGanji3/IntelligentVideoRecomendation.git
cd IntelligentVideoRecommendation
```

### 2. Set Up PostgreSQL Database

#### On macOS (using Homebrew):
```bash
brew install postgresql@14
brew services start postgresql@14
createdb video_recommendations
```

#### On Linux:
```bash
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo -u postgres createdb video_recommendations
```

#### On Windows:
1. Download and install PostgreSQL from the official website
2. Create a database named `video_recommendations` using pgAdmin or psql

### 3. Set Up Redis

#### On macOS (using Homebrew):
```bash
brew install redis
brew services start redis
```

#### On Linux:
```bash
sudo apt-get install redis-server
sudo systemctl start redis
```

#### On Windows:
1. Download Redis from the official website or use WSL
2. Start the Redis server

### 4. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env file with your database credentials

# Run database migrations
alembic upgrade head

# Seed the database with sample data
python scripts/seed_data.py

# Start the backend server
uvicorn app.main:app --reload --port 8000
```

The backend API will be available at `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 5. Frontend Setup

Open a new terminal window:

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local file
cp .env.example .env.local
# Edit .env.local if needed

# Start the development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

### 6. Verify Installation

1. **Backend Health Check**:
   ```bash
   curl http://localhost:8000/api/health
   ```

2. **Frontend**: Open `http://localhost:3000` in your browser

3. **API Documentation**: Open `http://localhost:8000/docs` in your browser

## Docker Setup (Alternative)

If you prefer using Docker:

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## Configuration

### Environment Variables

#### Backend (.env):
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `SECRET_KEY`: Secret key for JWT tokens (change in production)
- `EMBEDDING_MODEL`: Sentence transformer model name
- `CACHE_TTL`: Cache time-to-live in seconds

#### Frontend (.env.local):
- `NEXT_PUBLIC_API_URL`: Backend API URL

### Database Configuration

Update the `DATABASE_URL` in `backend/.env`:
```
DATABASE_URL=postgresql://username:password@localhost:5432/video_recommendations
```

### Redis Configuration

Update the `REDIS_URL` in `backend/.env`:
```
REDIS_URL=redis://localhost:6379
```

## Troubleshooting

### Database Connection Issues

1. Ensure PostgreSQL is running:
   ```bash
   # macOS/Linux
   brew services list  # or systemctl status postgresql
   ```

2. Check database credentials in `.env`

3. Verify database exists:
   ```bash
   psql -l | grep video_recommendations
   ```

### Redis Connection Issues

1. Ensure Redis is running:
   ```bash
   redis-cli ping
   # Should return: PONG
   ```

2. Check Redis URL in `.env`

### Port Already in Use

If port 8000 or 3000 is already in use:

1. **Backend**: Change port in `uvicorn` command:
   ```bash
   uvicorn app.main:app --reload --port 8001
   ```

2. **Frontend**: Update `package.json` scripts or use:
   ```bash
   npm run dev -- -p 3001
   ```

### ML Model Download Issues

The first run will download the sentence transformer model. This may take a few minutes depending on your internet connection.

### FAISS Index Issues

If you encounter FAISS index errors:

1. Delete the `data/` directory in the backend
2. Re-run the seed script:
   ```bash
   python scripts/seed_data.py
   ```

## Next Steps

1. **Explore the API**: Visit `http://localhost:8000/docs`
2. **View Recommendations**: Open `http://localhost:3000`
3. **Watch Videos**: Click on videos to record watch history
4. **Check Recommendations**: See how recommendations change based on watch history

## Production Deployment

For production deployment:

1. Set `DEBUG=false` in `.env`
2. Use a strong `SECRET_KEY`
3. Configure proper CORS origins
4. Use managed databases (Cloud SQL, Redis Cloud)
5. Deploy to GCP Cloud Run or GKE
6. Set up monitoring and logging
7. Configure SSL/TLS certificates

## Support

For issues or questions:
1. Check the [README.md](README.md) for general information
2. Review API documentation at `/docs`
3. Check logs for error messages

