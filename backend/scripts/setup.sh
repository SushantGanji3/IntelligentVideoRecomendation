#!/bin/bash

# Setup script for backend
echo "Setting up backend..."

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "Please edit .env file with your database credentials"
fi

# Create data directory
mkdir -p data

# Run migrations
echo "Running database migrations..."
alembic upgrade head

# Seed database
echo "Seeding database..."
python scripts/seed_data.py

echo "Setup complete!"
echo "To start the server, run: uvicorn app.main:app --reload --port 8000"

