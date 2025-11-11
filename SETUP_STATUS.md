# Setup Status

## ✅ Completed Steps

### Step 1: Database Setup
- ⚠️ **PostgreSQL**: Not installed on system. You need to install PostgreSQL 14+.
  - **macOS**: `brew install postgresql@14`
  - **Linux**: `sudo apt-get install postgresql postgresql-contrib`
  - **Windows**: Download from https://www.postgresql.org/download/
  
- After installing PostgreSQL, create the database:
  ```bash
  createdb video_recommendations
  ```

### Step 2: Environment Configuration
- ✅ Created `backend/.env` file with default configuration
- ✅ Created `frontend/.env.local` file with API URL
- ⚠️ **Redis**: Not installed on system. You need to install Redis 6+.
  - **macOS**: `brew install redis`
  - **Linux**: `sudo apt-get install redis-server`
  - **Windows**: Download from https://redis.io/download or use WSL

### Step 3: Dependencies Installation
- ✅ Created Python virtual environment (`backend/venv`)
- ✅ Created `data/` directory for FAISS index
- ✅ Frontend dependencies installed successfully (`npm install` completed)
- ⚠️ **Backend dependencies**: Installation in progress or needs to be completed
  - The installation includes large packages (PyTorch, sentence-transformers) which can take 10-20 minutes
  - Requirements file has been updated for Python 3.14 compatibility

## 🔄 Next Steps

### 1. Install PostgreSQL and Redis

**Install PostgreSQL:**
```bash
# macOS
brew install postgresql@14
brew services start postgresql@14

# Create database
createdb video_recommendations
```

**Install Redis:**
```bash
# macOS
brew install redis
brew services start redis

# Test Redis
redis-cli ping  # Should return PONG
```

### 2. Complete Backend Dependencies Installation

The backend dependencies installation may take 10-20 minutes due to large packages like PyTorch and sentence-transformers.

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

**Note**: If you encounter any errors, you may need to:
- Update pip: `pip install --upgrade pip`
- Install build tools: `pip install setuptools wheel`
- For macOS ARM (M1/M2), some packages may need special handling

### 3. Update Database Configuration

Edit `backend/.env` and update the `DATABASE_URL` with your PostgreSQL credentials:

```env
DATABASE_URL=postgresql://your_username:your_password@localhost:5432/video_recommendations
```

If you're using the default PostgreSQL setup:
```env
DATABASE_URL=postgresql://$(whoami)@localhost:5432/video_recommendations
```

### 4. Run Database Migrations

```bash
cd backend
source venv/bin/activate
alembic upgrade head
```

### 5. Seed the Database

```bash
cd backend
source venv/bin/activate
python scripts/seed_data.py
```

This will:
- Create sample users (demo_user, test_user)
- Create 20 sample videos
- Generate embeddings for all videos
- Build the FAISS index

### 6. Start the Services

**Terminal 1 - Redis (if not running as service):**
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

### 7. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🐳 Alternative: Docker Setup

If you have Docker installed, you can use Docker Compose to run everything:

```bash
docker-compose up -d
```

This will automatically:
- Start PostgreSQL
- Start Redis
- Start Backend
- Start Frontend

## 📝 Current Status

- ✅ Project structure created
- ✅ Environment files created
- ✅ Frontend dependencies installed
- ⚠️ Backend dependencies need to be installed
- ⚠️ PostgreSQL needs to be installed
- ⚠️ Redis needs to be installed
- ⚠️ Database needs to be created and migrated
- ⚠️ Database needs to be seeded

## 🆘 Troubleshooting

### PostgreSQL Connection Issues
- Ensure PostgreSQL is running: `brew services list` (macOS) or `systemctl status postgresql` (Linux)
- Check if database exists: `psql -l | grep video_recommendations`
- Verify credentials in `backend/.env`

### Redis Connection Issues
- Ensure Redis is running: `redis-cli ping` (should return PONG)
- Check Redis URL in `backend/.env`

### Backend Installation Issues
- Python version: Ensure you're using Python 3.11+ (you have Python 3.14)
- Virtual environment: Ensure you're in the virtual environment (`source venv/bin/activate`)
- Large packages: PyTorch and sentence-transformers are large; installation may take time
- Memory: Ensure you have enough disk space (several GB for ML packages)

### Port Already in Use
- Backend (8000): Change port in uvicorn command or kill process using port 8000
- Frontend (3000): Change port in `package.json` or use `npm run dev -- -p 3001`
- PostgreSQL (5432): Usually fine, but check if another PostgreSQL instance is running
- Redis (6379): Usually fine, but check if another Redis instance is running

## 📚 Documentation

- **README.md**: Main project documentation
- **SETUP.md**: Detailed setup instructions
- **QUICK_START.md**: Quick start guide
- **API_DOCUMENTATION.md**: API reference
- **CONFIGURATION.md**: Configuration guide

## ✨ Once Everything is Running

1. Open http://localhost:3000 in your browser
2. You'll see recommended videos (for new users, these will be popular videos)
3. Click on a video to "watch" it
4. Watch history will be recorded
5. Recommendations will update based on your watch history
6. Check the API documentation at http://localhost:8000/docs

## 🎯 Default Test Users

After seeding the database:
- **Username**: `demo_user`, **Password**: `demo123`
- **Username**: `test_user`, **Password**: `test123`

These users are created by the seed script and can be used for testing.

