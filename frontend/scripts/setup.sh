#!/bin/bash

# Setup script for frontend
echo "Setting up frontend..."

# Install dependencies
echo "Installing dependencies..."
npm install

# Create .env.local file if it doesn't exist
if [ ! -f ".env.local" ]; then
    echo "Creating .env.local file..."
    cp .env.example .env.local
    echo "Please edit .env.local file if needed"
fi

echo "Setup complete!"
echo "To start the development server, run: npm run dev"

