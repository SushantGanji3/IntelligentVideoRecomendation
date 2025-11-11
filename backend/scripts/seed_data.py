"""
Script to seed the database with sample videos and users
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.video import Video
from app.ml.recommender import recommendation_service
from passlib.context import CryptContext
import random
import bcrypt

# Configure bcrypt context with explicit backend to avoid compatibility issues
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__ident="2b"  # Use bcrypt 2b format
)

# Workaround for passlib/bcrypt compatibility
def hash_password(password: str) -> str:
    """Hash password using bcrypt directly"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Sample video data
SAMPLE_VIDEOS = [
    {
        "video_id": "ml_intro_001",
        "title": "Introduction to Machine Learning",
        "description": "Learn the basics of machine learning, including supervised and unsupervised learning algorithms.",
        "tags": ["machine learning", "AI", "data science", "tutorial"],
        "category": "Education",
        "duration": 600,
        "thumbnail_url": "https://via.placeholder.com/320x180?text=ML+Intro"
    },
    {
        "video_id": "neural_networks_001",
        "title": "Neural Networks Explained",
        "description": "Deep dive into how neural networks work, from perceptrons to deep learning.",
        "tags": ["neural networks", "deep learning", "AI", "tutorial"],
        "category": "Education",
        "duration": 900,
        "thumbnail_url": "https://via.placeholder.com/320x180?text=Neural+Networks"
    },
    {
        "video_id": "python_basics_001",
        "title": "Python Programming Basics",
        "description": "Start your programming journey with Python. Learn syntax, data types, and control structures.",
        "tags": ["python", "programming", "tutorial", "coding"],
        "category": "Education",
        "duration": 1200,
        "thumbnail_url": "https://via.placeholder.com/320x180?text=Python+Basics"
    },
    {
        "video_id": "react_tutorial_001",
        "title": "React.js Tutorial for Beginners",
        "description": "Build modern web applications with React. Learn components, state, and hooks.",
        "tags": ["react", "javascript", "web development", "frontend"],
        "category": "Education",
        "duration": 1800,
        "thumbnail_url": "https://via.placeholder.com/320x180?text=React+Tutorial"
    },
    {
        "video_id": "docker_intro_001",
        "title": "Docker Containerization Guide",
        "description": "Learn how to containerize applications with Docker. From basics to deployment.",
        "tags": ["docker", "containers", "devops", "deployment"],
        "category": "Technology",
        "duration": 1500,
        "thumbnail_url": "https://via.placeholder.com/320x180?text=Docker+Guide"
    },
    {
        "video_id": "kubernetes_101_001",
        "title": "Kubernetes Orchestration 101",
        "description": "Master Kubernetes for container orchestration. Deploy and scale applications with ease.",
        "tags": ["kubernetes", "containers", "devops", "orchestration"],
        "category": "Technology",
        "duration": 2400,
        "thumbnail_url": "https://via.placeholder.com/320x180?text=Kubernetes+101"
    },
    {
        "video_id": "data_structures_001",
        "title": "Data Structures and Algorithms",
        "description": "Essential data structures and algorithms every programmer should know.",
        "tags": ["algorithms", "data structures", "programming", "computer science"],
        "category": "Education",
        "duration": 2100,
        "thumbnail_url": "https://via.placeholder.com/320x180?text=Data+Structures"
    },
    {
        "video_id": "system_design_001",
        "title": "System Design Fundamentals",
        "description": "Learn how to design scalable systems. Understand load balancing, caching, and databases.",
        "tags": ["system design", "architecture", "scalability", "distributed systems"],
        "category": "Technology",
        "duration": 2700,
        "thumbnail_url": "https://via.placeholder.com/320x180?text=System+Design"
    },
    {
        "video_id": "golang_intro_001",
        "title": "Go Programming Language Tutorial",
        "description": "Learn Go (Golang) for backend development. Fast, efficient, and concurrent programming.",
        "tags": ["golang", "go", "backend", "programming"],
        "category": "Education",
        "duration": 1600,
        "thumbnail_url": "https://via.placeholder.com/320x180?text=Go+Tutorial"
    },
    {
        "video_id": "microservices_001",
        "title": "Microservices Architecture",
        "description": "Build and deploy microservices. Learn service communication, API gateways, and patterns.",
        "tags": ["microservices", "architecture", "distributed systems", "backend"],
        "category": "Technology",
        "duration": 3000,
        "thumbnail_url": "https://via.placeholder.com/320x180?text=Microservices"
    },
    {
        "video_id": "graphql_api_001",
        "title": "GraphQL API Development",
        "description": "Create efficient APIs with GraphQL. Learn queries, mutations, and subscriptions.",
        "tags": ["graphql", "API", "backend", "web development"],
        "category": "Technology",
        "duration": 1400,
        "thumbnail_url": "https://via.placeholder.com/320x180?text=GraphQL+API"
    },
    {
        "video_id": "ml_models_001",
        "title": "Building ML Models from Scratch",
        "description": "Implement machine learning models from scratch using NumPy and Python.",
        "tags": ["machine learning", "python", "numpy", "AI"],
        "category": "Education",
        "duration": 3300,
        "thumbnail_url": "https://via.placeholder.com/320x180?text=ML+Models"
    },
    {
        "video_id": "nlp_basics_001",
        "title": "Natural Language Processing Basics",
        "description": "Introduction to NLP. Learn tokenization, embeddings, and text classification.",
        "tags": ["NLP", "natural language processing", "AI", "machine learning"],
        "category": "Education",
        "duration": 1900,
        "thumbnail_url": "https://via.placeholder.com/320x180?text=NLP+Basics"
    },
    {
        "video_id": "web_scraping_001",
        "title": "Web Scraping with Python",
        "description": "Extract data from websites using BeautifulSoup and Scrapy.",
        "tags": ["web scraping", "python", "data extraction", "automation"],
        "category": "Education",
        "duration": 1100,
        "thumbnail_url": "https://via.placeholder.com/320x180?text=Web+Scraping"
    },
    {
        "video_id": "database_design_001",
        "title": "Database Design Principles",
        "description": "Learn relational database design, normalization, and SQL optimization.",
        "tags": ["database", "SQL", "design", "data modeling"],
        "category": "Education",
        "duration": 2000,
        "thumbnail_url": "https://via.placeholder.com/320x180?text=Database+Design"
    },
    {
        "video_id": "redis_caching_001",
        "title": "Redis Caching Strategies",
        "description": "Implement efficient caching with Redis. Learn caching patterns and best practices.",
        "tags": ["redis", "caching", "performance", "backend"],
        "category": "Technology",
        "duration": 1300,
        "thumbnail_url": "https://via.placeholder.com/320x180?text=Redis+Caching"
    },
    {
        "video_id": "api_security_001",
        "title": "API Security Best Practices",
        "description": "Secure your APIs with authentication, authorization, and encryption.",
        "tags": ["security", "API", "authentication", "backend"],
        "category": "Technology",
        "duration": 1700,
        "thumbnail_url": "https://via.placeholder.com/320x180?text=API+Security"
    },
    {
        "video_id": "cloud_deployment_001",
        "title": "Cloud Deployment with GCP",
        "description": "Deploy applications to Google Cloud Platform. Use Cloud Run, GKE, and Cloud SQL.",
        "tags": ["GCP", "cloud", "deployment", "devops"],
        "category": "Technology",
        "duration": 2200,
        "thumbnail_url": "https://via.placeholder.com/320x180?text=GCP+Deployment"
    },
    {
        "video_id": "ci_cd_001",
        "title": "CI/CD Pipeline Setup",
        "description": "Automate your deployment pipeline with GitHub Actions and CI/CD tools.",
        "tags": ["CI/CD", "devops", "automation", "deployment"],
        "category": "Technology",
        "duration": 1800,
        "thumbnail_url": "https://via.placeholder.com/320x180?text=CI+CD+Pipeline"
    },
    {
        "video_id": "testing_strategies_001",
        "title": "Software Testing Strategies",
        "description": "Learn unit testing, integration testing, and test-driven development.",
        "tags": ["testing", "TDD", "quality assurance", "software development"],
        "category": "Education",
        "duration": 1500,
        "thumbnail_url": "https://via.placeholder.com/320x180?text=Testing+Strategies"
    }
]

# Sample users
SAMPLE_USERS = [
    {
        "username": "demo_user",
        "email": "demo@example.com",
        "password": "demo123"
    },
    {
        "username": "test_user",
        "email": "test@example.com",
        "password": "test123"
    }
]


def seed_users(db: Session):
    """Seed users into the database"""
    print("Seeding users...")
    for user_data in SAMPLE_USERS:
        existing_user = db.query(User).filter(User.username == user_data["username"]).first()
        if existing_user:
            print(f"User {user_data['username']} already exists, skipping...")
            continue
        
        user = User(
            username=user_data["username"],
            email=user_data["email"],
            hashed_password=hash_password(user_data["password"])
        )
        db.add(user)
        print(f"Created user: {user_data['username']}")
    
    db.commit()
    print("Users seeded successfully!")


def seed_videos(db: Session):
    """Seed videos into the database and generate embeddings"""
    print("Seeding videos...")
    videos_created = 0
    
    for video_data in SAMPLE_VIDEOS:
        existing_video = db.query(Video).filter(Video.video_id == video_data["video_id"]).first()
        if existing_video:
            print(f"Video {video_data['video_id']} already exists, skipping...")
            continue
        
        # Add random views and likes
        video_data["views"] = random.randint(100, 10000)
        video_data["likes"] = random.randint(10, video_data["views"] // 10)
        
        video = Video(**video_data)
        db.add(video)
        db.flush()  # Flush to get the video ID
        
        # Generate embedding
        from app.ml.embeddings import embedding_service
        embedding = embedding_service.generate_video_embedding(
            title=video.title,
            description=video.description,
            tags=video.tags,
            category=video.category
        )
        video.embedding = embedding.tolist()
        
        # Add to FAISS index
        from app.ml.faiss_index import faiss_index
        faiss_index.add_vectors(embedding.reshape(1, -1), [video.id])
        
        videos_created += 1
        print(f"Created video: {video_data['title']}")
    
    db.commit()
    
    # Save FAISS index
    from app.ml.faiss_index import faiss_index
    faiss_index.save()
    
    print(f"Videos seeded successfully! Created {videos_created} videos.")


def main():
    """Main function to seed the database"""
    # Create tables
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created!")
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Seed users
        seed_users(db)
        
        # Seed videos
        seed_videos(db)
        
        print("\nDatabase seeded successfully!")
        print("\nSample users:")
        print("  - demo_user / demo123")
        print("  - test_user / test123")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()

