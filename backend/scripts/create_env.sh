#!/bin/bash

# Create .env file from example
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo ".env file created from .env.example"
    echo "Please edit .env file with your database credentials"
else
    echo ".env file already exists"
fi

