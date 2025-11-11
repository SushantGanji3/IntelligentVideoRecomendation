# Quick Start Guide

## What You Need to Provide

### Required (for local development):

1. **PostgreSQL Database**: 
   - Install PostgreSQL 14+ on your machine
   - Create a database named `video_recommendations`
   - Update `DATABASE_URL` in `backend/.env`

2. **Redis Server**: 
   - Install Redis 6+ on your machine
   - Start Redis server
   - Update `REDIS_URL` in `backend/.env` if needed

### Optional (for enhanced features):

1. **Google Cloud Platform (GCP)**: 
   - For cloud deployment
   - GCP Project ID
   - Service Account Key (JSON file)
   - Cloud SQL credentials (if using managed database)

2. **Pinecone API Key**: 
   - Alternative to FAISS for vector storage
   - Get from: https://app.pinecone.io/
   - Requires code modification to use

3. **YouTube Data API Key**: 
   - For fetching real video metadata
   - Get from: https://console.cloud.google.com/
   - Requires code modification to integrate

## Quick Setup (5 minutes)

### 1. Install Dependencies

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

### 2. Configure Environment

**Backend (.env):**
```bash
cd backend
cp .env.example .env
# Edit .env with your database credentials
```

**Frontend (.env.local):**
```bash
cd frontend
cp .env.example .env.local
# Edit if needed (default should work)
```

### 3. Set Up Database

```bash
cd backend
# Create database (PostgreSQL)
createdb video_recommendations

# Run migrations
alembic upgrade head

# Seed with sample data
python scripts/seed_data.py
```

### 4. Start Services

**Terminal 1 - Redis:**
```bash
redis-server
```

**Terminal 2 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

**Terminal 3 - Frontend:**
```bash
cd frontend
npm run dev
```

### 5. Access Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Using Docker (Alternative)

If you have Docker installed:

```bash
docker-compose up -d
```

This will start all services (PostgreSQL, Redis, Backend, Frontend) automatically.

## Default Credentials

After running the seed script, you can use these test users:

- **Username**: `demo_user`
- **Password**: `demo123`

- **Username**: `test_user`
- **Password**: `test123`

## Troubleshooting

### Database Connection Error

1. Check PostgreSQL is running: `psql -l`
2. Verify database exists: `psql -l | grep video_recommendations`
3. Check `DATABASE_URL` in `backend/.env`

### Redis Connection Error

1. Check Redis is running: `redis-cli ping` (should return PONG)
2. Verify `REDIS_URL` in `backend/.env`

### Port Already in Use

- Change backend port: `uvicorn app.main:app --reload --port 8001`
- Change frontend port: Update `package.json` or use `npm run dev -- -p 3001`

### ML Model Download

The first run will download the sentence transformer model (~90MB). This may take a few minutes.

## Next Steps

1. **Explore the API**: Visit http://localhost:8000/docs
2. **View Recommendations**: Open http://localhost:3000
3. **Watch Videos**: Click on videos to record watch history
4. **Check Recommendations**: See how recommendations change based on watch history
5. **Read Documentation**: See `SETUP.md` and `API_DOCUMENTATION.md` for more details

## Project Structure

```
IntelligentVideoRecommendation/
├── backend/           # Python FastAPI backend
│   ├── app/          # Application code
│   ├── alembic/      # Database migrations
│   └── scripts/      # Utility scripts
├── frontend/         # Next.js frontend
│   ├── app/          # Next.js app directory
│   ├── components/   # React components
│   └── lib/          # Utilities
├── docker-compose.yml # Docker configuration
└── README.md         # Main documentation
```

## Support

For detailed setup instructions, see:
- `SETUP.md` - Complete setup guide
- `CONFIGURATION.md` - Configuration details
- `API_DOCUMENTATION.md` - API reference

For issues or questions, check the logs:
- Backend logs: Terminal where uvicorn is running
- Frontend logs: Browser console and terminal
- Database logs: PostgreSQL logs
- Redis logs: Redis logs

