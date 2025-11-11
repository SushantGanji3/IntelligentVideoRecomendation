# Intelligent Video Recommendation System

A scalable YouTube-like video recommendation system built with modern Google-style architecture, featuring ML-powered similarity search, real-time recommendations, and a full-stack web application.

## Architecture Overview

```
┌─────────────────────────────┐
│     React Frontend          │
│   (Next.js + Tailwind)      │
└────────────┬────────────────┘
             │ REST/gRPC
┌────────────▼────────────────┐
│   Backend API (FastAPI)     │
│   + gRPC Services           │
└────────────┬────────────────┘
             │
┌────────────▼────────────────┐
│  Recommendation Engine      │
│  (Embeddings + Faiss)       │
└────────────┬────────────────┘
             │
┌────────────▼────────────────┐
│  Data Storage               │
│  (PostgreSQL + Redis)       │
└─────────────────────────────┘
```

## Features

- **ML-Powered Recommendations**: Vector embeddings and similarity search
- **Scalable Backend**: FastAPI with async support, gRPC for microservices
- **Real-time Caching**: Redis for fast recommendation retrieval
- **User History Tracking**: Watch history and preference learning
- **Explainable Recommendations**: Shows why videos are recommended
- **Modern Frontend**: React/Next.js with Tailwind CSS
- **Cloud-Ready**: Docker containers, GCP deployment ready

## Tech Stack

### Backend
- **Python 3.11+** with FastAPI
- **gRPC** with Protocol Buffers
- **PostgreSQL** for data storage
- **Redis** for caching
- **FAISS** for vector similarity search
- **SQLAlchemy** for ORM

### Frontend
- **Next.js 14** (React)
- **Tailwind CSS** for styling
- **TypeScript** for type safety

### ML/Recommendation
- **Sentence Transformers** for embeddings
- **FAISS** for fast similarity search
- **NumPy/Pandas** for data processing

## Setup Instructions

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Redis 6+
- Docker (optional, for containerized deployment)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/SushantGanji3/IntelligentVideoRecomendation.git
cd IntelligentVideoRecommendation
```

2. **Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Frontend Setup**
```bash
cd frontend
npm install
```

4. **Environment Configuration**

Create `.env` files in both `backend/` and `frontend/` directories:

**backend/.env**:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/video_recommendations
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**frontend/.env.local**:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

5. **Database Setup**
```bash
cd backend
alembic upgrade head
python scripts/seed_data.py
```

6. **Start Services**

Terminal 1 - Redis:
```bash
redis-server
```

Terminal 2 - Backend:
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

Terminal 3 - Frontend:
```bash
cd frontend
npm run dev
```

## API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Required API Keys / Configuration

### Optional (for enhanced features):
- **Google Cloud Platform (GCP)**: For cloud deployment
  - GCP Project ID
  - Service Account Key
  - Cloud SQL credentials (if using)
  
- **Pinecone** (alternative to FAISS): For managed vector database
  - Pinecone API Key
  - Pinecone Environment

- **YouTube Data API** (optional): For fetching real video metadata
  - YouTube API Key

**Note**: The system works with simulated data by default. No API keys are required for basic functionality.

## Project Structure

```
IntelligentVideoRecommendation/
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Configuration, security
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   └── ml/           # ML models and embeddings
│   ├── alembic/          # Database migrations
│   ├── scripts/          # Utility scripts
│   └── tests/            # Test files
├── frontend/
│   ├── app/              # Next.js app directory
│   ├── components/       # React components
│   └── lib/              # Utilities
├── docker-compose.yml    # Docker orchestration
└── README.md
```

## Usage

1. **View Recommendations**: Navigate to the homepage to see recommended videos
2. **Watch Videos**: Click on a video to watch and update your history
3. **View History**: Check your watch history in the user profile
4. **Explore Recommendations**: See why videos are recommended with similarity scores

## Deployment

### Docker
```bash
docker-compose up -d
```

### GCP Cloud Run
```bash
gcloud run deploy video-recommendations --source .
```

## License

MIT License

