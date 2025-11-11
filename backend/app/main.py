from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import recommendations, videos, users, health

app = FastAPI(
    title="Intelligent Video Recommendation API",
    description="YouTube-like recommendation system with ML-powered similarity search",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(videos.router, prefix="/api/videos", tags=["videos"])
app.include_router(recommendations.router, prefix="/api/recommendations", tags=["recommendations"])


@app.get("/")
async def root():
    return {
        "message": "Intelligent Video Recommendation API",
        "version": "1.0.0",
        "docs": "/docs"
    }

